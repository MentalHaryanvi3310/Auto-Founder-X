from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    subscription_tier = db.Column(db.String(20), default='free')
    voice_profile_url = db.Column(db.String(255))
    persona_data = db.Column(db.Text)
    
    # Relationships
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'subscription_tier': self.subscription_tier,
            'is_active': self.is_active
        }

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    business_model = db.Column(db.String(50))
    target_market = db.Column(db.Text)
    budget_range = db.Column(db.String(50))
    timeline = db.Column(db.String(50))
    status = db.Column(db.String(20), default='planning')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=False)
    marketplace_votes = db.Column(db.Integer, default=0)
    battle_arena_score = db.Column(db.Integer, default=0)
    
    # Relationships
    project_agents = db.relationship('ProjectAgent', backref='project', lazy=True, cascade='all, delete-orphan')
    marketplace_item = db.relationship('MarketplaceItem', backref='project', uselist=False, cascade='all, delete-orphan')
    competition_entries = db.relationship('CompetitionEntry', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'business_model': self.business_model,
            'target_market': self.target_market,
            'budget_range': self.budget_range,
            'timeline': self.timeline,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_public': self.is_public,
            'marketplace_votes': self.marketplace_votes,
            'battle_arena_score': self.battle_arena_score
        }

class Agent(db.Model):
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    capabilities = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    version = db.Column(db.String(20), default='1.0')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    project_agents = db.relationship('ProjectAgent', backref='agent', lazy=True)

    def __repr__(self):
        return f'<Agent {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'capabilities': self.capabilities,
            'is_active': self.is_active,
            'version': self.version,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProjectAgent(db.Model):
    __tablename__ = 'project_agents'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    status = db.Column(db.String(20), default='idle')
    current_task = db.Column(db.Text)
    progress_percentage = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    output_data = db.Column(db.Text)
    
    # Relationships
    agent_tasks = db.relationship('AgentTask', backref='project_agent', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ProjectAgent {self.project_id}-{self.agent_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'agent_id': self.agent_id,
            'status': self.status,
            'current_task': self.current_task,
            'progress_percentage': self.progress_percentage,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'output_data': self.output_data
        }

class AgentTask(db.Model):
    __tablename__ = 'agent_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_agent_id = db.Column(db.Integer, db.ForeignKey('project_agents.id'), nullable=False)
    task_name = db.Column(db.String(200), nullable=False)
    task_description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    result_data = db.Column(db.Text)
    error_message = db.Column(db.Text)

    def __repr__(self):
        return f'<AgentTask {self.task_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_agent_id': self.project_agent_id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result_data': self.result_data,
            'error_message': self.error_message
        }

class MarketplaceItem(db.Model):
    __tablename__ = 'marketplace_items'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2))
    is_for_sale = db.Column(db.Boolean, default=False)
    votes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MarketplaceItem {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': float(self.price) if self.price else None,
            'is_for_sale': self.is_for_sale,
            'votes': self.votes,
            'views': self.views,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BattleArenaCompetition(db.Model):
    __tablename__ = 'battle_arena_competitions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='upcoming')
    prize_credits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    competition_entries = db.relationship('CompetitionEntry', backref='competition', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<BattleArenaCompetition {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'prize_credits': self.prize_credits,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CompetitionEntry(db.Model):
    __tablename__ = 'competition_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('battle_arena_competitions.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    votes = db.Column(db.Integer, default=0)
    ranking = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CompetitionEntry {self.competition_id}-{self.project_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            'project_id': self.project_id,
            'votes': self.votes,
            'ranking': self.ranking,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }

