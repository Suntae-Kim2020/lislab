'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { Loader2 } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function KakaoMessageCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { token, user, setUser } = useAuthStore();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const errorParam = searchParams.get('error');

      if (errorParam) {
        setError('카카오 메시지 연동이 취소되었습니다.');
        setTimeout(() => router.push('/my/mailing-settings'), 2000);
        return;
      }

      if (!code) {
        setError('잘못된 요청입니다.');
        setTimeout(() => router.push('/my/mailing-settings'), 2000);
        return;
      }

      if (!token || !user) {
        setError('로그인이 필요합니다.');
        setTimeout(() => router.push('/login'), 2000);
        return;
      }

      try {
        const redirectUri = `${window.location.origin}/auth/kakao/message/callback`;

        const response = await fetch(`${API_BASE_URL}/api/accounts/auth/kakao/message/connect/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            code,
            redirect_uri: redirectUri,
          }),
        });

        if (!response.ok) {
          throw new Error('카카오 메시지 연동에 실패했습니다.');
        }

        const data = await response.json();

        // 사용자 정보 업데이트 (kakao_message_token 포함)
        setUser({
          ...user,
          kakao_message_token: data.kakao_message_token,
        });

        // 메일링 설정 페이지로 리다이렉트
        router.push('/my/mailing-settings');
      } catch (err: any) {
        console.error('Kakao message connect error:', err);
        setError(err.message || '카카오 메시지 연동에 실패했습니다.');
        setTimeout(() => router.push('/my/mailing-settings'), 2000);
      }
    };

    handleCallback();
  }, [searchParams, router, token, user, setUser]);

  return (
    <div className="container flex items-center justify-center min-h-screen">
      <div className="text-center">
        {error ? (
          <div>
            <p className="text-lg text-red-600 mb-4">{error}</p>
            <p className="text-sm text-muted-foreground">메일링 설정 페이지로 이동합니다...</p>
          </div>
        ) : (
          <div>
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
            <p className="text-lg">카카오 메시지 연동 중...</p>
          </div>
        )}
      </div>
    </div>
  );
}
