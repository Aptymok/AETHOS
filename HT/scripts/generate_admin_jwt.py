# scripts/generate_admin_jwt.py
import jwt
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os
import json

def generate_rsa_keypair_secure():
    """Genera par de llaves RSA-4096 seguras para producción"""
    print("🔐 Generando par de llaves RSA-4096...")
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,  # Enterprise-grade
        backend=default_backend()
    )
    
    # Serializar llave privada
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    # Serializar llave pública
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    return private_pem, public_pem

def create_admin_jwt_token(private_key):
    """Crea JWT administrativo con permisos elevados y tiempo real"""
    
    # Timestamps realistas para producción
    issued_at_dt = datetime.datetime.utcnow()
    expiration_dt = issued_at_dt + datetime.timedelta(days=365)  # 1 año de validez
    # Usar timestamps numéricos (segundos desde epoch) para compatibilidad con verificadores
    issued_at = int(issued_at_dt.timestamp())
    expiration = int(expiration_dt.timestamp())
    
    payload = {
        # Identificación
        "sub": "HellTheater.Administrator",
        "iss": "HellTheater.Auth.System",
        "aud": "HellTheater.API.Admin",
        
    # Timestamps reales
    "iat": issued_at,
    "exp": expiration,
    "nbf": issued_at,  # Not Before
        
        # Metadatos administrativos
        "username": "HellTheater.Administrator.Aethos",
        "role": "SystemAdministrator",
        "tier": "Enterprise",
        
        # Permisos administrativos completos
        "permissions": [
            # Sistema
            "system:admin",
            "system:config",
            "system:monitor",
            "system:maintenance",
            
            # Usuarios
            "users:read:all", 
            "users:write:all",
            "users:delete:all",
            "users:impersonate",
            
            # Datos
            "data:export",
            "data:import", 
            "data:cleanse",
            "data:backup",
            
            # Operaciones
            "ops:emergency",
            "ops:protocols",
            "ops:shutdown",
            "ops:restart",
            
            # Seguridad
            "security:keys:rotate",
            "security:audit",
            "security:ban",
            "security:whitelist",
            
            # Clústeres
            "clusters:create",
            "clusters:delete", 
            "clusters:modify",
            "clusters:monitor",
            
            # IA y Agentes
            "ai:agents:manage",
            "ai:models:update",
            "ai:training:execute",
            
            # Tiempo Real
            "realtime:broadcast",
            "realtime:notify:all",
            "realtime:connections"
        ],
        
        # Configuración de sesión
        "session_type": "admin_persistent",
        "mfa_verified": True,
        "ip_whitelisted": True,
        
        # Metadata del sistema
        "version": "2.0.0",
        "environment": "production"
    }
    
    # Codificar el token
    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
        headers={
            "kid": "admin_key_2024",
            "typ": "JWT"
        }
    )
    
    return token, payload

