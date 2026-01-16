# 댓글 관련

from flask import Blueprint, request, jsonify
from models import db, Post, Comment

comments_bp = Blueprint('comments', __name__)

#댓글 생성
@comments_bp.post('/posts/<int:post_id>/comments')
def post_comment(post_id):
    
    #게시글 찾기
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
    
    #전달 받은 내용 data 변수 안에 넣고 항목 분류
    data = request.json
    if not data or 'content' not in data or 'user_id' not in data:
        return jsonify({'error': '잘못된 접근입니다.'}), 400
    
    new_comment = Comment(
        post_id= post.id,
        content=data['content'],
        user_id=data['user_id']
    )
    
    #댓글 추가 및 저장
    db.session.add(new_comment)
    db.session.commit()
    
    #아래 내용 반환
    return jsonify({
        'post_id': new_comment.post_id,
        'id': new_comment.id,
        'content': new_comment.content,
        'user_id': new_comment.user_id,
        'created_at': new_comment.created_at.isoformat()
    }), 201

#댓글 수정
@comments_bp.put('/comments/<int:comment_id>')
def put_comment(comment_id):
    
    #댓글 찾기
    comment = Comment.query.get(comment_id)
    if comment is None:
        return jsonify({'error': '댓글을 찾을 수 없습니다.'}), 404
    
    #댓글 수정
    data = request.json
    comment.content = data['content']
    
    #저장
    db.session.commit()
    
    #아래 내용 반환
    return jsonify({
        'post_id': comment.post_id,
        'id': comment.id,
        'content': comment.content,
        'user_id': comment.user_id,
        'created_at': comment.created_at.isoformat()
    }), 200
    
#댓글 삭제
@comments_bp.delete('/comments/<int:comment_id>')
def delete_comment(comment_id):
    
    #댓글 찾기
    comment = Comment.query.get(comment_id)
    if comment is None:
        return jsonify({'error': '댓글을 찾을 수 없습니다.'}), 404
    
    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        'message': '댓글 삭제 완료.'
    }), 200
    
#댓글 조회
@comments_bp.get('/posts/<int:post_id>/comments')

def get_comments(post_id):
    
    #게시글 찾기
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
    
    #댓글 찾기
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    result = []
    for comment in comments:
        result.append({
            'id': comment.id,
            'content': comment.content,
            'user_id': comment.user_id,
            'created_at': comment.created_at.isoformat()
        })
        
    return jsonify(result), 200