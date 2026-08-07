'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { teamApi, TeamMember } from '@/lib/api/team';
import {
  Building2,
  ExternalLink,
  HeartHandshake,
  Mail,
  Sparkles,
  Users,
} from 'lucide-react';

const SPONSOR_CONTACT_EMAIL = 'kim.suntae@jbnu.ac.kr';

const SPONSORS = [
  {
    name: '(주)아르고넷',
    tagline: 'AI 기반 연구성과 · 연구데이터 관리 전문 기업',
    logo: '/sponsors/argonet.png',
    url: 'https://argonet.co.kr/',
    linkLabel: 'argonet.co.kr 바로가기',
    description:
      '(주)아르고넷은 “정보, 자원, 시스템, 사람이 서로 소통하는 더 나은 지식세상”을 지향하며 AI 기반 연구성과·연구데이터 관리 분야를 선도해 온 전문 기업입니다. 대학과 정부출연연구기관, 학회를 대상으로 연구자의 논문·특허·저서 등 다양한 성과정보를 통합 수집하고 객관적 지표로 분석하는 연구성과관리시스템(R2RIMS/S2RIMS), 기관의 학술 자산을 개방형으로 축적·공개하는 기관 리포지터리 ScholarWorks, 데이터관리계획(DMP) 수립부터 R&D 연구데이터의 보존·공유·재사용까지 지원하는 연구데이터 리포지터리 DataWorks를 공급하고 있습니다. 또한 학술지 논문 투고·심사 관리 서비스, AI 검색 솔루션 ARi Search, 콘텐츠 통합관리 시스템 Contentree 등을 통해 메타데이터 표준과 시맨틱·AI 기술을 실제 서비스로 구현해 왔습니다. 오픈 사이언스 생태계에 필요한 실무 역량과 현장 경험을 바탕으로 LIS Lab의 교육·연구 활동을 후원하고 있습니다.',
  },
  {
    name: '(주)알투어스',
    tagline: '연구데이터 전주기 컨설팅 전문 기업',
    logo: '/sponsors/r2urs.svg',
    url: 'https://r2urs.com/',
    linkLabel: 'r2urs.com 바로가기',
    description:
      '주식회사 알투어스(R2URS)는 연구데이터의 수집·저장·관리·보존·출판·재사용에 이르는 전주기를 아우르는 연구데이터 컨설팅 전문 기업입니다. 국제 표준에 기반한 실행 중심의 컨설팅을 지향하며, 신뢰할 수 있는 데이터 리포지터리의 국제 인증인 CoreTrustSeal 획득 컨설팅을 핵심 역량으로 삼고 있습니다. 이와 함께 기관의 연구데이터 거버넌스 체계 수립(조직·규정·프로세스 정비), 연구자가 실무에 바로 활용할 수 있는 전주기 가이드라인 제작, 학문 분야별 메타데이터 스키마 설계와 표준 제정, DOI·ISNI 등 식별체계 연계, 기관평가 대응을 위한 성과 분석과 증빙 체계화, 연구데이터 플랫폼·리포지터리 구축 및 운영 지원까지 폭넓은 서비스를 제공합니다. 17개 기관과 34건의 과제를 수행하며 축적한 현장 경험을 바탕으로 LIS Lab의 교육·연구 활동을 후원하고 있습니다.',
  },
];

// 후원 기업이 채워질 예비 자리 (홍보 슬롯)
const OPEN_SPONSOR_SLOTS = [
  '연구정보 · 학술출판',
  'AI · 데이터 플랫폼',
  '도서관 · 아카이브',
];

