# LIS - Learning Information System

교육 콘텐츠 관리 및 공유 플랫폼

## 기술 스택

- **Backend**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL
- **Python**: 3.11+

## 주요 기능

### 사용자 역할
- 비회원(Guest): 콘텐츠 열람
- 회원(User): 댓글, 즐겨찾기, 게시판 작성
- 관리자(Admin): 콘텐츠 관리, 통계, 운영

### 핵심 모듈
1. **콘텐츠 관리**: 교육 웹페이지 생성/수정/버전관리
2. **댓글 시스템**: 콘텐츠별 댓글/답글
3. **게시판**: 공지사항, 콘텐츠 개발 요청
4. **메일링 리스트**: 구독/발송 관리
5. **즐겨찾기**: 사용자별 콘텐츠 북마크

## 프로젝트 구조

```
LIS/
├── manage.py
├── requirements.txt
├── config/              # Django 설정
├── apps/
│   ├── accounts/        # 사용자/인증
│   ├── contents/        # 교육 콘텐츠
│   ├── comments/        # 댓글
│   ├── boards/          # 게시판
│   └── mailing/         # 메일링
├── static/
└── media/
```

## 설치 및 실행

### 1. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
```bash
cp .env.example .env
# .env 파일을 열어 설정값 수정
```

### 4. 데이터베이스 설정
```bash
# PostgreSQL 데이터베이스 생성
createdb lis_db

# 마이그레이션
python manage.py makemigrations
python manage.py migrate
```

### 5. 관리자 계정 생성
```bash
python manage.py createsuperuser
```

### 6. 개발 서버 실행
```bash
python manage.py runserver
```

## 개발 가이드

### 코드 스타일
```bash
# 포맷팅
black .
isort .

# 린팅
flake8
```

### 테스트
```bash
pytest
```

## API 문서

서버 실행 후 다음 주소에서 API 문서 확인:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## 라이선스

MIT License
