# routes.py
from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth', __name__)

# Input validation schemas
class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=lambda s: 3 <= len(s) <= 80)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda s: len(s) >= 6)
    role = fields.Str(required=True, validate=lambda s: s in ['buyer', 'seller', 'adopter', 'breeder'])

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UpdateProfileSchema(Schema):
    username = fields.Str(validate=lambda s: 3 <= len(s) <= 80)
    email = fields.Email()
    role = fields.Str(validate=lambda s: s in ['buyer', 'seller', 'adopter', 'breeder'])
    password = fields.Str(validate=lambda s: len(s) >= 6)

# User Registration
@auth_bp.route('/user/register', methods=['POST'])
def register_user():
    try:
        data = RegisterSchema().load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        role=data['role']
    )
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

# User Authentication
@auth_bp.route('/user/login', methods=['POST'])
def login_user():
    try:
        data = LoginSchema().load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={'user_id': user.id, 'role': user.role})
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# User Profile Management
@auth_bp.route('/user/profile', methods=['GET', 'PUT'])
@jwt_required()
def user_profile():
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user['user_id'])

    if request.method == 'GET':
        return jsonify({
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }), 200

    elif request.method == 'PUT':
        try:
            data = UpdateProfileSchema().load(request.json)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'password' in data:
            user.set_password(data['password'])

        try:
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Username or email already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error'}), 500
