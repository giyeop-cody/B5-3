"""Pydantic 스키마 (요청/응답 모델)"""
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
    id: int
    status: PostStatus
    author_id: int
    board_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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


# ===== Auth 스키마 =====
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str
