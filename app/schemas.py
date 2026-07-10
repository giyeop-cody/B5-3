"""Pydantic 스키마 (요청/응답 모델)

양방향 관계 순환참조 방지 전략:
- SQLAlchemy 모델은 양방향 관계(back_populates)를 가지지만,
  Pydantic 응답 모델에서는 관계 객체 전체를 포함하지 않습니다.
- 대신 FK ID(author_id, board_id)만 포함하여 JSON 직렬화 시
  순환참조(User → Post → User → ...)를 방지합니다.

예시:
  PostResponse.author_id = 1  (O: ID만 포함)
  PostResponse.author = User(...)  (X: 객체 전체 포함 시 순환참조)

필요시 중첩 응답 모델 사용:
  - PostWithAuthorResponse: author 정보 포함 (단방향만)
  - UserWithPostsResponse: posts 목록 포함 (단방향만)
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models import PostStatus


# ===== Board 스키마 =====
class BoardBase(BaseModel):
    name: str = Field(..., max_length=50, description="게시판 이름")
    description: Optional[str] = Field(None, max_length=500, description="게시판 설명")


class BoardCreate(BoardBase):
    pass


class BoardResponse(BoardBase):
    id: int

    class Config:
        from_attributes = True


# ===== Post 스키마 =====
class PostBase(BaseModel):
    title: str = Field(..., max_length=200, description="게시글 제목")
    content: Optional[str] = Field(None, description="게시글 내용")


class PostCreate(PostBase):
    board_id: int = Field(..., description="게시판 ID")


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200, description="게시글 제목")
    content: Optional[str] = Field(None, description="게시글 내용")


class PostResponse(PostBase):
    """게시글 응답 모델

    순환참조 방지를 위해 author_id, board_id만 포함합니다.
    author(User), board(Board) 객체 전체는 포함하지 않습니다.
    """
    id: int
    status: PostStatus
    author_id: int    # author 객체 대신 ID만 (순환참조 방지)
    board_id: int     # board 객체 대신 ID만 (순환참조 방지)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostWithAuthorResponse(PostResponse):
    """게시글 + 작성자 정보 (중첩 응답, 단방향만)

    author 정보는 포함하지만, author.posts는 포함하지 않아 순환참조 방지
    """
    author_username: Optional[str] = None
    board_name: Optional[str] = None


# ===== User 스키마 =====
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=100)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserWithPostsResponse(UserResponse):
    """사용자 + 게시글 목록 (중첩 응답, 단방향만)

    posts 목록은 포함하지만, 각 post.author는 포함하지 않아 순환참조 방지
    """
    posts: List[PostResponse] = []


# ===== Auth 스키마 =====
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str
