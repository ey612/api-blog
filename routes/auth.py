# 회원가입

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

#회원가입
@auth_bp.post('/register')
def register():
    data = request.json #Postman에서 보낸 데이터 받기
    
    #중복체크
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '❌ 이미 존재하는 이메일입니다.'}), 400
    
    #비밀번호 해싱
    hashed_password = generate_password_hash(data['password'])
    
    #새 사용자 생성
    new_user = User(
        username = data['username'],
        email = data['email'],
        password = hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    }), 201

#사용자 리스트 출력
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

#로그인
@auth_bp.post('/login')
def login():
    try:
        data = request.json
        
        #데이터 확인
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': '이메일과 비밀번호를 확인해주세요.'}), 400
        
        #사용자 찾기
        user = User.query.filter_by(email=data['email']).first()
        
        #사용자가 없거나 비밀번호가 틀리면
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': '이메일 또는 비밀번호가 잘못되었습니다.'})
        
        return jsonify({
            'message': '로그인 성공!',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    except Exception as e:
        print(f"error: {str(e)}")
        return jsonify({error: str(e)}), 500

