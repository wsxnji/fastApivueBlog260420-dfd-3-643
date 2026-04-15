from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from routes import router
from admin.auth import router as admin_router
import crud
import schemas

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化用户数据
db = SessionLocal()
try:
    if not crud.get_user_by_username(db, "admin"):
        admin_user = schemas.UserCreate(
            username="admin",
            password="admin",
            role="超级管理员"
        )
        crud.create_user(db, admin_user)
    
    if not crud.get_user_by_username(db, "user1"):
        user1 = schemas.UserCreate(
            username="user1",
            password="user1",
            role="普通用户"
        )
        crud.create_user(db, user1)
finally:
    db.close()

app = FastAPI(title="Personal Blog API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api")
app.include_router(admin_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to Personal Blog API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
