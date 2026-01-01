'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import * as authApi from '@/lib/api/auth';
import { useEffect } from 'react';

// 로그인 훅
export function useLogin() {
  const router = useRouter();
  const { setUser, setToken } = useAuthStore();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      // 토큰 저장
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);

      // authStore에 토큰 저장
      setToken(data.access);

      // 사용자 정보 조회 후 스토어 업데이트
      authApi.getCurrentUser().then((user) => {
        setUser(user);
        queryClient.invalidateQueries({ queryKey: ['currentUser'] });
        router.push('/');
      });
    },
  });
}

// 회원가입 훅
export function useRegister() {
  const router = useRouter();

  return useMutation({
    mutationFn: authApi.register,
    onSuccess: () => {
      // 회원가입 성공 시 로그인 페이지로 이동
      router.push('/login?registered=true');
    },
  });
}

// 로그아웃 훅
export function useLogout() {
  const router = useRouter();
  const { logout } = useAuthStore();
  const queryClient = useQueryClient();

  return () => {
    logout();
    queryClient.clear();
    router.push('/login');
  };
}

// 현재 사용자 정보 조회 훅
export function useCurrentUser() {
  const { setUser, setToken, setLoading } = useAuthStore();

  const query = useQuery({
    queryKey: ['currentUser'],
    queryFn: authApi.getCurrentUser,
    enabled: typeof window !== 'undefined' && !!localStorage.getItem('access_token'),
    retry: false,
    staleTime: 1000 * 60 * 5, // 5분
  });

  useEffect(() => {
    // localStorage에서 토큰 로드
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        setToken(token);
      }
    }

    if (query.data) {
      setUser(query.data);
    } else if (query.error) {
      setUser(null);
      setLoading(false);
    }
  }, [query.data, query.error, setUser, setToken, setLoading]);

  return query;
}

// 자동 로그인 체크 훅
export function useAuthCheck() {
  const { setLoading } = useAuthStore();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setLoading(false);
    }
  }, [setLoading]);

  useCurrentUser();
}

// 비밀번호 변경 훅
export function useChangePassword() {
  return useMutation({
    mutationFn: authApi.changePassword,
  });
}
