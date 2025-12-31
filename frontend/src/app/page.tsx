'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuthStore } from '@/store/authStore';

export default function HomePage() {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="container mx-auto py-6 px-4">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center space-y-4 py-6 text-center">
        <div className="relative w-full max-w-2xl mx-auto p-8 bg-gradient-to-b from-background via-muted/30 to-background rounded-xl">
          <div className="relative">
            <Image
              src="/lis-lab-hero.png"
              alt="LIS Lab - Library & Information Science Learning Platform"
              width={672}
              height={384}
              priority
              className="rounded-lg mx-auto shadow-2xl"
            />
            <div className="absolute inset-0 rounded-lg bg-gradient-to-t from-background/20 via-transparent to-background/20 pointer-events-none"></div>
          </div>
        </div>
        <div className="flex gap-4">
          <Button asChild size="lg">
            <Link href="/contents">콘텐츠 둘러보기</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/register">시작하기</Link>
          </Button>
        </div>
      </section>

      {/* Features */}
      <section className="py-12">
        <h2 className="mb-8 text-center text-3xl font-bold">주요 기능</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <Link href="/contents" className="transition-transform hover:scale-105">
            <Card className="h-full cursor-pointer">
              <CardHeader>
                <CardTitle>교육 콘텐츠</CardTitle>
                <CardDescription>
                  체계적으로 분류된 교육 자료
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  카테고리별로 정리된 고품질 교육 콘텐츠를 제공합니다.
                </p>
              </CardContent>
            </Card>
          </Link>

          <Card>
            <CardHeader>
              <CardTitle>댓글 시스템</CardTitle>
              <CardDescription>
                질문하고 답변 받기
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                콘텐츠에 대해 자유롭게 질문하고 관리자의 답변을 받을 수 있습니다.
              </p>
            </CardContent>
          </Card>

          <Link href="/boards" className="transition-transform hover:scale-105">
            <Card className="h-full cursor-pointer">
              <CardHeader>
                <CardTitle>게시판</CardTitle>
                <CardDescription>
                  공지사항 및 요청 사항
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  공지사항 확인 및 새로운 콘텐츠 개발을 요청할 수 있습니다.
                </p>
              </CardContent>
            </Card>
          </Link>

          {isAuthenticated ? (
            <Link href="/my/favorites" className="transition-transform hover:scale-105">
              <Card className="h-full cursor-pointer">
                <CardHeader>
                  <CardTitle>즐겨찾기</CardTitle>
                  <CardDescription>
                    나만의 콘텐츠 관리
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    관심 있는 콘텐츠를 즐겨찾기하여 빠르게 접근할 수 있습니다.
                  </p>
                </CardContent>
              </Card>
            </Link>
          ) : (
            <Card className="opacity-60">
              <CardHeader>
                <CardTitle>즐겨찾기</CardTitle>
                <CardDescription>
                  나만의 콘텐츠 관리
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  관심 있는 콘텐츠를 즐겨찾기하여 빠르게 접근할 수 있습니다.
                </p>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader>
              <CardTitle>버전 관리</CardTitle>
              <CardDescription>
                콘텐츠 개정 이력
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                콘텐츠의 변경 이력을 확인하고 이전 버전을 조회할 수 있습니다.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>메일링 리스트</CardTitle>
              <CardDescription>
                최신 소식 받기
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                새로운 콘텐츠와 업데이트 소식을 이메일로 받아보세요.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="flex flex-col items-center justify-center space-y-4 py-12 text-center">
        <h2 className="text-3xl font-bold">지금 시작하세요</h2>
        <p className="max-w-[600px] text-muted-foreground">
          회원가입하고 다양한 교육 콘텐츠를 경험해보세요.
        </p>
        <Button asChild size="lg">
          <Link href="/register">무료 회원가입</Link>
        </Button>
      </section>
    </div>
  );
}
