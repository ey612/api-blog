
# routes/auth.py
from flask import Blueprint, current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from models import db, User


auth_bp = Blueprint("auth", __name__)


# 회원가입
@auth_bp.post("/register")
def register():
    data = request.json

    # 필수 필드 누락 여부 확인
    if not data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "필수 항목을 입력해주세요."}), 400

    # 사용자 이름이 문자열이 아니거나 빈 문자열·공백만 있는 경우 거절
    if not isinstance(data["username"], str) or not data["username"].strip():
        return jsonify({"error": "사용자 이름을 입력해주세요."}), 400

    # 이메일이 문자열이 아니거나 빈 문자열·공백만 있는 경우 거절
    if not isinstance(data["email"], str) or not data["email"].strip():
        return jsonify({"error": "이메일을 입력해주세요."}), 400

    # 비밀번호가 문자열이 아니거나 빈 문자열·공백만 있는 경우 거절
    if not isinstance(data["password"], str) or not data["password"].strip():
        return jsonify({"error": "비밀번호를 입력해주세요."}), 400

    # 이메일 중복 확인
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "이미 존재하는 이메일입니다."}), 400

    # 사용자 이름 중복 확인
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "이미 존재하는 이름입니다."}), 400

    # 비밀번호 해싱 및 사용자 생성
    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
    }), 201


# 사용자 목록 조회
@auth_bp.get("/users")
def get_users():
    users = User.query.all()
    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })

    return jsonify(result), 200


# 로그인
@auth_bp.post("/login")
def login():
    try:
        data = request.json

        # 필수 필드 누락 여부 확인
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "이메일과 비밀번호를 확인해주세요."}), 400

        # 이메일이 문자열이 아니거나 빈 문자열·공백만 있는 경우
        if not isinstance(data["email"], str) or not data["email"].strip():
            return jsonify({"error": "이메일을 입력해주세요."}), 400

        # 비밀번호가 문자열이 아니거나 빈 문자열·공백만 있는 경우
        if not isinstance(data["password"], str) or not data["password"].strip():
            return jsonify({"error": "비밀번호를 입력해주세요."}), 400

        # 사용자 조회 및 비밀번호 확인
        user = User.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"error": "이메일 또는 비밀번호가 잘못되었습니다."}), 401

        return jsonify({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }), 200

    except Exception:
        current_app.logger.exception("로그인 처리 중 오류 발생")
        return jsonify({"error": "서버 오류가 발생했습니다."}), 500
