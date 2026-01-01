import { apiClient } from './client';

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  user_type: string;
  phone: string;
  organization: string;
  bio: string;
  profile_image: string | null;
  is_email_verified: boolean;
  created_at: string;
}

export interface UpdateProfileRequest {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  organization?: string;
  bio?: string;
  profile_image?: string | null;
  user_type?: string;
}

export interface ChangePasswordRequest {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}

// 현재 사용자 프로필 조회
export const getCurrentUser = async (): Promise<UserProfile> => {
  const response = await apiClient.get<UserProfile>('/accounts/users/me/');
  return response.data;
};

// 프로필 수정
export const updateProfile = async (userId: number, data: UpdateProfileRequest): Promise<UserProfile> => {
  const response = await apiClient.patch<UserProfile>(`/accounts/users/${userId}/`, data);
  return response.data;
};

// 비밀번호 변경
export const changePassword = async (data: ChangePasswordRequest): Promise<{ detail: string }> => {
  const response = await apiClient.post<{ detail: string }>('/accounts/users/change_password/', data);
  return response.data;
};
