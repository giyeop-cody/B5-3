"""화면 라우터 (Jinja2 템플릿)

공통 에러/알림 표시 전략 (#16):
- 세션 기반 flash message 사용
- set_flash(): 세션에 메시지 저장
- get_flash(): 세션에서 메시지 읽기 + 삭제 (1회용)
- 모든 템플릿에서 base.html의 flash 영역으로 자동 표시
"""
from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.board_repository import BoardRepository
from app.repositories.post_repository import PostRepository
from app.services.board_service import BoardService
from app.services.post_service import PostService
from app.auth.session import get_current_user_from_session, login_user, logout_user
from app.auth.service import AuthService
from app.repositories.user_repository import UserRepository
from typing import Optional

router = APIRouter(tags=["views"])
templates = Jinja2Templates(directory="app/templates")


# ===== Flash Message 유틸리티 (#16: 공통 에러 표시 전략) =====

def set_flash(request: Request, category: str, message: str):
    """세션에 flash 메시지 저장 (1회용)

    Args:
        category: "success", "error", "warning" 중 하나
        message: 사용자에게 표시할 메시지
    """
    request.session["_flash"] = {"category": category, "message": message}


def get_flash(request: Request) -> Optional[dict]:
    """세션에서 flash 메시지를 읽고 삭제 (1회용)"""
    flash = request.session.pop("_flash", None)
    return flash


# ===== 홈페이지 =====
@router.get("/")
async def home(request: Request):
    """홈페이지"""
    user = get_current_user_from_session(request)
    flash = get_flash(request)
    return templates.TemplateResponse(
        request, "home.html", {"user": user, "flash": flash}
    )


# ===== 인증 화면 =====
@router.get("/login")
async def login_page(request: Request, next: Optional[str] = Query(None)):
    """로그인 페이지

    Args:
        next: 로그인 후 이동할 원래 페이지 (#2: next 파라미터)
              예: /login?next=/posts/new
    """
    user = get_current_user_from_session(request)
    if user:
        return RedirectResponse(url="/", status_code=302)

    flash = get_flash(request)
    return templates.TemplateResponse(
        request, "login.html",
        {"user": None, "error": None, "next_url": next, "flash": flash}
    )


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next_url: Optional[str] = Form(None),  # hidden field에서 전달 (#2)
    db: Session = Depends(get_db)
):
    """로그인 처리

    성공 시: next_url이 있으면 해당 페이지로, 없으면 메인으로 이동 (#1, #2)
    실패 시: 에러 메시지와 함께 로그인 페이지 재표시
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    user = auth_service.authenticate(username, password)

    if not user:
        return templates.TemplateResponse(
            request, "login.html",
            {
                "user": None,
                "error": "아이디 또는 비밀번호가 올바르지 않습니다",
                "next_url": next_url
            }
        )

    login_user(request, user.id)

    # #1: 로그인 성공 피드백
    set_flash(request, "success", f"{user.username}님, 환영합니다! 로그인되었습니다.")

    # #2: next 파라미터가 있으면 원래 페이지로 복귀
    redirect_url = next_url if next_url and next_url.startswith("/") else "/"
    return RedirectResponse(url=redirect_url, status_code=302)


@router.post("/logout")
async def logout_submit(request: Request):
    """로그아웃 처리"""
    logout_user(request)
    set_flash(request, "success", "로그아웃되었습니다.")
    return RedirectResponse(url="/", status_code=302)


# ===== 게시판 화면 =====
@router.get("/boards")
async def boards_list(request: Request, db: Session = Depends(get_db)):
    """게시판 목록"""
    user = get_current_user_from_session(request)
    flash = get_flash(request)
    board_service = BoardService(BoardRepository(db))
    boards = board_service.get_all_boards()

    return templates.TemplateResponse(
        request, "boards/list.html",
        {"user": user, "boards": boards, "flash": flash}
    )


# ===== 내 글 =====
@router.get("/my-posts")
async def my_posts(request: Request, db: Session = Depends(get_db)):
    """내가 작성한 글 목록"""
    user = get_current_user_from_session(request)

    if not user:
        # #2: 원래 페이지 복귀를 위한 next 파라미터
        return RedirectResponse(url="/login?next=/my-posts", status_code=302)

    flash = get_flash(request)
    post_service = PostService(PostRepository(db))
    posts = post_service.get_posts_by_author(user.id)

    return templates.TemplateResponse(
        request, "my_posts.html",
        {"user": user, "posts": posts, "flash": flash}
    )


@router.get("/boards/{board_id}")
async def board_detail(
    request: Request,
    board_id: int,
    db: Session = Depends(get_db)
):
    """게시판 상세 (게시글 목록 포함)"""
    user = get_current_user_from_session(request)
    flash = get_flash(request)
    board_service = BoardService(BoardRepository(db))
    post_service = PostService(PostRepository(db))

    try:
        board = board_service.get_board(board_id)
        posts = post_service.get_posts_by_board(board_id)

        return templates.TemplateResponse(
            request, "boards/detail.html",
            {"user": user, "board": board, "posts": posts, "flash": flash}
        )
    except ValueError:
        set_flash(request, "error", f"게시판 #{board_id}를 찾을 수 없습니다.")
        return RedirectResponse(url="/boards", status_code=302)


# ===== 게시글 화면 =====
@router.get("/posts/new")
async def post_create_page(
    request: Request,
    board_id: int = None,
    db: Session = Depends(get_db)
):
    """게시글 작성 페이지"""
    user = get_current_user_from_session(request)

    if not user:
        # #2: 원래 페이지 복귀
        next_url = f"/posts/new?board_id={board_id}" if board_id else "/posts/new"
        return RedirectResponse(url=f"/login?next={next_url}", status_code=302)

    flash = get_flash(request)
    board_service = BoardService(BoardRepository(db))
    boards = board_service.get_all_boards()

    return templates.TemplateResponse(
        request, "posts/create.html",
        {
            "user": user,
            "boards": boards,
            "selected_board_id": board_id,
            "flash": flash
        }
    )


@router.post("/posts/new")
async def post_create_submit(
    request: Request,
    title: str = Form(...),
    content: str = Form(""),
    board_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """게시글 작성 처리"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(url="/login?next=/posts/new", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post = post_service.create_post(
            title=title,
            content=content,
            author_id=user.id,
            board_id=board_id
        )
        set_flash(request, "success", "게시글이 작성되었습니다.")
        return RedirectResponse(url=f"/posts/{post.id}", status_code=302)
    except ValueError as e:
        board_service = BoardService(BoardRepository(db))
        boards = board_service.get_all_boards()

        return templates.TemplateResponse(
            request, "posts/create.html",
            {
                "user": user,
                "boards": boards,
                "error": str(e),
                "title": title,
                "content": content,
                "selected_board_id": board_id
            }
        )


