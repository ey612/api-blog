# 회원가입

from flask import Blueprint, request, jsonify
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/register')
def register():
    data = request.json
    
    #중복체크
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '❌ 이미 존재하는 이메일입니다.'}), 400
    
    #새 사용자 생성
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'] #TODO: 해싱 필요
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    }), 201

@auth_bp.get('/users')
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    return jsonify(result), 200


@auth_bp.post('/login')
def login():
    #TODO: 나중에 구현
    return jsonify({'message': '로그인 기능 구현 예정'}), 200

