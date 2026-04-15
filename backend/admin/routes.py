from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models import User
from admin import schemas
from admin.crud import get_user_by_username, get_users, create_user, update_user, delete_user
from admin.auth import (
    verify_password, 
    create_access_token, 
    get_current_active_user,
    require_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = get_user_by_username(db, user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=schemas.User)
def get_me(current_user: User = Depends(get_current_active_user)):
    """获取当前登录用户信息"""
    return current_user


@router.get("/menus", response_model=schemas.MenuResponse)
def get_menus(current_user: User = Depends(get_current_active_user)):
    """获取导航菜单（根据角色返回不同菜单）"""
    
    # 基础菜单 - 所有用户都能看到
    base_menus = [
        {
            "id": "posts",
            "name": "文章管理",
            "path": "/admin/posts",
            "icon": "document"
        }
    ]
    
    # 管理员额外菜单
    admin_menus = [
        {
            "id": "users",
            "name": "用户管理",
            "path": "/admin/users",
            "icon": "user"
        }
    ]
    
    # 根据角色返回菜单
    if current_user.role == "admin":
        menus = base_menus + admin_menus
    else:
        menus = base_menus
    
    return {"menus": menus}


# ==================== 用户管理接口（仅管理员）====================

@router.get("/users", response_model=list[schemas.User])
def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """获取用户列表（仅管理员）"""
    return get_users(db, skip=skip, limit=limit)


@router.post("/users", response_model=schemas.User)
def create_new_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """创建用户（仅管理员）"""
    # 检查用户名是否已存在
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 验证角色
    if user.role not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的角色类型"
        )
    
    return create_user(db=db, user=user)


@router.put("/users/{user_id}", response_model=schemas.User)
def update_existing_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """更新用户（仅管理员）"""
    db_user = update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return db_user


@router.delete("/users/{user_id}")
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """删除用户（仅管理员）"""
    # 不能删除自己
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除当前登录用户"
        )
    
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return {"message": "用户删除成功"}