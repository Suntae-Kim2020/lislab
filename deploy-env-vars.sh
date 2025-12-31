#!/bin/bash
# Google Cloud 배포용 환경 변수 설정 스크립트
# 사용법: source deploy-env-vars.sh

export PROJECT_ID="your-gcp-project-id"
export REGION="asia-northeast3"
export SERVICE_NAME="lislab"

# 데이터베이스
export DB_ENGINE="django.db.backends.postgresql"
export DB_NAME="lis_db"
export DB_USER="postgres"
export CLOUD_SQL_CONNECTION_NAME="project:region:instance"

# 이메일 (Gmail SMTP)
export EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
export EMAIL_HOST="smtp.gmail.com"
export EMAIL_PORT="587"
export EMAIL_USE_TLS="True"
export EMAIL_HOST_USER="kistiman@gmail.com"
# 비밀번호는 Secret Manager에서 관리

# Django
export DEBUG="False"
export ALLOWED_HOSTS="your-domain.com,.run.app"

echo "✅ 환경 변수 설정 완료!"
echo "다음 명령어로 Cloud Run 배포:"
echo "gcloud run deploy \$SERVICE_NAME --source . --region \$REGION"
