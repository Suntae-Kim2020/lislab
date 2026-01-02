import apiClient from './client';

export interface Content {
  id: number;
  title: string;
  slug: string;
  summary: string;
  content_html?: string;
  thumbnail: string | null;
  category: number;
  category_name: string;
  tags: Array<{ id: number; name: string; slug: string }>;
  author: number;
  author_name: string;
  status: 'DRAFT' | 'PUBLISHED' | 'PRIVATE' | 'ARCHIVED';
  version: string;
  view_count: number;
  estimated_time: number;
  difficulty: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
  prerequisites?: string;
  learning_objectives?: string;
  created_at: string;
  updated_at: string;
  is_favorited: boolean;
  favorite_count?: number;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  order: number;
}

// 콘텐츠 목록 조회
export const getContents = async (params?: {
  search?: string;
  category?: string;
  tag?: string;
  difficulty?: string;
  page?: number;
}): Promise<{ results: Content[]; count: number; next: string | null; previous: string | null }> => {
  const response = await apiClient.get<{ results: Content[]; count: number; next: string | null; previous: string | null }>('/contents/contents/', { params });
  return response.data;
};

// 콘텐츠 상세 조회
export const getContent = async (slug: string): Promise<Content> => {
  const response = await apiClient.get<Content>(`/contents/contents/${slug}/`);
  return response.data;
};

// 카테고리 목록 조회
export const getCategories = async (): Promise<Category[]> => {
  const response = await apiClient.get<Category[] | { results: Category[]; next: string | null }>('/contents/categories/');

  // 페이지네이션이 비활성화된 경우 배열 직접 반환
  if (Array.isArray(response.data)) {
    return response.data;
  }

  // 페이지네이션이 활성화된 경우 (하위 호환성)
  let allCategories: Category[] = [];
  let nextUrl: string | null = '/contents/categories/';

  while (nextUrl) {
    const pageResponse: Awaited<ReturnType<typeof apiClient.get<{ results: Category[]; next: string | null }>>> = await apiClient.get<{ results: Category[]; next: string | null }>(nextUrl);
    allCategories = [...allCategories, ...pageResponse.data.results];
    nextUrl = pageResponse.data.next;
  }

  return allCategories;
};

// 즐겨찾기 토글
export const toggleFavorite = async (slug: string): Promise<{ detail: string }> => {
  const response = await apiClient.post<{ detail: string }>(`/contents/contents/${slug}/favorite/`);
  return response.data;
};

// 즐겨찾기 목록 조회
export const getFavorites = async (): Promise<Content[]> => {
  const response = await apiClient.get<{ results: { id: number; content: Content; created_at: string }[] }>('/contents/favorites/');
  return response.data.results.map(fav => fav.content);
};

// 같은 카테고리의 다른 콘텐츠 조회
export const getRelatedContents = async (categoryId: number, currentSlug: string): Promise<Content[]> => {
  const response = await apiClient.get<{ results: Content[] }>('/contents/contents/', {
    params: {
      category: categoryId,
      page_size: 50,
    },
  });
  // 현재 콘텐츠는 제외
  return response.data.results.filter(content => content.slug !== currentSlug);
};
