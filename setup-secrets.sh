#!/bin/bash
# Google Cloud Secret Manager 설정 스크립트
# 프로젝트: hybrid-flame-323510

PROJECT_ID="hybrid-flame-323510"

echo "🔐 Google Cloud Secret Manager 설정을 시작합니다..."
echo "프로젝트: $PROJECT_ID"
echo ""

# Secret Manager API 활성화 확인
echo "1️⃣  Secret Manager API 활성화 중..."
gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID

echo ""
echo "2️⃣  비밀 정보 생성 중..."

# Django SECRET_KEY 생성
echo "   - Django SECRET_KEY 생성..."
echo -n "-qhl_7-9&o=q3#9^v4ig3yktp&x3w5oa02pu0#tild5c2(zc&@" | \
  gcloud secrets create django-secret-key \
  --project=$PROJECT_ID \
  --data-file=- \
  --replication-policy="automatic" 2>/dev/null || \
  echo "     ⚠️  django-secret-key 이미 존재 (건너뜀)"

# Gmail 앱 비밀번호 생성
echo "   - Email 비밀번호 생성..."
echo -n "wbce rxkb vexd yhuf" | \
  gcloud secrets create email-password \
  --project=$PROJECT_ID \
  --data-file=- \
  --replication-policy="automatic" 2>/dev/null || \
  echo "     ⚠️  email-password 이미 존재 (건너뜀)"

# 데이터베이스 비밀번호 생성 (Cloud SQL에서 설정할 비밀번호를 여기에 입력)
echo ""
echo "📝 Cloud SQL 데이터베이스 비밀번호를 입력해주세요:"
echo "   (아직 Cloud SQL을 생성하지 않았다면, 나중에 다시 실행하세요)"
read -s -p "   DB 비밀번호: " DB_PASSWORD
echo ""

if [ ! -z "$DB_PASSWORD" ]; then
  echo "   - 데이터베이스 비밀번호 생성..."
  echo -n "$DB_PASSWORD" | \
    gcloud secrets create db-password \
    --project=$PROJECT_ID \
    --data-file=- \
    --replication-policy="automatic" 2>/dev/null || \
    echo "     ⚠️  db-password 이미 존재 (건너뜀)"
else
  echo "   ⏭️  데이터베이스 비밀번호 건너뜀"
fi

echo ""
echo "3️⃣  생성된 비밀 정보 확인..."
gcloud secrets list --project=$PROJECT_ID

echo ""
echo "✅ Secret Manager 설정 완료!"
echo ""
echo "다음 명령어로 Cloud Run에서 사용할 수 있습니다:"
echo "gcloud run deploy lislab \\"
echo "  --project=$PROJECT_ID \\"
echo "  --set-secrets=\"DJANGO_SECRET_KEY=django-secret-key:latest,EMAIL_HOST_PASSWORD=email-password:latest,DB_PASSWORD=db-password:latest\""
