# 🤖 LOCA Gen-AI Development & Deployment Makefile
# Spring Boot Profile Style Environment Management

.PHONY: help install dev local staging prod test clean lint format docker health env-info

# 기본 설정
PYTHON := python3
PIP := pip3
PROJECT_NAME := loca-gen-ai
SRC_DIR := src

# Spring Boot 스타일 환경 관리
ENV_DEV := development
ENV_LOCAL := local
ENV_STAGING := staging
ENV_PROD := production

help: ## 📋 사용 가능한 명령어 목록 표시
	@echo "🤖 LOCA Gen-AI Development Commands (Spring Boot Profile Style)"
	@echo "=================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 📦 의존성 설치
	@echo "📦 Installing dependencies..."
	$(PIP) install -r requirements.txt
	@if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt; fi

# 🌍 환경별 실행 명령어 (Spring Boot Profile 스타일)
dev: ## 🔧 개발 환경으로 서버 시작 (auto-reload)
	@echo "🔧 Starting development server (auto-reload enabled)..."
	@echo "📄 Using profile: $(ENV_DEV)"
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=$(ENV_DEV) $(PYTHON) main.py

local: ## 🏠 로컬 환경으로 서버 시작
	@echo "🏠 Starting local server..."
	@echo "📄 Using profile: $(ENV_LOCAL)"
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=$(ENV_LOCAL) $(PYTHON) main.py

staging: ## 🎭 스테이징 환경으로 서버 시작
	@echo "🎭 Starting staging server..."
	@echo "📄 Using profile: $(ENV_STAGING)"
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=$(ENV_STAGING) $(PYTHON) main.py

prod: ## 🚀 운영 환경으로 서버 시작
	@echo "🚀 Starting production server..."
	@echo "📄 Using profile: $(ENV_PROD)"
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=$(ENV_PROD) $(PYTHON) main.py

# 🔍 환경 정보
env-info: ## ℹ️ 현재 환경 설정 정보 표시
	@echo "🔍 Environment Information"
	@echo "=========================="
	@echo "📋 Available profiles:"
	@echo "  - development (.env.development)"
	@echo "  - local (.env.local)"
	@echo "  - staging (.env.staging)"
	@echo "  - production (.env.production)"
	@echo ""
	@echo "📄 Available environment files:"
	@cd $(SRC_DIR) && find . -name ".env*" -type f | sort
	@echo ""
	@echo "🔧 Current LOCA_DEPLOYMENT_ENV: $${LOCA_DEPLOYMENT_ENV:-'Not Set (will default to local)'}"

env-setup: ## ⚙️ 환경 파일 초기 설정
	@echo "⚙️ Setting up environment files..."
	@cd $(SRC_DIR) && \
	if [ ! -f .env.development ]; then cp .env.example .env.development && echo "✅ Created .env.development"; fi && \
	if [ ! -f .env.local ]; then cp .env.example .env.local && echo "✅ Created .env.local"; fi && \
	if [ ! -f .env.staging ]; then cp .env.example .env.staging && echo "✅ Created .env.staging"; fi && \
	if [ ! -f .env.production ]; then cp .env.example .env.production && echo "✅ Created .env.production"; fi
	@echo "💡 Please edit the environment files with your specific settings"

env-validate: ## ✅ 환경 설정 검증
	@echo "✅ Validating environment configuration..."
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=local $(PYTHON) -c "from configuration import get_loca_config; config = get_loca_config(); print('✅ Local config validation passed')"
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=development $(PYTHON) -c "from configuration import get_loca_config; config = get_loca_config(); print('✅ Development config validation passed')"

# 🧪 테스트
test: ## 🧪 테스트 실행
	@echo "🧪 Running tests..."
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=local $(PYTHON) -m pytest tests/ -v

