# ai_tools/drawing.py

import os
import requests
from PIL import Image
from io import BytesIO
import base64

# Google Gemini API 라이브러리 임포트
import google.generativeai as genai

# .env 파일에서 환경 변수를 로드합니다.
# 이 파일에서 직접 load_dotenv()를 호출하는 것보다,
# test_ai_tools.py나 main 스크립트에서 한 번만 호출하는 것이 좋습니다.
# from dotenv import load_dotenv
# load_dotenv() # test_ai_tools.py에서 이미 호출하고 있다면 여기서는 주석 처리하거나 제거

# --- 설정 (환경 변수에서 API 키 로드) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- OpenAI DALL-E 설정 ---
DALL_E_MODEL = "dall-e-3"
DALL_E_SIZE = "1024x1024"
DALL_E_QUALITY = "standard"
DALL_E_N = 1 # DALL-E 3는 1개만 지원

# --- Gemini API 설정 ---
# Gemini API 키 설정
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("경고: Gemini API 키가 설정되지 않았습니다. .env 파일에 GEMINI_API_KEY를 설정하세요.")

def _get_openai_headers():
    """OpenAI API 호출에 필요한 HTTP 헤더를 반환합니다."""
    if not OPENAI_API_KEY:
        print("경고: OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 설정하세요.")
        return None
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

def _get_image_description_with_gemini(image_path: str) -> str | None:
    """
    Gemini 1.5 Flash를 사용하여 이미지의 내용을 설명하는 텍스트를 생성합니다.
    """
    if not GEMINI_API_KEY:
        print("오류: Gemini API 키가 설정되지 않아 이미지 설명을 건너뜁니다.")
        return None

    # response 변수를 미리 None으로 초기화 (UnboundLocalError 해결)
    response = None 
    try:
        # 이미지 파일을 바이트로 읽기
        img_bytes = Image.open(image_path)

        # Gemini 1.5 Flash 모델 초기화 (최신 버전 사용)
        model = genai.GenerativeModel('gemini-1.5-flash') 

        # 이미지와 질문을 함께 모델에 전달하여 이미지 설명 요청
        response = model.generate_content([ 
            "Describe this image in detail, focusing on its main subjects, background, and overall composition. Provide enough detail for an artist to redraw it.",
            img_bytes
        ])

        # 응답 텍스트 반환
        return response.text

    except FileNotFoundError:
        print(f"오류: 이미지를 찾을 수 없습니다: {image_path}")
        return None
    except Exception as e:
        print(f"오류: Gemini API로 이미지 설명을 생성하는 중 오류 발생: {e}")
        # response가 None이 아닐 때만 접근하도록 수정
        if response and hasattr(response, 'candidates') and response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
            print(f"Gemini Safety Ratings: {response.candidates[0].safety_ratings}")
        return None

def draw(image_path: str, style_prompt: str, output_path: str = "my_styled_artwork.png") -> str | None:
    """
    주어진 이미지를 Gemini Vision으로 분석하고, DALL-E 3로 스타일 변환하여 이미지를 생성합니다.
    """
    if not os.path.exists(image_path):
        print(f"오류: 입력 이미지 파일이 존재하지 않습니다: {image_path}")
        return None

    print(f"DEBUG: Gemini Vision으로 이미지 '{image_path}' 내용 분석 시작...")
    image_description = _get_image_description_with_gemini(image_path)

    if not image_description:
        print("오류: 이미지 설명을 가져오는 데 실패했습니다. 이미지 생성을 건너뜁니다.")
        return None

    print(f"DEBUG: Gemini가 설명한 이미지 내용: {image_description[:100]}...")
    
    # Gemini 설명을 DALL-E에 더 적합하게 정제
    cleaned_description = image_description.strip()
    
    # 흔히 붙는 Gemini의 서두 문구 제거 (새로운 방식으로 유연하게 제거)
    prefixes_to_remove = [
        "Here's a description of the image suitable for an artist to recreate:",
        "Here's a description of the image suitable for an artist to redraw:",
        "The image depicts:",
        "Description:",
        "The image is" # 추가된 부분, 이전에 제거되지 않은 서두일 가능성
    ]
    
    for prefix in prefixes_to_remove:
        if cleaned_description.lower().startswith(prefix.lower()): # 소문자로 비교하여 유연하게 제거
            cleaned_description = cleaned_description[len(prefix):].strip()
            break 

    cleaned_description = cleaned_description.strip() # 추가적인 공백이나 줄바꿈 정리
    
    # DALL-E 프롬프트 길이 제한 (200자로 유지, 단어 단위로 자름)
    max_dalle_content_length = 200 
    if len(cleaned_description) > max_dalle_content_length:
        words = cleaned_description.split()
        current_length = 0
        truncated_words = []
        for word in words:
            if current_length + len(word) + 1 > max_dalle_content_length: # +1은 공백
                break
            truncated_words.append(word)
            current_length += len(word) + 1
        cleaned_description = " ".join(truncated_words) + "..." if truncated_words else "An image."
        
    # 최종 DALL-E 프롬프트 생성 (핵심 내용만)
    dall_e_prompt = (
        f"An artwork depicting: {cleaned_description}. "
        f"Render this scene in a {style_prompt} style. "
        "Focus on the artistic medium and overall aesthetic, ensuring the main subjects are clearly recognizable. "
        "The image should be visually appealing and harmonious. Realistic photo quality, high detail." # DALL-E 선호 문구 유지
    )
    
    print(f"DEBUG: DALL-E 3 프롬프트 생성: {dall_e_prompt[:150]}...")

    headers = _get_openai_headers()
    if not headers:
        return None

    payload = {
        "model": DALL_E_MODEL,
        "prompt": dall_e_prompt,
        "n": DALL_E_N,
        "size": DALL_E_SIZE,
        "quality": DALL_E_QUALITY
    }

    print(f"DEBUG: OpenAI DALL-E 3 API 호출 시도...")
    try:
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload)
        response.raise_for_status() # HTTP 오류가 발생하면 예외 발생

        data = response.json()
        if data and data['data']:
            image_url = data['data'][0]['url']
            print(f"DEBUG: 생성된 이미지 URL: {image_url}")

            # 생성된 이미지를 다운로드하여 저장
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # 저장 경로 생성
            with open(output_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"성공: 변환된 이미지를 '{output_path}'에 저장했습니다.")
            return output_path
        else:
            print(f"오류: DALL-E API 응답에 'data' 필드가 없거나 비어 있습니다. 응답: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"오류: DALL-E API 호출 중 네트워크 또는 API 오류 발생: {e}")
        if response and response.status_code == 401:
            print("API 키가 유효하지 않거나 만료되었습니다. OpenAI API 키를 확인하세요.")
        elif response and response.status_code == 429:
            print("API 호출 제한에 도달했습니다. 잠시 후 다시 시도하세요.")
        elif response and response.json():
            print(f"API 오류 상세: {response.json().get('error', {})}")
        return None
    except Exception as e:
        print(f"오류: 이미지 저장 중 알 수 없는 오류 발생: {e}")
        return None

# --- 예시 (직접 실행 시) ---
if __name__ == "__main__":
    print("drawing.py 모듈이 직접 실행되었습니다. test_ai_tools.py를 통해 테스트하는 것이 좋습니다.")