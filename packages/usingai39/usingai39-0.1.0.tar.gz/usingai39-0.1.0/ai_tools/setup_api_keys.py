import os
from dotenv import set_key, load_dotenv

ENV_PATH = ".env"

def setup_env_key(var_name, description):
    print(f"\n🔑 {description} ({var_name})")
    existing = os.getenv(var_name)
    if existing:
        print(f"현재 값: {existing}")
    new_value = input(f"새로운 값을 입력하거나 Enter로 유지하세요: ")
    if new_value:
        set_key(ENV_PATH, var_name, new_value)

def main():
    print("✨ AI Tools 환경설정 시작 (.env 생성 또는 업데이트)")

    # 🔧 인코딩을 명시해서 UTF-8로 저장되도록 변경
    if not os.path.exists(ENV_PATH):
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write("# 사용자 API 키 설정\n")

    load_dotenv(ENV_PATH)

    setup_env_key("OPENAI_API_KEY", "OpenAI API 키")
    setup_env_key("GEMINI_API_KEY", "Gemini API 키")

    print("\n✅ 설정 완료! .env 파일이 업데이트되었습니다.")

if __name__ == "__main__":
    main()
