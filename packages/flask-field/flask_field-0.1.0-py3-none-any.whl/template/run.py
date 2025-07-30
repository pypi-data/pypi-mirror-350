from flask import Flask
from app.config import Config
from app.modules.db_manager import init_db
from app.routes import routes_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes_bp)

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)