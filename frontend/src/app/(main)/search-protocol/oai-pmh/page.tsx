'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Database, Search, Download, Network, BookOpen, ExternalLink } from 'lucide-react';

const OAI_VERBS = [
  {
    verb: 'Identify',
    description: '저장소 정보 조회',
    params: '없음',
    example: 'verb=Identify',
    response: '저장소 이름, 관리자 이메일, 프로토콜 버전 등'
  },
  {
    verb: 'ListMetadataFormats',
    description: '지원하는 메타데이터 형식 목록',
    params: 'identifier (선택)',
    example: 'verb=ListMetadataFormats',
    response: 'oai_dc, mods, marc21 등의 형식 목록'
  },
  {
    verb: 'ListSets',
    description: '저장소의 세트(컬렉션) 목록',
    params: 'resumptionToken (선택)',
    example: 'verb=ListSets',
    response: '세트 이름과 설명 목록'
  },
  {
    verb: 'ListIdentifiers',
    description: '레코드 식별자 목록만 조회',
    params: 'metadataPrefix (필수), from, until, set',
    example: 'verb=ListIdentifiers&metadataPrefix=oai_dc',
    response: '레코드 식별자와 타임스탬프 목록'
  },
  {
    verb: 'ListRecords',
    description: '전체 메타데이터 레코드 조회',
    params: 'metadataPrefix (필수), from, until, set',
    example: 'verb=ListRecords&metadataPrefix=oai_dc&from=2024-01-01',
    response: '완전한 메타데이터 레코드 목록'
  },
  {
    verb: 'GetRecord',
    description: '특정 레코드 하나만 조회',
    params: 'identifier (필수), metadataPrefix (필수)',
    example: 'verb=GetRecord&identifier=oai:example:123&metadataPrefix=oai_dc',
    response: '지정한 레코드의 완전한 메타데이터'
  }
];

const METADATA_FORMATS = [
  {
    name: 'oai_dc',
    fullName: 'Dublin Core',
    description: 'OAI-PMH의 기본 메타데이터 형식',
    elements: 'title, creator, subject, description, publisher, contributor, date, type, format, identifier, source, language, relation, coverage, rights',
    usage: '가장 보편적으로 사용되는 간단한 형식'
  },
  {
    name: 'mods',
    fullName: 'Metadata Object Description Schema',
    description: '더 상세한 서지 정보를 표현',
    elements: 'titleInfo, name, typeOfResource, genre, originInfo, language, physicalDescription, abstract, subject, classification 등',
    usage: '도서관, 박물관 등에서 상세한 메타데이터 필요 시'
  },
  {
    name: 'marc21',
    fullName: 'MARC 21',
    description: '도서관 표준 서지 형식',
    elements: '숫자 태그 기반 (001-999), 각 필드는 특정 서지 정보',
    usage: '전통적인 도서관 시스템과의 호환성'
  },
  {
    name: 'etd_ms',
    fullName: 'Electronic Theses and Dissertations',
    description: '학위논문 전용 메타데이터',
    elements: 'degree, discipline, grantor, advisor 등 학위논문 특화 요소',
    usage: '학위논문 저장소'
  }
];

