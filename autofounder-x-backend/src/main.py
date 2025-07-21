import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.projects import projects_bp
from src.routes.agents import agents_bp
from src.routes.marketplace import marketplace_bp
from src.routes.battle_arena import battle_arena_bp
from src.init_data import init_all_data

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = 'autofounder-x-secret-key-2025'
app.config['JWT_SECRET_KEY'] = 'autofounder-x-jwt-secret-key-2025'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire for demo

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app, origins="*")  # Allow all origins for development

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(projects_bp, url_prefix='/api')
app.register_blueprint(agents_bp, url_prefix='/api')
app.register_blueprint(marketplace_bp, url_prefix='/api')
app.register_blueprint(battle_arena_bp, url_prefix='/api')

# Create database tables and initialize data
with app.app_context():
    db.create_all()
    
    # Check if agents exist, if not initialize data
    from src.models.user import Agent
    if Agent.query.count() == 0:
        init_all_data()

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Frontend not built yet. Please build the React frontend and place it in the static folder.", 404

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'message': 'AutoFounder X Backend is running',
        'version': '1.0.0'
    }

# API info endpoint
@app.route('/api/info', methods=['GET'])
def api_info():
    return {
        'name': 'AutoFounder X API',
        'version': '1.0.0',
        'description': 'The AI Co-Founder That Never Sleeps',
        'endpoints': {
            'authentication': '/api/auth/*',
            'projects': '/api/projects/*',
            'agents': '/api/agents/*',
            'marketplace': '/api/marketplace/*',
            'battle_arena': '/api/battle-arena/*',
            'users': '/api/users/*'
        }
    }

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

