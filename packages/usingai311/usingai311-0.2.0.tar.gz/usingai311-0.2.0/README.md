# usingai: AI 기반 게임/앱 모듈 컬렉션

이 패키지는 **Google Gemini API**와 **OpenAI DALL·E 3 API**를 활용하여,  
게임 및 애플리케이션 개발에 사용할 수 있는 다양한 AI 기능들을 제공합니다.  
현재 **이미지 스타일 변환** 및 **AI 챗봇** 기능을 포함하고 있습니다.

---

## 🚀 주요 기능

- **🖼️ 이미지 스타일 변환**  
  텍스트 프롬프트 기반으로 예술 스타일(유화, 픽셀아트, 수묵화 등)을 적용하여 이미지를 생성합니다.

- **🤖 AI 챗봇**  
  텍스트 또는 이미지 기반 질문에 답하는 멀티모달 챗봇 기능 (Gemini API 사용)

---

## 📦 설치 방법

```bash
pip install usingai
```

---

## ⚙️ 사용법

### 1. API 키 자동 설정

최초 실행 시 `.env` 파일이 없으면 자동으로 생성됩니다.  
명령어 실행 후 안내에 따라 **OpenAI** 및 **Google Gemini** API 키를 입력하세요.


🔑 아래 링크에서 각 API 키를 발급받을 수 있습니다:

- [OpenAI API 키 발급하기](https://platform.openai.com/account/api-keys)
- [Google Gemini API 키 발급하기](https://ai.google.dev/gemini-api/docs/get-started)

```bash
python -m ai_tools.main
```

또는 `main.py`를 바로 실행해도 자동으로 설정 스크립트가 호출됩니다.

---

### 2. 실행 예시

실행 후 아래와 같은 메뉴가 제공됩니다:

```
💾 출력 이미지를 저장할 폴더를 입력하세요 (Enter 시 입력 이미지와 같은 위치):

```

이후 경로는 수정할 수 없으니 주의하세요!

```
1. 이미지 스타일 변환
2. AI 챗봇
3. 종료
```

---

## 🧪 테스트

테스트용 이미지 생성 및 모듈 테스트를 진행할 수 있습니다.

```bash
python tests/test_ai_tools.py
```

---

## 🛠️ 개발 체크리스트 보기

👉 [✅ checklist.md 보기](docs/checklist.md)

---

## 🤝 기여 (Contributing)

이 프로젝트는 오픈 소스로 개발되고 있으며 누구나 환영합니다.  
자세한 기여 방법은 [`CONTRIBUTING.md`](CONTRIBUTING.md)를 확인하세요.

---

## 📄 라이선스

이 프로젝트는 [MIT License](LICENSE)에 따라 배포됩니다.

---

## ⚠️ 사용 시 주의사항

- 본 프로젝트는 OpenAI 및 Google Gemini API를 사용하며, 각 API 제공자의 **사용 정책을 반드시 준수**해야 합니다.
- 생성된 콘텐츠에 대해 개발자는 책임지지 않으며, 사용자의 책임 하에 사용해야 합니다.

📄 자세한 정책은 [OpenAI 정책](https://openai.com/policies/usage-policies), [Gemini 정책](https://ai.google.dev/terms)을 참고하세요.