export default function OAIPMHPage() {
  const [baseUrl, setBaseUrl] = useState('http://export.arxiv.org/oai2');
  const [selectedVerb, setSelectedVerb] = useState('Identify');
  const [identifier, setIdentifier] = useState('');
  const [metadataPrefix, setMetadataPrefix] = useState('oai_dc');

  const buildUrl = () => {
    let url = `${baseUrl}?verb=${selectedVerb}`;

    if (selectedVerb === 'GetRecord') {
      if (identifier) url += `&identifier=${identifier}`;
      url += `&metadataPrefix=${metadataPrefix}`;
    } else if (selectedVerb === 'ListRecords' || selectedVerb === 'ListIdentifiers') {
      url += `&metadataPrefix=${metadataPrefix}`;
    }

    return url;
  };

  const handleTest = () => {
    const url = buildUrl();
    window.open(url, '_blank');
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-2">OAI-PMH 프로토콜</h1>
        <p className="text-muted-foreground">
          Open Archives Initiative Protocol for Metadata Harvesting
        </p>
      </div>

      {/* Introduction */}
      <Card className="mb-6 border-primary">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5" />
            OAI-PMH란?
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-sm">
              <strong>OAI-PMH</strong>는 디지털 저장소(리포지토리)에서 메타데이터를 수집(하베스팅)하기 위한
              표준 프로토콜입니다. 2001년에 개발되어 현재 전 세계 도서관, 박물관, 학술 저장소에서
              널리 사용되고 있습니다.
            </p>

            <div className="grid md:grid-cols-3 gap-4 mt-4">
              <Card>
                <CardHeader className="pb-3">
                  <Database className="h-8 w-8 text-primary mb-2" />
                  <CardTitle className="text-base">데이터 제공자</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  메타데이터를 보유하고 OAI-PMH를 통해 공개하는 저장소
                  <div className="mt-2 text-xs text-muted-foreground">
                    예: 대학 도서관, 박물관, 학술 저장소
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <Search className="h-8 w-8 text-primary mb-2" />
                  <CardTitle className="text-base">서비스 제공자</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  여러 저장소로부터 메타데이터를 수집하여 통합 검색 서비스 제공
                  <div className="mt-2 text-xs text-muted-foreground">
                    예: 통합 검색 포털, 디지털 도서관 연합
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <Network className="h-8 w-8 text-primary mb-2" />
                  <CardTitle className="text-base">HTTP 기반</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  간단한 HTTP GET/POST 요청으로 메타데이터 교환
                  <div className="mt-2 text-xs text-muted-foreground">
                    XML 형식으로 응답 반환
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Interactive Test Tool */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ExternalLink className="h-5 w-5" />
            OAI-PMH 요청 테스트
          </CardTitle>
          <CardDescription>실제 저장소에 요청을 보내보세요</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Base URL</label>
              <Input
                value={baseUrl}
                onChange={(e) => setBaseUrl(e.target.value)}
                placeholder="http://example.org/oai"
              />
              <p className="text-xs text-muted-foreground mt-1">
                예시: http://export.arxiv.org/oai2 (arXiv 저장소)
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Verb (요청 유형)</label>
                <select
                  className="w-full p-2 border rounded"
                  value={selectedVerb}
                  onChange={(e) => setSelectedVerb(e.target.value)}
                >
                  {OAI_VERBS.map((v) => (
                    <option key={v.verb} value={v.verb}>
                      {v.verb} - {v.description}
                    </option>
                  ))}
                </select>
              </div>

              {(selectedVerb === 'GetRecord' || selectedVerb === 'ListRecords' || selectedVerb === 'ListIdentifiers') && (
                <div>
                  <label className="text-sm font-medium mb-2 block">Metadata Prefix</label>
                  <select
                    className="w-full p-2 border rounded"
                    value={metadataPrefix}
                    onChange={(e) => setMetadataPrefix(e.target.value)}
                  >
                    <option value="oai_dc">oai_dc (Dublin Core)</option>
                    <option value="mods">mods</option>
                    <option value="marc21">marc21</option>
                  </select>
                </div>
              )}

              {selectedVerb === 'GetRecord' && (
                <div>
                  <label className="text-sm font-medium mb-2 block">Identifier</label>
                  <Input
                    value={identifier}
                    onChange={(e) => setIdentifier(e.target.value)}
                    placeholder="oai:arXiv.org:cs/0001001"
                  />
                </div>
              )}
            </div>

            <div className="bg-muted p-3 rounded">
              <p className="text-sm font-medium mb-1">생성된 URL:</p>
              <code className="text-xs break-all">{buildUrl()}</code>
            </div>

            <Button onClick={handleTest} className="w-full gap-2">
              <ExternalLink className="h-4 w-4" />
              새 창에서 요청 보내기
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* OAI-PMH Verbs */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>6가지 OAI-PMH Verb (요청)</CardTitle>
          <CardDescription>OAI-PMH 프로토콜의 모든 요청은 이 6가지 verb 중 하나를 사용합니다</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {OAI_VERBS.map((verb, index) => (
              <Card key={index} className="border-l-4 border-l-primary">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-base">
                        <Badge className="mr-2">{verb.verb}</Badge>
                        {verb.description}
                      </CardTitle>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="text-sm space-y-2">
                  <div>
                    <strong>매개변수:</strong> {verb.params}
                  </div>
                  <div>
                    <strong>예시:</strong>
                    <code className="block mt-1 bg-muted p-2 rounded text-xs">
                      ?{verb.example}
                    </code>
                  </div>
                  <div>
                    <strong>응답:</strong> {verb.response}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Detailed Guide */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>OAI-PMH 상세 가이드</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="metadata">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="metadata">메타데이터 형식</TabsTrigger>
              <TabsTrigger value="workflow">작동 원리</TabsTrigger>
              <TabsTrigger value="examples">활용 사례</TabsTrigger>
              <TabsTrigger value="response">응답 구조</TabsTrigger>
            </TabsList>

            <TabsContent value="metadata" className="space-y-4">
              <h3 className="font-semibold">주요 메타데이터 형식</h3>
              <div className="space-y-3">
                {METADATA_FORMATS.map((format, index) => (
                  <Card key={index}>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base flex items-center gap-2">
                        <Badge variant="outline">{format.name}</Badge>
                        {format.fullName}
                      </CardTitle>
                      <CardDescription>{format.description}</CardDescription>
                    </CardHeader>
                    <CardContent className="text-sm space-y-2">
                      <div>
                        <strong>주요 요소:</strong>
                        <p className="text-xs text-muted-foreground mt-1">{format.elements}</p>
                      </div>
                      <div>
                        <strong>사용처:</strong> {format.usage}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="workflow" className="space-y-4">
              <h3 className="font-semibold mb-3">메타데이터 하베스팅 프로세스</h3>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <Badge className="mt-1">1</Badge>
                  <div>
                    <h4 className="font-medium">저장소 확인 (Identify)</h4>
                    <p className="text-sm text-muted-foreground">
                      먼저 Identify 요청으로 저장소 정보를 확인합니다.
                    </p>
                    <code className="text-xs bg-muted p-2 rounded block mt-2">
                      GET http://repository.org/oai?verb=Identify
                    </code>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Badge className="mt-1">2</Badge>
                  <div>
                    <h4 className="font-medium">지원 형식 확인 (ListMetadataFormats)</h4>
                    <p className="text-sm text-muted-foreground">
                      어떤 메타데이터 형식을 지원하는지 확인합니다.
                    </p>
                    <code className="text-xs bg-muted p-2 rounded block mt-2">
                      GET http://repository.org/oai?verb=ListMetadataFormats
                    </code>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Badge className="mt-1">3</Badge>
                  <div>
                    <h4 className="font-medium">세트 확인 (ListSets) - 선택사항</h4>
                    <p className="text-sm text-muted-foreground">
                      필요시 특정 컬렉션만 수집하기 위해 세트 목록을 확인합니다.
                    </p>
                    <code className="text-xs bg-muted p-2 rounded block mt-2">
                      GET http://repository.org/oai?verb=ListSets
                    </code>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Badge className="mt-1">4</Badge>
                  <div>
                    <h4 className="font-medium">메타데이터 수집 (ListRecords)</h4>
                    <p className="text-sm text-muted-foreground">
                      실제 메타데이터 레코드를 수집합니다. 날짜 범위 지정 가능.
                    </p>
                    <code className="text-xs bg-muted p-2 rounded block mt-2">
                      GET http://repository.org/oai?verb=ListRecords&metadataPrefix=oai_dc&from=2024-01-01
                    </code>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Badge className="mt-1">5</Badge>
                  <div>
                    <h4 className="font-medium">증분 수집 (Resumption Token)</h4>
                    <p className="text-sm text-muted-foreground">
                      응답에 resumptionToken이 있으면 계속해서 다음 페이지를 가져옵니다.
                    </p>
                    <code className="text-xs bg-muted p-2 rounded block mt-2">
                      GET http://repository.org/oai?verb=ListRecords&resumptionToken=xyz123
                    </code>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="examples" className="space-y-4">
              <h3 className="font-semibold mb-3">OAI-PMH 활용 사례</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">학술 저장소 연합</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm">
                    <p className="mb-2">여러 대학의 학위논문 저장소를 통합하여 하나의 검색 포털 제공</p>
                    <ul className="space-y-1 text-xs text-muted-foreground">
                      <li>• 국내: RISS, NDSL</li>
                      <li>• 해외: NDLTD, BASE</li>
                      <li>• 각 대학이 데이터 제공자</li>
                      <li>• 통합 포털이 서비스 제공자</li>
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">디지털 도서관</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm">
                    <p className="mb-2">공공 도서관의 디지털 자료를 통합 검색</p>
                    <ul className="space-y-1 text-xs text-muted-foreground">
                      <li>• 국립중앙도서관</li>
                      <li>• 지역 도서관 연합</li>
                      <li>• 전자책, 고문서 등</li>
                      <li>• 통합 목록 제공</li>
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">문화유산 포털</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm">
                    <p className="mb-2">박물관, 미술관의 소장품 정보 통합</p>
                    <ul className="space-y-1 text-xs text-muted-foreground">
                      <li>• 국립중앙박물관</li>
                      <li>• 각 지역 박물관</li>
                      <li>• Europeana (유럽)</li>
                      <li>• DPLA (미국)</li>
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">오픈 액세스 저장소</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm">
                    <p className="mb-2">연구 논문의 오픈 액세스 제공</p>
                    <ul className="space-y-1 text-xs text-muted-foreground">
                      <li>• arXiv (물리학, 수학)</li>
                      <li>• PubMed Central (의학)</li>
                      <li>• RePEc (경제학)</li>
                      <li>• 기관 리포지토리</li>
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="response" className="space-y-4">
              <h3 className="font-semibold mb-3">OAI-PMH XML 응답 구조</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-sm mb-2">Identify 응답 예시</h4>
                  <pre className="bg-muted p-4 rounded text-xs overflow-x-auto">
{`<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
  <responseDate>2024-12-28T10:00:00Z</responseDate>
  <request verb="Identify">http://example.org/oai</request>
  <Identify>
    <repositoryName>Example Digital Library</repositoryName>
    <baseURL>http://example.org/oai</baseURL>
    <protocolVersion>2.0</protocolVersion>
    <adminEmail>admin@example.org</adminEmail>
    <earliestDatestamp>2020-01-01</earliestDatestamp>
    <deletedRecord>transient</deletedRecord>
    <granularity>YYYY-MM-DD</granularity>
  </Identify>
</OAI-PMH>`}
                  </pre>
                </div>

                <div>
                  <h4 className="font-medium text-sm mb-2">GetRecord 응답 예시 (Dublin Core)</h4>
                  <pre className="bg-muted p-4 rounded text-xs overflow-x-auto">
{`<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
  <responseDate>2024-12-28T10:00:00Z</responseDate>
  <request verb="GetRecord"
           identifier="oai:example:123"
           metadataPrefix="oai_dc">
    http://example.org/oai
  </request>
  <GetRecord>
    <record>
      <header>
        <identifier>oai:example:123</identifier>
        <datestamp>2024-01-15</datestamp>
        <setSpec>computer_science</setSpec>
      </header>
      <metadata>
        <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                   xmlns:dc="http://purl.org/dc/elements/1.1/">
          <dc:title>인공지능 기초 연구</dc:title>
          <dc:creator>홍길동</dc:creator>
          <dc:subject>인공지능</dc:subject>
          <dc:subject>기계학습</dc:subject>
          <dc:description>인공지능의 기초 개념을 다룬 연구</dc:description>
          <dc:publisher>한국대학교</dc:publisher>
          <dc:date>2024-01-15</dc:date>
          <dc:type>학위논문</dc:type>
          <dc:identifier>http://example.org/papers/123</dc:identifier>
          <dc:language>kor</dc:language>
          <dc:rights>CC BY 4.0</dc:rights>
        </oai_dc:dc>
      </metadata>
    </record>
  </GetRecord>
</OAI-PMH>`}
                  </pre>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Key Concepts */}
      <Card>
        <CardHeader>
          <CardTitle>핵심 개념 정리</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div>
              <h4 className="font-semibold mb-2">✓ 장점</h4>
              <ul className="space-y-1 text-muted-foreground">
                <li>• 간단한 HTTP 기반 프로토콜</li>
                <li>• 표준화된 메타데이터 형식</li>
                <li>• 증분 하베스팅 지원</li>
                <li>• 전 세계적으로 널리 사용</li>
                <li>• 낮은 진입 장벽</li>
                <li>• 오픈소스 도구 풍부</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-2">⚠ 제약사항</h4>
              <ul className="space-y-1 text-muted-foreground">
                <li>• 메타데이터만 교환 (원문 아님)</li>
                <li>• 단방향 통신 (Pull 방식)</li>
                <li>• 복잡한 검색 기능 없음</li>
                <li>• 실시간 동기화 어려움</li>
                <li>• 보안 기능 제한적</li>
                <li>• 대용량 처리 시 성능 이슈</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
