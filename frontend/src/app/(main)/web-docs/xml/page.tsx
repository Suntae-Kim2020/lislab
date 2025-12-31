'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Code, Eye, BookOpen, GitCompare } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

const DEFAULT_XML = `<?xml version="1.0" encoding="UTF-8"?>
<bookstore>
    <book category="web">
        <title lang="ko">XML 기초 학습</title>
        <author>홍길동</author>
        <year>2024</year>
        <price>25000</price>
    </book>
    <book category="programming">
        <title lang="en">Learning Python</title>
        <author>김철수</author>
        <year>2023</year>
        <price>30000</price>
    </book>
</bookstore>`;

const XML_EXAMPLES = [
  {
    title: '기본 구조',
    description: 'XML 문서의 기본 구조',
    code: `<?xml version="1.0" encoding="UTF-8"?>
<root>
    <message>안녕하세요, XML!</message>
</root>`
  },
  {
    title: '속성 사용',
    description: '요소에 속성 추가하기',
    code: `<?xml version="1.0" encoding="UTF-8"?>
<students>
    <student id="1001" grade="A">
        <name>홍길동</name>
        <age>20</age>
    </student>
    <student id="1002" grade="B">
        <name>김철수</name>
        <age>21</age>
    </student>
</students>`
  },
  {
    title: '계층 구조',
    description: '중첩된 요소로 계층 표현',
    code: `<?xml version="1.0" encoding="UTF-8"?>
<company>
    <department name="개발팀">
        <team name="프론트엔드">
            <member>
                <name>홍길동</name>
                <position>팀장</position>
            </member>
            <member>
                <name>김철수</name>
                <position>개발자</position>
            </member>
        </team>
        <team name="백엔드">
            <member>
                <name>이영희</name>
                <position>팀장</position>
            </member>
        </team>
    </department>
</company>`
  },
  {
    title: 'CDATA 섹션',
    description: '특수문자 포함하기',
    code: `<?xml version="1.0" encoding="UTF-8"?>
<code-examples>
    <example language="javascript">
        <![CDATA[
        function hello() {
            if (x < 10 && y > 5) {
                console.log("Hello!");
            }
        }
        ]]>
    </example>
</code-examples>`
  },
  {
    title: '주석',
    description: 'XML 주석 사용하기',
    code: `<?xml version="1.0" encoding="UTF-8"?>
<!-- 이것은 루트 요소입니다 -->
<catalog>
    <!-- 상품 목록 -->
    <product id="p001">
        <name>노트북</name>
        <!-- 가격은 원화 기준 -->
        <price currency="KRW">1500000</price>
    </product>
</catalog>`
  }
];

