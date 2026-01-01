'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import Link from 'next/link';
import { Heart, User, Mail } from 'lucide-react';

export default function MyPage() {
  const { user, isAuthenticated, isLoading } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="container py-8">
        <Skeleton className="h-12 w-64 mb-8" />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-48" />
          ))}
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">마이페이지</h1>
        <p className="text-muted-foreground">
          환영합니다, {user.first_name || user.username}님!
        </p>
      </div>

      {/* User Info */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>내 정보</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-sm text-muted-foreground">아이디</p>
              <p className="font-medium">{user.username}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">이메일</p>
              <p className="font-medium">{user.email}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">이름</p>
              <p className="font-medium">
                {user.last_name} {user.first_name}
              </p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">사용자 구분</p>
              <p className="font-medium">
                {user.user_type === 'STUDENT' && '학생'}
                {user.user_type === 'PROFESSOR' && '교수/연구자'}
                {user.user_type === 'JOB_SEEKER' && '취업준비생'}
                {user.user_type === 'OTHER' && '기타'}
              </p>
            </div>
          </div>
          {user.organization && (
            <div>
              <p className="text-sm text-muted-foreground">소속기관</p>
              <p className="font-medium">{user.organization}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Links */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <Heart className="h-8 w-8 mb-2 text-primary" />
            <CardTitle>즐겨찾기</CardTitle>
            <CardDescription>
              즐겨찾기한 콘텐츠를 관리하세요
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <Link href="/my/favorites">즐겨찾기 보기</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <User className="h-8 w-8 mb-2 text-primary" />
            <CardTitle>프로필 수정</CardTitle>
            <CardDescription>
              내 정보를 수정하세요
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="outline" className="w-full">
              <Link href="/my/profile">프로필 수정</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <Mail className="h-8 w-8 mb-2 text-primary" />
            <CardTitle>메일링 설정</CardTitle>
            <CardDescription>
              메일링 리스트 구독 관리
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="outline" className="w-full">
              <Link href="/my/mailing-settings">메일링 설정</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
