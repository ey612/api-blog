# 실행 페이지
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    
    #설정 로드
    app.config.from_object(Config)
    
    #CORS 설정
    CORS(app)
    
    #DB 초기화
    db.init_app(app)
    
    #Blueprint 등록 -- # Blueprint : 라우트를 그룹으로 묶는 방법
    from routes.auth import auth_bp
    from routes.posts import posts_bp
    from routes.comments import comments_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(posts_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    
    #테이블 생성
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)