'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { kakaoLogin } from '@/lib/api/social-auth';
import { useAuthStore } from '@/store/authStore';
import { Loader2 } from 'lucide-react';

export default function KakaoCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setUser, setToken } = useAuthStore();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleKakaoCallback = async () => {
      const code = searchParams.get('code');
      const error = searchParams.get('error');

      // 에러 처리
      if (error) {
        setError('카카오 로그인이 취소되었습니다.');
        setTimeout(() => router.push('/login'), 2000);
        return;
      }

      // Authorization code가 없는 경우
      if (!code) {
        setError('잘못된 요청입니다.');
        setTimeout(() => router.push('/login'), 2000);
        return;
      }

      try {
        // Redirect URI 생성
        const redirectUri = `${window.location.origin}/auth/kakao/callback`;

        // 백엔드 API 호출
        const response = await kakaoLogin(code, redirectUri);

        // JWT 토큰 저장
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);

        // 사용자 정보 및 토큰 저장
        setToken(response.access);
        setUser(response.user);

        // 신규 사용자인 경우 추가 정보 입력 페이지로 이동
        if (response.is_new_user) {
          router.push(`/auth/complete-signup?user_id=${response.user.id}`);
        } else {
          // 기존 사용자는 메인 페이지로 이동
          router.push('/');
        }
      } catch (err: any) {
        console.error('Kakao login error:', err);
        setError(err.response?.data?.error || '로그인에 실패했습니다.');
        setTimeout(() => router.push('/login'), 2000);
      }
    };

    handleKakaoCallback();
  }, [searchParams, router, setUser, setToken]);

  return (
    <div className="container flex items-center justify-center min-h-screen">
      <div className="text-center">
        {error ? (
          <div>
            <p className="text-lg text-red-600 mb-4">{error}</p>
            <p className="text-sm text-muted-foreground">로그인 페이지로 이동합니다...</p>
          </div>
        ) : (
          <div>
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
            <p className="text-lg">카카오 로그인 처리 중...</p>
          </div>
        )}
      </div>
    </div>
  );
}
