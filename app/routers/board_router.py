"""게시판 API 라우터"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.board_repository import BoardRepository
from app.services.board_service import BoardService
from app.schemas import BoardCreate, BoardResponse
from app.auth.dependencies import get_current_user
from app.models import User
from typing import List

router = APIRouter(prefix="/api/boards", tags=["boards"])


def get_board_service(db: Session = Depends(get_db)) -> BoardService:
    """BoardService 의존성 주입"""
    board_repo = BoardRepository(db)
    return BoardService(board_repo)


@router.get("/", response_model=List[BoardResponse])
async def list_boards(board_service: BoardService = Depends(get_board_service)):
    """게시판 목록 조회"""
    return board_service.get_all_boards()


@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: int,
    board_service: BoardService = Depends(get_board_service)
):
    """게시판 상세 조회"""
    try:
        return board_service.get_board(board_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    board_data: BoardCreate,
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_user)
):
    """게시판 생성 (인증 필요)"""
    try:
        return board_service.create_board(
            name=board_data.name,
            description=board_data.description
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