test-cov: ## 📊 테스트 커버리지 실행
	@echo "📊 Running tests with coverage..."
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=local $(PYTHON) -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# 🔧 코드 품질
lint: ## 🔍 코드 품질 검사
	@echo "🔍 Running code quality checks..."
	cd $(SRC_DIR) && $(PYTHON) -m flake8 . || echo "⚠️ Flake8 issues found"
	cd $(SRC_DIR) && $(PYTHON) -m pylint **/*.py || echo "⚠️ Pylint issues found"

format: ## ✨ 코드 포맷팅
	@echo "✨ Formatting code..."
	cd $(SRC_DIR) && $(PYTHON) -m black .
	cd $(SRC_DIR) && $(PYTHON) -m isort .

# 🧹 정리
clean: ## 🧹 임시 파일 정리
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# 🐳 Docker (환경별)
docker-build: ## 🐳 Docker 이미지 빌드
	@echo "🐳 Building Docker image..."
	docker build -t $(PROJECT_NAME):latest .

docker-dev: ## 🐳 Docker 개발 환경 실행
	@echo "🐳 Running Docker in development mode..."
	docker run -p 8000:8000 \
		-v $(PWD)/$(SRC_DIR):/app/$(SRC_DIR) \
		-e LOCA_DEPLOYMENT_ENV=development \
		--env-file $(SRC_DIR)/.env.development \
		$(PROJECT_NAME):latest

docker-prod: ## 🐳 Docker 운영 환경 실행
	@echo "🐳 Running Docker in production mode..."
	docker run -p 8000:8000 \
		-e LOCA_DEPLOYMENT_ENV=production \
		--env-file $(SRC_DIR)/.env.production \
		$(PROJECT_NAME):latest

# 🔍 모니터링
health: ## 💚 서버 헬스체크
	@echo "💚 Checking server health..."
	curl -f http://localhost:8000/health || echo "❌ Server is not running"

logs: ## 📄 애플리케이션 로그 확인
	@echo "📄 Showing application logs..."
	@if [ -f logs/application.log ]; then tail -f logs/application.log; else echo "📄 Log file not found"; fi

# 🛠️ 개발 도구
shell: ## 🐍 Python 대화형 셸 (앱 컨텍스트)
	@echo "🐍 Starting Python shell with app context..."
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=local $(PYTHON) -i -c "from main import get_app; app = get_app(); print('🤖 LOCA App loaded as: app')"

jupyter: ## 📓 Jupyter 노트북 시작
	@echo "📓 Starting Jupyter notebook..."
	cd $(SRC_DIR) && LOCA_DEPLOYMENT_ENV=local jupyter notebook

# 📦 배포 관련
deps-check: ## 📦 의존성 상태 확인
	@echo "📦 Checking dependencies..."
	$(PIP) list --outdated

deps-freeze: ## 🔒 현재 의존성 고정
	@echo "🔒 Freezing current dependencies..."
	$(PIP) freeze > requirements-current.txt

# 🚀 배포용 명령어들
deploy-staging: ## 🎭 스테이징 환경 배포
	@echo "🎭 Deploying to staging environment..."
	@echo "⚠️ Implement your staging deployment logic here"

deploy-prod: ## 🚀 운영 환경 배포
	@echo "🚀 Deploying to production environment..."
	@echo "⚠️ Implement your production deployment logic here"

# 📋 환경별 빠른 명령어
dev-quick: ## ⚡ 개발 환경 빠른 시작 (의존성 설치 + 서버 시작)
	@make install
	@make dev

reset-env: ## 🔄 환경 설정 초기화
	@echo "🔄 Resetting environment configuration..."
	cd $(SRC_DIR) && rm -f .env.development .env.local .env.staging .env.production
	@make env-setup

# 💡 사용 예시 출력
examples: ## 💡 사용 예시 표시
	@echo "💡 LOCA Gen-AI Usage Examples (Spring Boot Profile Style)"
	@echo "========================================================"
	@echo ""
	@echo "🔧 Development (auto-reload):"
	@echo "   make dev"
	@echo "   # or: LOCA_DEPLOYMENT_ENV=development python src/main.py"
	@echo ""
	@echo "🏠 Local environment:"
	@echo "   make local"
	@echo "   # or: LOCA_DEPLOYMENT_ENV=local python src/main.py"
	@echo ""
	@echo "🚀 Production:"
	@echo "   make prod"
	@echo "   # or: LOCA_DEPLOYMENT_ENV=production python src/main.py"
	@echo ""
	@echo "🐳 Docker:"
	@echo "   make docker-build && make docker-dev"
	@echo ""
	@echo "🔍 Environment info:"
	@echo "   make env-info"
	@echo ""
	@echo "⚙️ Setup new environment:"
	@echo "   make env-setup"