#!/usr/bin/env python3
"""
🔧 환경변수 관리 스크립트

환경별 .env 파일을 관리하고 검증하는 유틸리티
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Set
import argparse


def get_env_files() -> Dict[str, Path]:
    """환경별 .env 파일 경로 반환"""
    project_root = Path(__file__).parent.parent

    return {
        "example": project_root / ".env.example",
        "local": project_root / ".env",
        "development": project_root / ".env.development",
        "staging": project_root / ".env.staging",
        "production": project_root / ".env.production"
    }


def parse_env_file(env_path: Path) -> Set[str]:
    """env 파일에서 환경변수 키 추출"""
    if not env_path.exists():
        return set()

    variables = set()
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key = line.split('=')[0].strip()
                variables.add(key)

    return variables


def validate_env_consistency():
    """모든 환경 파일의 일관성 검사"""
    print("🔍 Validating environment files consistency...")

    env_files = get_env_files()

    # 예시 파일의 모든 변수를 기준으로 함
    if not env_files["example"].exists():
        print("❌ .env.example file not found!")
        return False

    example_vars = parse_env_file(env_files["example"])
    print(f"📋 Example file contains {len(example_vars)} variables")

    issues_found = False

    for env_name, env_path in env_files.items():
        if env_name == "example" or not env_path.exists():
            continue

        print(f"\n🔍 Checking {env_name} environment...")
        env_vars = parse_env_file(env_path)

        # 누락된 변수 확인
        missing_vars = example_vars - env_vars
        if missing_vars:
            print(f"⚠️  Missing variables in {env_name}:")
            for var in sorted(missing_vars):
                print(f"   - {var}")
            issues_found = True

        # 추가된 변수 확인
        extra_vars = env_vars - example_vars
        if extra_vars:
            print(f"ℹ️  Extra variables in {env_name}:")
            for var in sorted(extra_vars):
                print(f"   + {var}")

        if not missing_vars and not extra_vars:
            print(f"✅ {env_name} environment is consistent")

    if issues_found:
        print("\n❌ Environment consistency issues found!")
        return False
    else:
        print("\n✅ All environment files are consistent!")
        return True


def list_environment_variables():
    """모든 환경변수 목록 출력"""
    print("📋 All environment variables defined in .env.example:")
    print("=" * 80)

    env_files = get_env_files()
    if not env_files["example"].exists():
        print("❌ .env.example file not found!")
        return

    example_vars = parse_env_file(env_files["example"])

    # 카테고리별로 그룹화 (접두사 기준)
    categories = {}
    for var in example_vars:
        if var.startswith('LOCA_'):
            category = var.split('_')[1] if len(var.split('_')) > 1 else 'SYSTEM'
        elif var.startswith('LANGCHAIN_') or var.startswith('LANGSMITH_'):
            category = 'LANGCHAIN'
        elif var.startswith('OPENAI_') or var.startswith('AZURE_'):
            category = 'LLM'
        else:
            category = 'OTHER'

        if category not in categories:
            categories[category] = []
        categories[category].append(var)

    for category, vars_list in sorted(categories.items()):
        print(f"\n🏷️  {category} ({len(vars_list)} variables):")
        for var in sorted(vars_list):
            print(f"   {var}")

    print(f"\n📊 Total: {len(example_vars)} environment variables")


def create_env_from_template(target_env: str):
    """템플릿에서 특정 환경 파일 생성"""
    env_files = get_env_files()

    if target_env not in env_files:
        print(f"❌ Unknown environment: {target_env}")
        return False

    example_path = env_files["example"]
    target_path = env_files[target_env]

    if not example_path.exists():
        print("❌ .env.example file not found!")
        return False

    if target_path.exists():
        response = input(f"⚠️  {target_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False

    # 템플릿 복사
    import shutil
    shutil.copy2(example_path, target_path)
    print(f"✅ Created {target_path} from template")

    # 환경별 기본값 조정
    if target_env == "local":
        print("🔧 Adjusting for local development...")
        # 로컬 개발용 기본값으로 조정하는 로직 추가 가능

    return True


def main():
    parser = argparse.ArgumentParser(description="LOCA Environment Variables Manager")
    parser.add_argument("command", choices=["validate", "list", "create"],
                        help="Command to execute")
    parser.add_argument("--env", choices=["local", "development", "staging", "production"],
                        help="Target environment for create command")

    args = parser.parse_args()

    if args.command == "validate":
        success = validate_env_consistency()
        sys.exit(0 if success else 1)

    elif args.command == "list":
        list_environment_variables()

    elif args.command == "create":
        if not args.env:
            print("❌ --env argument required for create command")
            sys.exit(1)
        success = create_env_from_template(args.env)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()