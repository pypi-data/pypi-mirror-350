# main.py

import os
import subprocess
from dotenv import load_dotenv
import ai_tools.drawing as drawing_ai
from ai_tools import chatbot

def check_api_keys():
    """
    .env 파일을 확인하고 없을 경우 setup_api_keys.py를 실행하여 키를 설정.
    설정된 API 키를 반환함.
    """
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not openai_key or not gemini_key:
        print("❌ .env에 API 키가 설정되지 않았습니다. setup_api_keys.py를 다시 실행합니다.\n")
        subprocess.run(["python", "ai_tools/setup_api_keys.py"])

        # 다시 불러오기
        load_dotenv()
        openai_key = os.getenv("OPENAI_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        if not openai_key or not gemini_key:
            print("❌ API 키가 여전히 설정되지 않았습니다. 프로그램을 종료합니다.")
            return None, None

    return openai_key, gemini_key


def main():
    openai_key, gemini_key = check_api_keys()
    if not openai_key or not gemini_key:
        exit()

    print("✅ API 키가 정상적으로 설정되었습니다.\n")

    while True:
        print("\n--- AI 기반 도구 선택 ---")
        print("1. AI 이미지 스타일 변환 도구")
        print("2. AI 챗봇")
        print("3. 종료")

        choice = input("원하는 도구를 선택하세요 (1, 2, 3): ")

        if choice == '1':
            # --- AI 이미지 스타일 변환 도구 ---
            print("\n--- AI 이미지 스타일 변환 도구 ---")
            input_image_path = input("🖼️ 변환할 이미지 파일 경로를 입력하세요: ").replace('\\', '/')
            if not os.path.exists(input_image_path):
                print(f"❌ 오류: '{input_image_path}' 파일이 존재하지 않습니다.")
                continue

            user_description = input("📝 이 그림에서 무엇을 그리고 싶으신가요? (예: cute cat flying in space): ")
            style_prompt = input("🎨 적용할 스타일을 입력하세요 (예: watercolor, oil painting): ")
            
            base_name = os.path.splitext(os.path.basename(input_image_path))[0]
            output_filename = f"output_{base_name}_{style_prompt.replace(' ', '_')}.jpg"

            print("🧠 프롬프트 구성 중...")
            print("🖌️ 이미지 생성 중...")

            result_path = drawing_ai.draw(input_image_path, user_description, style_prompt, output_filename)
            if result_path:
                print(f"\n✅ 이미지 생성 완료: {result_path}")
            else:
                print("❌ 이미지 생성 실패. 오류 메시지를 확인해주세요.")

        elif choice == '2':
            # --- 챗봇 ---
            print("\n--- AI 챗봇 ---")
            while True:
                sub = input("1: 텍스트, 2: 이미지+텍스트, 3: 돌아가기 > ")
                if sub == '1':
                    prompt = input("💬 질문: ")
                    if prompt.lower() in ['exit', '종료']:
                        break
                    response = chatbot.chat_text_only(prompt)
                    print("🤖", response or "응답 없음")
                elif sub == '2':
                    img_path = input("🖼️ 이미지 경로: ").replace('\\', '/')
                    if not os.path.exists(img_path):
                        print("❌ 이미지가 존재하지 않습니다.")
                        continue
                    prompt = input("💬 질문: ")
                    response = chatbot.chat_with_image(img_path, prompt)
                    print("🤖", response or "응답 없음")
                elif sub == '3':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '3':
            print("👋 AI-Tools를 종료합니다.")
            break
        else:
            print("❗ 1, 2, 3 중 하나를 선택하세요.")


if __name__ == "__main__":
    main()
