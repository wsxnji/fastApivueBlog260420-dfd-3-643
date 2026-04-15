import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User
from admin.auth import get_password_hash


def init_users():
    db = next(get_db())
    
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin = User(
            username="admin",
            password=get_password_hash("admin"),
            role="admin"
        )
        db.add(admin)
        print("创建超级管理员: admin/admin")
    
    user1 = db.query(User).filter(User.username == "user1").first()
    if not user1:
        user = User(
            username="user1",
            password=get_password_hash("user1"),
            role="user"
        )
        db.add(user)
        print("创建普通用户: user1/user1")
    
    db.commit()
    print("用户初始化完成！")


if __name__ == "__main__":
    init_users()
