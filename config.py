# 환경 파일
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    #SQLite 데이터베이스 경로
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    #경고 메시지 끄기
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #한글 깨짐 방지
    JSON_AS_ASCII = False
    
    #JWT 시크릿 키
    SECRET_KEY = os.environ.get('SECRET_KEY')