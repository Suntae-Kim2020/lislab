'use client';

import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Lock } from 'lucide-react';

interface LoginRequiredProps {
  children: React.ReactNode;
  /** 안내 문구 (선택) */
  message?: string;
}

/**
 * 로그인한 회원에게만 children을 렌더링한다.
 * 비회원에게는 로그인/회원가입 안내 화면을 보여준다.
 * 로그인 후 원래 보려던 페이지로 되돌아가도록 next 경로를 보존한다.
 */
export function LoginRequired({ children, message }: LoginRequiredProps) {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuthStore();

  // 클릭 시점에 현재 URL을 계산 (useSearchParams는 정적 프리렌더와 충돌하므로 사용하지 않음)
  const rememberAndGo = (target: '/login' | '/register') => {
    const nextPath =
      typeof window !== 'undefined'
        ? window.location.pathname + window.location.search
        : '/';
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('post_login_redirect', nextPath);
    }
    router.push(`${target}?next=${encodeURIComponent(nextPath)}`);
  };

  if (isLoading) {
    return (
      <div className="container mx-auto py-12 px-4">
        <div className="max-w-2xl mx-auto space-y-4">
          <Skeleton className="h-8 w-2/3" />
          <Skeleton className="h-6 w-full" />
          <Skeleton className="h-6 w-5/6" />
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto py-16 px-4">
        <div className="max-w-xl mx-auto">
          <Card>
            <CardContent className="pt-10 pb-10 text-center space-y-4">
              <div className="flex justify-center">
                <div className="flex items-center justify-center w-14 h-14 rounded-full bg-primary/10">
                  <Lock className="h-7 w-7 text-primary" />
                </div>
              </div>
              <h1 className="text-2xl font-bold">로그인이 필요한 콘텐츠입니다</h1>
              <p className="text-muted-foreground leading-relaxed">
                {message ??
                  'LIS Lab의 모든 교육 콘텐츠는 회원가입 후 로그인하신 회원에게 무료로 공개됩니다.'}
              </p>
              <div className="flex flex-col sm:flex-row gap-2 justify-center pt-2">
                <Button onClick={() => rememberAndGo('/login')}>
                  로그인하기
                </Button>
                <Button variant="outline" onClick={() => rememberAndGo('/register')}>
                  회원가입
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
