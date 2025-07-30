from setuptools import setup, find_packages

setup(
    name='usingai311', # 패키지 이름 (pip install usingai 로 설치될 이름)
    version='0.2.0', # 패키지 버전
    author='Sang hyuck Won', # 당신의 이름 또는 닉네임
    author_email='yhnujk@naver.com', # 당신의 이메일 주소
    description='A collection of AI-powered tools for games and apps.', # 패키지 설명
    long_description=open('readme.md', encoding='utf-8').read(), # README.md 내용을 긴 설명으로 사용
    long_description_content_type='text/markdown', # long_description의 컨텐츠 타입
    url='https://github.com/yhnujk/ai_tools_project.git', # 당신의 GitHub 저장소 URL
    packages=find_packages(), # 'ai_tools'와 같은 모든 패키지 폴더를 자동으로 찾음
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # 라이선스 (MIT License 선택 시)
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', # 이 패키지가 요구하는 최소 파이썬 버전
    install_requires=[ # 이 패키지가 의존하는 외부 라이브러리 목록
        'Pillow>=9.0.0',
        'requests>=2.20.0',
        'openai>=1.0.0',
        'google-generativeai>=0.3.0',
        'python-dotenv>=1.0.0',
    ],
    entry_points={
    'console_scripts': [
        'usingai = ai_tools.main:main'  # main.py 안의 main() 함수 실행
    ],
},

    # 'setuptools'는 일반적으로 install_requires에 포함하지 않습니다.
    # setuptools는 패키지를 설치하기 위한 도구이지, 패키지 실행에 필요한 의존성이 아니기 때문입니다.
)