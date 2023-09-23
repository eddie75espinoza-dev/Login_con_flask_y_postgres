import pytest
from .app import app, create_user, db, User


# Establece una base de datos temporal para pruebas
@pytest.fixture
def test_app():
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite'
        app.config['TESTING'] = True
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

# Test para la función create_user
def test_create_user(test_app):
    # Datos de prueba
    user_name = "test_user"
    mail = "test@example.com"
    passw = "password123"
    role = "user"

    # Llama a la función create_user
    user = create_user(user_name, mail, passw, role)

    # Verifica que el usuario se haya creado correctamente
    assert user is not None
    assert user.user_name == user_name
    assert user.user_mail == mail
    assert user.user_role == role

    # Verifica que el usuario exista en la base de datos
    user_from_db = User.query.filter_by(id=user.id).first()
    assert user_from_db is not None
    assert user_from_db.user_name == user_name
    assert user_from_db.user_mail == mail
    assert user_from_db.user_role == role
