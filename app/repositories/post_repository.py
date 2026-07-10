"""게시글 리포지토리"""
from sqlalchemy.orm import Session
from app.models import Post, PostStatus
from typing import List, Optional


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> Post:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return (
            self.db.query(Post)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_author(self, author_id: int) -> List[Post]:
        return (
            self.db.query(Post)
            .filter(Post.author_id == author_id)
            .order_by(Post.created_at.desc())
            .all()
        )

    def get_by_board(self, board_id: int) -> List[Post]:
        return (
            self.db.query(Post)
            .filter(Post.board_id == board_id)
            .order_by(Post.created_at.desc())
            .all()
        )

    def search(self, query: str) -> List[Post]:
        """제목 또는 내용으로 검색"""
        search_pattern = f"%{query}%"
        return (
            self.db.query(Post)
            .filter(
                (Post.title.ilike(search_pattern))
                | (Post.content.ilike(search_pattern))
            )
            .order_by(Post.created_at.desc())
            .all()
        )

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
