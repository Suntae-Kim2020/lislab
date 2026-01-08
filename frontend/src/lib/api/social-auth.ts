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
  first_name: string;
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

export interface CompleteSocialSignupResponse {
  message: string;
  user: {
    id: number;
    username: string;
    first_name: string;
    email: string;
    user_type: string;
    organization: string;
    phone: string;
  };
}

/**
 * 소셜 로그인 후 추가 정보 입력
 */
export const completeSocialSignup = async (data: CompleteSocialSignupRequest): Promise<CompleteSocialSignupResponse> => {
  const response = await apiClient.patch('/accounts/auth/social/complete/', data);
  return response.data;
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
    scope: 'talk_message', // 최초 로그인 시 메시지 권한 포함
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

// ============================================
// 네이버 로그인
// ============================================

export interface NaverLoginResponse {
  access: string;
  refresh: string;
  user: User;
  is_new_user: boolean;
  naver_info?: {
    email: string | null;
    name: string | null;
    phone: string | null;
  };
}

/**
 * 네이버 로그인 콜백 처리
 */
export const naverLogin = async (code: string, state: string, redirectUri: string): Promise<NaverLoginResponse> => {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  const response = await fetch(`${API_BASE_URL}/api/accounts/auth/naver/callback/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      code,
      state,
      redirect_uri: redirectUri,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `Naver login failed: ${response.status}`);
  }

  return response.json();
};

/**
 * 네이버 로그인 URL 생성
 */
export const getNaverLoginUrl = (redirectUri: string): string => {
  const naverAuthUrl = 'https://nid.naver.com/oauth2.0/authorize';
  const state = Math.random().toString(36).substring(2, 15); // CSRF 방지용 state

  // state를 sessionStorage에 저장 (콜백에서 검증용)
  if (typeof window !== 'undefined') {
    sessionStorage.setItem('naver_oauth_state', state);
  }

  const params = new URLSearchParams({
    client_id: process.env.NEXT_PUBLIC_NAVER_CLIENT_ID || '',
    redirect_uri: redirectUri,
    response_type: 'code',
    state: state,
  });
  return `${naverAuthUrl}?${params.toString()}`;
};


// ============================================
// 구글 로그인
// ============================================

export interface GoogleLoginResponse {
  access: string;
  refresh: string;
  user: User;
  is_new_user: boolean;
  google_info?: {
    email: string | null;
    name: string | null;
  };
}

/**
 * 구글 로그인 콜백 처리
 */
export const googleLogin = async (code: string, redirectUri: string): Promise<GoogleLoginResponse> => {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  const response = await fetch(`${API_BASE_URL}/api/accounts/auth/google/callback/`, {
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
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `Google login failed: ${response.status}`);
  }

  return response.json();
};

/**
 * 구글 로그인 URL 생성
 */
export const getGoogleLoginUrl = (redirectUri: string): string => {
  const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
  const params = new URLSearchParams({
    client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '',
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'email profile',
    access_type: 'offline',
    prompt: 'consent',
  });
  return `${googleAuthUrl}?${params.toString()}`;
};
