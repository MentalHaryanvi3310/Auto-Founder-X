from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import Project, ProjectAgent, Agent, User, db
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        
        query = Project.query.filter_by(user_id=current_user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Paginate results
        projects = query.order_by(Project.created_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        # Get agent status for each project
        project_list = []
        for project in projects.items:
            project_dict = project.to_dict()
            
            # Get agent status
            agent_status = {}
            project_agents = ProjectAgent.query.filter_by(project_id=project.id).all()
            for pa in project_agents:
                agent = Agent.query.get(pa.agent_id)
                if agent:
                    agent_status[agent.type] = pa.status
            
            project_dict['agents_status'] = agent_status
            project_list.append(project_dict)
        
        return jsonify({
            'success': True,
            'projects': project_list,
            'total': projects.total,
            'page': page,
            'pages': projects.pages
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get projects: {str(e)}'}), 500

@projects_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'success': False, 'message': 'Project name is required'}), 400
        
        # Create new project
        project = Project(
            user_id=current_user_id,
            name=data['name'].strip(),
            description=data.get('description', '').strip(),
            business_model=data.get('business_model', ''),
            target_market=data.get('target_market', ''),
            budget_range=data.get('budget_range', ''),
            timeline=data.get('timeline', ''),
            status='planning'
        )
        
        db.session.add(project)
        db.session.flush()  # Get the project ID
        
        # Add selected agents to the project
        selected_agents = data.get('selected_agents', [])
        for agent_type in selected_agents:
            agent = Agent.query.filter_by(type=agent_type).first()
            if agent:
                project_agent = ProjectAgent(
                    project_id=project.id,
                    agent_id=agent.id,
                    status='idle'
                )
                db.session.add(project_agent)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to create project: {str(e)}'}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        
        if not project:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        project_dict = project.to_dict()
        
        # Get detailed agent information
        agents_info = []
        project_agents = ProjectAgent.query.filter_by(project_id=project.id).all()
        for pa in project_agents:
            agent = Agent.query.get(pa.agent_id)
            if agent:
                agent_info = {
                    'agent': agent.to_dict(),
                    'project_agent': pa.to_dict()
                }
                agents_info.append(agent_info)
        
        project_dict['agents'] = agents_info
        
        return jsonify({
            'success': True,
            'project': project_dict
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get project: {str(e)}'}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        
        if not project:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            project.name = data['name'].strip()
        if 'description' in data:
            project.description = data['description'].strip()
        if 'business_model' in data:
            project.business_model = data['business_model']
        if 'target_market' in data:
            project.target_market = data['target_market']
        if 'budget_range' in data:
            project.budget_range = data['budget_range']
        if 'timeline' in data:
            project.timeline = data['timeline']
        if 'status' in data:
            project.status = data['status']
        if 'is_public' in data:
            project.is_public = data['is_public']
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project updated successfully',
            'project': project.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to update project: {str(e)}'}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        
        if not project:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        # Soft delete - mark as inactive instead of actual deletion
        project.is_active = False
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to delete project: {str(e)}'}), 500

@projects_bp.route('/projects/<int:project_id>/agents', methods=['GET'])
@jwt_required()
def get_project_agents(project_id):
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        
        if not project:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        project_agents = ProjectAgent.query.filter_by(project_id=project_id).all()
        agents_data = []
        
        for pa in project_agents:
            agent = Agent.query.get(pa.agent_id)
            if agent:
                agent_data = {
                    'agent': agent.to_dict(),
                    'project_agent': pa.to_dict()
                }
                agents_data.append(agent_data)
        
        return jsonify({
            'success': True,
            'agents': agents_data
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get project agents: {str(e)}'}), 500

@projects_bp.route('/projects/<int:project_id>/agents', methods=['POST'])
@jwt_required()
def add_project_agent(project_id):
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        
        if not project:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        data = request.get_json()
        agent_type = data.get('agent_type')
        
        if not agent_type:
            return jsonify({'success': False, 'message': 'Agent type is required'}), 400
        
        agent = Agent.query.filter_by(type=agent_type).first()
        if not agent:
            return jsonify({'success': False, 'message': 'Agent not found'}), 404
        
        # Check if agent is already added to project
        existing_pa = ProjectAgent.query.filter_by(project_id=project_id, agent_id=agent.id).first()
        if existing_pa:
            return jsonify({'success': False, 'message': 'Agent already added to project'}), 400
        
        # Add agent to project
        project_agent = ProjectAgent(
            project_id=project_id,
            agent_id=agent.id,
            status='idle'
        )
        
        db.session.add(project_agent)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Agent added to project successfully',
            'project_agent': project_agent.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to add agent to project: {str(e)}'}), 500

