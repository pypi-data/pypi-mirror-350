# main.py

import os
import subprocess
from dotenv import load_dotenv
import ai_tools.drawing as drawing_ai
import ai_tools.chatbot as chatbot # 챗봇 모듈 임포트

# .env 파일 존재 확인 & 없으면 자동 실행

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

def check_api_keys():
    if not os.path.exists(".env"):
        print("⚠️ .env 파일이 없습니다. API 키를 설정합니다...\n")
        subprocess.run(["python", "setup_api_keys.py"])

    if not openai_key or not gemini_key:
        print("❌ 필수 API 키가 누락되었습니다. 종료합니다.")
        return False
    return True


if not openai_key or not gemini_key:
    print("❌ .env에 API 키가 설정되지 않았습니다. setup_api_keys.py를 다시 실행해주세요.")
    exit()

# ✅ 사용자 프롬프트 직접 입력 받기
print("✅ API 키가 정상적으로 설정되었습니다.")

# Gemeni 챗봇 테스트
print("💬 Gemini 챗봇 테스트를 시작합니다.")

user_input = input("질문을 입력하세요: ")
chat_response = chatbot(user_input)

if chat_response and isinstance(chat_response, str):
    print(f"\n🤖 Gemini 응답: {chat_response}")
else:
    print("❌ 챗봇 응답을 받지 못했습니다. API 키가 올바른지 확인해주세요.")
    exit()

print("\n🎨 [DALL·E 스타일 이미지 생성 테스트]")
image_prompt = input("🖼️ 어떤 이미지를 생성할까요?: ")
image_url = drawing_ai(image_prompt)

if image_url and image_url.startswith("http"):
    print(f"\n🖼️ 생성된 이미지 URL:\n{image_url}")
else:
    print("❌ 이미지 생성에 실패했습니다. OpenAI API 키가 유효한지 확인해주세요.")

print("AI-Tools v0.1.0 package initialized. Welcome to the future of AI-powered content creation!")

def main():
    while True:
        print("\n--- AI 기반 도구 선택 ---")
        print("1. AI 이미지 스타일 변환 도구")
        print("2. AI 챗봇")
        print("3. 종료")
        
        choice = input("원하는 도구를 선택하세요 (1, 2, 3): ")

        if choice == '1':
            # --- AI 이미지 스타일 변환 도구 ---
            print("\n--- AI 이미지 스타일 변환 도구 ---")
            print("기존 이미지를 AI가 원하는 스타일로 변환해 드립니다.")
            
            input_image_path_raw = input("변환할 이미지 파일의 전체 경로를 입력하세요 (예: C:\\Users\\YourName\\Pictures\\my_photo.jpg 또는 C:/Users/YourName/Pictures/my_photo.jpg): ")
            # 경로 슬래시 정규화 (Windows 사용자를 위해)
            input_image_path = input_image_path_raw.replace('\\', '/')

            if not os.path.exists(input_image_path):
                print(f"❌ 오류: '{input_image_path}' 파일을 찾을 수 없습니다. 경로를 다시 확인해주세요.")
                continue # 다시 메뉴로 돌아감
            
            style_prompt = input("원하는 이미지 스타일을 입력하세요 (예: oil painting, pixel art, watercolor): ")

            print(f"\n'{input_image_path}' 이미지를 '{style_prompt}' 스타일로 변환 중...")
            print("이 과정은 몇 초에서 몇 분이 소요될 수 있습니다. 잠시 기다려 주세요...")

            # 출력 파일명 생성
            base_name = os.path.splitext(os.path.basename(input_image_path))[0]
            output_filename = f"output_{base_name}_{style_prompt.replace(' ', '_')}.jpg"

            # 이미지 변환 함수 호출
            result_path = drawing_ai.draw(input_image_path, style_prompt, output_filename)

            if result_path:
                print(f"\n✅ 이미지 변환 성공! 결과는 '{result_path}'에 저장되었습니다.")
                print(f"이 경로로 이동하여 생성된 이미지를 확인해 보세요.")
            else:
                print("\n❌ 이미지 변환에 실패했습니다. 오류 메시지를 확인해주세요.")

        elif choice == '2':
            # --- AI 챗봇 기능 ---
            print("\n--- AI 챗봇 ---")
            print("텍스트 기반 질문 또는 이미지와 함께 질문할 수 있습니다.")
            print("챗봇을 종료하려면 '종료' 또는 'exit'를 입력하세요.")
            
            while True:
                chat_mode_choice = input("챗봇 모드를 선택하세요 (1: 텍스트 전용, 2: 이미지와 함께, 3: 메인 메뉴로 돌아가기): ")
                
                if chat_mode_choice == '1':
                    user_text_prompt = input("텍스트 질문을 입력하세요: ")
                    if user_text_prompt.lower() in ['종료', 'exit']:
                        break
                    response = chatbot.chat_text_only(user_text_prompt)
                    if response:
                        print(f"➡️ 챗봇: {response}")
                    else:
                        print("챗봇 응답을 가져오는 데 실패했습니다.")

                elif chat_mode_choice == '2':
                    image_path_raw = input("질문할 이미지 파일의 전체 경로를 입력하세요: ")
                    image_path = image_path_raw.replace('\\', '/')
                    if not os.path.exists(image_path):
                        print(f"❌ 오류: '{image_path}' 파일을 찾을 수 없습니다. 다시 시도해주세요.")
                        continue
                    
                    user_image_text_prompt = input("이미지와 함께 질문할 텍스트를 입력하세요: ")
                    if user_image_text_prompt.lower() in ['종료', 'exit']:
                        break
                    response = chatbot.chat_with_image(image_path, user_image_text_prompt)
                    if response:
                        print(f"➡️ 챗봇: {response}")
                    else:
                        print("챗봇 응답을 가져오는 데 실패했습니다.")

                elif chat_mode_choice == '3':
                    print("메인 메뉴로 돌아갑니다.")
                    break
                else:
                    print("유효하지 않은 선택입니다. 다시 입력해주세요.")

        elif choice == '3':
            print("AI-Tools를 종료합니다. 이용해주셔서 감사합니다!")
            break
        else:
            print("유효하지 않은 선택입니다. 1, 2, 3 중 하나를 입력하세요.")

if __name__ == "__main__":
    main()