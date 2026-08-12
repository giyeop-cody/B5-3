"""게시글 서비스"""
from app.repositories.post_repository import PostRepository
from app.models import Post, PostStatus
from typing import List


class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_post(self, post_id: int, user_id: int = None) -> Post:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError(f"게시글 #{post_id}를 찾을 수 없습니다")
        # 비공개 글은 작성자 본인만 조회 가능
        if post.status == PostStatus.HIDDEN:
            if user_id is None or post.author_id != user_id:
                raise ValueError("비공개 게시글입니다")
        return post

    def get_all_posts(self, skip: int = 0, limit: int = 100, viewer_id: int = None) -> List[Post]:
        return self.post_repo.get_all(skip=skip, limit=limit, viewer_id=viewer_id)

    def get_posts_by_author(self, author_id: int, viewer_id: int = None) -> List[Post]:
        return self.post_repo.get_by_author(author_id, viewer_id=viewer_id)

    def get_posts_by_board(self, board_id: int, viewer_id: int = None) -> List[Post]:
        return self.post_repo.get_by_board(board_id, viewer_id=viewer_id)

    def search_posts(self, query: str, viewer_id: int = None) -> List[Post]:
        if not query or len(query.strip()) < 2:
            raise ValueError("검색어는 2글자 이상이어야 합니다")
        return self.post_repo.search(query, viewer_id=viewer_id)

    def create_post(
        self,
        title: str,
        content: str,
        author_id: int,
        board_id: int
    ) -> Post:
        # 비즈니스 로직: 유효성 검증
        if not title or len(title.strip()) == 0:
            raise ValueError("제목은 필수입니다")

        if len(title) > 200:
            raise ValueError("제목은 200자 이내로 작성해주세요")

        return self.post_repo.create(
            title=title.strip(),
            content=content or "",
            author_id=author_id,
            board_id=board_id
        )

    def update_post(
        self,
        post_id: int,
        user_id: int,
        title: str = None,
        content: str = None
    ) -> Post:
        post = self.get_post(post_id)

        # 권한 확인: 작성자만 수정 가능
        if post.author_id != user_id:
            raise PermissionError("자신의 게시글만 수정할 수 있습니다")

        if title and len(title) > 200:
            raise ValueError("제목은 200자 이내로 작성해주세요")

        return self.post_repo.update(post, title=title, content=content)

    def delete_post(self, post_id: int, user_id: int):
        post = self.get_post(post_id)

        # 권한 확인: 작성자만 삭제 가능
        if post.author_id != user_id:
            raise PermissionError("자신의 게시글만 삭제할 수 있습니다")

        self.post_repo.delete(post)

    def publish_post(self, post_id: int, user_id: int) -> Post:
        """게시글 공개"""
        post = self.get_post(post_id)

        if post.author_id != user_id:
            raise PermissionError("자신의 게시글만 공개할 수 있습니다")

        if post.status == PostStatus.PUBLISHED:
            raise ValueError("이미 공개된 게시글입니다")

        return self.post_repo.update_status(post, PostStatus.PUBLISHED)

    def hide_post(self, post_id: int, user_id: int) -> Post:
        """게시글 비공개"""
        post = self.get_post(post_id)

        if post.author_id != user_id:
            raise PermissionError("자신의 게시글만 비공개할 수 있습니다")

        if post.status == PostStatus.HIDDEN:
            raise ValueError("이미 비공개된 게시글입니다")

        return self.post_repo.update_status(post, PostStatus.HIDDEN)
