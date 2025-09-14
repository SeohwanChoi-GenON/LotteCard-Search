"""
🚀 LOCA Gen-AI Application Entry Point

DDD + Ports & Adapters (Hexagonal Architecture) 기반의
LOCA Gen-AI 애플리케이션 진입점입니다.

아키텍처 흐름:
1. Configuration Layer에서 설정 초기화
2. Infrastructure Primary Adapter(FastAPI)를 통해 애플리케이션 생성
3. Uvicorn 서버로 HTTP 요청 수신 시작

레이어 의존성:
- main.py (Entry Point)
  ├── configuration/ (Configuration Layer)
  └── infrastructure/adapters/primary/web/ (Primary Adapter)
      └── application/ports/primary/ (Primary Ports - Use Cases)
          └── domain/ (Domain Layer)
"""
import asyncio
import sys
import os
from pathlib import Path

# 프로젝트 루트 경로를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import uvicorn
from fastapi import FastAPI

# Configuration Layer
from configuration import get_loca_config, LOCAConfig

# Infrastructure Primary Adapter
from infrastructure.adapters.primary.web.app_factory import create_app


class LOCAApplicationRunner:
    """LOCA 애플리케이션 실행 관리자"""

    def __init__(self):
        self.config: LOCAConfig = get_loca_config()
        self.app: FastAPI = None

    async def initialize_application(self) -> FastAPI:
        """애플리케이션 초기화"""
        print(f"🌟 Initializing {self.config.system_name} {self.config.system_version}")
        print(f"📍 Environment: {self.config.deployment_env.value}")
        print(f"🔧 Debug Mode: {self.config.debug_mode}")

        # Primary Adapter(FastAPI App) 생성
        self.app = await create_app(self.config)

        return self.app

    def get_uvicorn_config(self) -> dict:
        """Uvicorn 서버 설정 구성"""
        base_config = {
            "host": self.config.app.host,
            "port": self.config.app.port,
            "log_level": self.config.monitoring.log_level.lower(),
            "access_log": self.config.monitoring.enable_access_log,
            "timeout_keep_alive": 30,
            "timeout_graceful_shutdown": 10,
        }

        # 환경별 설정
        if self.config.is_development():
            # 개발 환경 설정
            base_config.update({
                "reload": True,
                "reload_dirs": [str(project_root)],
                "reload_excludes": ["*.pyc", "__pycache__"],
                "workers": 1,  # 리로드 모드에서는 단일 워커
            })

        elif self.config.is_production():
            # 운영 환경 설정
            base_config.update({
                "workers": self.config.app.worker_count or self._calculate_worker_count(),
                "worker_class": "uvicorn.workers.UvicornWorker",
                "preload": True,  # 워커 프로세스 미리 로드
                "keepalive": 2,
            })

        else:
            # 기본 설정 (local, test 등)
            base_config.update({
                "workers": 1,
                "reload": self.config.debug_mode,
            })

        return base_config

    def _calculate_worker_count(self) -> int:
        """최적 워커 수 계산"""
        try:
            # CPU 코어 수 기반 계산 (일반적으로 (2 x CPU) + 1)
            cpu_count = os.cpu_count() or 1
            return min(max((2 * cpu_count) + 1, 2), 8)  # 최소 2, 최대 8
        except:
            return 2  # 기본값

    async def run_async(self):
        """비동기 방식으로 애플리케이션 실행"""
        try:
            # 애플리케이션 초기화
            app = await self.initialize_application()

            # Uvicorn 서버 설정
            uvicorn_config = self.get_uvicorn_config()

            print(f"🚀 Starting {self.config.system_name} server...")
            print(f"🌐 Server will run at: http://{uvicorn_config['host']}:{uvicorn_config['port']}")
            print(f"📚 API Documentation: http://{uvicorn_config['host']}:{uvicorn_config['port']}{self.config.app.docs_url}")

            # 개발 모드에서는 직접 실행, 운영에서는 app 반환
            if self.config.is_development():
                config = uvicorn.Config(app, **uvicorn_config)
                server = uvicorn.Server(config)
                await server.serve()
            else:
                # 운영 환경에서는 별도 프로세스 관리자 사용 권장
                uvicorn.run(app, **uvicorn_config)

        except Exception as e:
            print(f"❌ Failed to start application: {e}")
            if self.config.debug_mode:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    def run_sync(self):
        """동기 방식으로 애플리케이션 실행"""
        try:
            # 이벤트 루프 생성 및 실행
            if sys.platform.startswith('win'):
                # Windows에서 ProactorEventLoop 사용
                loop = asyncio.ProactorEventLoop()
                asyncio.set_event_loop(loop)
            else:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # 애플리케이션 실행
            loop.run_until_complete(self.run_async())

        except KeyboardInterrupt:
            print(f"\n🛑 {self.config.system_name} server stopped by user")
        except Exception as e:
            print(f"❌ Application crashed: {e}")
            if self.config.debug_mode:
                import traceback
                traceback.print_exc()
            sys.exit(1)
        finally:
            # 이벤트 루프 정리
            try:
                loop.close()
            except:
                pass


def create_app_for_deployment() -> FastAPI:
    """
    배포용 애플리케이션 팩토리 함수

    WSGI/ASGI 서버(Gunicorn, Uvicorn 등)에서 직접 사용할 수 있는
    FastAPI 앱 인스턴스를 반환합니다.

    사용 예:
    - gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
    - uvicorn main:app --workers 4
    """
    config = get_loca_config()

    # 비동기 앱 생성을 동기 방식으로 래핑
    async def _create_app():
        return await create_app(config)

    # 이벤트 루프에서 앱 생성
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_create_app())


def main():
    """
    🎯 메인 진입점

    LOCA Gen-AI 애플리케이션을 시작합니다.
    DDD + Ports & Adapters 아키텍처를 사용하여 구성된 애플리케이션을 실행합니다.
    """
    print("="*80)
    print("🤖 LOCA Gen-AI Application Starting...")
    print("📐 Architecture: Domain Driven Design + Ports & Adapters (Hexagonal)")
    print("🐍 Python FastAPI Application")
    print("="*80)

    try:
        # 애플리케이션 러너 생성 및 실행
        runner = LOCAApplicationRunner()
        runner.run_sync()

    except Exception as e:
        print(f"💥 Critical error during startup: {e}")
        sys.exit(1)


# 배포용 앱 인스턴스 (WSGI/ASGI 서버용)
app = create_app_for_deployment()

if __name__ == "__main__":
    main()