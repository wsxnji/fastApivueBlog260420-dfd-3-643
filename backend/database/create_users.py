import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine, Base
import models
import crud
import schemas

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    if not crud.get_user_by_username(db, "admin"):
        admin_user = schemas.UserCreate(
            username="admin",
            password="admin",
            role="超级管理员"
        )
        crud.create_user(db, admin_user)
        print("创建用户: admin (超级管理员)")

    if not crud.get_user_by_username(db, "user1"):
        user1 = schemas.UserCreate(
            username="user1",
            password="user1",
            role="普通用户"
        )
        crud.create_user(db, user1)
        print("创建用户: user1 (普通用户)")

    print("用户初始化完成!")
finally:
    db.close()
