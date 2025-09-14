import uvicorn
import logging

from configuration.web.app_factory import create_app
from configuration.settings.app_settings import get_settings
from configuration.settings.constants import UvicornConfig
from configuration.di_container import init_container

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 전역 앱 인스턴스 (import string 방식을 위함)
app = None

def create_application():
    """애플리케이션 팩토리 함수"""
    global app
    if app is None:
        # 설정 로드
        settings = get_settings()

        # DI 컨테이너 초기화
        init_container(settings)

        # FastAPI 앱 생성
        app = create_app(settings)
        logger.info("Application created successfully")

    return app

# 모듈 로드 시 앱 생성 (import string 방식을 위함)
app = create_application()

def main():
    """애플리케이션 진입점"""
    try:
        settings = get_settings()

        logger.info("Starting LOCA Chat API server...")

        # 개발 환경과 프로덕션 환경 구분
        if settings.DEBUG:
            # 개발 환경: reload 사용 (import string 방식)
            uvicorn.run(
                "main:app",
                host=UvicornConfig.HOST,
                port=UvicornConfig.PORT,
                log_level=UvicornConfig.LOG_LEVEL,
                timeout_keep_alive=UvicornConfig.TIMEOUT_KEEP_ALIVE,
                reload=True
            )
        else:
            # 프로덕션 환경: workers 사용
            uvicorn.run(
                app=app,
                host=UvicornConfig.HOST,
                port=UvicornConfig.PORT,
                workers=UvicornConfig.WORKERS,
                log_level=UvicornConfig.LOG_LEVEL,
                timeout_keep_alive=UvicornConfig.TIMEOUT_KEEP_ALIVE
            )

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise


if __name__ == '__main__':
    main()