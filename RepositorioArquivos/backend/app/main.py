from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

from app.routes import routes_blueprint

# Inicializar extensões
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurações da aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URI',
        'mysql+pymysql://root:rootpassword@mysql/repo_arquivos'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.abspath('./upload')

    # Criar pasta de upload se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Habilitar CORS para o frontend e backend
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

    # Inicializar extensões
    bcrypt.init_app(app)
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(routes_blueprint)

    # Testar conexão com o banco de dados
    try:
        with app.app_context():
            db.create_all()
            print("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    return app

if __name__ == "__main__":
    app = create_app()
    print("Rotas registradas:")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True, host="0.0.0.0", port=5000)
