# HTML 페이지 라우트

from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

# 메인 페이지 (게시글 목록)
@views_bp.get('/')
def index():
    return render_template('index.html')

# 회원가입 페이지
@views_bp.get('/register')
def register():
    return render_template('register.html')

# 로그인 페이지
@views_bp.get('/login')
def login():
    return render_template('login.html')

# 게시글 작성 페이지
@views_bp.get('/posts/new')
def post_new():
    return render_template('post_write.html')

# 게시글 수정 페이지
@views_bp.get('/posts/<int:post_id>/edit')
def post_edit(post_id):
    return render_template('post_edit.html')

# 게시글 상세 페이지
@views_bp.get('/posts/<int:post_id>')
def post_detail(post_id):
    return render_template('post_detail.html')
