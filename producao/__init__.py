from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def criar_app():
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/producao'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
    db.init_app(app)
    app.secret_key = "essaehminhachavesecreta"
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "routes.Login"

    from producao.models import usuario

    @login_manager.user_loader
    def load_user(user_id):
        return usuario.query.get(int(user_id))

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()

    return app

