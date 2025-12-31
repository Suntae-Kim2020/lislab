'use client';

import { ContentCard } from '@/components/features/ContentCard';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { useFavorites, useToggleFavorite } from '@/lib/hooks/useContents';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function FavoritesPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuthStore();
  const router = useRouter();
  const { data: favorites, isLoading, error } = useFavorites();
  const toggleFavoriteMutation = useToggleFavorite();

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  const handleToggleFavorite = (slug: string) => {
    toggleFavoriteMutation.mutate(slug);
  };

  if (authLoading || isLoading) {
    return (
      <div className="container py-8">
        <Skeleton className="h-12 w-64 mb-8" />
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-64" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4 text-red-500">오류 발생</h1>
          <p className="text-muted-foreground mb-4">
            즐겨찾기 목록을 불러오는데 실패했습니다.
          </p>
          <pre className="text-left bg-gray-100 p-4 rounded mb-4 overflow-auto text-sm">
            {JSON.stringify(error, null, 2)}
          </pre>
          <Button onClick={() => window.location.reload()}>
            새로고침
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">즐겨찾기</h1>
        <p className="text-muted-foreground">
          즐겨찾기한 콘텐츠를 관리하세요.
        </p>
      </div>

      {favorites && favorites.length > 0 ? (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {favorites.map((content) => (
            <ContentCard
              key={content.id}
              content={content}
              onToggleFavorite={handleToggleFavorite}
              isAuthenticated={true}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-muted-foreground mb-4">
            아직 즐겨찾기한 콘텐츠가 없습니다.
          </p>
          <a
            href="/contents"
            className="text-primary hover:underline"
          >
            콘텐츠 둘러보기
          </a>
        </div>
      )}
    </div>
  );
}
