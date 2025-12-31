'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Code, Eye, BookOpen } from 'lucide-react';

const DEFAULT_HTML = `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>나의 첫 HTML 페이지</title>
</head>
<body>
    <h1>HTML 기초 학습</h1>
    <p>여기에 HTML 코드를 작성해보세요!</p>

    <h2>제목 태그</h2>
    <p>h1부터 h6까지 사용할 수 있습니다.</p>

    <h2>목록</h2>
    <ul>
        <li>첫 번째 항목</li>
        <li>두 번째 항목</li>
        <li>세 번째 항목</li>
    </ul>

    <h2>링크</h2>
    <a href="https://www.w3schools.com/html/" target="_blank">HTML 튜토리얼</a>

    <h2>이미지</h2>
    <img src="https://via.placeholder.com/300x200" alt="예제 이미지">
</body>
</html>`;

const HTML_EXAMPLES = [
  {
    title: '기본 구조',
    description: 'HTML 문서의 기본 구조',
    code: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>페이지 제목</title>
</head>
<body>
    <h1>안녕하세요!</h1>
    <p>이것은 HTML 문서입니다.</p>
</body>
</html>`
  },
  {
    title: '텍스트 서식',
    description: '다양한 텍스트 서식 태그',
    code: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>텍스트 서식</title>
</head>
<body>
    <h1>텍스트 서식 예제</h1>

    <p><strong>굵은 글씨</strong></p>
    <p><em>기울임 글씨</em></p>
    <p><mark>형광펜 효과</mark></p>
    <p><del>취소선</del></p>
    <p><u>밑줄</u></p>
    <p>H<sub>2</sub>O (아래 첨자)</p>
    <p>X<sup>2</sup> (위 첨자)</p>
</body>
</html>`
  },
  {
    title: '목록',
    description: '순서 있는 목록과 순서 없는 목록',
    code: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>목록</title>
</head>
<body>
    <h2>순서 없는 목록</h2>
    <ul>
        <li>사과</li>
        <li>바나나</li>
        <li>오렌지</li>
    </ul>

    <h2>순서 있는 목록</h2>
    <ol>
        <li>첫 번째</li>
        <li>두 번째</li>
        <li>세 번째</li>
    </ol>
</body>
</html>`
  },
  {
    title: '테이블',
    description: '표 만들기',
    code: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>테이블</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h2>학생 정보</h2>
    <table>
        <tr>
            <th>이름</th>
            <th>나이</th>
            <th>학년</th>
        </tr>
        <tr>
            <td>홍길동</td>
            <td>20</td>
            <td>2학년</td>
        </tr>
        <tr>
            <td>김철수</td>
            <td>21</td>
            <td>3학년</td>
        </tr>
    </table>
</body>
</html>`
  },
  {
    title: '폼 (Form)',
    description: '사용자 입력 폼',
    code: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>폼</title>
</head>
<body>
    <h2>회원가입 폼</h2>
    <form>
        <label for="name">이름:</label><br>
        <input type="text" id="name" name="name"><br><br>

        <label for="email">이메일:</label><br>
        <input type="email" id="email" name="email"><br><br>

        <label for="password">비밀번호:</label><br>
        <input type="password" id="password" name="password"><br><br>

        <label for="gender">성별:</label><br>
        <input type="radio" id="male" name="gender" value="male">
        <label for="male">남성</label>
        <input type="radio" id="female" name="gender" value="female">
        <label for="female">여성</label><br><br>

        <input type="submit" value="제출">
    </form>
</body>
</html>`
  }
];

export default function HTMLLearningPage() {
  const [htmlCode, setHtmlCode] = useState(DEFAULT_HTML);

  const handlePreview = () => {
    const previewWindow = window.open('', '_blank', 'width=800,height=600');
    if (previewWindow) {
      previewWindow.document.write(htmlCode);
      previewWindow.document.close();
    }
  };

  const loadExample = (code: string) => {
    setHtmlCode(code);
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-2">HTML 기초 학습</h1>
        <p className="text-muted-foreground">
          HTML 태그를 직접 작성하고 결과를 확인해보세요.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* HTML Editor */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Code className="h-5 w-5" />
                    HTML 에디터
                  </CardTitle>
                  <CardDescription>아래에 HTML 코드를 입력하세요</CardDescription>
                </div>
                <Button onClick={handlePreview} className="gap-2">
                  <Eye className="h-4 w-4" />
                  미리보기
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <Textarea
                value={htmlCode}
                onChange={(e) => setHtmlCode(e.target.value)}
                className="font-mono text-sm min-h-[500px]"
                placeholder="HTML 코드를 입력하세요..."
              />
            </CardContent>
          </Card>
        </div>

        {/* Examples Sidebar */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                예제 코드
              </CardTitle>
              <CardDescription>예제를 클릭하여 에디터에 불러오세요</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {HTML_EXAMPLES.map((example, index) => (
                  <Card
                    key={index}
                    className="cursor-pointer hover:bg-accent transition-colors"
                    onClick={() => loadExample(example.code)}
                  >
                    <CardHeader className="p-4">
                      <CardTitle className="text-sm">{example.title}</CardTitle>
                      <CardDescription className="text-xs">
                        {example.description}
                      </CardDescription>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Learning Guide */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>HTML 기본 태그 가이드</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="structure">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="structure">구조</TabsTrigger>
              <TabsTrigger value="text">텍스트</TabsTrigger>
              <TabsTrigger value="list">목록</TabsTrigger>
              <TabsTrigger value="link">링크</TabsTrigger>
              <TabsTrigger value="media">미디어</TabsTrigger>
            </TabsList>

            <TabsContent value="structure" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">문서 구조 태그</h3>
                <ul className="space-y-2 text-sm">
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;!DOCTYPE html&gt;</code> - HTML5 문서 선언</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;html&gt;</code> - HTML 문서의 루트 요소</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;head&gt;</code> - 메타데이터 영역</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;body&gt;</code> - 본문 내용</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;div&gt;</code> - 블록 레벨 컨테이너</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;span&gt;</code> - 인라인 컨테이너</li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="text" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">텍스트 관련 태그</h3>
                <ul className="space-y-2 text-sm">
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;h1&gt; ~ &lt;h6&gt;</code> - 제목 (h1이 가장 큰 제목)</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;p&gt;</code> - 단락</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;strong&gt;</code> - 굵은 글씨 (중요)</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;em&gt;</code> - 기울임 (강조)</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;br&gt;</code> - 줄 바꿈</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;hr&gt;</code> - 수평선</li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="list" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">목록 태그</h3>
                <ul className="space-y-2 text-sm">
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;ul&gt;</code> - 순서 없는 목록</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;ol&gt;</code> - 순서 있는 목록</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;li&gt;</code> - 목록 항목</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;dl&gt;</code> - 정의 목록</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;dt&gt;</code> - 정의 용어</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;dd&gt;</code> - 정의 설명</li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="link" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">링크 태그</h3>
                <ul className="space-y-2 text-sm">
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;a href="URL"&gt;</code> - 하이퍼링크</li>
                  <li><code className="bg-muted px-2 py-1 rounded">target="_blank"</code> - 새 탭에서 열기</li>
                  <li><code className="bg-muted px-2 py-1 rounded">href="#id"</code> - 페이지 내 이동</li>
                  <li><code className="bg-muted px-2 py-1 rounded">href="mailto:email"</code> - 이메일 링크</li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="media" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">미디어 태그</h3>
                <ul className="space-y-2 text-sm">
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;img src="URL" alt="설명"&gt;</code> - 이미지</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;video&gt;</code> - 비디오</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;audio&gt;</code> - 오디오</li>
                  <li><code className="bg-muted px-2 py-1 rounded">&lt;iframe&gt;</code> - 외부 페이지 삽입</li>
                </ul>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
