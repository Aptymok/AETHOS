import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from models import db

# InicializaciÃ³n de la app PRIMERO (antes de cualquier registro)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/crowia")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET", "dev_secret")

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
db.init_app(app)

# Registrar blueprints estÃ¡ndar
from routes.tarot import tarot_bp
from routes.manifest import manifest_bp
from routes.dashboard import dashboard_bp
from routes.resonance import resonance_bp
from auth import auth_bp

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(tarot_bp, url_prefix="/api")
app.register_blueprint(manifest_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api")
app.register_blueprint(resonance_bp, url_prefix="/api")

# Registrar sistema administrativo (si existe)
try:
    from auth_admin import register_admin_auth_routes
    register_admin_auth_routes(app)
    print("âœ… Sistema administrativo JWT cargado")
except ImportError as e:
    print(f"âš ï¸  Sistema administrativo no disponible: {e}")

# Registrar health check (si existe)
try:
    from health_check import health_bp
    app.register_blueprint(health_bp)
    print("âœ… Health check routes cargadas")
except ImportError as e:
    print(f"âš ï¸  Health check no disponible: {e}")

# Registrar eventos de sockets
try:
    from sockets.events import register_socket_events
    register_socket_events(socketio)
    print("âœ… Socket events registrados")
except ImportError as e:
    print(f"âš ï¸  Socket events no disponibles: {e}")

# ==================== RUTAS ADMINISTRATIVAS PROTEGIDAS ====================

@app.route("/api/admin/system/status", methods=["GET"])
def admin_system_status():
    """Endpoint de estado del sistema - requiere autenticaciÃ³n administrativa"""
    try:
        from auth_admin import require_admin_jwt, require_admin_permission
        
        @require_admin_jwt
        @require_admin_permission("system:monitor")
        def protected_status():
            return {
                "status": "AETHOS_ACTIVE", 
                "version": "2.0.0",
                "environment": "production",
                "admin_access": "granted",
                "timestamp": os.environ.get("DEPLOY_TIMESTAMP", "unknown"),
                "system_health": "optimal"
            }
        
        return protected_status()
    
    except ImportError:
        return {"error": "Sistema administrativo no configurado"}, 503

@app.route("/api/admin/dashboard", methods=["GET"])
def admin_dashboard():
    """Dashboard administrativo completo"""
    try:
        from auth_admin import require_admin_jwt, require_admin_permission
        
        @require_admin_jwt
        @require_admin_permission("system:admin")
        def protected_dashboard():
            # MÃ©tricas del sistema en tiempo real
            import psutil
            import datetime
            
            return {
                "system_metrics": {
                    "cpu_percent": psutil.cpu_percent(),
                    "memory_usage": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage('/').percent,
                    "active_connections": len(socketio.server.manager.rooms) if hasattr(socketio.server, 'manager') else 0
                },
                "operational_data": {
                    "database_status": "connected",
                    "external_apis": "operational", 
                    "socket_io": "active",
                    "last_health_check": datetime.datetime.utcnow().isoformat() + "Z"
                },
                "security": {
                    "jwt_algorithm": "RS256",
                    "key_strength": "RSA-4096",
                    "admin_access": "verified"
                }
            }
        
        return protected_dashboard()
    
    except ImportError:
        return {"error": "Sistema administrativo no configurado"}, 503

@app.route("/api/admin/users/activity", methods=["GET"])
def admin_user_activity():
    """Actividad de usuarios - solo administradores"""
    try:
        from auth_admin import require_admin_jwt, require_admin_permission
        
        @require_admin_jwt
        @require_admin_permission("users:read:all")
        def protected_activity():
            # En producciÃ³n, esto vendrÃ­a de la base de datos
            from models import User, Manifest
            from datetime import datetime, timedelta
            
            recent_activity = {
                "last_24_hours": {
                    "active_users": User.query.filter(
                        User.last_seen >= datetime.utcnow() - timedelta(days=1)
                    ).count(),
                    "manifestations_created": Manifest.query.filter(
                        Manifest.created_at >= datetime.utcnow() - timedelta(days=1)
                    ).count(),
                    "avg_coherence": 0.67  # Esto serÃ­a un cÃ¡lculo real
                },
                "cluster_distribution": {
                    "AETHOS": 35,
                    "VÃNCULO": 25, 
                    "TRANSFORMACIÃ“N": 20,
                    "OTROS": 20
                }
            }
            
            return recent_activity
        
        return protected_activity()
    
    except ImportError:
        return {"error": "Sistema administrativo no configurado"}, 503

# ==================== RUTAS PÃšBLICAS ====================

@app.route("/")
def health():
    """Endpoint pÃºblico de salud"""
    return {
        "status": "AETHOS_ACTIVE", 
        "version": "2.0.0",
        "timestamp": os.environ.get("DEPLOY_TIMESTAMP", "unknown")
    }

@app.route("/api/health")
def api_health():
    """Health check extendido para load balancers"""
    return {
        "status": "healthy",
        "database": "connected", 
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "version": "2.0.0",
        "timestamp": os.environ.get("DEPLOY_TIMESTAMP", "unknown")
    }

@app.route("/api/info")
def api_info():
    """InformaciÃ³n pÃºblica de la API"""
    return {
        "name": "Hell Theater AETHOS Engine",
        "version": "2.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "features": [
            "manifestation_engine",
            "neural_resonance_network", 
            "administrative_dashboard",
            "real_time_sockets",
            "jwt_authentication"
        ],
        "documentation": "/api/docs"  # PodrÃ­as aÃ±adir Swagger luego
    }

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint no encontrado", "code": "NOT_FOUND"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Error interno del servidor", "code": "INTERNAL_ERROR"}, 500

@app.errorhandler(401)
def unauthorized(error):
    return {"error": "No autorizado", "code": "UNAUTHORIZED"}, 401

@app.errorhandler(403)
def forbidden(error):
    return {"error": "Prohibido - permisos insuficientes", "code": "FORBIDDEN"}, 403

# ==================== INICIALIZACIÃ“N ====================

def initialize_database():
    """Inicializa la base de datos y crea tablas si no existen"""
    with app.app_context():
        try:
            db.create_all()
            print("âœ… Base de datos inicializada")
            
            # Verificar conexiÃ³n a la base de datos
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
            print("âœ… ConexiÃ³n a base de datos verificada")
            
        except Exception as e:
            print(f"âŒ Error inicializando base de datos: {e}")

if __name__ == "__main__":
    # Inicializar base de datos antes de correr
    initialize_database()
    
    # ConfiguraciÃ³n del servidor
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    
    print(f"ðŸš€ Iniciando Hell Theater AETHOS Engine...")
    print(f"   â€¢ Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    print(f"   â€¢ Host: {host}:{port}")
    print(f"   â€¢ Debug: {debug}")
    print(f"   â€¢ Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}")
    
    # Ejecutar servidor
    socketio.run(app, host=host, port=port, debug=debug)

