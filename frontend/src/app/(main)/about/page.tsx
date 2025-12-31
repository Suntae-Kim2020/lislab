import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { BookOpen, Heart, GraduationCap, Users, Cloud, DollarSign, FileText, Mail } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="container mx-auto py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">LIS Lab 소개</h1>
          <p className="text-xl text-muted-foreground">
            Library & Information Science Learning Platform
          </p>
          <p className="text-lg text-muted-foreground mt-2">
            문헌정보학 교육의 새로운 패러다임
          </p>
        </div>

        {/* 운영자 소개 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <GraduationCap className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">운영자 소개</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h3 className="text-lg font-semibold">김선태 교수</h3>
              <p className="text-muted-foreground">전북대학교 문헌정보학과</p>
            </div>
            <Separator />
            <p className="leading-relaxed">
              문헌정보학을 순수하게 공부하는 학생들에게 더 나은 교육 환경을 제공하고자
              LIS Lab을 설립하였습니다. 실무와 이론을 결합한 실용적인 교육 콘텐츠를 통해
              차세대 문헌정보학 전문가 양성에 기여하고자 합니다.
            </p>
          </CardContent>
        </Card>

        {/* 서비스 목적 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <BookOpen className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">서비스 목적</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed">
              LIS Lab은 문헌정보학을 공부하는 학생들을 위한 교육 콘텐츠 제작 및 공유 플랫폼입니다.
              전통적인 도서관학부터 최신 정보기술까지, 문헌정보학의 모든 분야를 아우르는
              양질의 교육 자료를 제공합니다.
            </p>

            <div className="bg-muted p-4 rounded-lg space-y-3">
              <h4 className="font-semibold flex items-center gap-2">
                <FileText className="h-4 w-4" />
                주요 서비스 내용
              </h4>
              <ul className="space-y-2 ml-6">
                <li className="list-disc">
                  <strong>체계적인 교육 콘텐츠:</strong> 초급부터 고급까지 단계별 학습 자료 제공
                </li>
                <li className="list-disc">
                  <strong>실습 중심 학습:</strong> 이론과 실무를 결합한 실용적 콘텐츠
                </li>
                <li className="list-disc">
                  <strong>맞춤형 콘텐츠 제작:</strong> 학습자의 요청에 따른 콘텐츠 제작 및 공유
                </li>
                <li className="list-disc">
                  <strong>커뮤니티 운영:</strong> 질의응답 및 학습자 간 소통 공간 제공
                </li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* 콘텐츠 제작 요청 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Users className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">콘텐츠 제작 요청</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed">
              학습 과정에서 필요한 주제나 깊이 있는 설명이 필요한 내용이 있다면
              언제든지 콘텐츠 제작을 요청하실 수 있습니다.
            </p>

            <div className="bg-blue-50 dark:bg-blue-950 p-4 rounded-lg space-y-2">
              <h4 className="font-semibold">요청 방법</h4>
              <ol className="space-y-2 ml-6">
                <li className="list-decimal">
                  게시판 → "콘텐츠 개발 요청" 게시판 이용
                </li>
                <li className="list-decimal">
                  필요한 주제와 상세 내용 작성
                </li>
                <li className="list-decimal">
                  검토 후 우선순위에 따라 콘텐츠 제작 및 공유
                </li>
              </ol>
            </div>
          </CardContent>
        </Card>

        {/* 이용 조건 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">이용 조건</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 flex-shrink-0 mt-1">
                  ✓
                </div>
                <div>
                  <h4 className="font-semibold text-green-700 dark:text-green-300 mb-1">
                    학습 목적 사용 (무료)
                  </h4>
                  <p className="text-sm text-muted-foreground">
                    모든 교육 콘텐츠는 개인 학습, 연구, 교육 목적으로 자유롭게 이용하실 수 있습니다.
                    학생, 연구자, 교육자 누구나 무료로 접근하고 활용할 수 있습니다.
                  </p>
                </div>
              </div>

              <Separator />

              <div className="flex items-start gap-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 flex-shrink-0 mt-1">
                  ✕
                </div>
                <div>
                  <h4 className="font-semibold text-red-700 dark:text-red-300 mb-1">
                    상업적 이용 금지
                  </h4>
                  <p className="text-sm text-muted-foreground">
                    본 플랫폼의 모든 콘텐츠는 상업적 목적으로 사용할 수 없습니다.
                    영리 활동, 유료 교육 서비스, 출판물 제작 등에 활용하는 것은 엄격히 금지됩니다.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-amber-50 dark:bg-amber-950 p-4 rounded-lg mt-4">
              <p className="text-sm">
                <strong>※ 주의사항:</strong> 콘텐츠의 저작권은 LIS Lab 및 콘텐츠 제작자에게 있으며,
                무단 복제 및 상업적 이용 시 법적 조치가 취해질 수 있습니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 운영 환경 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Cloud className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">운영 환경 및 철학</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div>
                <h4 className="font-semibold mb-2">클라우드 기반 서비스</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  LIS Lab은 최신 클라우드 인프라를 활용하여 안정적이고 확장 가능한 서비스를 제공합니다.
                  언제 어디서나 접속 가능한 학습 환경을 구축하고 있습니다.
                </p>
              </div>

              <Separator />

              <div>
                <h4 className="font-semibold mb-2">비영리 교육 플랫폼</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  본 서비스는 <strong className="text-foreground">수익 창출을 목적으로 하지 않습니다</strong>.
                  순수하게 문헌정보학 교육의 질을 높이고, 학습자들에게 더 나은 학습 기회를 제공하기 위해
                  운영되는 비영리 교육 플랫폼입니다.
                </p>
              </div>

              <Separator />

              <div>
                <h4 className="font-semibold mb-2">지속 가능한 운영 모델</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  서비스의 지속적인 발전과 안정적인 운영을 위해 다양한 노력을 기울이고 있습니다.
                  기술적 혁신과 효율적인 자원 관리를 통해 최소한의 비용으로 최대한의 교육 효과를
                  창출하고자 합니다.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 후원 안내 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Heart className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">후원 안내</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed">
              LIS Lab은 문헌정보학 교육 발전을 위해 기업 및 개인의 후원을 받고 있습니다.
              여러분의 소중한 후원은 더 나은 교육 환경을 만드는 데 큰 힘이 됩니다.
            </p>

            <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-950 dark:to-purple-950 p-6 rounded-lg space-y-4">
              <h4 className="font-semibold text-lg flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                후원금 사용 내역
              </h4>

              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">1️⃣</span>
                  <div>
                    <h5 className="font-semibold">서비스 운영비</h5>
                    <p className="text-sm text-muted-foreground">
                      클라우드 인프라, 도메인, SSL 인증서 등 서비스 운영에 필요한 기술적 비용
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-2xl">2️⃣</span>
                  <div>
                    <h5 className="font-semibold">콘텐츠 제작비</h5>
                    <p className="text-sm text-muted-foreground">
                      양질의 교육 콘텐츠 제작, 실습 환경 구축, 자료 수집 및 정리
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-2xl">3️⃣</span>
                  <div>
                    <h5 className="font-semibold">교육 활동 지원</h5>
                    <p className="text-sm text-muted-foreground">
                      오프라인 워크샵, 세미나, 특강 등 문헌정보학 분야 교육 행사 개최 및 지원
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-2xl">4️⃣</span>
                  <div>
                    <h5 className="font-semibold">학습자 지원</h5>
                    <p className="text-sm text-muted-foreground">
                      학습 자료 제공, 실습 도구 지원, 학습 커뮤니티 운영
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <Separator />

            <div className="bg-green-50 dark:bg-green-950 p-4 rounded-lg">
              <h4 className="font-semibold mb-2 flex items-center gap-2">
                <FileText className="h-4 w-4" />
                투명한 재정 운영
              </h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                LIS Lab은 <strong className="text-foreground">모든 후원금과 지출 내역을 투명하게 공개</strong>합니다.
                후원금 수령 현황과 사용 내역을 정기적으로 업데이트하여 후원자 여러분께
                신뢰할 수 있는 운영 실태를 보고드릴 예정입니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 문의 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Mail className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">문의하기</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed">
              LIS Lab에 대한 문의사항이나 제안사항이 있으시면 언제든지 연락 주시기 바랍니다.
            </p>

            <div className="bg-muted p-4 rounded-lg space-y-2">
              <div className="flex items-center gap-2">
                <span className="font-semibold">이메일:</span>
                <a href="mailto:kim.suntae@jbnu.ac.kr" className="text-primary hover:underline">
                  kim.suntae@jbnu.ac.kr
                </a>
              </div>
              <div className="flex items-center gap-2">
                <span className="font-semibold">소속:</span>
                <span>전북대학교 문헌정보학과</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 푸터 메시지 */}
        <div className="text-center py-8 border-t">
          <p className="text-lg font-semibold mb-2">
            함께 만들어가는 문헌정보학 교육의 미래
          </p>
          <p className="text-muted-foreground">
            LIS Lab과 함께 성장하는 문헌정보학 전문가가 되어주세요.
          </p>
        </div>
      </div>
    </div>
  );
}
