from app import create_app
from app.extensions import db
from app.models import User

class TestConfig:
    TESTING = True
    SECRET_KEY = 'test-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


def test_app_starts_and_registers_employee():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        user = User(name='Test Employee', email='test@example.com')
        user.set_password('StrongPass123')
        db.session.add(user)
        db.session.commit()
        assert User.query.filter_by(email='test@example.com').first().check_password('StrongPass123')
    client = app.test_client()
    response = client.get('/login')
    assert response.status_code == 200
