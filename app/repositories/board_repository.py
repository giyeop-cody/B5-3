"""게시판 리포지토리"""
from sqlalchemy.orm import Session
from app.models import Board


class BoardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, board_id: int) -> Board:
        return self.db.query(Board).filter(Board.id == board_id).first()

    def get_by_name(self, name: str) -> Board:
        return self.db.query(Board).filter(Board.name == name).first()

    def get_all(self):
        return self.db.query(Board).all()

    def create(self, name: str, description: str = None) -> Board:
        board = Board(name=name, description=description)
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board
