from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import MarketplaceItem, Project, User, db
from datetime import datetime

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/marketplace/items', methods=['GET'])
def get_marketplace_items():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 12, type=int)
        category = request.args.get('category')
        sort = request.args.get('sort', 'recent')  # recent, votes, views
        
        query = MarketplaceItem.query.join(Project).filter(Project.is_public == True)
        
        if category:
            query = query.filter(MarketplaceItem.category == category)
        
        # Apply sorting
        if sort == 'votes':
            query = query.order_by(MarketplaceItem.votes.desc())
        elif sort == 'views':
            query = query.order_by(MarketplaceItem.views.desc())
        else:  # recent
            query = query.order_by(MarketplaceItem.created_at.desc())
        
        # Paginate results
        items = query.paginate(page=page, per_page=limit, error_out=False)
        
        # Format response with additional project and user info
        items_list = []
        for item in items.items:
            item_dict = item.to_dict()
            
            # Add project info
            project = Project.query.get(item.project_id)
            if project:
                item_dict['project'] = {
                    'name': project.name,
                    'description': project.description,
                    'status': project.status
                }
                
                # Add user info
                user = User.query.get(project.user_id)
                if user:
                    item_dict['creator'] = {
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
            
            items_list.append(item_dict)
        
        return jsonify({
            'success': True,
            'items': items_list,
            'total': items.total,
            'page': page,
            'pages': items.pages
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get marketplace items: {str(e)}'}), 500

@marketplace_bp.route('/marketplace/items/<int:item_id>', methods=['GET'])
def get_marketplace_item(item_id):
    try:
        item = MarketplaceItem.query.get(item_id)
        if not item:
            return jsonify({'success': False, 'message': 'Item not found'}), 404
        
        # Increment view count
        item.views += 1
        db.session.commit()
        
        item_dict = item.to_dict()
        
        # Add project info
        project = Project.query.get(item.project_id)
        if project:
            item_dict['project'] = project.to_dict()
            
            # Add user info
            user = User.query.get(project.user_id)
            if user:
                item_dict['creator'] = {
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
        
        return jsonify({
            'success': True,
            'item': item_dict
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get marketplace item: {str(e)}'}), 500

@marketplace_bp.route('/marketplace/publish', methods=['POST'])
@jwt_required()
def publish_to_marketplace():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        project_id = data.get('project_id')
        if not project_id:
            return jsonify({'success': False, 'message': 'Project ID is required'}), 400
        
        # Verify project ownership
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        if not project:
            return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        # Check if already published
        existing_item = MarketplaceItem.query.filter_by(project_id=project_id).first()
        if existing_item:
            return jsonify({'success': False, 'message': 'Project already published to marketplace'}), 400
        
        # Create marketplace item
        marketplace_item = MarketplaceItem(
            project_id=project_id,
            title=data.get('title', project.name),
            description=data.get('description', project.description),
            category=data.get('category', 'general'),
            price=data.get('price'),
            is_for_sale=data.get('is_for_sale', False)
        )
        
        # Make project public
        project.is_public = True
        project.updated_at = datetime.utcnow()
        
        db.session.add(marketplace_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project published to marketplace successfully',
            'item': marketplace_item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to publish to marketplace: {str(e)}'}), 500

@marketplace_bp.route('/marketplace/vote', methods=['POST'])
@jwt_required()
def vote_marketplace_item():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        item_id = data.get('item_id')
        if not item_id:
            return jsonify({'success': False, 'message': 'Item ID is required'}), 400
        
        item = MarketplaceItem.query.get(item_id)
        if not item:
            return jsonify({'success': False, 'message': 'Item not found'}), 404
        
        # Check if user owns the project (can't vote for own project)
        project = Project.query.get(item.project_id)
        if project and project.user_id == current_user_id:
            return jsonify({'success': False, 'message': 'Cannot vote for your own project'}), 400
        
        # In a real implementation, you'd track individual votes to prevent duplicate voting
        # For now, we'll just increment the vote count
        item.votes += 1
        
        # Also update project marketplace votes
        if project:
            project.marketplace_votes += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vote recorded successfully',
            'votes': item.votes
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to vote: {str(e)}'}), 500

@marketplace_bp.route('/marketplace/categories', methods=['GET'])
def get_categories():
    try:
        # Get distinct categories from marketplace items
        categories = db.session.query(MarketplaceItem.category).distinct().all()
        category_list = [cat[0] for cat in categories if cat[0]]
        
        # Add default categories if none exist
        if not category_list:
            category_list = [
                'AI & Machine Learning',
                'E-commerce',
                'SaaS Tools',
                'Mobile Apps',
                'Web Applications',
                'Productivity',
                'Health & Fitness',
                'Education',
                'Finance',
                'Entertainment'
            ]
        
        return jsonify({
            'success': True,
            'categories': category_list
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get categories: {str(e)}'}), 500

@marketplace_bp.route('/marketplace/my-items', methods=['GET'])
@jwt_required()
def get_my_marketplace_items():
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's published items
        items = db.session.query(MarketplaceItem).join(Project)\
                          .filter(Project.user_id == current_user_id).all()
        
        items_list = []
        for item in items:
            item_dict = item.to_dict()
            
            # Add project info
            project = Project.query.get(item.project_id)
            if project:
                item_dict['project'] = {
                    'name': project.name,
                    'status': project.status
                }
            
            items_list.append(item_dict)
        
        return jsonify({
            'success': True,
            'items': items_list
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get my marketplace items: {str(e)}'}), 500

