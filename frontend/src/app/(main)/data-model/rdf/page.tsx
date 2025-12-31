'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Code, BookOpen, Network, Lightbulb, CheckCircle2, ArrowRight, PlayCircle, Sparkles } from 'lucide-react';

const LEARNING_STEPS = [
  {
    id: 'step1',
    title: '1단계: RDF가 뭔가요?',
    subtitle: '시맨틱 웹의 기초를 이해해봅시다',
    content: `
      <div class="space-y-4">
        <div class="bg-blue-50 dark:bg-blue-950 p-4 rounded-lg">
          <p class="font-semibold mb-2">🤔 문제 상황</p>
          <p>웹에는 엄청난 정보가 있지만, 컴퓨터는 그 의미를 이해하지 못합니다.</p>
          <p class="mt-2">예를 들어 "홍길동이 논문을 작성했다"라는 문장을 사람은 이해하지만, 컴퓨터는 단순한 텍스트로만 봅니다.</p>
        </div>

        <div class="bg-green-50 dark:bg-green-950 p-4 rounded-lg">
          <p class="font-semibold mb-2">💡 해결책: RDF</p>
          <p><strong>RDF (Resource Description Framework)</strong>는 데이터를 컴퓨터가 이해할 수 있는 형태로 표현하는 방법입니다.</p>
        </div>

        <div class="border-l-4 border-primary pl-4">
          <p class="font-semibold mb-2">핵심 아이디어</p>
          <p>모든 정보를 <strong>"누가 - 무엇을 - 어떻게"</strong> 형태로 쪼개서 표현합니다.</p>
          <p class="mt-2">이것을 <strong>트리플(Triple)</strong>이라고 부릅니다.</p>
        </div>
      </div>
    `,
    example: `# 이것은 우리가 이해하는 방식:
"홍길동이 인공지능 논문을 작성했다"

# RDF로 표현하면:
주어(Subject):    홍길동
서술어(Predicate): 작성했다
목적어(Object):   인공지능 논문`,
  },
  {
    id: 'step2',
    title: '2단계: 트리플 이해하기',
    subtitle: '주어-서술어-목적어 구조',
    content: `
      <div class="space-y-4">
        <p>RDF의 기본 단위는 <strong>트리플(Triple)</strong>입니다. 항상 3개의 요소로 구성됩니다.</p>

        <div class="grid grid-cols-3 gap-4 my-4">
          <div class="bg-blue-100 dark:bg-blue-900 p-4 rounded text-center">
            <div class="font-bold text-lg mb-2">주어</div>
            <div class="text-sm">Subject</div>
            <div class="mt-2">누가/무엇이</div>
          </div>
          <div class="bg-green-100 dark:bg-green-900 p-4 rounded text-center">
            <div class="font-bold text-lg mb-2">서술어</div>
            <div class="text-sm">Predicate</div>
            <div class="mt-2">어떤 관계/속성</div>
          </div>
          <div class="bg-purple-100 dark:bg-purple-900 p-4 rounded text-center">
            <div class="font-bold text-lg mb-2">목적어</div>
            <div class="text-sm">Object</div>
            <div class="mt-2">무엇을/값</div>
          </div>
        </div>

        <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded">
          <p class="font-semibold mb-3">📝 실제 예시들:</p>
          <div class="space-y-2 text-sm">
            <div class="flex items-center gap-2">
              <span class="bg-blue-200 dark:bg-blue-800 px-2 py-1 rounded">홍길동</span>
              <span>→</span>
              <span class="bg-green-200 dark:bg-green-800 px-2 py-1 rounded">나이</span>
              <span>→</span>
              <span class="bg-purple-200 dark:bg-purple-800 px-2 py-1 rounded">30</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="bg-blue-200 dark:bg-blue-800 px-2 py-1 rounded">홍길동</span>
              <span>→</span>
              <span class="bg-green-200 dark:bg-green-800 px-2 py-1 rounded">직업</span>
              <span>→</span>
              <span class="bg-purple-200 dark:bg-purple-800 px-2 py-1 rounded">교수</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="bg-blue-200 dark:bg-blue-800 px-2 py-1 rounded">홍길동</span>
              <span>→</span>
              <span class="bg-green-200 dark:bg-green-800 px-2 py-1 rounded">알고있다</span>
              <span>→</span>
              <span class="bg-purple-200 dark:bg-purple-800 px-2 py-1 rounded">김철수</span>
            </div>
          </div>
        </div>

        <div class="bg-yellow-50 dark:bg-yellow-950 p-4 rounded">
          <p class="font-semibold mb-2">💡 왜 이렇게 표현할까요?</p>
          <p>컴퓨터가 데이터 간의 관계를 이해하고 연결할 수 있습니다!</p>
        </div>
      </div>
    `,
    example: `# 사람이 읽는 방식:
홍길동은 30살이고, 교수이며, 김철수를 안다.

# RDF 트리플로 분해:
1. 홍길동 - 나이 - 30
2. 홍길동 - 직업 - 교수
3. 홍길동 - 알고있다 - 김철수`,
  },
  {
    id: 'step3',
    title: '3단계: Turtle 문법 배우기',
    subtitle: 'RDF를 작성하는 가장 쉬운 방법',
    content: `
      <div class="space-y-4">
        <p><strong>Turtle</strong>은 RDF를 작성하는 가장 읽기 쉬운 형식입니다.</p>

        <div class="space-y-4">
          <div>
            <p class="font-semibold mb-2">1️⃣ 네임스페이스 선언 (접두어 정의)</p>
            <p class="text-sm mb-2">긴 URL을 짧게 줄이기 위한 약어를 만듭니다.</p>
            <div class="bg-gray-100 dark:bg-gray-900 p-3 rounded font-mono text-sm">
              @prefix ex: &lt;http://example.org/&gt; .<br/>
              @prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .
            </div>
            <p class="text-xs text-gray-600 mt-2">이제 긴 URL 대신 ex:, foaf: 같은 짧은 접두어를 쓸 수 있어요!</p>
          </div>

          <div>
            <p class="font-semibold mb-2">2️⃣ 트리플 작성</p>
            <p class="text-sm mb-2">주어, 서술어, 목적어를 공백으로 구분하고 마침표(.)로 끝냅니다.</p>
            <div class="bg-gray-100 dark:bg-gray-900 p-3 rounded font-mono text-sm">
              ex:홍길동 foaf:name "홍길동" .
            </div>
          </div>

          <div>
            <p class="font-semibold mb-2">3️⃣ 같은 주어 여러 속성 (세미콜론 ; 사용)</p>
            <p class="text-sm mb-2">같은 사람의 여러 정보를 한번에 쓸 수 있습니다.</p>
            <div class="bg-gray-100 dark:bg-gray-900 p-3 rounded font-mono text-sm">
              ex:홍길동 foaf:name "홍길동" ;<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:age 30 ;<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:title "교수" .
            </div>
            <p class="text-xs text-gray-600 mt-2">세미콜론(;)을 쓰면 주어를 반복하지 않아도 돼요!</p>
          </div>

          <div>
            <p class="font-semibold mb-2">4️⃣ 여러 값 나열 (쉼표 , 사용)</p>
            <div class="bg-gray-100 dark:bg-gray-900 p-3 rounded font-mono text-sm">
              ex:홍길동 foaf:knows ex:김철수, ex:이영희, ex:박민수 .
            </div>
            <p class="text-xs text-gray-600 mt-2">홍길동이 여러 사람을 안다는 것을 간단하게 표현!</p>
          </div>
        </div>

        <div class="bg-green-50 dark:bg-green-950 p-4 rounded">
          <p class="font-semibold mb-2">✨ 기억하세요!</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li>마침표(.) = 트리플 끝</li>
            <li>세미콜론(;) = 같은 주어, 다른 서술어</li>
            <li>쉼표(,) = 같은 주어와 서술어, 여러 목적어</li>
          </ul>
        </div>
      </div>
    `,
    example: `@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

# 간단한 방식
ex:홍길동 foaf:name "홍길동" .
ex:홍길동 foaf:age 30 .
ex:홍길동 foaf:title "교수" .

# 똑같은 내용을 더 깔끔하게!
ex:홍길동 foaf:name "홍길동" ;
          foaf:age 30 ;
          foaf:title "교수" .`,
  },
  {
    id: 'step4',
    title: '4단계: 실전 예제',
    subtitle: '실제로 작성해봅시다',
    content: `
      <div class="space-y-4">
        <p class="font-semibold">이제 실제 상황을 RDF로 표현해볼까요?</p>

        <div class="bg-blue-50 dark:bg-blue-950 p-4 rounded-lg">
          <p class="font-semibold mb-2">📖 시나리오</p>
          <p>홍길동 교수님이 "인공지능 윤리"라는 논문을 2024년에 작성했습니다.</p>
          <p>이 논문은 한국대학교에서 발행되었고, 주제는 "AI"와 "윤리"입니다.</p>
        </div>

        <div class="space-y-3">
          <div>
            <p class="font-semibold text-sm mb-2">🔍 이 정보를 트리플로 분해하면:</p>
            <div class="text-sm space-y-1 bg-gray-50 dark:bg-gray-900 p-3 rounded">
              <div>1. 논문 - 제목 - "인공지능 윤리"</div>
              <div>2. 논문 - 작성자 - 홍길동</div>
              <div>3. 논문 - 발행년도 - 2024</div>
              <div>4. 논문 - 발행기관 - 한국대학교</div>
              <div>5. 논문 - 주제 - "AI"</div>
              <div>6. 논문 - 주제 - "윤리"</div>
            </div>
          </div>

          <div>
            <p class="font-semibold text-sm mb-2">📝 Turtle로 작성하면:</p>
            <div class="bg-gray-100 dark:bg-gray-900 p-4 rounded font-mono text-xs overflow-x-auto">
              @prefix ex: &lt;http://example.org/&gt; .<br/>
              @prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br/>
              <br/>
              ex:논문001 dc:title "인공지능 윤리" ;<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dc:creator "홍길동" ;<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dc:date "2024" ;<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dc:publisher "한국대학교" ;<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dc:subject "AI", "윤리" .
            </div>
          </div>
        </div>

        <div class="bg-yellow-50 dark:bg-yellow-950 p-4 rounded">
          <p class="font-semibold mb-2">💡 포인트</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li><strong>dc:</strong>는 Dublin Core의 약자 (도서관에서 많이 쓰는 표준 어휘)</li>
            <li>같은 주어의 여러 속성을 세미콜론(;)으로 연결</li>
            <li>여러 주제는 쉼표(,)로 나열</li>
          </ul>
        </div>
      </div>
    `,
    example: `@prefix ex: <http://example.org/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .

ex:논문001 dc:title "인공지능 윤리" ;
          dc:creator "홍길동" ;
          dc:date "2024" ;
          dc:publisher "한국대학교" ;
          dc:subject "AI", "윤리" .

# 이제 컴퓨터가 이 논문에 대한
# 모든 정보를 이해할 수 있어요!`,
  },
  {
    id: 'step5',
    title: '5단계: 관계 표현하기',
    subtitle: '사람들 사이의 연결을 나타내봅시다',
    content: `
      <div class="space-y-4">
        <p>RDF의 진짜 힘은 <strong>관계를 표현</strong>하는 것입니다!</p>

        <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-950 dark:to-purple-950 p-4 rounded-lg">
          <p class="font-semibold mb-3">👥 소셜 네트워크 예제</p>
          <p class="mb-2">홍길동, 김철수, 이영희가 서로를 알고 있습니다.</p>
          <div class="flex items-center justify-center gap-4 my-4 text-sm">
            <div class="bg-white dark:bg-gray-800 px-4 py-2 rounded-lg shadow">홍길동</div>
            <span>↔</span>
            <div class="bg-white dark:bg-gray-800 px-4 py-2 rounded-lg shadow">김철수</div>
            <span>↔</span>
            <div class="bg-white dark:bg-gray-800 px-4 py-2 rounded-lg shadow">이영희</div>
          </div>
        </div>

        <div>
          <p class="font-semibold text-sm mb-2">RDF로 표현:</p>
          <div class="bg-gray-100 dark:bg-gray-900 p-4 rounded font-mono text-xs overflow-x-auto">
            @prefix ex: &lt;http://example.org/&gt; .<br/>
            @prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br/>
            <br/>
            ex:홍길동 a foaf:Person ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:name "홍길동" ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:age 30 ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:knows ex:김철수, ex:이영희 .<br/>
            <br/>
            ex:김철수 a foaf:Person ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:name "김철수" ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:age 28 ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:knows ex:홍길동, ex:이영희 .<br/>
            <br/>
            ex:이영희 a foaf:Person ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:name "이영희" ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:age 25 ;<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foaf:knows ex:홍길동, ex:김철수 .
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 mt-4">
          <div class="bg-blue-50 dark:bg-blue-950 p-3 rounded">
            <p class="font-semibold text-sm mb-2">🔤 a 는 무엇?</p>
            <p class="text-xs"><code>a</code>는 "타입이다"라는 뜻입니다.</p>
            <p class="text-xs mt-1"><code>ex:홍길동 a foaf:Person</code> = "홍길동은 사람이다"</p>
          </div>
          <div class="bg-green-50 dark:bg-green-950 p-3 rounded">
            <p class="font-semibold text-sm mb-2">🔗 foaf:knows</p>
            <p class="text-xs">FOAF (Friend of a Friend)의 "안다"는 관계</p>
            <p class="text-xs mt-1">소셜 네트워크를 표현하는 표준 어휘</p>
          </div>
        </div>

        <div class="bg-green-50 dark:bg-green-950 p-4 rounded mt-4">
          <p class="font-semibold mb-2">✨ 이렇게 하면 뭐가 좋을까요?</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li>컴퓨터가 "홍길동이 아는 사람들"을 자동으로 찾을 수 있어요</li>
            <li>"친구의 친구" 같은 간접 관계도 추적 가능해요</li>
            <li>여러 데이터베이스를 연결할 수 있어요</li>
          </ul>
        </div>
      </div>
    `,
    example: `@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

# 세 사람의 정보와 관계를 표현
ex:홍길동 a foaf:Person ;
          foaf:name "홍길동" ;
          foaf:knows ex:김철수, ex:이영희 .

ex:김철수 a foaf:Person ;
          foaf:name "김철수" ;
          foaf:knows ex:홍길동 .

ex:이영희 a foaf:Person ;
          foaf:name "이영희" ;
          foaf:knows ex:홍길동 .`,
  },
];