@router.get("/posts/{post_id}")
async def post_detail(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시글 상세"""
    user = get_current_user_from_session(request)
    flash = get_flash(request)
    post_service = PostService(PostRepository(db))

    try:
        post = post_service.get_post(post_id)

        return templates.TemplateResponse(
            request, "posts/detail.html",
            {"user": user, "post": post, "flash": flash}
        )
    except ValueError:
        set_flash(request, "error", f"게시글 #{post_id}를 찾을 수 없습니다.")
        return RedirectResponse(url="/boards", status_code=302)


@router.get("/posts/{post_id}/edit")
async def post_edit_page(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시글 수정 페이지"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(
            url=f"/login?next=/posts/{post_id}/edit", status_code=302
        )

    flash = get_flash(request)
    post_service = PostService(PostRepository(db))

    try:
        post = post_service.get_post(post_id)

        if post.author_id != user.id:
            set_flash(request, "error", "자신의 게시글만 수정할 수 있습니다.")
            return RedirectResponse(url=f"/posts/{post_id}", status_code=302)

        return templates.TemplateResponse(
            request, "posts/edit.html",
            {"user": user, "post": post, "flash": flash}
        )
    except ValueError:
        set_flash(request, "error", f"게시글 #{post_id}를 찾을 수 없습니다.")
        return RedirectResponse(url="/boards", status_code=302)


@router.post("/posts/{post_id}/edit")
async def post_edit_submit(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(""),
    db: Session = Depends(get_db)
):
    """게시글 수정 처리"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(
            url=f"/login?next=/posts/{post_id}/edit", status_code=302
        )

    post_service = PostService(PostRepository(db))

    try:
        post = post_service.update_post(
            post_id=post_id,
            user_id=user.id,
            title=title,
            content=content
        )
        set_flash(request, "success", "게시글이 수정되었습니다.")
        return RedirectResponse(url=f"/posts/{post.id}", status_code=302)
    except (ValueError, PermissionError) as e:
        post = post_service.get_post(post_id)
        return templates.TemplateResponse(
            request, "posts/edit.html",
            {"user": user, "post": post, "error": str(e)}
        )


@router.post("/posts/{post_id}/delete")
async def post_delete(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시글 삭제"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post = post_service.get_post(post_id)
        board_id = post.board_id
        post_service.delete_post(post_id=post_id, user_id=user.id)
        set_flash(request, "success", "게시글이 삭제되었습니다.")
        return RedirectResponse(url=f"/boards/{board_id}", status_code=302)
    except PermissionError:
        set_flash(request, "error", "자신의 게시글만 삭제할 수 있습니다.")
        return RedirectResponse(url=f"/posts/{post_id}", status_code=302)
    except ValueError:
        set_flash(request, "error", "게시글을 찾을 수 없습니다.")
        return RedirectResponse(url="/boards", status_code=302)


@router.post("/posts/{post_id}/publish")
async def post_publish(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시글 공개 (#6: 실패 시 오류 사유 표시)"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post_service.publish_post(post_id=post_id, user_id=user.id)
        set_flash(request, "success", "게시글이 공개되었습니다.")
    except PermissionError:
        set_flash(request, "error", "자신의 게시글만 공개할 수 있습니다.")
    except ValueError as e:
        set_flash(request, "error", str(e))

    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)


@router.post("/posts/{post_id}/hide")
async def post_hide(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시글 비공개 (#6: 실패 시 오류 사유 표시)"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post_service.hide_post(post_id=post_id, user_id=user.id)
        set_flash(request, "success", "게시글이 비공개로 변경되었습니다.")
    except PermissionError:
        set_flash(request, "error", "자신의 게시글만 비공개할 수 있습니다.")
    except ValueError as e:
        set_flash(request, "error", str(e))

    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)
