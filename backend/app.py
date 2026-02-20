from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database.db_connection import db

app = Flask(__name__)
app.config.from_object(Config)

CORS(
    app,
    resources={
        r"/auth/*": {"origins": "http://localhost:5173"},
        r"/filmes/*": {"origins": "http://localhost:5173"},
        r"/series/*": {"origins": "http://localhost:5173"},
        r"/episodios/*": {"origins": "http://localhost:5173"},
        r"/historico/*": {"origins": "http://localhost:5173"}, 
    },
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True
)

db.init_app(app)

app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]
jwt = JWTManager(app)

with app.app_context():
    from models import tabelas
    db.create_all()

# BLUEPRINTS
from routes.auth_routes import auth_bp
from routes.filmes import filmes_bp
from routes.series import series_bp
from routes.episodios import episodios_bp
from routes.historico import historico_bp
from routes.player import player_bp  

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(filmes_bp, url_prefix="/filmes")
app.register_blueprint(series_bp, url_prefix="/series")
app.register_blueprint(episodios_bp, url_prefix="/episodios")
app.register_blueprint(historico_bp, url_prefix="/historico")  
app.register_blueprint(player_bp, url_prefix="/player")

if __name__ == "__main__":
    app.run(debug=True)
