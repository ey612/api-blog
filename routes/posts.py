# 게시글 관련

from flask import Blueprint, request, jsonify
from models import db, Post

posts_bp = Blueprint('posts', __name__)

# 게시글 생성
@posts_bp.post('/posts')
def create_post():
    data = request.json
    
    new_post = Post(
        title=data['title'],
        content=data['content'],
        user_id=data['user_id'] #TODO: JWT에서 가져오기
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({
        'id': new_post.id,
        'title': new_post.title,
        'content': new_post.content
    }), 201

#게시글 목록 조회
@posts_bp.get('/posts')
def get_posts():
    posts = Post.query.all()
    result = []
    
    for post in posts:
        result.append({
            'id': post.id,
            'title': post.title,
            'user_id': post.user_id,
            'created_at': post.created_at.isoformat()
        })
    return jsonify(result), 200


#게시글 조회
@posts_bp.get('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'user_id': post.user_id,
        'created_at': post.created_at.isoformat()
    }), 200

#게시글 수정
@posts_bp.put('/posts/<int:post_id>')
def put_post(post_id):
    
    post = Post.query.get(post_id)
    
    if post is None:
        return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
    
    data = request.json
    post.title = data['title']
    post.content = data['content']

    db.session.commit()
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content
    }), 200
    
#게시글 삭제
@posts_bp.delete('/posts/<int:post_id>')
def delete_post(post_id):
    
    post = Post.query.get(post_id)
    
    if post is None:
        return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        'message': '게시글 삭제 완료.'
    }), 200
    