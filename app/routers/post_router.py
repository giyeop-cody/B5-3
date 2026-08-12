"""게시글 API 라우터"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.post_repository import PostRepository
from app.services.post_service import PostService
from app.schemas import PostCreate, PostUpdate, PostResponse
from app.auth.dependencies import get_current_user, get_optional_user
from app.auth.exceptions import NotFoundError, PermissionDeniedError, ValidationError
from app.models import User
from typing import List, Optional

router = APIRouter(prefix="/api/posts", tags=["posts"])


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    """PostService 의존성 주입"""
    post_repo = PostRepository(db)
    return PostService(post_repo)


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    board_id: Optional[int] = Query(None, description="게시판 ID로 필터링"),
    author_id: Optional[int] = Query(None, description="작성자 ID로 필터링"),
    q: Optional[str] = Query(None, description="검색어"),
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=1000, description="가져올 개수"),
    post_service: PostService = Depends(get_post_service),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """게시글 목록 조회 (필터링/검색 지원) — 비공개 글은 작성자 본인만"""
    viewer_id = current_user.id if current_user else None
    try:
        if q:
            return post_service.search_posts(q, viewer_id=viewer_id)
        elif board_id:
            return post_service.get_posts_by_board(board_id, viewer_id=viewer_id)
        elif author_id:
            return post_service.get_posts_by_author(author_id, viewer_id=viewer_id)
        else:
            return post_service.get_all_posts(skip=skip, limit=limit, viewer_id=viewer_id)
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """게시글 상세 조회 — 공개 글은 누구나, 비공개 글은 작성자만"""
    user_id = current_user.id if current_user else None
    try:
        return post_service.get_post(post_id, user_id=user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user)  # 인증 필수
):
    """게시글 생성 (인증 필요)"""
    try:
        return post_service.create_post(
            title=post_data.title,
            content=post_data.content,
            author_id=current_user.id,  # 인증된 사용자 ID 사용
            board_id=post_data.board_id
        )
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user)  # 인증 필수
):
    """게시글 수정 (인증 필요)"""
    try:
        return post_service.update_post(
            post_id=post_id,
            user_id=current_user.id,
            title=post_data.title,
            content=post_data.content
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except PermissionDeniedError as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user)  # 인증 필수
):
    """게시글 삭제 (인증 필요)"""
    try:
        post_service.delete_post(
            post_id=post_id,
            user_id=current_user.id
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except PermissionDeniedError as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.post("/{post_id}/publish", response_model=PostResponse)
async def publish_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user)  # 인증 필수
):
    """게시글 공개 (상태 변경: DRAFT/HIDDEN → PUBLISHED)"""
    try:
        return post_service.publish_post(
            post_id=post_id,
            user_id=current_user.id
        )
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionDeniedError as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.post("/{post_id}/hide", response_model=PostResponse)
async def hide_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user)  # 인증 필수
):
    """게시글 비공개 (상태 변경: DRAFT/PUBLISHED → HIDDEN)"""
    try:
        return post_service.hide_post(
            post_id=post_id,
            user_id=current_user.id
        )
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionDeniedError as e:
        raise HTTPException(status_code=403, detail=e.message)
