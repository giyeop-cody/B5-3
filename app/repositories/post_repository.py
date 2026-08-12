"""게시글 리포지토리"""
from sqlalchemy.orm import Session
from app.models import Post, PostStatus
from typing import List, Optional


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> Post:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, viewer_id: int = None) -> List[Post]:
        """전체 게시글 조회 (viewer_id가 없거나 작성자가 아니면 HIDDEN 제외)"""
        query = self.db.query(Post)
        if viewer_id is None:
            query = query.filter(Post.status != PostStatus.HIDDEN)
        query = query.order_by(Post.created_at.desc()).offset(skip).limit(limit)
        return query.all()

    def get_by_author(self, author_id: int, viewer_id: int = None) -> List[Post]:
        """작성자별 게시글 조회 (viewer_id != author_id면 HIDDEN 제외)"""
        query = self.db.query(Post).filter(Post.author_id == author_id)
        if viewer_id is None or viewer_id != author_id:
            query = query.filter(Post.status != PostStatus.HIDDEN)
        return query.order_by(Post.created_at.desc()).all()

    def get_by_board(self, board_id: int, viewer_id: int = None) -> List[Post]:
        """게시판별 게시글 조회 (비로그인 시 HIDDEN 제외)"""
        query = self.db.query(Post).filter(Post.board_id == board_id)
        if viewer_id is None:
            query = query.filter(Post.status != PostStatus.HIDDEN)
        else:
            # 로그인 사용자: 타인의 비공개 글만 제외, 본인 글은 표시
            query = query.filter(
                (Post.status != PostStatus.HIDDEN) | (Post.author_id == viewer_id)
            )
        return query.order_by(Post.created_at.desc()).all()

    def search(self, query: str, viewer_id: int = None) -> List[Post]:
        """제목 또는 내용으로 검색 (비로그인 시 HIDDEN 제외)"""
        search_pattern = f"%{query}%"
        q = self.db.query(Post).filter(
            (Post.title.ilike(search_pattern))
            | (Post.content.ilike(search_pattern))
        )
        if viewer_id is None:
            q = q.filter(Post.status != PostStatus.HIDDEN)
        else:
            q = q.filter(
                (Post.status != PostStatus.HIDDEN) | (Post.author_id == viewer_id)
            )
        return q.order_by(Post.created_at.desc()).all()

    def create(
        self,
        title: str,
        content: str,
        author_id: int,
        board_id: int,
        status: PostStatus = PostStatus.DRAFT
    ) -> Post:
        post = Post(
            title=title,
            content=content,
            author_id=author_id,
            board_id=board_id,
            status=status
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update(self, post: Post, title: str = None, content: str = None) -> Post:
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        self.db.commit()
        self.db.refresh(post)
        return post

    def update_status(self, post: Post, status: PostStatus) -> Post:
        post.status = status
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post):
        self.db.delete(post)
        self.db.commit()
