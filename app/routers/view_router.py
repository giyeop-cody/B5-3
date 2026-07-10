"""화면 라우터 (Jinja2 템플릿)"""
from fastapi import APIRouter, Depends, Request, Form
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

router = APIRouter(tags=["views"])
templates = Jinja2Templates(directory="app/templates")


# ===== 홈페이지 =====
@router.get("/")
async def home(request: Request):
    """홈페이지"""
    user = get_current_user_from_session(request)
    return templates.TemplateResponse(
        request, "home.html", {"user": user}
    )


# ===== 인증 화면 =====
@router.get("/login")
async def login_page(request: Request):
    """로그인 페이지"""
    user = get_current_user_from_session(request)
    if user:
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse(
        request, "login.html", {"user": None, "error": None}
    )


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """로그인 처리"""
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    user = auth_service.authenticate(username, password)

    if not user:
        return templates.TemplateResponse(
            request, "login.html",
            {"user": None, "error": "아이디 또는 비밀번호가 올바르지 않습니다"}
        )

    login_user(request, user.id)
    return RedirectResponse(url="/", status_code=302)


@router.post("/logout")
async def logout_submit(request: Request):
    """로그아웃 처리"""
    logout_user(request)
    return RedirectResponse(url="/", status_code=302)


# ===== 게시판 화면 =====
@router.get("/boards")
async def boards_list(request: Request, db: Session = Depends(get_db)):
    """게시판 목록"""
    user = get_current_user_from_session(request)
    board_service = BoardService(BoardRepository(db))
    boards = board_service.get_all_boards()

    return templates.TemplateResponse(
        request, "boards/list.html", {"user": user, "boards": boards}
    )


@router.get("/boards/{board_id}")
async def board_detail(
    request: Request,
    board_id: int,
    db: Session = Depends(get_db)
):
    """게시판 상세 (게시글 목록 포함)"""
    user = get_current_user_from_session(request)
    board_service = BoardService(BoardRepository(db))
    post_service = PostService(PostRepository(db))

    try:
        board = board_service.get_board(board_id)
        posts = post_service.get_posts_by_board(board_id)

        return templates.TemplateResponse(
            request, "boards/detail.html",
            {"user": user, "board": board, "posts": posts}
        )
    except ValueError:
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
        return RedirectResponse(url="/login", status_code=302)

    board_service = BoardService(BoardRepository(db))
    boards = board_service.get_all_boards()

    return templates.TemplateResponse(
        request, "posts/create.html",
        {
            "user": user,
            "boards": boards,
            "selected_board_id": board_id
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
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post = post_service.create_post(
            title=title,
            content=content,
            author_id=user.id,
            board_id=board_id
        )
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
    post_service = PostService(PostRepository(db))

    try:
        post = post_service.get_post(post_id)

        return templates.TemplateResponse(
            request, "posts/detail.html",
            {"user": user, "post": post}
        )
    except ValueError:
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
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post = post_service.get_post(post_id)

        if post.author_id != user.id:
            return RedirectResponse(url=f"/posts/{post_id}", status_code=302)

        return templates.TemplateResponse(
            request, "posts/edit.html",
            {"user": user, "post": post}
        )
    except ValueError:
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
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post = post_service.update_post(
            post_id=post_id,
            user_id=user.id,
            title=title,
            content=content
        )
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
        return RedirectResponse(url=f"/boards/{board_id}", status_code=302)
    except (ValueError, PermissionError):
        return RedirectResponse(url=f"/posts/{post_id}", status_code=302)


@router.post("/posts/{post_id}/publish")
async def post_publish(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시글 공개"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post_service.publish_post(post_id=post_id, user_id=user.id)
    except (ValueError, PermissionError):
        pass

    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)


@router.post("/posts/{post_id}/hide")
async def post_hide(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시글 비공개"""
    user = get_current_user_from_session(request)

    if not user:
        return RedirectResponse(url="/login", status_code=302)

    post_service = PostService(PostRepository(db))

    try:
        post_service.hide_post(post_id=post_id, user_id=user.id)
    except (ValueError, PermissionError):
        pass

    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)
