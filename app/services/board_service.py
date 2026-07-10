"""게시판 서비스"""
from app.repositories.board_repository import BoardRepository
from app.models import Board
from typing import List


class BoardService:
    def __init__(self, board_repo: BoardRepository):
        self.board_repo = board_repo

    def get_board(self, board_id: int) -> Board:
        board = self.board_repo.get_by_id(board_id)
        if not board:
            raise ValueError(f"게시판 #{board_id}를 찾을 수 없습니다")
        return board

    def get_all_boards(self) -> List[Board]:
        return self.board_repo.get_all()

    def create_board(self, name: str, description: str = None) -> Board:
        # 중복 체크
        existing = self.board_repo.get_by_name(name)
        if existing:
            raise ValueError(f"'{name}' 게시판은 이미 존재합니다")

        return self.board_repo.create(name=name, description=description)
