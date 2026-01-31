import os  
from fastapi import FastAPI, HTTPException  
from fastapi.middleware.cors import CORSMiddleware  
from sqlalchemy import create_engine, Column, Integer, String, DateTime  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker, Session  
from pydantic import BaseModel  
from datetime import datetime  
import logging  
# 配置日誌  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  
# 環境變數  
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')  
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')  
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')  
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'zeabur')  
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')  
# 構建 MySQL 連接字符串  
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"  
logger.info(f"連接到 MySQL: {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")  
# 創建數據庫引擎  
engine = create_engine(  
    DATABASE_URL,  
    pool_pre_ping=True,  
    pool_recycle=3600,  
    echo=False  
)  
# 創建會話工廠  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
# 基類  
Base = declarative_base()  
# 定義模型  
class User(Base):  
    __tablename__ = "users"  
      
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String(100), index=True)  
    email = Column(String(100), unique=True, index=True)  
    created_at = Column(DateTime, default=datetime.utcnow)  
# 創建所有表  
Base.metadata.create_all(bind=engine)  
# Pydantic 模型  
class UserCreate(BaseModel):  
    name: str  
    email: str  
class UserResponse(BaseModel):  
    id: int  
    name: str  
    email: str  
    created_at: datetime  
      
    class Config:  
        from_attributes = True  
# 創建 FastAPI 應用  
app = FastAPI(  
    title="APIProject",  
    description="FastAPI with MySQL",  
    version="1.0.0"  
)  
# 添加 CORS 中間件  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
# 依賴注入  
def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close()  
# 路由  
@app.get("/")  
async def root():  
    return {  
        "message": "歡迎使用 APIProject",  
        "status": "running",  
        "database": MYSQL_DATABASE,  
        "host": MYSQL_HOST  
    }  
@app.get("/health")  
async def health_check(db: Session = None):  
    """健康檢查端點"""  
    try:  
        # 測試數據庫連接  
        db = SessionLocal()  
        db.execute("SELECT 1")  
        db.close()  
        return {  
            "status": "healthy",  
            "database": "connected",  
            "message": "應用運行正常"  
        }  
    except Exception as e:  
        logger.error(f"健康檢查失敗: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"數據庫連接失敗: {str(e)}")  
@app.post("/users", response_model=UserResponse)  
async def create_user(user: UserCreate, db: Session = None):  
    """創建新用戶"""  
    try:  
        db = SessionLocal()  
        db_user = User(name=user.name, email=user.email)  
        db.add(db_user)  
        db.commit()  
        db.refresh(db_user)  
        db.close()  
        return db_user  
    except Exception as e:  
        logger.error(f"創建用戶失敗: {str(e)}")  
        raise HTTPException(status_code=400, detail=f"創建用戶失敗: {str(e)}")  
@app.get("/users", response_model=list[UserResponse])  
async def get_users(db: Session = None):  
    """獲取所有用戶"""  
    try:  
        db = SessionLocal()  
        users = db.query(User).all()  
        db.close()  
        return users  
    except Exception as e:  
        logger.error(f"獲取用戶失敗: {str(e)}")  
        raise HTTPException(status_code=400, detail=f"獲取用戶失敗: {str(e)}")  
@app.get("/users/{user_id}", response_model=UserResponse)  
async def get_user(user_id: int, db: Session = None):  
    """獲取特定用戶"""  
    try:  
        db = SessionLocal()  
        user = db.query(User).filter(User.id == user_id).first()  
        db.close()  
        if not user:  
            raise HTTPException(status_code=404, detail="用戶不存在")  
        return user  
    except HTTPException:  
        raise  
    except Exception as e:  
        logger.error(f"獲取用戶失敗: {str(e)}")  
        raise HTTPException(status_code=400, detail=f"獲取用戶失敗: {str(e)}")  
@app.delete("/users/{user_id}")  
async def delete_user(user_id: int, db: Session = None):  
    """刪除用戶"""  
    try:  
        db = SessionLocal()  
        user = db.query(User).filter(User.id == user_id).first()  
        if not user:  
            db.close()  
            raise HTTPException(status_code=404, detail="用戶不存在")  
        db.delete(user)  
        db.commit()  
        db.close()  
        return {"message": "用戶已刪除"}  
    except HTTPException:  
        raise  
    except Exception as e:  
        logger.error(f"刪除用戶失敗: {str(e)}")  
        raise HTTPException(status_code=400, detail=f"刪除用戶失敗: {str(e)}")  
if __name__ == "__main__":  
    import uvicorn  
    port = int(os.environ.get("PORT", 8080))  
    uvicorn.run(app, host="0.0.0.0", port=port)  
