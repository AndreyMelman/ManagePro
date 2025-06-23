from fastapi import (
    APIRouter,
    Request,
    Form,
    Depends,
    Response,
    status,
    HTTPException,
)
from fastapi.responses import RedirectResponse
from core.schemas.user import UserCreate, UserUpdate
from api.dependencies.authentication import (
    get_user_manager,
    authentication_backend,
    get_access_tokens_db,
)
from core.authentication.user_manager import UserManager
from fastapi_users.password import PasswordHelper

from core.models import AccessToken
from utils.templates import templates
from fastapi import status as http_status
from fastapi_users.schemas import BaseUserUpdate
from fastapi_users.exceptions import (
    UserNotExists,
    UserAlreadyExists,
)

router = APIRouter()


@router.get("/login")
async def login_get(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "request": request,
        },
    )


@router.post("/login")
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
    access_tokens_db: AccessToken = Depends(get_access_tokens_db),
):
    strategy = authentication_backend.get_strategy(access_tokens_db)

    try:
        user = await user_manager.get_by_email(email)
    except UserNotExists:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={
                "request": request,
                "error": "Неверный email или пароль",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    password_helper = PasswordHelper()
    is_valid, new_hash = password_helper.verify_and_update(
        password, user.hashed_password
    )

    if not is_valid:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={
                "request": request,
                "error": "Неверный email или пароль",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if new_hash is not None:
        user.hashed_password = new_hash
        user_update = BaseUserUpdate(password=new_hash)
        await user_manager.update(user_update, user)

    token = await strategy.write_token(user)
    response = RedirectResponse(
        url="/profile",
        status_code=status.HTTP_302_FOUND,
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,
        path="/",
    )
    return response


@router.get("/register")
async def register_get(request: Request):
    return templates.TemplateResponse(
        "auth/register.html",
        {"request": request},
    )


@router.post("/register")
async def register_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
    access_tokens_db: AccessToken = Depends(get_access_tokens_db),
):
    try:
        await user_manager.get_by_email(email)
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Пользователь с таким email уже существует",
                "email": email,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception:
        pass

    user_create = UserCreate(email=email, password=password)

    try:
        user = await user_manager.create(user_create, safe=True)
    except UserAlreadyExists:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Пользователь с таким email уже существует",
                "email": email,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": f"Ошибка регистрации: {str(e)}",
                "email": email,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    strategy = authentication_backend.get_strategy(access_tokens_db)
    token = await strategy.write_token(user)

    response = RedirectResponse(
        url="/profile",
        status_code=status.HTTP_302_FOUND,
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,  # 1 день
        path="/",
    )
    return response


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(
        url="/login",
        status_code=status.HTTP_302_FOUND,
    )
    response.delete_cookie(key="access_token", path="/")
    return response


async def get_current_user_from_cookie(
    request: Request,
    user_manager: UserManager = Depends(get_user_manager),
    access_tokens_db=Depends(get_access_tokens_db),
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    strategy = authentication_backend.get_strategy(access_tokens_db)

    user = await strategy.read_token(token, user_manager)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return user


@router.get("/profile")
async def profile(
    request: Request,
    user=Depends(get_current_user_from_cookie),
):
    return templates.TemplateResponse(
        "auth/profile.html",
        {"request": request, "user": user},
    )


@router.get("/profile/edit")
async def edit_profile_get(
    request: Request,
    user=Depends(get_current_user_from_cookie),
):
    return templates.TemplateResponse(
        "auth/edit_profile.html",
        {"request": request, "user": user},
    )


@router.post("/profile/edit")
async def edit_profile_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(None),
    password_confirm: str = Form(None),
    user_manager: UserManager = Depends(get_user_manager),
    user=Depends(get_current_user_from_cookie),
    access_tokens_db: AccessToken = Depends(get_access_tokens_db),
):
    errors = []
    if email != user.email:
        try:
            existing = await user_manager.get_by_email(email)
            if existing:
                errors.append("Пользователь с таким email уже существует")
        except UserNotExists:
            pass
    if password:
        if password != password_confirm:
            errors.append("Пароли не совпадают")
    if errors:
        return templates.TemplateResponse(
            "auth/edit_profile.html",
            {"request": request, "user": user, "errors": errors, "email": email},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    update_data = {}
    if email != user.email:
        update_data["email"] = email
    if password:
        password_helper = PasswordHelper()
        update_data["password"] = password_helper.hash(password)
    if update_data:
        user_update = UserUpdate(**update_data)
        await user_manager.update(user_update, user)
    strategy = authentication_backend.get_strategy(access_tokens_db)
    token = await strategy.write_token(user)
    response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,
        path="/",
    )
    return response
