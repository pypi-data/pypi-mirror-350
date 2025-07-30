import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from typing import Optional

# .env 파일에서 환경 변수 로드
def setup_gemini_api() -> bool:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Gemini API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"❌ Gemini 설정 중 오류 발생: {e}")
        return False

# Gemini 챗봇 모델 초기화
CHAT_MODEL = 'gemini-1.5-flash'
VISION_MODEL = 'gemini-1.5-flash'  # 이미지 처리를 위해 flash 모델 사용

def chat_text_only(prompt: str) -> Optional[str]:
    if not setup_gemini_api():
        return None
    """
    텍스트 기반 질문에 Gemini 챗봇으로 응답합니다.
    """
    try:
        model = genai.GenerativeModel(CHAT_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"오류: 텍스트 챗봇 응답 생성 중 오류 발생: {e}")
        return None

def chat_with_image(image_path: str, text_prompt: str) -> Optional[str]:
    if not setup_gemini_api():
        return None
    """
    이미지와 텍스트를 함께 사용하여 Gemini Vision 챗봇으로 응답합니다.
    """
    try:
        model = genai.GenerativeModel(VISION_MODEL)
        
        # 이미지 로드
        if not os.path.exists(image_path):
            print(f"오류: 이미지 파일이 존재하지 않습니다: {image_path}")
            return None
            
        img = Image.open(image_path)
        
        # 멀티모달 프롬프트 구성
        response = model.generate_content([text_prompt, img])
        return response.text
    except Exception as e:
        print(f"오류: 이미지 포함 챗봇 응답 생성 중 오류 발생: {e}")
        return None
