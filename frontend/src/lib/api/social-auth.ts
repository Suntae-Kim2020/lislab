import apiClient from './client';

export interface KakaoLoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    user_type: string;
    organization: string;
    social_provider: string;
  };
  is_new_user: boolean;
}

export interface CompleteSocialSignupRequest {
  user_id: number;
  user_type: 'STUDENT' | 'PROFESSOR' | 'JOB_SEEKER' | 'OTHER';
  organization?: string;
  phone?: string;
}

/**
 * 카카오 로그인 콜백 처리
 */
export const kakaoLogin = async (code: string, redirectUri: string): Promise<KakaoLoginResponse> => {
  const response = await apiClient.post<KakaoLoginResponse>('/accounts/auth/kakao/callback/', {
    code,
    redirect_uri: redirectUri,
  });
  return response.data;
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
  });
  return `${kakaoAuthUrl}?${params.toString()}`;
};
