#!/usr/bin/env python3
"""
初始化用户数据脚本
创建两个测试用户：
1. admin/admin - 超级管理员
2. user1/user1 - 普通用户
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import User
from admin.auth import get_password_hash


def init_users():
    """初始化用户数据"""
    # 创建表
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 检查是否已有用户
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"数据库中已有 {existing_users} 个用户，跳过初始化")
            return
        
        # 创建超级管理员
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("admin"),
            role="admin",
            is_active=True
        )
        
        # 创建普通用户
        normal_user = User(
            username="user1",
            hashed_password=get_password_hash("user1"),
            role="user",
            is_active=True
        )
        
        db.add(admin_user)
        db.add(normal_user)
        db.commit()
        
        print("用户初始化成功！")
        print("超级管理员: admin / admin")
        print("普通用户: user1 / user1")
        
    except Exception as e:
        print(f"初始化用户失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_users()