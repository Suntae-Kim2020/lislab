import apiClient from './client';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  user_type: 'STUDENT' | 'PROFESSOR' | 'JOB_SEEKER' | 'OTHER';
  first_name?: string;
  last_name?: string;
  phone?: string;
  organization?: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'GUEST' | 'USER' | 'ADMIN';
  user_type: string;
  phone: string;
  organization: string;
  bio: string;
  profile_image: string | null;
  is_email_verified: boolean;
  social_provider?: string;
  kakao_message_token?: string;
  has_kakao_message_token?: boolean;
  created_at: string;
}

// 로그인
export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const response = await apiClient.post<LoginResponse>('/token/', data);
  return response.data;
};

// 회원가입
export const register = async (data: RegisterRequest): Promise<User> => {
  const response = await apiClient.post<User>('/accounts/users/', data);
  return response.data;
};

// 현재 사용자 정보 조회
export const getCurrentUser = async (): Promise<User> => {
  const response = await apiClient.get<User>('/accounts/users/me/');
  return response.data;
};

// 비밀번호 변경
export const changePassword = async (data: {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}): Promise<void> => {
  await apiClient.post('/accounts/users/change_password/', data);
};

// 로그아웃 (클라이언트 측)
export const logout = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};
