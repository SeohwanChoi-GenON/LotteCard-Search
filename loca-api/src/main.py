from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loca_api.api.v1.loca_talk import router as loca_talk_router

# FastAPI 앱 생성
app = FastAPI(
    title="LOCA API",
    description="롯데카드 LOCA앱 챗봇 및 검색 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영환경에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(
    loca_talk_router,
    prefix="/api/v1/loca-talk",
    tags=["loca-talk"]
)

@app.get("/")
async def root():
    """API 상태 확인"""
    return {"message": "LOCA API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)