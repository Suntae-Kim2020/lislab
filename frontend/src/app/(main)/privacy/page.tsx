import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Shield, Lock, Eye, UserCheck, FileText, Mail } from 'lucide-react';

export default function PrivacyPage() {
  return (
    <div className="container mx-auto py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">개인정보 처리방침</h1>
          <p className="text-lg text-muted-foreground">
            LIS Lab 개인정보 처리방침
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            시행일자: 2025년 1월 1일
          </p>
        </div>

        {/* 소개 */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <p className="leading-relaxed">
              LIS Lab(이하 "서비스")은 이용자의 개인정보를 중요시하며, 「개인정보 보호법」,
              「정보통신망 이용촉진 및 정보보호 등에 관한 법률」 등 관련 법령을 준수하고 있습니다.
              본 개인정보 처리방침은 서비스가 어떠한 정보를 수집하고, 수집한 정보를 어떻게 사용하며,
              필요에 따라 누구와 이를 공유하는지 알려드립니다.
            </p>
          </CardContent>
        </Card>

        {/* 1. 개인정보의 수집 항목 및 방법 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <UserCheck className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">1. 개인정보의 수집 항목 및 방법</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">회원가입 시 수집하는 정보</h4>
              <ul className="space-y-2 ml-6">
                <li className="list-disc">
                  <strong>필수 항목:</strong> 이메일, 비밀번호, 이름(성, 이름)
                </li>
                <li className="list-disc">
                  <strong>선택 항목:</strong> 전화번호, 소속기관, 회원구분(학생/연구자/교육자/실무자/기타), 자기소개
                </li>
              </ul>
            </div>

            <Separator />

            <div>
              <h4 className="font-semibold mb-2">서비스 이용 과정에서 자동 수집되는 정보</h4>
              <ul className="space-y-2 ml-6">
                <li className="list-disc">IP 주소</li>
                <li className="list-disc">쿠키 및 세션 정보</li>
                <li className="list-disc">서비스 이용 기록 (접속 로그, 콘텐츠 조회 기록, 댓글 작성 기록 등)</li>
                <li className="list-disc">기기 정보 (OS, 브라우저 종류 등)</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* 2. 개인정보의 수집 및 이용 목적 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">2. 개인정보의 수집 및 이용 목적</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <ul className="space-y-2 ml-6">
              <li className="list-disc">
                <strong>회원 관리:</strong> 본인 확인, 회원제 서비스 제공, 부정 이용 방지
              </li>
              <li className="list-disc">
                <strong>서비스 제공:</strong> 콘텐츠 열람, 댓글 작성, 즐겨찾기, 게시판 이용 등
              </li>
              <li className="list-disc">
                <strong>서비스 개선:</strong> 신규 서비스 개발, 맞춤형 콘텐츠 제공, 통계 분석
              </li>
              <li className="list-disc">
                <strong>소통:</strong> 공지사항 전달, 문의 응대, 교육 관련 안내
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* 3. 개인정보의 보유 및 이용 기간 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Eye className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">3. 개인정보의 보유 및 이용 기간</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed">
              서비스는 원칙적으로 개인정보 수집 및 이용 목적이 달성된 후에는 해당 정보를
              지체 없이 파기합니다. 단, 다음의 경우에는 명시한 기간 동안 보존합니다.
            </p>

            <div className="bg-muted p-4 rounded-lg space-y-3">
              <h4 className="font-semibold">회원 정보</h4>
              <ul className="space-y-2 ml-6">
                <li className="list-disc">
                  <strong>보유 기간:</strong> 회원 탈퇴 시까지
                </li>
                <li className="list-disc">
                  <strong>탈퇴 후:</strong> 즉시 파기 (단, 관련 법령에 따라 보존이 필요한 경우 예외)
                </li>
              </ul>
            </div>

            <div className="bg-blue-50 dark:bg-blue-950 p-4 rounded-lg space-y-2">
              <h4 className="font-semibold">관련 법령에 따른 보존</h4>
              <ul className="space-y-2 ml-6 text-sm">
                <li className="list-disc">
                  <strong>계약 또는 청약철회 등에 관한 기록:</strong> 5년 (전자상거래법)
                </li>
                <li className="list-disc">
                  <strong>소비자 불만 또는 분쟁처리 기록:</strong> 3년 (전자상거래법)
                </li>
                <li className="list-disc">
                  <strong>접속 로그 기록:</strong> 3개월 (통신비밀보호법)
                </li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* 4. 개인정보의 제3자 제공 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">4. 개인정보의 제3자 제공</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed">
              서비스는 <strong className="text-foreground">원칙적으로 이용자의 개인정보를 제3자에게 제공하지 않습니다</strong>.
              다만, 다음의 경우에는 예외로 합니다.
            </p>

            <ul className="space-y-2 ml-6 mt-4">
              <li className="list-disc">이용자가 사전에 동의한 경우</li>
              <li className="list-disc">법령의 규정에 의거하거나, 수사 목적으로 법령에 정해진 절차와 방법에 따라 수사기관의 요구가 있는 경우</li>
            </ul>
          </CardContent>
        </Card>

        {/* 5. 개인정보 처리의 위탁 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">5. 개인정보 처리의 위탁</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed mb-4">
              서비스는 원활한 서비스 제공을 위해 다음과 같이 개인정보 처리 업무를 외부에 위탁하고 있습니다.
            </p>

            <div className="bg-muted p-4 rounded-lg">
              <ul className="space-y-2">
                <li>
                  <strong>수탁업체:</strong> 클라우드 서비스 제공업체
                </li>
                <li>
                  <strong>위탁업무:</strong> 데이터 보관 및 관리
                </li>
              </ul>
            </div>

            <p className="text-sm text-muted-foreground mt-4">
              ※ 위탁업체가 변경될 경우, 변경된 내용을 본 처리방침을 통해 공지하겠습니다.
            </p>
          </CardContent>
        </Card>

        {/* 6. 정보주체의 권리와 행사 방법 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <UserCheck className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">6. 정보주체의 권리와 행사 방법</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed">
              이용자는 다음과 같은 권리를 행사할 수 있습니다.
            </p>

            <ul className="space-y-3 ml-6">
              <li className="list-disc">
                <strong>개인정보 열람 요구:</strong> 마이페이지에서 본인의 정보 확인
              </li>
              <li className="list-disc">
                <strong>개인정보 정정 요구:</strong> 마이페이지 &gt; 프로필 설정에서 직접 수정
              </li>
              <li className="list-disc">
                <strong>개인정보 삭제 요구:</strong> 회원 탈퇴를 통해 즉시 삭제
              </li>
              <li className="list-disc">
                <strong>개인정보 처리정지 요구:</strong> 개인정보 보호책임자에게 이메일로 요청
              </li>
            </ul>

            <div className="bg-amber-50 dark:bg-amber-950 p-4 rounded-lg mt-4">
              <p className="text-sm">
                <strong>※ 주의사항:</strong> 만 14세 미만 아동의 경우, 법정대리인의 동의가 필요하며,
                법정대리인은 아동의 개인정보에 대한 열람, 정정, 삭제, 처리정지를 요구할 수 있습니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 7. 개인정보의 파기 절차 및 방법 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Lock className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">7. 개인정보의 파기 절차 및 방법</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">파기 절차</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                이용자가 입력한 정보는 목적이 달성된 후 별도의 DB로 옮겨져(종이의 경우 별도의 서류함)
                내부 방침 및 기타 관련 법령에 의한 정보보호 사유에 따라 일정 기간 저장된 후 파기됩니다.
              </p>
            </div>

            <Separator />

            <div>
              <h4 className="font-semibold mb-2">파기 방법</h4>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">
                  <strong>전자적 파일:</strong> 기록을 재생할 수 없는 기술적 방법을 사용하여 삭제
                </li>
                <li className="list-disc">
                  <strong>종이 문서:</strong> 분쇄기로 분쇄하거나 소각
                </li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* 8. 개인정보 보호책임자 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Mail className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">8. 개인정보 보호책임자</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed">
              서비스는 개인정보 처리에 관한 업무를 총괄해서 책임지고,
              개인정보 처리와 관련한 정보주체의 불만처리 및 피해구제를 위하여
              아래와 같이 개인정보 보호책임자를 지정하고 있습니다.
            </p>

            <div className="bg-muted p-4 rounded-lg space-y-2">
              <div>
                <span className="font-semibold">성명:</span> 김선태 교수
              </div>
              <div>
                <span className="font-semibold">소속:</span> 전북대학교 문헌정보학과
              </div>
              <div className="flex items-center gap-2">
                <span className="font-semibold">이메일:</span>
                <a href="mailto:kim.suntae@jbnu.ac.kr" className="text-primary hover:underline">
                  kim.suntae@jbnu.ac.kr
                </a>
              </div>
            </div>

            <p className="text-sm text-muted-foreground">
              ※ 개인정보 침해에 대한 신고나 상담이 필요하신 경우에는 아래 기관에 문의하실 수 있습니다.
            </p>

            <div className="bg-blue-50 dark:bg-blue-950 p-4 rounded-lg space-y-2 text-sm">
              <div>• 개인정보 침해신고센터 (privacy.kisa.or.kr / 국번없이 118)</div>
              <div>• 개인정보 분쟁조정위원회 (www.kopico.go.kr / 1833-6972)</div>
              <div>• 대검찰청 사이버수사과 (www.spo.go.kr / 국번없이 1301)</div>
              <div>• 경찰청 사이버안전국 (cyberbureau.police.go.kr / 국번없이 182)</div>
            </div>
          </CardContent>
        </Card>

        {/* 9. 개인정보의 안전성 확보 조치 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Lock className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">9. 개인정보의 안전성 확보 조치</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="leading-relaxed mb-4">
              서비스는 개인정보의 안전성 확보를 위해 다음과 같은 조치를 취하고 있습니다.
            </p>

            <ul className="space-y-2 ml-6">
              <li className="list-disc">
                <strong>관리적 조치:</strong> 내부관리계획 수립 및 시행, 정기적 직원 교육
              </li>
              <li className="list-disc">
                <strong>기술적 조치:</strong> 개인정보 암호화, 접근 권한 관리, 보안프로그램 설치
              </li>
              <li className="list-disc">
                <strong>물리적 조치:</strong> 전산실, 자료보관실 등의 접근 통제
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* 10. 쿠키의 운영 및 거부 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Eye className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">10. 쿠키(Cookie)의 운영 및 거부</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">쿠키란?</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                웹사이트를 운영하는데 이용되는 서버가 이용자의 브라우저에 보내는 작은 텍스트 파일로,
                이용자의 컴퓨터 하드디스크에 저장됩니다.
              </p>
            </div>

            <Separator />

            <div>
              <h4 className="font-semibold mb-2">쿠키의 사용 목적</h4>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">로그인 상태 유지</li>
                <li className="list-disc">이용자 맞춤 서비스 제공</li>
                <li className="list-disc">접속 빈도 및 방문 시간 파악</li>
              </ul>
            </div>

            <Separator />

            <div>
              <h4 className="font-semibold mb-2">쿠키 설정 거부 방법</h4>
              <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                이용자는 쿠키 설치에 대한 선택권을 가지고 있습니다.
                웹브라우저 옵션 설정을 통해 모든 쿠키를 허용하거나, 쿠키가 저장될 때마다 확인을 거치거나,
                모든 쿠키의 저장을 거부할 수 있습니다.
              </p>
              <p className="text-sm text-amber-600 dark:text-amber-400">
                ※ 단, 쿠키 설치를 거부할 경우 일부 서비스 이용에 제한이 있을 수 있습니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 11. 개인정보 처리방침의 변경 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">11. 개인정보 처리방침의 변경</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed">
              본 개인정보 처리방침은 법령, 정책 또는 보안기술의 변경에 따라 내용의 추가, 삭제 및 수정이 있을 시에는
              변경사항 시행일의 최소 7일 전부터 서비스 공지사항을 통해 공지할 것입니다.
            </p>

            <div className="bg-muted p-4 rounded-lg mt-4">
              <p className="font-semibold">
                • 공고일자: 2025년 1월 1일
              </p>
              <p className="font-semibold">
                • 시행일자: 2025년 1월 1일
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 푸터 메시지 */}
        <div className="text-center py-8 border-t">
          <p className="text-lg font-semibold mb-2">
            LIS Lab은 이용자의 개인정보를 소중히 다룹니다
          </p>
          <p className="text-muted-foreground">
            개인정보 처리방침에 대한 문의사항이 있으시면 언제든지 연락 주시기 바랍니다.
          </p>
        </div>
      </div>
    </div>
  );
}