def save_environment_files(public_key, private_key, jwt_token):
    """Guarda las configuraciones en archivos para .env"""
    
    # Crear directorio si no existe
    os.makedirs('config', exist_ok=True)
    
    # 1. Archivo .env.production (PARA PRODUCCIÓN)
    # Escape public key newlines to store as single-line env var safely
    public_key_escaped = public_key.strip().replace('\n', '\\n')
    env_content = (
        "# 🔐 HELL THEATER - PRODUCTION JWT CONFIGURATION\n"
        f"# Generated: {datetime.datetime.utcnow().isoformat()}Z\n\n"
        "# JWT Configuration\n"
        f"JWT_PUBLIC_KEY={public_key_escaped}\n"
        f"ADMIN_JWT_TOKEN={jwt_token}\n\n"
        "# Security Settings\n"
        "JWT_ALGORITHM=RS256\n"
        "JWT_EXPIRE_DAYS=365\n"
        "JWT_AUDIENCE=HellTheater.API.Admin\n"
        "JWT_ISSUER=HellTheater.Auth.System\n\n"
        "# Admin Role Requirements\n"
        "ADMIN_ROLE=SystemAdministrator\n"
        "MIN_ADMIN_TIER=Enterprise\n"
        "REQUIRE_MFA=true\n\n"
        "# System Flags\n"
        "ENVIRONMENT=production\n"
        "LOG_LEVEL=INFO\n"
        "SECURE_COOKIES=true\n"
    )
    
    # 2. Archivo con la private key (GUARDAR EN LUGAR SEGURO!)
    private_key_content = f"""# 🚨 CRITICAL: PRIVATE JWT KEY - KEEP SECURE!
# Hell Theater Administrative JWT Signing Key
# Generated: {datetime.datetime.utcnow().isoformat()}Z
# Environment: PRODUCTION
# Security Level: ENTERPRISE

{private_key}

# 🚨 SECURITY INSTRUCTIONS:
# 1. Store this file in secure vault (Hashicorp Vault, AWS Secrets Manager, etc.)
# 2. NEVER commit to version control
# 3. Rotate every 6 months
# 4. Access should be limited to deployment systems only
"""
    
    # Escribir archivos
    with open('.env.production', 'w', encoding='utf-8') as f:
        f.write(env_content)

    with open('config/jwt_private_key.pem', 'w', encoding='utf-8') as f:
        f.write(private_key_content)
    
    # Archivo de verificación
    token_expiration_iso = (datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat()
    verification_content = (
        "# ✅ JWT SETUP VERIFICATION\n"
        "ADMIN_JWT_GENERATED=TRUE\n"
        f"GENERATION_TIMESTAMP={datetime.datetime.utcnow().isoformat()}Z\n"
        "KEY_STRENGTH=RSA-4096\n"
        f"TOKEN_EXPIRATION={token_expiration_iso}\n"
    )
    
    with open('config/jwt_setup.verification', 'w', encoding='utf-8') as f:
        f.write(verification_content)

def main():
    """Ejecuta la generación completa del sistema JWT administrativo"""
    print("🚀 HELL THEATER - ADMIN JWT GENERATOR (PRODUCTION)")
    print("=" * 60)
    
    try:
        # Generar llaves
        private_key, public_key = generate_rsa_keypair_secure()
        print("✅ Llaves RSA-4096 generadas")
        
        # Generar token JWT
        jwt_token, payload = create_admin_jwt_token(private_key)
        print("✅ Token JWT administrativo generado")
        
        # Guardar archivos de configuración
        save_environment_files(public_key, private_key, jwt_token)
        print("✅ Archivos de configuración guardados")
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("🎯 CONFIGURACIÓN COMPLETA - RESUMEN")
        print("=" * 60)
        
        print(f"\n📋 PAYLOAD ADMINISTRATIVO:")
        print(f"   • Role: {payload['role']}")
        print(f"   • Username: {payload['username']}")
        print(f"   • Permissions: {len(payload['permissions'])} permisos")
        # payload['iat'] and payload['exp'] ahora son timestamps numéricos
        print(f"   • Issued: {datetime.datetime.fromtimestamp(payload['iat']).isoformat()}")
        print(f"   • Expires: {datetime.datetime.fromtimestamp(payload['exp']).isoformat()}")
        print(f"   • Duration: 365 días")
        
        print(f"\n🔐 ARCHIVOS GENERADOS:")
        print(f"   ✅ .env.production - Variables de entorno para producción")
        print(f"   ✅ config/jwt_private_key.pem - Llave privada (GUARDAR SEGURO)")
        print(f"   ✅ config/jwt_setup.verification - Verificación de instalación")
        
        print(f"\n🚨 PRÓXIMOS PASOS CRÍTICOS:")
        print(f"   1. Mueve '.env.production' a '.env' en tu servidor")
        print(f"   2. Guarda 'config/jwt_private_key.pem' en un vault seguro")
        print(f"   3. NUNCA commits la llave privada al repositorio")
        print(f"   4. Configura rotación automática cada 6 meses")
        
        print(f"\n📁 ESTRUCTURA FINAL:")
        print(f"   📄 .env.production → JWT_PUBLIC_KEY y ADMIN_JWT_TOKEN")
        print(f"   🔐 config/jwt_private_key.pem → Llave de firma (SECRETO)")
        print(f"   ✅ config/jwt_setup.verification → Verificación")
        
        print(f"\n🎉 CONFIGURACIÓN ADMINISTRATIVA LISTA PARA PRODUCCIÓN!")
        
    except Exception as e:
        print(f"❌ Error durante la generación: {str(e)}")
        raise

if __name__ == "__main__":
    main()