from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import BattleArenaCompetition, CompetitionEntry, Project, User, db
from datetime import datetime, date

battle_arena_bp = Blueprint('battle_arena', __name__)

@battle_arena_bp.route('/battle-arena/competitions', methods=['GET'])
def get_competitions():
    try:
        status = request.args.get('status', 'active')  # active, upcoming, completed
        
        query = BattleArenaCompetition.query
        
        if status == 'active':
            query = query.filter(
                BattleArenaCompetition.start_date <= date.today(),
                BattleArenaCompetition.end_date >= date.today()
            )
        elif status == 'upcoming':
            query = query.filter(BattleArenaCompetition.start_date > date.today())
        elif status == 'completed':
            query = query.filter(BattleArenaCompetition.end_date < date.today())
        
        competitions = query.order_by(BattleArenaCompetition.start_date.desc()).all()
        
        competitions_list = []
        for comp in competitions:
            comp_dict = comp.to_dict()
            
            # Add entry count
            entry_count = CompetitionEntry.query.filter_by(competition_id=comp.id).count()
            comp_dict['entry_count'] = entry_count
            
            competitions_list.append(comp_dict)
        
        return jsonify({
            'success': True,
            'competitions': competitions_list
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get competitions: {str(e)}'}), 500

@battle_arena_bp.route('/battle-arena/competitions', methods=['POST'])
@jwt_required()
def create_competition():
    try:
        # This would typically be admin-only functionality
        data = request.get_json()
        
        competition = BattleArenaCompetition(
            name=data['name'],
            description=data.get('description', ''),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            prize_credits=data.get('prize_credits', 0),
            status='upcoming'
        )
        
        db.session.add(competition)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Competition created successfully',
            'competition': competition.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to create competition: {str(e)}'}), 500

@battle_arena_bp.route('/battle-arena/enter', methods=['POST'])
@jwt_required()
def enter_competition():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        competition_id = data.get('competition_id')
        project_id = data.get('project_id')
        
        if not competition_id or not project_id:
            return jsonify({'success': False, 'message': 'Competition ID and Project ID are required'}), 400
        
        # Verify project ownership
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        if not project:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        # Verify competition exists and is active
        competition = BattleArenaCompetition.query.get(competition_id)
        if not competition:
            return jsonify({'success': False, 'message': 'Competition not found'}), 404
        
        if competition.end_date < date.today():
            return jsonify({'success': False, 'message': 'Competition has ended'}), 400
        
        # Check if already entered
        existing_entry = CompetitionEntry.query.filter_by(
            competition_id=competition_id, 
            project_id=project_id
        ).first()
        
        if existing_entry:
            return jsonify({'success': False, 'message': 'Project already entered in this competition'}), 400
        
        # Create entry
        entry = CompetitionEntry(
            competition_id=competition_id,
            project_id=project_id
        )
        
        db.session.add(entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Successfully entered competition',
            'entry': entry.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to enter competition: {str(e)}'}), 500

@battle_arena_bp.route('/battle-arena/leaderboard/<int:competition_id>', methods=['GET'])
def get_leaderboard(competition_id):
    try:
        competition = BattleArenaCompetition.query.get(competition_id)
        if not competition:
            return jsonify({'success': False, 'message': 'Competition not found'}), 404
        
        # Get entries ordered by votes
        entries = db.session.query(CompetitionEntry, Project, User)\
                           .join(Project, CompetitionEntry.project_id == Project.id)\
                           .join(User, Project.user_id == User.id)\
                           .filter(CompetitionEntry.competition_id == competition_id)\
                           .order_by(CompetitionEntry.votes.desc())\
                           .all()
        
        leaderboard = []
        for rank, (entry, project, user) in enumerate(entries, 1):
            entry_dict = entry.to_dict()
            entry_dict['ranking'] = rank
            entry_dict['project'] = {
                'name': project.name,
                'description': project.description,
                'status': project.status
            }
            entry_dict['creator'] = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            leaderboard.append(entry_dict)
        
        return jsonify({
            'success': True,
            'competition': competition.to_dict(),
            'leaderboard': leaderboard
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get leaderboard: {str(e)}'}), 500

@battle_arena_bp.route('/battle-arena/vote', methods=['POST'])
@jwt_required()
def vote_competition_entry():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        entry_id = data.get('entry_id')
        if not entry_id:
            return jsonify({'success': False, 'message': 'Entry ID is required'}), 400
        
        entry = CompetitionEntry.query.get(entry_id)
        if not entry:
            return jsonify({'success': False, 'message': 'Entry not found'}), 404
        
        # Check if user owns the project (can't vote for own project)
        project = Project.query.get(entry.project_id)
        if project and project.user_id == current_user_id:
            return jsonify({'success': False, 'message': 'Cannot vote for your own project'}), 400
        
        # Check if competition is still active
        competition = BattleArenaCompetition.query.get(entry.competition_id)
        if competition and competition.end_date < date.today():
            return jsonify({'success': False, 'message': 'Competition has ended'}), 400
        
        # In a real implementation, you'd track individual votes to prevent duplicate voting
        # For now, we'll just increment the vote count
        entry.votes += 1
        
        # Also update project battle arena score
        if project:
            project.battle_arena_score += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vote recorded successfully',
            'votes': entry.votes
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to vote: {str(e)}'}), 500

@battle_arena_bp.route('/battle-arena/my-entries', methods=['GET'])
@jwt_required()
def get_my_entries():
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's competition entries
        entries = db.session.query(CompetitionEntry, Project, BattleArenaCompetition)\
                           .join(Project, CompetitionEntry.project_id == Project.id)\
                           .join(BattleArenaCompetition, CompetitionEntry.competition_id == BattleArenaCompetition.id)\
                           .filter(Project.user_id == current_user_id)\
                           .order_by(CompetitionEntry.submitted_at.desc())\
                           .all()
        
        entries_list = []
        for entry, project, competition in entries:
            entry_dict = entry.to_dict()
            entry_dict['project'] = {
                'name': project.name,
                'status': project.status
            }
            entry_dict['competition'] = {
                'name': competition.name,
                'status': competition.status,
                'end_date': competition.end_date.isoformat() if competition.end_date else None
            }
            entries_list.append(entry_dict)
        
        return jsonify({
            'success': True,
            'entries': entries_list
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get my entries: {str(e)}'}), 500

