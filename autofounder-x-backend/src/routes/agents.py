from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..agents.agent_manager import agent_manager
from ..models.user import Project, db

agents_bp = Blueprint('agents', __name__)

@agents_bp.route('/agents', methods=['GET'])
@jwt_required()
def get_agents():
    """Get all available agents"""
    agents = agent_manager.get_all_agents()
    return jsonify({
        "success": True,
        "agents": agents
    })

@agents_bp.route('/agents/<agent_id>', methods=['GET'])
@jwt_required()
def get_agent(agent_id):
    """Get specific agent details"""
    agent_status = agent_manager.get_agent_status(agent_id)
    
    if "error" in agent_status:
        return jsonify({"success": False, "error": agent_status["error"]}), 404
    
    return jsonify({
        "success": True,
        "agent": agent_status
    })

@agents_bp.route('/agents/<agent_id>/start', methods=['POST'])
@jwt_required()
def start_agent(agent_id):
    """Start a specific agent"""
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    project_id = data.get('project_id')
    
    # Verify project ownership if project_id is provided
    if project_id:
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        if not project:
            return jsonify({"success": False, "error": "Project not found"}), 404
        
        # Use project data for agent execution
        project_data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "business_model": project.business_model,
            "target_market": project.target_market,
            "current_stage": project.status,
            "user_id": current_user_id
        }
    else:
        project_data = data.get('project_data', {})
        project_data['user_id'] = current_user_id
    
    result = agent_manager.start_agent(agent_id, project_data)
    
    if not result["success"]:
        return jsonify(result), 400
    
    return jsonify(result)

@agents_bp.route('/agents/<agent_id>/stop', methods=['POST'])
@jwt_required()
def stop_agent(agent_id):
    """Stop a specific agent"""
    result = agent_manager.stop_agent(agent_id)
    
    if not result["success"]:
        return jsonify(result), 400
    
    return jsonify(result)

@agents_bp.route('/agents/start-all', methods=['POST'])
@jwt_required()
def start_all_agents():
    """Start all agents"""
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    project_id = data.get('project_id')
    
    # Verify project ownership if project_id is provided
    if project_id:
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        if not project:
            return jsonify({"success": False, "error": "Project not found"}), 404
        
        # Update project status to building
        project.status = 'building'
        db.session.commit()
        
        # Use project data for agent execution
        project_data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "business_model": project.business_model,
            "target_market": project.target_market,
            "current_stage": project.status,
            "user_id": current_user_id
        }
    else:
        project_data = data.get('project_data', {})
        project_data['user_id'] = current_user_id
    
    result = agent_manager.start_all_agents(project_data)
    return jsonify(result)

@agents_bp.route('/agents/stop-all', methods=['POST'])
@jwt_required()
def stop_all_agents():
    """Stop all agents"""
    result = agent_manager.stop_all_agents()
    return jsonify(result)

@agents_bp.route('/agents/<agent_id>/configure', methods=['POST'])
@jwt_required()
def configure_agent(agent_id):
    """Configure a specific agent"""
    data = request.get_json() or {}
    config = data.get('config', {})
    
    result = agent_manager.configure_agent(agent_id, config)
    
    if not result["success"]:
        return jsonify(result), 400
    
    return jsonify(result)

@agents_bp.route('/agents/<agent_id>/results', methods=['GET'])
@jwt_required()
def get_agent_results(agent_id):
    """Get results from a specific agent"""
    result = agent_manager.get_agent_results(agent_id)
    
    if not result["success"]:
        return jsonify(result), 404
    
    return jsonify(result)

@agents_bp.route('/agents/results', methods=['GET'])
@jwt_required()
def get_all_results():
    """Get results from all agents"""
    result = agent_manager.get_all_results()
    return jsonify(result)

@agents_bp.route('/agents/<agent_id>/logs', methods=['GET'])
@jwt_required()
def get_agent_logs(agent_id):
    """Get logs from a specific agent"""
    result = agent_manager.get_agent_logs(agent_id)
    
    if not result["success"]:
        return jsonify(result), 404
    
    return jsonify(result)

@agents_bp.route('/agents/system-status', methods=['GET'])
@jwt_required()
def get_system_status():
    """Get overall system status"""
    status = agent_manager.get_system_status()
    return jsonify({
        "success": True,
        "status": status
    })

@agents_bp.route('/agents/<agent_id>/clear', methods=['POST'])
@jwt_required()
def clear_agent_results(agent_id):
    """Clear results for a specific agent"""
    result = agent_manager.clear_agent_results(agent_id)
    
    if not result["success"]:
        return jsonify(result), 400
    
    return jsonify(result)

@agents_bp.route('/agents/clear-all', methods=['POST'])
@jwt_required()
def clear_all_results():
    """Clear all agent results"""
    result = agent_manager.clear_agent_results()
    return jsonify(result)

# Legacy endpoints for backward compatibility
@agents_bp.route('/agents/ideation/trends', methods=['GET'])
@jwt_required()
def get_trends():
    """Get market trends (legacy endpoint)"""
    try:
        # Get results from ideation agent if available
        result = agent_manager.get_agent_results('ideation')
        if result["success"] and "market_trends" in result["results"]:
            trends = result["results"]["market_trends"]["trending_sectors"][:5]
        else:
            # Fallback mock data
            trends = [
                {'keyword': 'AI automation', 'growth': 85, 'tam': '50B'},
                {'keyword': 'sustainable tech', 'growth': 72, 'tam': '30B'},
                {'keyword': 'remote work tools', 'growth': 65, 'tam': '25B'},
                {'keyword': 'health tech', 'growth': 78, 'tam': '40B'},
                {'keyword': 'fintech solutions', 'growth': 68, 'tam': '35B'}
            ]
        
        return jsonify({
            'success': True,
            'trends': trends
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get trends: {str(e)}'}), 500

@agents_bp.route('/agents/ideation/analyze', methods=['POST'])
@jwt_required()
def analyze_idea():
    """Analyze business idea (legacy endpoint)"""
    try:
        data = request.get_json()
        idea = data.get('idea')
        
        if not idea:
            return jsonify({'success': False, 'message': 'Idea is required'}), 400
        
        # Start ideation agent with the idea
        project_data = {"idea": idea, "analysis_type": "quick"}
        result = agent_manager.start_agent('ideation', project_data)
        
        # For now, return mock analysis (in real implementation, wait for agent results)
        analysis = {
            'viability_score': 78,
            'market_potential': 'High',
            'competition_level': 'Medium',
            'technical_complexity': 'Medium',
            'estimated_tam': '15B',
            'key_challenges': [
                'Market saturation in some segments',
                'Technical implementation complexity',
                'Regulatory considerations'
            ],
            'opportunities': [
                'Growing market demand',
                'Limited direct competitors',
                'Potential for viral growth'
            ]
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to analyze idea: {str(e)}'}), 500