export default function PeoplePage() {
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    teamApi
      .getMembers()
      .then(setMembers)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="container mx-auto py-12 px-4">
      <div className="max-w-5xl mx-auto">
        {/* 후원 기업 섹션 */}
        <section className="mb-16">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-2 mb-3">
              <HeartHandshake className="h-7 w-7 text-primary" />
              <h2 className="text-2xl md:text-3xl font-bold">
                LIS Lab 운영에 도움을 주는 기업들
              </h2>
            </div>
            <p className="text-muted-foreground">
              LIS Lab의 교육·연구 활동은 아래 기업들의 후원으로 운영됩니다.
            </p>
          </div>

          {/* 후원 기업 카드 */}
          <div className="space-y-6 mb-6">
            {SPONSORS.map((sponsor) => (
              <Card
                key={sponsor.name}
                className="overflow-hidden border-primary/20"
              >
                <CardContent className="p-6 md:p-8">
                  <div className="flex flex-col md:flex-row gap-6 md:gap-8">
                    {/* 로고 */}
                    <a
                      href={sponsor.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-shrink-0 self-start"
                    >
                      <div className="w-56 h-24 rounded-lg bg-white border flex items-center justify-center p-4 transition-shadow hover:shadow-md">
                        <img
                          src={sponsor.logo}
                          alt={`${sponsor.name} 로고`}
                          className="max-w-full max-h-full object-contain"
                        />
                      </div>
                    </a>

                    {/* 소개 */}
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2 mb-2">
                        <h3 className="text-xl font-semibold">
                          {sponsor.name}
                        </h3>
                        <span className="inline-flex items-center rounded-full bg-primary/10 text-primary text-xs font-medium px-2.5 py-0.5">
                          {sponsor.tagline}
                        </span>
                      </div>

                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {sponsor.description}
                      </p>

                      <a
                        href={sponsor.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 mt-4 text-sm font-medium text-primary hover:underline"
                      >
                        {sponsor.linkLabel}
                        <ExternalLink className="h-3.5 w-3.5" />
                      </a>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* 예비 후원 기업 자리 */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {OPEN_SPONSOR_SLOTS.map((slot) => (
              <div
                key={slot}
                className="group rounded-xl border-2 border-dashed border-primary/30 bg-primary/[0.03] hover:bg-primary/[0.06] hover:border-primary/50 transition-colors p-6 flex flex-col items-center justify-center text-center min-h-[180px]"
              >
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-3">
                  <Building2 className="h-6 w-6 text-primary/70" />
                </div>
                <p className="font-semibold text-sm">예비 후원 기업</p>
                <p className="text-xs text-muted-foreground mt-1">{slot}</p>
                <p className="inline-flex items-center gap-1 text-[11px] text-primary/80 mt-3">
                  <Sparkles className="h-3 w-3" />이 자리에 귀사의 로고가
                  소개됩니다
                </p>
              </div>
            ))}
          </div>

          {/* 후원 문의 */}
          <div className="mt-6 rounded-xl border bg-muted/40 p-5 flex flex-col sm:flex-row sm:items-center justify-center gap-3 text-center sm:text-left">
            <Mail className="h-5 w-5 text-primary mx-auto sm:mx-0 flex-shrink-0" />
            <p className="text-sm text-muted-foreground">
              LIS Lab에 도움을 주고 싶은 기업은{' '}
              <a
                href={`mailto:${SPONSOR_CONTACT_EMAIL}?subject=LIS%20Lab%20후원%20문의`}
                className="font-medium text-primary hover:underline"
              >
                {SPONSOR_CONTACT_EMAIL}
              </a>
              {' '}로 연락을 주시면 됩니다.
            </p>
          </div>
        </section>

        {/* 헤더 */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Users className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold">LIS Lab 사람들</h1>
          </div>
          <p className="text-lg text-muted-foreground">
            LIS Lab을 함께 만들어가는 팀원들을 소개합니다.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12 text-muted-foreground">
            로딩 중...
          </div>
        ) : members.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            등록된 팀 멤버가 없습니다.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {members.map((member) => (
              <Card key={member.id} className="overflow-hidden">
                <CardContent className="pt-6 flex flex-col items-center text-center">
                  {/* 사진 */}
                  <div className="w-32 h-32 rounded-full overflow-hidden bg-muted mb-4 flex-shrink-0">
                    {member.photo ? (
                      <img
                        src={member.photo}
                        alt={member.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-4xl text-muted-foreground">
                        {member.name.charAt(0)}
                      </div>
                    )}
                  </div>

                  {/* 이름 & 직함 */}
                  <h3 className="text-xl font-semibold">{member.name}</h3>
                  {member.title && (
                    <p className="text-sm text-muted-foreground mt-1">
                      {member.title}
                    </p>
                  )}

                  {/* 소개 */}
                  {member.bio && (
                    <p className="text-sm text-muted-foreground mt-3 leading-relaxed">
                      {member.bio}
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
