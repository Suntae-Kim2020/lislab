'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as profileApi from '@/lib/api/profile';

// 현재 사용자 프로필 조회
export function useCurrentUser() {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: profileApi.getCurrentUser,
    staleTime: 0, // 항상 최신 데이터 사용
    refetchOnMount: true, // 마운트 시 항상 refetch
  });
}

// 프로필 수정
export function useUpdateProfile() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, data }: { userId: number; data: profileApi.UpdateProfileRequest }) =>
      profileApi.updateProfile(userId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['currentUser'] });
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
  });
}

// 비밀번호 변경
export function useChangePassword() {
  return useMutation({
    mutationFn: profileApi.changePassword,
  });
}
