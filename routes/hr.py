# routes/hr.py
from flask import Blueprint, request, jsonify
from flask_jwt_required import jwt_required
from utils.rbac import require_role

hr_bp = Blueprint('hr', __name__)

@hr_bp.route('/leave/<int:leave_id>/review', methods=['POST'])
@jwt_required()
@require_role('hrOfficer')
def review_leave(leave_id):
    data = request.get_json()
    status = data.get('status')  # 'approved' or 'rejected'
    if status not in ['approved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    # In real app: update DB, send email
    return jsonify({'message': f'Leave {status}'})
