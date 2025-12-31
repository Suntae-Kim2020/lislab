"""
샘플 데이터 생성 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.contents.models import Category, Tag, Content
from django.utils.text import slugify

# 관리자 계정 가져오기
admin = User.objects.filter(username='admin').first()
if not admin:
    print("Admin user not found. Please create a superuser first.")
    exit(1)

print(f"✓ Admin user: {admin.username}")

# 카테고리 생성
categories_data = [
    {"name": "프로그래밍", "description": "프로그래밍 언어 및 개발 도구"},
    {"name": "데이터 과학", "description": "데이터 분석, 머신러닝, AI"},
    {"name": "웹 개발", "description": "프론트엔드 및 백엔드 개발"},
    {"name": "데이터베이스", "description": "SQL, NoSQL 데이터베이스"},
    {"name": "클라우드", "description": "AWS, Azure, GCP 등 클라우드 서비스"},
]

categories = {}
for idx, cat_data in enumerate(categories_data, 1):
    category, created = Category.objects.get_or_create(
        slug=slugify(cat_data['name']),
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
            'order': idx,
        }
    )
    categories[cat_data['name']] = category
    print(f"{'✓ Created' if created else '○ Exists'} category: {category.name}")

# 태그 생성
tags_data = [
    "Python", "JavaScript", "React", "Django", "PostgreSQL",
    "Machine Learning", "Deep Learning", "AWS", "Docker", "Git"
]

tags = {}
for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(
        slug=slugify(tag_name),
        defaults={'name': tag_name}
    )
    tags[tag_name] = tag
    print(f"{'✓ Created' if created else '○ Exists'} tag: {tag.name}")

# 샘플 콘텐츠 생성
contents_data = [
    {
        "title": "Python 기초 - 변수와 데이터 타입",
        "summary": "Python의 기본 문법인 변수 선언과 다양한 데이터 타입에 대해 학습합니다.",
        "category": "프로그래밍",
        "tags": ["Python"],
        "difficulty": "BEGINNER",
        "estimated_time": 30,
        "prerequisites": "프로그래밍 경험 없음",
        "learning_objectives": "Python의 변수 개념과 기본 데이터 타입을 이해하고 사용할 수 있습니다.",
        "content": """
<h2>변수란?</h2>
<p>변수는 데이터를 저장하는 공간입니다. Python에서는 변수를 선언할 때 타입을 명시하지 않아도 됩니다.</p>

<h3>변수 선언 예시</h3>
<pre><code>name = "홍길동"
age = 25
height = 175.5
is_student = True</code></pre>

<h2>기본 데이터 타입</h2>
<ul>
<li><strong>문자열 (str):</strong> 텍스트 데이터</li>
<li><strong>정수 (int):</strong> 정수 숫자</li>
<li><strong>실수 (float):</strong> 소수점 숫자</li>
<li><strong>불린 (bool):</strong> True/False 값</li>
</ul>

<h2>실습 예제</h2>
<pre><code># 변수 선언
x = 10
y = 20

# 연산
result = x + y
print(f"결과: {result}")  # 출력: 결과: 30</code></pre>
"""
    },
    {
        "title": "Django REST Framework로 API 만들기",
        "summary": "Django REST Framework를 사용하여 RESTful API를 구축하는 방법을 학습합니다.",
        "category": "웹 개발",
        "tags": ["Python", "Django"],
        "difficulty": "INTERMEDIATE",
        "estimated_time": 60,
        "prerequisites": "Django 기본 지식, Python 프로그래밍 경험",
        "learning_objectives": "DRF를 사용하여 CRUD API를 구현하고 시리얼라이저를 활용할 수 있습니다.",
        "content": """
<h2>Django REST Framework란?</h2>
<p>Django REST Framework(DRF)는 Django 기반의 강력한 웹 API 구축 도구입니다.</p>

<h2>설치</h2>
<pre><code>pip install djangorestframework</code></pre>

<h2>Serializer 만들기</h2>
<pre><code>from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'</code></pre>

<h2>ViewSet 작성</h2>
<pre><code>from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer</code></pre>

<h2>URL 설정</h2>
<pre><code>from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = router.urls</code></pre>
"""
    },
    {
        "title": "React Hooks 완벽 가이드",
        "summary": "React의 Hooks를 활용한 현대적인 컴포넌트 개발 방법을 배웁니다.",
        "category": "웹 개발",
        "tags": ["JavaScript", "React"],
        "difficulty": "INTERMEDIATE",
        "estimated_time": 45,
        "prerequisites": "React 기초, JavaScript ES6+ 문법",
        "learning_objectives": "useState, useEffect 등 주요 Hooks를 이해하고 실무에 적용할 수 있습니다.",
        "content": """
<h2>Hooks란?</h2>
<p>Hooks는 함수형 컴포넌트에서 상태와 생명주기 기능을 사용할 수 있게 해주는 기능입니다.</p>

