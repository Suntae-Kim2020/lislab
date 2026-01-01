'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as contentsApi from '@/lib/api/contents';

// 콘텐츠 목록 조회 훅
export function useContents(params?: {
  search?: string;
  category?: string;
  tag?: string;
  difficulty?: string;
  page?: number;
}) {
  return useQuery({
    queryKey: ['contents', params],
    queryFn: () => contentsApi.getContents(params),
    staleTime: 1000 * 60 * 5, // 5분
  });
}

// 콘텐츠 상세 조회 훅
export function useContent(slug: string) {
  return useQuery({
    queryKey: ['content', slug],
    queryFn: () => contentsApi.getContent(slug),
    enabled: !!slug,
    staleTime: 0, // 캐시 사용 안 함 - 항상 최신 데이터 가져오기
    gcTime: 0, // 가비지 컬렉션 시간도 0으로 설정
  });
}

// 카테고리 목록 조회 훅
export function useCategories() {
  return useQuery({
    queryKey: ['categories'],
    queryFn: contentsApi.getCategories,
    staleTime: 0, // 캐시 사용 안 함
  });
}

// 즐겨찾기 토글 훅
export function useToggleFavorite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (slug: string) => contentsApi.toggleFavorite(slug),
    onSuccess: (_, slug) => {
      // 콘텐츠 상세 및 목록 쿼리 무효화
      queryClient.invalidateQueries({ queryKey: ['content', slug] });
      queryClient.invalidateQueries({ queryKey: ['contents'] });
      queryClient.invalidateQueries({ queryKey: ['favorites'] });
    },
  });
}

// 즐겨찾기 목록 조회 훅
export function useFavorites() {
  return useQuery({
    queryKey: ['favorites'],
    queryFn: contentsApi.getFavorites,
    staleTime: 1000 * 60 * 5,
  });
}

// 같은 카테고리의 관련 콘텐츠 조회 훅
export function useRelatedContents(categoryId: number, currentSlug: string) {
  return useQuery({
    queryKey: ['relatedContents', categoryId, currentSlug],
    queryFn: () => contentsApi.getRelatedContents(categoryId, currentSlug),
    enabled: !!categoryId && !!currentSlug,
    staleTime: 1000 * 60 * 5,
  });
}
