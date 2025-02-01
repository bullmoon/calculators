from flask import Flask
from routes.main import main_bp
from routes.emission import emission_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(emission_bp)

if __name__ == "__main__":
    app.run(debug=True)
