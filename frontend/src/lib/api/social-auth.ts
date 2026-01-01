import apiClient from './client';
import { User } from './auth';

export interface KakaoLoginResponse {
  access: string;
  refresh: string;
  user: User;
  is_new_user: boolean;
}

export interface CompleteSocialSignupRequest {
  user_id: number;
  email: string;
  user_type: 'STUDENT' | 'PROFESSOR' | 'JOB_SEEKER' | 'OTHER';
  organization?: string;
  phone?: string;
}

/**
 * 카카오 로그인 콜백 처리
 */
export const kakaoLogin = async (code: string, redirectUri: string): Promise<KakaoLoginResponse> => {
  // apiClient 대신 fetch 사용 (인증 전이므로 Authorization 헤더 불필요)
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  const response = await fetch(`${API_BASE_URL}/api/accounts/auth/kakao/callback/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      code,
      redirect_uri: redirectUri,
    }),
  });

  if (!response.ok) {
    throw new Error(`Kakao login failed: ${response.status}`);
  }

  return response.json();
};

/**
 * 소셜 로그인 후 추가 정보 입력
 */
export const completeSocialSignup = async (data: CompleteSocialSignupRequest): Promise<void> => {
  await apiClient.patch('/accounts/auth/social/complete/', data);
};

/**
 * 카카오 로그인 URL 생성
 */
export const getKakaoLoginUrl = (redirectUri: string): string => {
  const kakaoAuthUrl = 'https://kauth.kakao.com/oauth/authorize';
  const params = new URLSearchParams({
    client_id: process.env.NEXT_PUBLIC_KAKAO_APP_KEY || '',
    redirect_uri: redirectUri,
    response_type: 'code',
    // scope 파라미터 완전히 제거 (기본 권한만 사용)
  });
  return `${kakaoAuthUrl}?${params.toString()}`;
};

/**
 * 카카오 메시지 연동 URL 생성 (기존 사용자용)
 */
export const getKakaoMessageConnectUrl = (redirectUri: string): string => {
  const kakaoAuthUrl = 'https://kauth.kakao.com/oauth/authorize';
  const params = new URLSearchParams({
    client_id: process.env.NEXT_PUBLIC_KAKAO_APP_KEY || '',
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'talk_message', // 메시지 전송 권한만 요청
  });
  return `${kakaoAuthUrl}?${params.toString()}`;
};