export default function XMLLearningPage() {
  const [xmlCode, setXmlCode] = useState(DEFAULT_XML);

  const handleValidate = () => {
    try {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlCode, 'text/xml');
      const parseError = xmlDoc.querySelector('parsererror');

      if (parseError) {
        alert('❌ XML 오류:\n\n' + parseError.textContent);
      } else {
        const previewWindow = window.open('', '_blank', 'width=800,height=600');
        if (previewWindow) {
          const formattedXml = xmlCode
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

          previewWindow.document.write(`
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <title>XML 미리보기</title>
                <style>
                    body {
                        font-family: monospace;
                        padding: 20px;
                        background: #f5f5f5;
                    }
                    pre {
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        overflow-x: auto;
                    }
                    .success {
                        color: green;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }
                </style>
            </head>
            <body>
                <div class="success">✓ 유효한 XML 문서입니다!</div>
                <pre>${formattedXml}</pre>
            </body>
            </html>
          `);
          previewWindow.document.close();
        }
      }
    } catch (error) {
      alert('XML 파싱 오류: ' + (error as Error).message);
    }
  };

  const loadExample = (code: string) => {
    setXmlCode(code);
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-2">XML 기초 학습</h1>
        <p className="text-muted-foreground">
          eXtensible Markup Language - 확장 가능한 마크업 언어
        </p>
      </div>

      {/* HTML vs XML Comparison */}
      <Card className="mb-6 border-primary">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <GitCompare className="h-5 w-5" />
            HTML vs XML - 주요 차이점
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <Badge>HTML</Badge>
                문서 표시용
              </h3>
              <ul className="space-y-2 text-sm">
                <li>✓ 웹 페이지를 <strong>표시</strong>하기 위한 언어</li>
                <li>✓ 미리 정의된 태그만 사용 (h1, p, div 등)</li>
                <li>✓ 태그를 닫지 않아도 되는 경우 있음</li>
                <li>✓ 대소문자 구분 안 함</li>
                <li>✓ 속성값에 따옴표 생략 가능</li>
                <li>✓ 주 목적: 데이터 표시 및 스타일링</li>
              </ul>
              <div className="mt-3 p-3 bg-muted rounded text-xs">
                <code>
                  &lt;h1&gt;제목&lt;/h1&gt;<br/>
                  &lt;img src=image.jpg&gt;<br/>
                  &lt;BR&gt;
                </code>
              </div>
            </div>
            <div>
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <Badge variant="secondary">XML</Badge>
                데이터 저장/전송용
              </h3>
              <ul className="space-y-2 text-sm">
                <li>✓ 데이터를 <strong>저장하고 전송</strong>하기 위한 언어</li>
                <li>✓ 사용자가 태그를 정의할 수 있음</li>
                <li>✓ 모든 태그를 반드시 닫아야 함</li>
                <li>✓ 대소문자 엄격하게 구분</li>
                <li>✓ 속성값에 반드시 따옴표 사용</li>
                <li>✓ 주 목적: 데이터 구조화 및 교환</li>
              </ul>
              <div className="mt-3 p-3 bg-muted rounded text-xs">
                <code>
                  &lt;title&gt;제목&lt;/title&gt;<br/>
                  &lt;image src="image.jpg"/&gt;<br/>
                  &lt;linebreak/&gt;
                </code>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* XML Editor */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Code className="h-5 w-5" />
                    XML 에디터
                  </CardTitle>
                  <CardDescription>아래에 XML 코드를 입력하세요</CardDescription>
                </div>
                <Button onClick={handleValidate} className="gap-2">
                  <Eye className="h-4 w-4" />
                  검증 및 미리보기
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <Textarea
                value={xmlCode}
                onChange={(e) => setXmlCode(e.target.value)}
                className="font-mono text-sm min-h-[500px]"
                placeholder="XML 코드를 입력하세요..."
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
                {XML_EXAMPLES.map((example, index) => (
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
          <CardTitle>XML 핵심 개념</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="rules">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="rules">기본 규칙</TabsTrigger>
              <TabsTrigger value="structure">구조</TabsTrigger>
              <TabsTrigger value="attributes">속성</TabsTrigger>
              <TabsTrigger value="special">특수 문자</TabsTrigger>
              <TabsTrigger value="usage">활용</TabsTrigger>
            </TabsList>

            <TabsContent value="rules" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">XML 작성 규칙</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <strong>1. XML 선언:</strong> 문서 시작에 <code className="bg-muted px-2 py-1 rounded">&lt;?xml version="1.0" encoding="UTF-8"?&gt;</code>
                  </li>
                  <li>
                    <strong>2. 루트 요소:</strong> 반드시 하나의 루트 요소만 존재
                  </li>
                  <li>
                    <strong>3. 닫는 태그 필수:</strong> 모든 태그는 반드시 닫아야 함 <code className="bg-muted px-2 py-1 rounded">&lt;tag&gt;&lt;/tag&gt;</code> 또는 <code className="bg-muted px-2 py-1 rounded">&lt;tag/&gt;</code>
                  </li>
                  <li>
                    <strong>4. 대소문자 구분:</strong> <code className="bg-muted px-2 py-1 rounded">&lt;Name&gt;</code>과 <code className="bg-muted px-2 py-1 rounded">&lt;name&gt;</code>은 다른 태그
                  </li>
                  <li>
                    <strong>5. 올바른 중첩:</strong> 태그는 올바르게 중첩되어야 함
                  </li>
                  <li>
                    <strong>6. 속성값 따옴표:</strong> 속성값은 반드시 따옴표로 감싸야 함
                  </li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="structure" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">XML 문서 구조</h3>
                <div className="bg-muted p-4 rounded text-sm font-mono">
                  <div className="text-green-600">&lt;?xml version="1.0" encoding="UTF-8"?&gt;</div>
                  <div className="text-blue-600 mt-2">&lt;!-- 주석: 이것은 루트 요소입니다 --&gt;</div>
                  <div className="mt-2">&lt;root&gt;</div>
                  <div className="ml-4">&lt;child attribute="value"&gt;</div>
                  <div className="ml-8">텍스트 내용</div>
                  <div className="ml-4">&lt;/child&gt;</div>
                  <div>&lt;/root&gt;</div>
                </div>
                <ul className="space-y-2 text-sm mt-4">
                  <li><strong>프롤로그:</strong> XML 선언 및 DTD</li>
                  <li><strong>루트 요소:</strong> 문서의 최상위 요소</li>
                  <li><strong>자식 요소:</strong> 중첩된 요소들</li>
                  <li><strong>텍스트:</strong> 요소 사이의 데이터</li>
                  <li><strong>속성:</strong> 요소에 대한 추가 정보</li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="attributes" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">속성 사용하기</h3>
                <p className="text-sm mb-3">속성은 요소에 대한 메타데이터를 제공합니다.</p>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm font-medium mb-1">✓ 올바른 예:</p>
                    <code className="bg-green-50 text-green-800 px-3 py-2 rounded block text-sm">
                      &lt;person age="25" gender="male"&gt;홍길동&lt;/person&gt;
                    </code>
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-1">✗ 잘못된 예:</p>
                    <code className="bg-red-50 text-red-800 px-3 py-2 rounded block text-sm">
                      &lt;person age=25 gender=male&gt;홍길동&lt;/person&gt;
                    </code>
                  </div>
                  <div className="bg-blue-50 p-3 rounded text-sm">
                    <strong>팁:</strong> 속성 vs 요소 선택<br/>
                    - 메타데이터는 속성으로 (id, type, category)<br/>
                    - 실제 데이터는 요소로 (name, description, content)
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="special" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">특수 문자 처리</h3>
                <p className="text-sm mb-3">XML에서 특별한 의미를 가진 문자들은 엔티티로 표현해야 합니다.</p>
                <table className="w-full text-sm border">
                  <thead className="bg-muted">
                    <tr>
                      <th className="p-2 text-left border">문자</th>
                      <th className="p-2 text-left border">엔티티</th>
                      <th className="p-2 text-left border">설명</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="p-2 border font-mono">&lt;</td>
                      <td className="p-2 border font-mono">&amp;lt;</td>
                      <td className="p-2 border">Less than</td>
                    </tr>
                    <tr>
                      <td className="p-2 border font-mono">&gt;</td>
                      <td className="p-2 border font-mono">&amp;gt;</td>
                      <td className="p-2 border">Greater than</td>
                    </tr>
                    <tr>
                      <td className="p-2 border font-mono">&amp;</td>
                      <td className="p-2 border font-mono">&amp;amp;</td>
                      <td className="p-2 border">Ampersand</td>
                    </tr>
                    <tr>
                      <td className="p-2 border font-mono">"</td>
                      <td className="p-2 border font-mono">&amp;quot;</td>
                      <td className="p-2 border">Quotation mark</td>
                    </tr>
                    <tr>
                      <td className="p-2 border font-mono">'</td>
                      <td className="p-2 border font-mono">&amp;apos;</td>
                      <td className="p-2 border">Apostrophe</td>
                    </tr>
                  </tbody>
                </table>
                <div className="mt-3 bg-muted p-3 rounded text-sm">
                  <strong>CDATA 섹션:</strong> 특수 문자가 많을 때는 CDATA 사용<br/>
                  <code className="mt-2 block">&lt;![CDATA[if (x &lt; 10 &amp;&amp; y &gt; 5) &#123; ... &#125;]]&gt;</code>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="usage" className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">XML 활용 분야</h3>
                <div className="grid md:grid-cols-2 gap-4 text-sm">
                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base">웹 서비스</CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm">
                      <ul className="space-y-1">
                        <li>• SOAP 프로토콜</li>
                        <li>• RSS 피드</li>
                        <li>• Sitemap</li>
                        <li>• AJAX 데이터 교환</li>
                      </ul>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base">설정 파일</CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm">
                      <ul className="space-y-1">
                        <li>• Android 레이아웃</li>
                        <li>• Maven pom.xml</li>
                        <li>• Spring config</li>
                        <li>• 애플리케이션 설정</li>
                      </ul>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base">문서 포맷</CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm">
                      <ul className="space-y-1">
                        <li>• Microsoft Office (docx, xlsx)</li>
                        <li>• SVG 이미지</li>
                        <li>• XHTML</li>
                        <li>• ePub 전자책</li>
                      </ul>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base">데이터 교환</CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm">
                      <ul className="space-y-1">
                        <li>• B2B 데이터 교환</li>
                        <li>• 금융 거래 (FpML)</li>
                        <li>• 의료 정보 (HL7)</li>
                        <li>• EDI 시스템</li>
                      </ul>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