const QUICK_EXAMPLES = [
  {
    title: '자기소개',
    code: `@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:나 a foaf:Person ;
     foaf:name "홍길동" ;
     foaf:age 30 ;
     foaf:mbox "hong@example.com" ;
     foaf:homepage <http://example.com> .`
  },
  {
    title: '회사 정보',
    code: `@prefix ex: <http://example.org/> .
@prefix org: <http://www.w3.org/ns/org#> .

ex:한국회사 a org:Organization ;
           org:name "한국회사" ;
           org:hasMember ex:홍길동 ;
           org:siteAddress "서울시 강남구" .`
  },
  {
    title: '도서 정보',
    code: `@prefix ex: <http://example.org/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .

ex:book1 dc:title "RDF 입문서" ;
         dc:creator "홍길동" ;
         dc:date "2024-12-29" ;
         dc:language "ko" .`
  }
];

export default function RDFLearningPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [userCode, setUserCode] = useState('');
  const [showHint, setShowHint] = useState(false);

  const currentLesson = LEARNING_STEPS[currentStep];

  const handleNextStep = () => {
    if (currentStep < LEARNING_STEPS.length - 1) {
      setCurrentStep(currentStep + 1);
      setShowHint(false);
    }
  };

  const handlePrevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      setShowHint(false);
    }
  };

  const loadExample = (code: string) => {
    setUserCode(code);
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-7xl">
      {/* Header */}
      <div className="mb-8 text-center">
        <div className="flex items-center justify-center gap-3 mb-3">
          <Network className="h-12 w-12 text-primary" />
          <h1 className="text-4xl font-bold">RDF 쉽게 배우기</h1>
        </div>
        <p className="text-lg text-muted-foreground">
          시맨틱 웹의 핵심! 데이터를 연결하는 방법을 단계별로 배워봅시다
        </p>
        <div className="mt-4 flex items-center justify-center gap-2">
          <Badge variant="secondary">중급</Badge>
          <Badge variant="outline">30분 소요</Badge>
          <Badge variant="outline">실습 포함</Badge>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium">학습 진행률</span>
          <span className="text-sm text-muted-foreground">
            {currentStep + 1} / {LEARNING_STEPS.length} 단계
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            className="bg-primary h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentStep + 1) / LEARNING_STEPS.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Learning Content */}
      <div className="grid gap-6 lg:grid-cols-2 mb-8">
        {/* Left: Lesson */}
        <Card className="lg:sticky lg:top-4 h-fit">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="text-2xl mb-2">{currentLesson.title}</CardTitle>
                <CardDescription className="text-base">{currentLesson.subtitle}</CardDescription>
              </div>
              <Badge variant="outline">{currentStep + 1}/{LEARNING_STEPS.length}</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div
              className="prose prose-sm max-w-none dark:prose-invert"
              dangerouslySetInnerHTML={{ __html: currentLesson.content }}
            />

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between mt-6 pt-6 border-t">
              <Button
                variant="outline"
                onClick={handlePrevStep}
                disabled={currentStep === 0}
              >
                이전 단계
              </Button>
              <div className="flex gap-2">
                {currentStep < LEARNING_STEPS.length - 1 ? (
                  <Button onClick={handleNextStep} className="gap-2">
                    다음 단계
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                ) : (
                  <Button variant="default" className="gap-2">
                    <CheckCircle2 className="h-4 w-4" />
                    학습 완료!
                  </Button>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Right: Practice */}
        <div className="space-y-6">
          {/* Example Code */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="h-5 w-5" />
                예제 코드
              </CardTitle>
              <CardDescription>이 단계에서 배운 내용을 코드로 확인해보세요</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg">
                <pre className="text-sm font-mono whitespace-pre-wrap overflow-x-auto">
                  {currentLesson.example}
                </pre>
              </div>
              <Button
                variant="outline"
                size="sm"
                className="mt-3"
                onClick={() => loadExample(currentLesson.example)}
              >
                <PlayCircle className="h-4 w-4 mr-2" />
                연습장에 불러오기
              </Button>
            </CardContent>
          </Card>

          {/* Practice Area */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                직접 작성해보기
              </CardTitle>
              <CardDescription>배운 내용을 응용해서 RDF를 작성해보세요</CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                placeholder="여기에 RDF 코드를 작성해보세요..."
                className="font-mono text-sm min-h-[300px]"
              />
              <div className="flex items-center gap-2 mt-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowHint(!showHint)}
                >
                  <Lightbulb className="h-4 w-4 mr-2" />
                  {showHint ? '힌트 숨기기' : '힌트 보기'}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setUserCode('')}
                >
                  지우기
                </Button>
              </div>

              {showHint && (
                <Alert className="mt-3">
                  <Lightbulb className="h-4 w-4" />
                  <AlertDescription>
                    <strong>힌트:</strong> 위의 예제 코드를 참고하되, 자신만의 데이터로 바꿔보세요!
                    예를 들어 이름, 나이, 직업 등을 자신의 정보로 변경해보세요.
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Quick Start Templates */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5" />
            빠른 시작 템플릿
          </CardTitle>
          <CardDescription>자주 사용하는 RDF 패턴을 바로 사용해보세요</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-4">
            {QUICK_EXAMPLES.map((example, index) => (
              <Card
                key={index}
                className="cursor-pointer hover:bg-accent transition-colors"
                onClick={() => loadExample(example.code)}
              >
                <CardHeader className="p-4">
                  <CardTitle className="text-base">{example.title}</CardTitle>
                </CardHeader>
                <CardContent className="p-4 pt-0">
                  <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                    {example.code.split('\n').slice(0, 3).join('\n')}...
                  </pre>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Additional Resources */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>더 알아보기</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="serialization">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="serialization">직렬화 형식</TabsTrigger>
              <TabsTrigger value="sparql">SPARQL</TabsTrigger>
              <TabsTrigger value="vocab">주요 어휘</TabsTrigger>
              <TabsTrigger value="tools">도구</TabsTrigger>
              <TabsTrigger value="resources">참고자료</TabsTrigger>
            </TabsList>

            <TabsContent value="serialization" className="space-y-4">
              <div className="space-y-4">
                <Alert>
                  <AlertDescription>
                    같은 RDF 데이터를 다양한 형식으로 표현할 수 있습니다. 각 형식은 상황에 따라 장단점이 있습니다.
                  </AlertDescription>
                </Alert>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Badge variant="default">추천</Badge>
                      Turtle (Terse RDF Triple Language)
                    </CardTitle>
                    <CardDescription>사람이 읽고 쓰기 가장 쉬운 형식</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:홍길동 a foaf:Person ;
          foaf:name "홍길동" ;
          foaf:age 30 ;
          foaf:mbox "hong@example.com" .`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>✓ <strong>장점:</strong> 가독성이 뛰어나고 간결함</div>
                        <div>✓ <strong>단점:</strong> 대용량 데이터 처리 시 파싱 속도가 느릴 수 있음</div>
                        <div>✓ <strong>용도:</strong> 문서 작성, 학습, 수동 편집</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">RDF/XML</CardTitle>
                    <CardDescription>XML 기반의 표준 RDF 형식</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:foaf="http://xmlns.com/foaf/0.1/"
         xmlns:ex="http://example.org/">

  <foaf:Person rdf:about="http://example.org/홍길동">
    <foaf:name>홍길동</foaf:name>
    <foaf:age rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">
      30
    </foaf:age>
    <foaf:mbox>hong@example.com</foaf:mbox>
  </foaf:Person>

</rdf:RDF>`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>✓ <strong>장점:</strong> XML 도구와 호환, W3C 표준</div>
                        <div>✓ <strong>단점:</strong> 장황하고 읽기 어려움</div>
                        <div>✓ <strong>용도:</strong> 레거시 시스템, XML 기반 워크플로우</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Badge variant="secondary">인기</Badge>
                      JSON-LD (JSON for Linking Data)
                    </CardTitle>
                    <CardDescription>JSON 형식의 링크드 데이터</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`{
  "@context": {
    "foaf": "http://xmlns.com/foaf/0.1/",
    "ex": "http://example.org/"
  },
  "@id": "ex:홍길동",
  "@type": "foaf:Person",
  "foaf:name": "홍길동",
  "foaf:age": {
    "@value": 30,
    "@type": "http://www.w3.org/2001/XMLSchema#integer"
  },
  "foaf:mbox": "hong@example.com"
}`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>✓ <strong>장점:</strong> JavaScript와 완벽 호환, 웹 API에 적합</div>
                        <div>✓ <strong>단점:</strong> @context 이해 필요</div>
                        <div>✓ <strong>용도:</strong> 웹 API, Schema.org, SEO</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">N-Triples</CardTitle>
                    <CardDescription>가장 단순한 라인 기반 형식</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`<http://example.org/홍길동> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.org/홍길동> <http://xmlns.com/foaf/0.1/name> "홍길동" .
<http://example.org/홍길동> <http://xmlns.com/foaf/0.1/age> "30"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/홍길동> <http://xmlns.com/foaf/0.1/mbox> "hong@example.com" .`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>✓ <strong>장점:</strong> 파싱이 매우 빠르고 간단함, 스트리밍 가능</div>
                        <div>✓ <strong>단점:</strong> 파일 크기가 크고 가독성 낮음</div>
                        <div>✓ <strong>용도:</strong> 대용량 데이터 처리, 데이터 교환</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <div className="bg-blue-50 dark:bg-blue-950 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">💡 어떤 형식을 선택해야 할까요?</h4>
                  <ul className="text-sm space-y-1 list-disc list-inside">
                    <li><strong>학습/문서:</strong> Turtle (가장 읽기 쉬움)</li>
                    <li><strong>웹 API:</strong> JSON-LD (JavaScript와 호환)</li>
                    <li><strong>대용량 데이터:</strong> N-Triples (빠른 처리)</li>
                    <li><strong>레거시 시스템:</strong> RDF/XML (표준 형식)</li>
                  </ul>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="sparql" className="space-y-4">
              <div className="space-y-4">
                <Alert>
                  <AlertDescription>
                    SPARQL은 RDF 데이터를 검색하고 조작하는 쿼리 언어입니다. SQL과 유사하지만 그래프 구조에 특화되어 있습니다.
                  </AlertDescription>
                </Alert>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">기본 SELECT 쿼리</CardTitle>
                    <CardDescription>RDF 데이터에서 원하는 정보 찾기</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="text-sm mb-2">
                        <strong>목표:</strong> 모든 사람의 이름 찾기
                      </div>
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name
WHERE {
  ?person a foaf:Person .
  ?person foaf:name ?name .
}`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>• <code className="bg-muted px-2 py-1">PREFIX</code>: 네임스페이스 정의 (Turtle과 동일)</div>
                        <div>• <code className="bg-muted px-2 py-1">SELECT</code>: 가져올 변수 지정</div>
                        <div>• <code className="bg-muted px-2 py-1">WHERE</code>: 패턴 매칭 조건</div>
                        <div>• <code className="bg-muted px-2 py-1">?변수</code>: 물음표로 시작하는 변수</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">FILTER로 조건 추가</CardTitle>
                    <CardDescription>특정 조건을 만족하는 데이터만 선택</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="text-sm mb-2">
                        <strong>목표:</strong> 30세 이상인 사람만 찾기
                      </div>
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?age
WHERE {
  ?person a foaf:Person .
  ?person foaf:name ?name .
  ?person foaf:age ?age .
  FILTER (?age >= 30)
}
ORDER BY DESC(?age)`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>• <code className="bg-muted px-2 py-1">FILTER</code>: 조건 필터링</div>
                        <div>• <code className="bg-muted px-2 py-1">ORDER BY</code>: 결과 정렬</div>
                        <div>• <code className="bg-muted px-2 py-1">DESC</code>: 내림차순 (ASC는 오름차순)</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">OPTIONAL 패턴</CardTitle>
                    <CardDescription>선택적 정보 포함하기</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="text-sm mb-2">
                        <strong>목표:</strong> 이메일이 있으면 함께 가져오기 (없어도 결과에 포함)
                      </div>
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?email
WHERE {
  ?person a foaf:Person .
  ?person foaf:name ?name .
  OPTIONAL { ?person foaf:mbox ?email }
}`}</pre>
                      </div>
                      <div className="text-sm">
                        이메일이 없는 사람도 결과에 포함되며, ?email은 null이 됩니다.
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">관계 탐색</CardTitle>
                    <CardDescription>친구의 친구 찾기</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="text-sm mb-2">
                        <strong>목표:</strong> 홍길동의 친구가 아는 사람들 찾기
                      </div>
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?friendOfFriend ?name
WHERE {
  ex:홍길동 foaf:knows ?friend .
  ?friend foaf:knows ?friendOfFriend .
  ?friendOfFriend foaf:name ?name .
  FILTER (?friendOfFriend != ex:홍길동)
}`}</pre>
                      </div>
                      <div className="text-sm">
                        2단계 관계를 탐색하여 간접 연결을 찾을 수 있습니다.
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">집계 쿼리 (COUNT, AVG)</CardTitle>
                    <CardDescription>데이터 통계 내기</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="text-sm mb-2">
                        <strong>목표:</strong> 각 사람이 아는 친구 수 세기
                      </div>
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name (COUNT(?friend) AS ?friendCount)
WHERE {
  ?person a foaf:Person .
  ?person foaf:name ?name .
  OPTIONAL { ?person foaf:knows ?friend }
}
GROUP BY ?name
ORDER BY DESC(?friendCount)`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>• <code className="bg-muted px-2 py-1">COUNT</code>: 개수 세기</div>
                        <div>• <code className="bg-muted px-2 py-1">AVG</code>: 평균 계산</div>
                        <div>• <code className="bg-muted px-2 py-1">GROUP BY</code>: 그룹화</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">실전 예제: DBpedia 쿼리</CardTitle>
                    <CardDescription>위키피디아에서 한국 대학교 찾기</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm font-mono overflow-x-auto">{`PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?university ?name ?students
WHERE {
  ?university a dbo:University .
  ?university dbo:country dbr:South_Korea .
  ?university rdfs:label ?name .
  ?university dbo:numberOfStudents ?students .
  FILTER (lang(?name) = "ko")
}
ORDER BY DESC(?students)
LIMIT 10`}</pre>
                      </div>
                      <div className="text-sm space-y-1">
                        <div>• <code className="bg-muted px-2 py-1">LIMIT</code>: 결과 개수 제한</div>
                        <div>• <code className="bg-muted px-2 py-1">lang()</code>: 언어 필터링</div>
                        <div>• 실제로 <a href="https://dbpedia.org/sparql" target="_blank" className="text-primary hover:underline">DBpedia SPARQL Endpoint</a>에서 실행 가능</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <div className="bg-green-50 dark:bg-green-950 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">🎯 SPARQL 연습하기</h4>
                  <ul className="text-sm space-y-2">
                    <li><strong>DBpedia:</strong> <a href="https://dbpedia.org/sparql" target="_blank" className="text-primary hover:underline">https://dbpedia.org/sparql</a></li>
                    <li><strong>Wikidata:</strong> <a href="https://query.wikidata.org" target="_blank" className="text-primary hover:underline">https://query.wikidata.org</a></li>
                    <li><strong>SPARQL Playground:</strong> 로컬 데이터로 연습</li>
                  </ul>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="vocab" className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">FOAF (Friend of a Friend)</CardTitle>
                    <CardDescription>사람과 관계를 표현</CardDescription>
                  </CardHeader>
                  <CardContent className="text-sm space-y-1">
                    <div><code className="bg-muted px-2 py-1">foaf:Person</code> - 사람</div>
                    <div><code className="bg-muted px-2 py-1">foaf:name</code> - 이름</div>
                    <div><code className="bg-muted px-2 py-1">foaf:knows</code> - ~을 안다</div>
                    <div><code className="bg-muted px-2 py-1">foaf:mbox</code> - 이메일</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">Dublin Core (DC)</CardTitle>
                    <CardDescription>문서 메타데이터</CardDescription>
                  </CardHeader>
                  <CardContent className="text-sm space-y-1">
                    <div><code className="bg-muted px-2 py-1">dc:title</code> - 제목</div>
                    <div><code className="bg-muted px-2 py-1">dc:creator</code> - 작성자</div>
                    <div><code className="bg-muted px-2 py-1">dc:date</code> - 날짜</div>
                    <div><code className="bg-muted px-2 py-1">dc:subject</code> - 주제</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">Schema.org</CardTitle>
                    <CardDescription>구조화된 데이터 (SEO)</CardDescription>
                  </CardHeader>
                  <CardContent className="text-sm space-y-1">
                    <div><code className="bg-muted px-2 py-1">schema:Person</code> - 사람</div>
                    <div><code className="bg-muted px-2 py-1">schema:Organization</code> - 조직</div>
                    <div><code className="bg-muted px-2 py-1">schema:Article</code> - 기사</div>
                    <div><code className="bg-muted px-2 py-1">schema:Event</code> - 이벤트</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">ORG (Organization)</CardTitle>
                    <CardDescription>조직 구조</CardDescription>
                  </CardHeader>
                  <CardContent className="text-sm space-y-1">
                    <div><code className="bg-muted px-2 py-1">org:Organization</code> - 조직</div>
                    <div><code className="bg-muted px-2 py-1">org:hasMember</code> - 구성원</div>
                    <div><code className="bg-muted px-2 py-1">org:memberOf</code> - ~의 구성원</div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="tools" className="space-y-4">
              <div className="space-y-3">
                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">RDF 검증 및 변환</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-2">
                    <div>• <strong>W3C RDF Validator:</strong> RDF 문법 검증</div>
                    <div>• <strong>EasyRDF Converter:</strong> Turtle ↔ RDF/XML ↔ JSON-LD 변환</div>
                    <div>• <strong>RDFShape:</strong> 온라인 RDF 편집기</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">SPARQL 쿼리 연습</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-2">
                    <div>• <strong>DBpedia SPARQL:</strong> 위키피디아 데이터 쿼리</div>
                    <div>• <strong>Wikidata Query Service:</strong> Wikidata 쿼리</div>
                    <div>• <strong>SPARQL Playground:</strong> 연습용 SPARQL 환경</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">RDF 데이터베이스</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-2">
                    <div>• <strong>Apache Jena:</strong> Java 기반 RDF 프레임워크</div>
                    <div>• <strong>RDF4J:</strong> Java RDF 라이브러리</div>
                    <div>• <strong>Virtuoso:</strong> 고성능 Triple Store</div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="resources" className="space-y-4">
              <div className="space-y-3">
                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">공식 문서</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-2">
                    <div>• W3C RDF 1.1 Primer</div>
                    <div>• W3C Turtle Specification</div>
                    <div>• SPARQL 1.1 Query Language</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">실습 데이터</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-2">
                    <div>• DBpedia: 위키피디아의 구조화된 데이터</div>
                    <div>• Wikidata: 협업 지식 베이스</div>
                    <div>• Linked Open Vocabularies: 어휘 검색</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">다음 학습</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-2">
                    <div>• <strong>RDFS:</strong> RDF Schema로 클래스와 속성 정의하기</div>
                    <div>• <strong>OWL:</strong> 복잡한 온톨로지 만들기</div>
                    <div>• <strong>SPARQL:</strong> RDF 데이터 검색하기</div>
                    <div>• <strong>추론:</strong> 규칙 기반 지식 추론하기</div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
