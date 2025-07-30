# ai_tools_project/test_ai_tools.py

import os
from dotenv import load_dotenv
from PIL import Image # Pillow 라이브러리 임포트

# .env 파일에서 환경 변수를 로드합니다.
# 이 줄은 파일의 가장 위에 한 번만 있어야 합니다.
load_dotenv()

# ai_tools 패키지 내 모듈 임포트
from ai_tools import drawing
from ai_tools import chatbot # (아직 구현되지 않은 챗봇 모듈)

def test_drawing_module():
    print("\n--- Drawing 모듈 테스트 시작 ---")

    # --- 테스트를 위한 입력 이미지 파일 생성 ---
    # 실제 이미지 파일이 없어도 테스트를 위해 임시 파일을 생성합니다.
    input_image_path = "test_drawing_input.png" # 파일명 변경
    try:
        # 간단한 더미 이미지 생성 (사각형 안에 원)
        img = Image.new('RGB', (400, 300), color = 'white')
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if (i - 200)**2 + (j - 150)**2 < 100**2: # 원 그리기
                    pixels[i,j] = (0, 0, 255) # 파란색
        img.save(input_image_path)
        print(f"테스트 입력 이미지 '{input_image_path}' 생성 완료.")
    except Exception as e:
        print(f"오류: 테스트 입력 이미지 생성 실패: {e}")
        return # 이미지 생성 실패 시 테스트 중단

    output_image_path = "test_drawing_output.png" # 출력 파일명 변경
    style = "cartoon style" # 테스트 스타일 변경 (예시)

    print(f"'{input_image_path}' 이미지를 '{style}' 스타일로 변환 시도...")
    generated_image_path = drawing.draw(input_image_path, style, output_image_path)

    if generated_image_path and os.path.exists(generated_image_path):
        print(f"성공: 테스트 이미지가 '{generated_image_path}'에 저장되었습니다.")
    else:
        print("실패: 테스트 이미지 생성 중 문제가 발생했습니다. 위 로그를 확인하세요.")

    # 테스트 후 생성된 임시 입력 파일 삭제 (선택 사항)
    try:
        if os.path.exists(input_image_path):
            os.remove(input_image_path)
            print(f"임시 입력 이미지 '{input_image_path}' 삭제 완료.")
    except Exception as e:
        print(f"오류: 임시 파일 삭제 실패: {e}")


def test_chatbot_module():
    print("\n--- Chatbot 모듈 테스트 시작 ---")
    # TODO: 챗봇 모듈이 구현되면 여기에 테스트 코드 추가
    print("챗봇 모듈은 아직 구현 중입니다.")

if __name__ == "__main__":
    # 각 모듈의 테스트 함수 호출
    test_drawing_module()
    test_chatbot_module()

    print("\n--- 모든 모듈 테스트 완료 ---")