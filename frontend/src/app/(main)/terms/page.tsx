import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { FileText, Users, Shield, AlertTriangle, Scale, BookOpen } from 'lucide-react';

export default function TermsPage() {
  return (
    <div className="container mx-auto py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">이용약관</h1>
          <p className="text-lg text-muted-foreground">
            LIS Lab 서비스 이용약관
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            시행일자: 2025년 1월 1일
          </p>
        </div>

        {/* 소개 */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <p className="leading-relaxed">
              본 약관은 LIS Lab(이하 "서비스")이 제공하는 문헌정보학 교육 플랫폼 서비스의 이용과 관련하여
              서비스와 이용자 간의 권리, 의무 및 책임사항, 기타 필요한 사항을 규정함을 목적으로 합니다.
            </p>
          </CardContent>
        </Card>

        {/* 제1조: 목적 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제1조 (목적)</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed">
              본 약관은 LIS Lab(이하 "서비스")이 제공하는 문헌정보학 교육 콘텐츠 및 관련 서비스의 이용 조건 및 절차,
              서비스 제공자와 이용자 간의 권리, 의무 및 책임 사항을 규정함을 목적으로 합니다.
            </p>
          </CardContent>
        </Card>

        {/* 제2조: 용어의 정의 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <BookOpen className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제2조 (용어의 정의)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="leading-relaxed mb-4">본 약관에서 사용하는 용어의 정의는 다음과 같습니다.</p>

            <ul className="space-y-3 ml-6">
              <li className="list-disc">
                <strong>"서비스"</strong>란 LIS Lab이 제공하는 문헌정보학 교육 콘텐츠 및 관련 기능을 의미합니다.
              </li>
              <li className="list-disc">
                <strong>"회원"</strong>이란 서비스에 접속하여 본 약관에 따라 서비스를 이용하는 자를 말합니다.
              </li>
              <li className="list-disc">
                <strong>"콘텐츠"</strong>란 서비스에서 제공하는 모든 교육 자료, 문서, 이미지, 동영상 등을 의미합니다.
              </li>
              <li className="list-disc">
                <strong>"게시물"</strong>이란 회원이 서비스에 게시한 글, 댓글, 자료 등을 의미합니다.
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* 제3조: 약관의 효력 및 변경 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제3조 (약관의 효력 및 변경)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 약관의 효력</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                본 약관은 서비스를 이용하고자 하는 모든 회원에게 그 효력을 발생합니다.
                회원가입 시 본 약관에 동의함으로써 약관의 효력이 발생합니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 약관의 변경</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 필요한 경우 관련 법령을 위배하지 않는 범위에서 본 약관을 변경할 수 있으며,
                약관이 변경되는 경우 변경 사항을 시행일자 7일 전부터 공지합니다.
                다만, 회원에게 불리한 변경의 경우에는 30일 전에 공지합니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">③ 변경 약관의 효력</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                변경된 약관은 공지된 시행일로부터 효력이 발생합니다.
                회원이 변경된 약관에 동의하지 않을 경우 서비스 이용을 중단하고 탈퇴할 수 있습니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제4조: 회원가입 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Users className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제4조 (회원가입)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 가입 신청</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원가입은 신청자가 약관의 내용에 동의하고 회원가입 신청을 한 후,
                서비스가 이를 승인함으로써 완료됩니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 가입 승인의 제한</p>
              <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                서비스는 다음 각 호에 해당하는 경우 회원가입을 승인하지 않거나 승인을 취소할 수 있습니다.
              </p>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">타인의 명의를 도용한 경우</li>
                <li className="list-disc">허위 정보를 기재한 경우</li>
                <li className="list-disc">부정한 용도로 서비스를 이용하고자 하는 경우</li>
                <li className="list-disc">관련 법령에 위배되는 경우</li>
                <li className="list-disc">과거에 서비스 이용 정지를 받은 이력이 있는 경우</li>
              </ul>
            </div>

            <div>
              <p className="font-semibold mb-2">③ 회원 정보의 변경</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원은 마이페이지를 통해 언제든지 본인의 개인정보를 열람하고 수정할 수 있습니다.
                회원은 회원가입 시 기재한 사항이 변경되었을 경우 즉시 변경사항을 수정해야 합니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제5조: 회원 탈퇴 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Users className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제5조 (회원 탈퇴 및 자격 상실)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 회원 탈퇴</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원은 언제든지 서비스에 탈퇴를 요청할 수 있으며, 서비스는 즉시 회원 탈퇴를 처리합니다.
                탈퇴 시 회원의 모든 정보는 삭제되며, 복구할 수 없습니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 자격 상실</p>
              <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                서비스는 회원이 다음 각 호의 사유에 해당하는 경우 사전 통지 없이 회원 자격을 제한 또는 정지시킬 수 있습니다.
              </p>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">타인의 정보를 도용한 경우</li>
                <li className="list-disc">서비스 운영을 고의로 방해한 경우</li>
                <li className="list-disc">공공질서 및 미풍양속에 위배되는 내용을 유포한 경우</li>
                <li className="list-disc">타인의 명예를 손상시키거나 불이익을 주는 경우</li>
                <li className="list-disc">관련 법령을 위반한 경우</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* 제6조: 서비스의 제공 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <BookOpen className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제6조 (서비스의 제공)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 제공 서비스</p>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">문헌정보학 교육 콘텐츠 제공</li>
                <li className="list-disc">게시판, 댓글, 즐겨찾기 등 커뮤니티 기능</li>
                <li className="list-disc">학습 자료 검색 및 열람</li>
                <li className="list-disc">기타 서비스가 정하는 부가 서비스</li>
              </ul>
            </div>

            <div>
              <p className="font-semibold mb-2">② 서비스 이용 시간</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 특별한 사유가 없는 한 연중무휴, 1일 24시간 제공됩니다.
                다만, 서비스 점검 등의 사유로 서비스가 일시 중단될 수 있으며,
                이 경우 사전에 공지합니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">③ 서비스의 변경 및 중단</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 운영상, 기술상의 필요에 따라 제공하고 있는 서비스를 변경 또는 중단할 수 있습니다.
                서비스 내용의 변경 또는 중단이 있는 경우 사전에 공지합니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제7조: 콘텐츠의 저작권 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제7조 (콘텐츠의 저작권 및 이용)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 저작권의 귀속</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스가 제공하는 모든 콘텐츠의 저작권 및 지적재산권은 LIS Lab 및 콘텐츠 제작자에게 귀속됩니다.
              </p>
            </div>

            <div className="bg-green-50 dark:bg-green-950 p-4 rounded-lg">
              <p className="font-semibold mb-2 text-green-700 dark:text-green-300">
                ② 학습 목적 이용 (무료)
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원은 서비스에서 제공하는 모든 콘텐츠를 <strong className="text-foreground">개인 학습, 연구, 교육 목적으로 무료로 이용</strong>할 수 있습니다.
                학생, 연구자, 교육자 누구나 자유롭게 접근하고 활용할 수 있습니다.
              </p>
            </div>

            <div className="bg-red-50 dark:bg-red-950 p-4 rounded-lg">
              <p className="font-semibold mb-2 text-red-700 dark:text-red-300">
                ③ 상업적 이용 금지
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                서비스의 모든 콘텐츠는 <strong className="text-foreground">상업적 목적으로 사용할 수 없습니다</strong>.
                다음 각 호의 행위는 엄격히 금지됩니다.
              </p>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">영리 목적의 교육 서비스에 활용</li>
                <li className="list-disc">유료 출판물 제작 및 판매</li>
                <li className="list-disc">상업적 광고 또는 마케팅 자료로 활용</li>
                <li className="list-disc">제3자에게 유상으로 제공 또는 판매</li>
              </ul>
            </div>

            <div>
              <p className="font-semibold mb-2">④ 저작권 침해 시 조치</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스의 콘텐츠를 무단으로 복제, 배포, 상업적으로 이용하는 경우
                저작권법에 따라 법적 조치가 취해질 수 있습니다.
              </p>
            </div>

            <div className="bg-amber-50 dark:bg-amber-950 p-4 rounded-lg">
              <p className="text-sm">
                <strong>※ 주의사항:</strong> 콘텐츠 이용 시 출처를 명시해야 하며,
                원본을 변경하거나 왜곡하여 사용할 수 없습니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제8조: 게시물의 관리 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제8조 (게시물의 관리)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 게시물의 저작권</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원이 서비스에 게시한 게시물의 저작권은 해당 게시물의 작성자에게 귀속됩니다.
                다만, 서비스는 서비스의 운영, 개선, 홍보 등의 목적으로 게시물을 사용할 수 있습니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 게시물의 삭제</p>
              <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                서비스는 다음 각 호에 해당하는 게시물을 사전 통지 없이 삭제하거나 이동 또는 등록을 거부할 수 있습니다.
              </p>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">타인을 비방하거나 명예를 손상시키는 내용</li>
                <li className="list-disc">음란물 또는 공공질서 및 미풍양속에 위배되는 내용</li>
                <li className="list-disc">범죄적 행위에 결부된다고 인정되는 내용</li>
                <li className="list-disc">타인의 저작권 등 권리를 침해하는 내용</li>
                <li className="list-disc">서비스의 목적과 무관한 광고성 내용</li>
                <li className="list-disc">동일한 내용을 중복하여 게시하는 경우</li>
              </ul>
            </div>

            <div>
              <p className="font-semibold mb-2">③ 게시물의 보관</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 게시물의 보관에 대해 책임을 지지 않으며,
                회원은 중요한 게시물은 별도로 보관해야 합니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제9조: 회원의 의무 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제9조 (회원의 의무)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 계정 관리</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원은 본인의 계정 정보를 안전하게 관리할 책임이 있으며,
                타인에게 계정을 양도하거나 대여할 수 없습니다.
                계정 도용 등으로 인한 피해는 회원 본인의 책임입니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 금지 행위</p>
              <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                회원은 다음 각 호의 행위를 해서는 안 됩니다.
              </p>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">허위 정보를 등록하거나 타인의 정보를 도용하는 행위</li>
                <li className="list-disc">서비스의 콘텐츠를 상업적 목적으로 무단 이용하는 행위</li>
                <li className="list-disc">서비스 운영을 방해하거나 시스템에 무리를 주는 행위</li>
                <li className="list-disc">타인의 개인정보를 수집, 저장, 공개하는 행위</li>
                <li className="list-disc">타인을 사칭하거나 허위 사실을 유포하는 행위</li>
                <li className="list-disc">관련 법령을 위반하는 행위</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* 제10조: 서비스 제공자의 의무 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제10조 (서비스 제공자의 의무)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 서비스 제공</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 안정적이고 지속적인 서비스 제공을 위해 노력합니다.
                서비스 장애 발생 시 신속한 복구를 위해 최선을 다합니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 개인정보 보호</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 관련 법령이 정하는 바에 따라 회원의 개인정보를 보호하기 위해 노력합니다.
                개인정보의 보호 및 사용에 대해서는 개인정보 처리방침을 따릅니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">③ 의견 수렴</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 회원의 의견을 소중히 여기며, 서비스 개선을 위해 적극 반영합니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제11조: 서비스 이용 제한 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제11조 (서비스 이용 제한)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 이용 제한 사유</p>
              <p className="text-sm text-muted-foreground leading-relaxed mb-2">
                서비스는 회원이 본 약관의 의무를 위반하거나 서비스의 정상적인 운영을 방해한 경우,
                경고, 일시 정지, 영구 이용 정지 등으로 서비스 이용을 제한할 수 있습니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 이용 제한 절차</p>
              <ul className="space-y-2 ml-6 text-sm text-muted-foreground">
                <li className="list-disc">1단계: 경고 (위반 내용 통지 및 시정 요청)</li>
                <li className="list-disc">2단계: 일시 정지 (7일~30일)</li>
                <li className="list-disc">3단계: 영구 이용 정지 (회원 자격 박탈)</li>
              </ul>
            </div>

            <div>
              <p className="font-semibold mb-2">③ 이의 제기</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                이용 제한에 대해 이의가 있는 회원은 이의 신청을 할 수 있으며,
                서비스는 이의 신청 내용을 검토하여 15일 이내에 답변합니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제12조: 면책 조항 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제12조 (면책 조항)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 서비스 제공의 면책</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스는 천재지변, 전쟁, 기간통신사업자의 서비스 중지 등 불가항력으로 인하여
                서비스를 제공할 수 없는 경우 서비스 제공에 대한 책임이 면제됩니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 회원 과실에 대한 면책</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원의 귀책사유로 인한 서비스 이용 장애에 대하여 서비스는 책임을 지지 않습니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">③ 비영리 서비스</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                본 서비스는 비영리 교육 목적으로 운영되며, 무료로 제공됩니다.
                서비스 이용으로 발생한 손해에 대해 서비스는 고의 또는 중과실이 없는 한 책임을 지지 않습니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">④ 게시물에 대한 면책</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                회원이 게시한 내용에 대한 책임은 전적으로 해당 회원에게 있으며,
                서비스는 회원이 게시한 내용의 진실성, 정확성 등에 대해 책임을 지지 않습니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 제13조: 분쟁 해결 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Scale className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">제13조 (분쟁 해결)</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold mb-2">① 준거법</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                본 약관의 해석 및 서비스와 회원 간의 분쟁에 대해서는 대한민국의 법률을 적용합니다.
              </p>
            </div>

            <div>
              <p className="font-semibold mb-2">② 관할법원</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                서비스 이용으로 발생한 분쟁에 대해 소송이 제기될 경우,
                민사소송법상의 관할법원을 전속 관할로 합니다.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* 부칙 */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <CardTitle className="text-2xl">부칙</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="bg-muted p-4 rounded-lg">
              <p className="font-semibold mb-2">본 약관은 2025년 1월 1일부터 시행됩니다.</p>
            </div>
          </CardContent>
        </Card>

        {/* 푸터 메시지 */}
        <div className="text-center py-8 border-t">
          <p className="text-lg font-semibold mb-2">
            LIS Lab은 공정하고 투명한 서비스 운영을 지향합니다
          </p>
          <p className="text-muted-foreground">
            이용약관에 대한 문의사항이 있으시면 kim.suntae@jbnu.ac.kr로 연락 주시기 바랍니다.
          </p>
        </div>
      </div>
    </div>
  );
}
