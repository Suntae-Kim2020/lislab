# LIS Lab 배포 가이드

## 📧 이메일 설정 (Gmail SMTP)

### 로컬 개발
`.env` 파일에 설정 (Git에 커밋 안 됨):
```
EMAIL_HOST_USER=kistiman@gmail.com
EMAIL_HOST_PASSWORD=wbce rxkb vexd yhuf
```

### Google Cloud 배포 시

#### 1. Secret Manager에 저장 (권장)
```bash
# 비밀 생성
gcloud secrets create email-password --data-file=- <<< "wbce rxkb vexd yhuf"

# Cloud Run에서 사용
gcloud run deploy lislab \
  --set-secrets="EMAIL_HOST_PASSWORD=email-password:latest"
```

#### 2. 환경 변수로 설정
```bash
gcloud run deploy lislab \
  --set-env-vars="EMAIL_HOST_USER=kistiman@gmail.com"
```

## ⚠️ 중요 사항

1. **절대 GitHub에 올리면 안 되는 것:**
   - `.env` 파일
   - 데이터베이스 비밀번호
   - Gmail 앱 비밀번호
   - Django SECRET_KEY

2. **GitHub에 올려도 되는 것:**
   - `.env.example` (템플릿)
   - `deploy-env-vars.sh` (템플릿)
   - 소스 코드

3. **새 환경에서 설정 방법:**
   ```bash
   # .env.example 복사
   cp .env.example .env
   
   # 실제 값으로 수정
   nano .env
   ```

## 🔐 Gmail 앱 비밀번호 재생성

현재 사용 중: `wbce rxkb vexd yhuf`

만약 비밀번호를 변경해야 한다면:
1. Google 계정 → 보안 → 2단계 인증
2. 앱 비밀번호 → 새 앱 비밀번호 생성
3. `.env` 파일 및 Google Secret Manager 업데이트

