# ai_tools/chatbot.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# .env 파일에서 환경 변수 로드
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Gemini API 키 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini 챗봇 모델 초기화
CHAT_MODEL = 'gemini-1.5-flash'
VISION_MODEL = 'gemini-1.5-flash' # 이미지 처리를 위해 flash 모델 사용

def chat_text_only(prompt: str) -> str | None:
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

def chat_with_image(image_path: str, text_prompt: str) -> str | None:
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
        print(f"오류: 이미지 포함 챗봇 응답 생성 중 오류 발생: {e}: {e}")
        return None

#if __name__ == '__main__':
    # 이 부분은 chatbot.py를 직접 실행했을 때 테스트하는 코드입니다.
    # 실제 main.py에서는 이 함수들을 호출합니다.

    print("--- 텍스트 전용 챗봇 테스트 ---")
    text_response = chat_text_only("안녕하세요? 당신은 누구인가요?")
    if text_response:
        print(f"챗봇 응답: {text_response}\n")

    print("--- 이미지 포함 챗봇 테스트 (예시) ---")
    # 실제 이미지 경로로 변경해야 합니다.
    example_image_path = "C:\\flower.jpg" # 실제 테스트할 이미지 경로로 변경하세요
    if os.path.exists(example_image_path):
        image_text_response = chat_with_image(example_image_path, "이 꽃은 어떤 종류인가요?")
        if image_text_response:
            print(f"챗봇 응답 (이미지 포함): {image_text_response}")
    else:
        print(f"오류: 이미지 포함 챗봇 테스트를 위해 '{example_image_path}' 파일을 찾을 수 없습니다.")