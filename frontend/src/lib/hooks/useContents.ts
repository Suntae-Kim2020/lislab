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
    // 낙관적 업데이트: mutation 실행 전 UI 즉시 업데이트
    onMutate: async (slug) => {
      // 진행 중인 refetch를 취소하여 낙관적 업데이트를 덮어쓰지 않도록 함
      await queryClient.cancelQueries({ queryKey: ['content', slug] });
      await queryClient.cancelQueries({ queryKey: ['contents'] });

      // 이전 값 저장 (롤백용)
      const previousContent = queryClient.getQueryData(['content', slug]);
      const previousContents = queryClient.getQueriesData({ queryKey: ['contents'] });

      // 콘텐츠 상세 낙관적 업데이트
      queryClient.setQueryData(['content', slug], (old: any) => {
        if (!old) return old;
        return {
          ...old,
          is_favorited: !old.is_favorited,
          favorite_count: old.is_favorited
            ? (old.favorite_count || 1) - 1
            : (old.favorite_count || 0) + 1,
        };
      });

      // 콘텐츠 목록 낙관적 업데이트
      queryClient.setQueriesData({ queryKey: ['contents'] }, (old: any) => {
        if (!old?.results) return old;
        return {
          ...old,
          results: old.results.map((content: any) =>
            content.slug === slug
              ? {
                  ...content,
                  is_favorited: !content.is_favorited,
                  favorite_count: content.is_favorited
                    ? (content.favorite_count || 1) - 1
                    : (content.favorite_count || 0) + 1,
                }
              : content
          ),
        };
      });

      return { previousContent, previousContents };
    },
    // 에러 발생 시 이전 값으로 롤백
    onError: (err, slug, context) => {
      if (context?.previousContent) {
        queryClient.setQueryData(['content', slug], context.previousContent);
      }
      if (context?.previousContents) {
        context.previousContents.forEach(([queryKey, data]) => {
          queryClient.setQueryData(queryKey, data);
        });
      }
    },
    // 성공 시 즐겨찾기 목록만 무효화 (상세/목록은 낙관적 업데이트 유지)
    onSuccess: () => {
      // 즐겨찾기 목록만 refetch (다른 페이지에서 사용)
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
