# routes/admin.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.rbac import require_role
from models import db, User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/employees/<int:employee_id>/terminate', methods=['POST'])
@jwt_required()
@require_role('admin')
def terminate_employee(employee_id):
    employee = User.query.filter_by(id=employee_id, role='employee').first()
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee terminated'})
