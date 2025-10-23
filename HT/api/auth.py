# api/auth_admin.py
"""
Sistema de Autenticación Administrativa - Hell Theater
"""

import jwt
import os
from functools import wraps
from flask import request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime
from flask import Blueprint

# Simple auth blueprint for public/dev auth endpoints
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/ping', methods=['GET'])
def auth_ping():
    return jsonify({'status': 'auth_ok'})

class AdminAuthSystem:
    def __init__(self):
        self.public_key = self._load_public_key()
        self.required_audience = os.getenv('JWT_AUDIENCE', 'HellTheater.API.Admin')
        self.required_issuer = os.getenv('JWT_ISSUER', 'HellTheater.Auth.System')
        self.admin_role = os.getenv('ADMIN_ROLE', 'SystemAdministrator')
    
    def _load_public_key(self):
        """Carga la llave pública RSA desde variables de entorno"""
        public_key_pem = os.getenv('JWT_PUBLIC_KEY')
        if not public_key_pem:
            raise ValueError("JWT_PUBLIC_KEY no configurada")
        
        try:
            if '\\n' in public_key_pem:
                public_key_pem = public_key_pem.replace('\\n', '\n')
            
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode('utf-8'),
                backend=default_backend()
            )
            return public_key
        except Exception as e:
            raise ValueError(f"Error cargando llave pública: {str(e)}")
    
    def verify_admin_token(self, token):
        """Verifica un token JWT administrativo"""
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=['RS256'],
                audience=self.required_audience,
                issuer=self.required_issuer,
                options={"verify_exp": True, "verify_nbf": True}
            )
            
            if not self._validate_admin_claims(payload):
                return None, "Invalid admin claims"
            
            return payload, None
            
        except jwt.ExpiredSignatureError:
            return None, "Token expired"
        except jwt.InvalidTokenError as e:
            return None, f"Invalid token: {str(e)}"
        except Exception as e:
            return None, f"Verification error: {str(e)}"
    
    def _validate_admin_claims(self, payload):
        """Valida claims específicos de administrador"""
        required_claims = ['role', 'permissions', 'username']
        
        for claim in required_claims:
            if claim not in payload:
                return False
        
        if payload.get('role') != self.admin_role:
            return False
        
        required_permissions = ['system:admin', 'users:read:all']
        user_permissions = payload.get('permissions', [])
        
        if not all(perm in user_permissions for perm in required_permissions):
            return False
        
        return True
    
    def has_permission(self, payload, permission):
        """Verifica si el administrador tiene un permiso específico"""
        return permission in payload.get('permissions', [])
    
    def get_admin_context(self, payload):
        """Obtiene contexto administrativo del payload"""
        return {
            'username': payload.get('username'),
            'role': payload.get('role'),
            'permissions': payload.get('permissions', []),
            'tier': payload.get('tier', 'Unknown')
        }

_admin_auth_instance = None

def get_admin_auth():
    """Lazy initializer for AdminAuthSystem. Returns None if admin auth is not configured."""
    global _admin_auth_instance
    if _admin_auth_instance is None:
        try:
            _admin_auth_instance = AdminAuthSystem()
        except Exception as e:
            # Do not raise during import; return None to indicate admin not configured
            _admin_auth_instance = None
    return _admin_auth_instance


# Decoradores
def require_admin_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        admin = get_admin_auth()
        if not admin:
            return jsonify({"error": "Sistema administrativo no configurado"}), 503

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "Authorization required",
                "code": "MISSING_AUTH_HEADER"
            }), 401

        token = auth_header[7:]
        payload, error = admin.verify_admin_token(token)

        if error:
            return jsonify({
                "error": "Invalid administrative token",
                "detail": error,
                "code": "INVALID_ADMIN_TOKEN"
            }), 401

        request.admin_payload = payload
        request.admin_context = admin.get_admin_context(payload)

        return f(*args, **kwargs)
    return decorated

def require_admin_permission(permission):
    def decorator(f):
        @wraps(f)
        @require_admin_jwt
        def decorated(*args, **kwargs):
            admin = get_admin_auth()
            if not admin:
                return jsonify({"error": "Sistema administrativo no configurado"}), 503

            if not admin.has_permission(request.admin_payload, permission):
                return jsonify({
                    "error": "Insufficient permissions",
                    "required_permission": permission,
                    "code": "INSUFFICIENT_PERMISSIONS"
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


# -------------------- User JWT (simple) --------------------
def require_jwt(f):
    """Decorator for regular user JWT-protected routes.
    Behavior:
      - If Authorization header present, attempt to verify token.
        * If JWT_SECRET is set, try HS256.
        * Else if JWT_PUBLIC_KEY is set, try RS256 with the PEM.
      - If no header and ENVIRONMENT=development, inject a dev user (id=1).
      - Otherwise return 401.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        env = os.getenv('ENVIRONMENT', 'development')

        if not auth_header:
            # Development-friendly default user
            if env == 'development':
                request.user = {'id': 1, 'username': 'dev'}
                return f(*args, **kwargs)
            return jsonify({"error": "Authorization required", "code": "MISSING_AUTH_HEADER"}), 401

        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid auth header", "code": "INVALID_AUTH_HEADER"}), 401

        token = auth_header[7:]

        # Try HS256 with JWT_SECRET
        secret = os.getenv('JWT_SECRET')
        public_pem = os.getenv('JWT_PUBLIC_KEY')

        try:
            if secret:
                payload = jwt.decode(token, secret, algorithms=['HS256'], options={"verify_exp": True})
            elif public_pem:
                # PyJWT accepts PEM text directly for RS256
                if '\\n' in public_pem:
                    public_pem = public_pem.replace('\\n', '\n')
                payload = jwt.decode(token, public_pem, algorithms=['RS256'], options={"verify_exp": True})
            else:
                # No verification configured; in production this should be disallowed
                if env == 'development':
                    request.user = {'id': 1, 'username': 'dev'}
                    return f(*args, **kwargs)
                return jsonify({"error": "Token verification not configured"}), 500

            # Attach simple user context expected by routes
            # Accept payload['user'] or payload itself as user dict
            user = payload.get('user') if isinstance(payload, dict) and 'user' in payload else payload
            request.user = user
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired", "code": "TOKEN_EXPIRED"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": "Invalid token", "detail": str(e), "code": "INVALID_TOKEN"}), 401
        except Exception as e:
            return jsonify({"error": "Token verification error", "detail": str(e)}), 500

    return decorated

# Funciones de registro para app.py
def register_admin_auth_routes(app):
    """Registra rutas administrativas de autenticación"""
    
    @app.route('/api/admin/auth/verify', methods=['GET'])
    @require_admin_jwt
    def admin_verify_token():
        return jsonify({
            "status": "valid",
            "admin": request.admin_context,
            "token_valid_until": datetime.datetime.fromtimestamp(
                request.admin_payload['exp']
            ).isoformat() if 'exp' in request.admin_payload else None
        })
    
    @app.route('/api/admin/auth/permissions', methods=['GET'])
    @require_admin_jwt
    def admin_list_permissions():
        return jsonify({
            "permissions": request.admin_context['permissions'],
            "total_permissions": len(request.admin_context['permissions'])
        })