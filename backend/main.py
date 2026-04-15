from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from routes import router
from admin.auth import router as auth_router
from crud import get_user_by_username, create_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/api/admin", tags=["admin"])


def init_db():
    db = SessionLocal()
    try:
        if not get_user_by_username(db, "admin"):
            create_user(db, "admin", "admin", "超级管理员")
            print("Created admin user")
        if not get_user_by_username(db, "user1"):
            create_user(db, "user1", "user1", "普通用户")
            print("Created user1")
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Welcome to Personal Blog API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
