
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from typing import Optional

def setup_gemini_api() -> bool:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Gemini API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"❌ Gemini 설정 중 오류 발생: {e}")
        return False

CHAT_MODEL = 'gemini-1.5-flash'
VISION_MODEL = 'gemini-1.5-flash'

def _get_image_description_with_gemini(image_path: str) -> Optional[str]:
    print(f"DEBUG: Gemini Vision으로 이미지 '{image_path}' 내용 분석 시작...")

    if not setup_gemini_api():
        print("오류: Gemini API 키가 설정되지 않아 이미지 설명을 건너뜁니다.")
        return None

    try:
        model = genai.GenerativeModel(VISION_MODEL)
        img = Image.open(image_path)
        response = model.generate_content([img])
        if response.text:
            print(f"Gemini가 설명한 이미지 내용: {response.text.strip()}")
            return response.text.strip()
        else:
            print("Gemini 응답에서 텍스트 설명을 찾을 수 없습니다.")
            return None
    except Exception as e:
        print(f"오류: 이미지 설명 분석 실패: {e}")
        return None

def draw(image_path: str, style_prompt: str,user_description: str, output_path: str = "styled_image.png") -> Optional[str]:
    description = _get_image_description_with_gemini(image_path)
    if not description:
        print("오류: 이미지 설명을 가져오는 데 실패했습니다. 이미지 생성을 건너뜁니다.")
        return None

    try:
        prompt = f"{description}, rendered in {style_prompt} style."
        print(f"DEBUG: 생성 프롬프트 → {prompt}")

        import openai
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",  # 또는 "512x512"
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        import requests
        img_data = requests.get(image_url).content
        with open(output_path, 'wb') as f:
            f.write(img_data)
        return output_path
    except Exception as e:
        print(f"오류: 이미지 생성 실패: {e}")
        return None
