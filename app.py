import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


load_dotenv()


# VARIABLES
USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASS")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DB = os.getenv("POSTGRES_DB")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Cambiar esto a una clave segura en un entorno de producción
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}"
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'  # Cambiar esto a una clave segura en un entorno de producción

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# MODELO
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(150), nullable=False)
    user_mail = db.Column(db.String(150), unique=True, nullable=False)
    user_passw = db.Column(db.String(100), nullable=False)
    user_role = db.Column(db.String(30), nullable=False)
    user_creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_last_login = db.Column(db.DateTime)
    failed_count = db.Column(db.Integer, default=0)


# CONSULTAS DB
def get_user_by_name(name: str) -> User:
    """Obtiene un Usuario por nombre"""
    user = User.query.filter_by(user_name=name).first()
    return user

def get_user_by_mail(mail: str) -> User:
    """Obtiene un Usuario por dirección de correo electrónico"""
    user = User.query.filter_by(user_mail=mail).first()
    if user:
        return user
    
def create_user(user_name: str, mail: str, passw: str, role: str):
    """Crea una nueva instancia de Usuario y guarda en la base de datos"""
    try:
        user = User(
            user_name=user_name,
            user_mail=mail,
            user_passw=passw,
            user_role=role
        )
        
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as exc:
        db.session.rollback()

     
# RUTAS
@app.route('/new_user', methods=['POST'])
def new_user():
    data = request.json  # Obtiene los datos del usuario desde la solicitud POST en formato JSON

    # Extrae los datos del usuario desde el JSON
    user_name = data.get('nombre_usuario')
    user_mail = data.get('correo_electronico')
    user_passw = data.get('contraseña')
    user_role = 'developer'

    # Verifica si el correo electrónico ya está en uso
    usuario_existente = get_user_by_mail(user_mail)
    if usuario_existente:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 400
    
    # Hashea la contraseña antes de almacenarla en la base de datos
    user_passw_hashed = bcrypt.generate_password_hash(user_passw).decode('utf-8')

    nuevo_usuario = create_user(user_name=user_name, mail=user_mail, passw=user_passw_hashed, role=user_role)

    return jsonify({"mensaje": f"Usuario {nuevo_usuario.user_name} creado con éxito"}), 201  # Devuelve una respuesta JSON con un mensaje y código de estado 201

@app.route('/login', methods=['POST'])
def login():
    user_name = request.json['nombre_usuario']
    user_passw = request.json['contraseña']
    
    user = get_user_by_name(name=user_name)
    
    if user:
        if bcrypt.check_password_hash(user.user_passw.encode('utf-8'), user_passw.encode('utf-8')):
            session['usuario_id'] = user.id
            user.failed_count = 0  # Reiniciar intentos fallidos
            user.user_last_login = datetime.utcnow()
            db.session.commit()
            
            # Generar un token JWT utilizando flask_jwt_extended
            token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            
            return jsonify({"mensaje": "Inicio de sesión exitoso", "rol": user.user_role, "token": token})
        else:
            user.failed_count += 1
            # Bloqueo de usuario por intentos fallidos
            if user.failed_count >= 3:
                user.failed_count = 0
                user.bloqueado = True  # Marcar la cuenta como bloqueada
                # TODO implementar método de desbloqueo
                return jsonify({"mensaje": "Usuario bloqueado"}), 401 
            db.session.commit()
            return jsonify({"mensaje": "Credenciales inválidas"}), 401
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

@app.route('/protegido', methods=['GET'])
@jwt_required()  # Protege esta ruta con un token JWT válido
def ruta_protegida():
    usuario_id = get_jwt_identity()
    return jsonify({"mensaje": "Esta es una ruta protegida", "usuario_id": usuario_id})


if __name__ == '__main__':
    # Crea la Base de Datos
    with app.app_context():
        db.create_all()
    app.run(debug=True)