<h2>useState - 상태 관리</h2>
<pre><code>import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    &lt;div&gt;
      &lt;p&gt;Count: {count}&lt;/p&gt;
      &lt;button onClick={() => setCount(count + 1)}&gt;
        증가
      &lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>

<h2>useEffect - 부수 효과 처리</h2>
<pre><code>import { useEffect, useState } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data));
  }, [userId]);

  if (!user) return &lt;div&gt;Loading...&lt;/div&gt;;
  return &lt;div&gt;{user.name}&lt;/div&gt;;
}</code></pre>

<h2>커스텀 Hook 만들기</h2>
<pre><code>function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}</code></pre>
"""
    },
    {
        "title": "PostgreSQL 성능 최적화 기법",
        "summary": "PostgreSQL 데이터베이스의 성능을 향상시키는 다양한 기법을 학습합니다.",
        "category": "데이터베이스",
        "tags": ["PostgreSQL"],
        "difficulty": "ADVANCED",
        "estimated_time": 90,
        "prerequisites": "SQL 기본 지식, PostgreSQL 사용 경험",
        "learning_objectives": "인덱스 최적화, 쿼리 튜닝, EXPLAIN 분석 등을 수행할 수 있습니다.",
        "content": """
<h2>성능 최적화의 중요성</h2>
<p>데이터베이스 성능은 애플리케이션의 전체 성능에 큰 영향을 미칩니다.</p>

<h2>1. 인덱스 활용</h2>
<pre><code>-- B-Tree 인덱스 생성
CREATE INDEX idx_users_email ON users(email);

-- 복합 인덱스
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);</code></pre>

<h2>2. EXPLAIN으로 쿼리 분석</h2>
<pre><code>EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 123
AND created_at > '2024-01-01';</code></pre>

<h2>3. 쿼리 최적화</h2>
<pre><code>-- 비효율적인 쿼리
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- 최적화된 쿼리 (함수 기반 인덱스 활용)
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';</code></pre>

<h2>4. 파티셔닝</h2>
<pre><code>-- 날짜 기반 파티셔닝
CREATE TABLE orders_2024_q1 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');</code></pre>
"""
    },
    {
        "title": "머신러닝 입문 - 선형 회귀",
        "summary": "가장 기본적인 머신러닝 알고리즘인 선형 회귀에 대해 알아봅니다.",
        "category": "데이터 과학",
        "tags": ["Python", "Machine Learning"],
        "difficulty": "BEGINNER",
        "estimated_time": 50,
        "prerequisites": "Python 기초, 기본 수학 지식",
        "learning_objectives": "선형 회귀의 개념을 이해하고 scikit-learn으로 구현할 수 있습니다.",
        "content": """
<h2>선형 회귀란?</h2>
<p>선형 회귀는 변수 간의 선형 관계를 모델링하는 기법입니다.</p>

<h2>수식</h2>
<p>y = wx + b</p>
<ul>
<li>y: 예측값</li>
<li>x: 입력 특성</li>
<li>w: 가중치</li>
<li>b: 편향</li>
</ul>

<h2>Python 구현</h2>
<pre><code>import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 샘플 데이터
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

# 모델 학습
model = LinearRegression()
model.fit(X, y)

# 예측
X_test = np.array([[6]])
prediction = model.predict(X_test)
print(f"예측값: {prediction[0]}")

# 시각화
plt.scatter(X, y, color='blue', label='실제값')
plt.plot(X, model.predict(X), color='red', label='회귀선')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()</code></pre>

<h2>평가 지표</h2>
<pre><code>from sklearn.metrics import mean_squared_error, r2_score

# MSE (평균 제곱 오차)
mse = mean_squared_error(y, model.predict(X))
print(f"MSE: {mse}")

# R² 점수
r2 = r2_score(y, model.predict(X))
print(f"R² Score: {r2}")</code></pre>
"""
    },
]

for content_data in contents_data:
    content, created = Content.objects.get_or_create(
        slug=slugify(content_data['title']),
        defaults={
            'title': content_data['title'],
            'summary': content_data['summary'],
            'content_html': content_data['content'],
            'category': categories[content_data['category']],
            'author': admin,
            'difficulty': content_data['difficulty'],
            'estimated_time': content_data['estimated_time'],
            'prerequisites': content_data.get('prerequisites'),
            'learning_objectives': content_data.get('learning_objectives'),
            'status': 'PUBLISHED',
            'version': '1.0',
        }
    )

    if created:
        # 태그 추가
        for tag_name in content_data['tags']:
            content.tags.add(tags[tag_name])
        print(f"✓ Created content: {content.title}")
    else:
        print(f"○ Exists content: {content.title}")

print("\n" + "="*50)
print("샘플 데이터 생성 완료!")
print("="*50)
print(f"카테고리: {Category.objects.count()}개")
print(f"태그: {Tag.objects.count()}개")
print(f"콘텐츠: {Content.objects.count()}개")
print("\n접속 정보:")
print("- Frontend: http://localhost:3000")
print("- Backend Admin: http://localhost:8000/admin")
print("- Admin 계정: admin / admin123")
