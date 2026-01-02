'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { ContentCard } from '@/components/features/ContentCard';
import { useContents, useCategories, useToggleFavorite } from '@/lib/hooks/useContents';
import { useAuthStore } from '@/store/authStore';
import { Search } from 'lucide-react';

function ContentsPageContent() {
  const { isAuthenticated } = useAuthStore();
  const searchParams = useSearchParams();
  const categoryParam = searchParams.get('category');

  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<string>(categoryParam || 'all');
  const [difficulty, setDifficulty] = useState<string>('all');
  const [page, setPage] = useState(1);

  // URL 파라미터가 변경될 때 카테고리 업데이트
  useEffect(() => {
    setCategory(categoryParam || 'all');
    setPage(1); // 카테고리 변경 시 첫 페이지로
  }, [categoryParam]);

  // 필터 변경 시 첫 페이지로 리셋
  useEffect(() => {
    setPage(1);
  }, [search, category, difficulty]);

  const { data: contentsData, isLoading } = useContents({
    search,
    category: category === 'all' ? '' : category,
    difficulty: difficulty === 'all' ? '' : difficulty,
    page
  });
  const { data: categories } = useCategories();
  const toggleFavoriteMutation = useToggleFavorite();

  // 모든 카테고리를 order 순서대로 정렬
  const sortedCategories = Array.isArray(categories)
    ? categories.sort((a, b) => a.order - b.order)
    : [];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
  };

  const handleToggleFavorite = (slug: string) => {
    if (!isAuthenticated) {
      alert('로그인이 필요합니다.');
      return;
    }
    toggleFavoriteMutation.mutate(slug);
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex flex-col gap-8">
        {/* Header */}
        <div className="flex flex-col gap-4">
          <h1 className="text-3xl font-bold">교육 콘텐츠</h1>
          <p className="text-muted-foreground">
            다양한 주제의 교육 콘텐츠를 탐색하고 학습하세요.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col gap-4">
          <form onSubmit={handleSearch} className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                type="search"
                placeholder="콘텐츠 검색..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button type="submit">검색</Button>
          </form>

          <div className="flex flex-wrap gap-2">
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="카테고리" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">전체</SelectItem>
                {sortedCategories.map((cat) => (
                  <SelectItem key={cat.id} value={cat.slug}>
                    {cat.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={difficulty} onValueChange={setDifficulty}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="난이도" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">전체</SelectItem>
                <SelectItem value="BEGINNER">초급</SelectItem>
                <SelectItem value="INTERMEDIATE">중급</SelectItem>
                <SelectItem value="ADVANCED">고급</SelectItem>
              </SelectContent>
            </Select>

            {(category !== 'all' || difficulty !== 'all' || search) && (
              <Button
                variant="outline"
                onClick={() => {
                  setCategory('all');
                  setDifficulty('all');
                  setSearch('');
                }}
              >
                필터 초기화
              </Button>
            )}
          </div>
        </div>

        {/* Content Grid */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {isLoading ? (
            Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="space-y-3">
                <Skeleton className="h-48 w-full" />
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </div>
            ))
          ) : contentsData?.results && contentsData.results.length > 0 ? (
            contentsData.results.map((content) => (
              <ContentCard
                key={content.id}
                content={content}
                onToggleFavorite={handleToggleFavorite}
                isAuthenticated={isAuthenticated}
              />
            ))
          ) : (
            <div className="col-span-full text-center py-12">
              <p className="text-muted-foreground">검색 결과가 없습니다.</p>
            </div>
          )}
        </div>

        {/* Pagination */}
        {contentsData && contentsData.count > 20 && (
          <div className="flex justify-center gap-2">
            <Button
              variant="outline"
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={!contentsData.previous}
            >
              이전
            </Button>
            <span className="flex items-center px-4 text-sm text-muted-foreground">
              페이지 {page}
            </span>
            <Button
              variant="outline"
              onClick={() => setPage(p => p + 1)}
              disabled={!contentsData.next}
            >
              다음
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ContentsPage() {
  return (
    <Suspense fallback={
      <div className="container mx-auto py-8 px-4">
        <div className="flex flex-col gap-8">
          <div className="flex flex-col gap-4">
            <Skeleton className="h-10 w-48" />
            <Skeleton className="h-6 w-96" />
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="space-y-3">
                <Skeleton className="h-48 w-full" />
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </div>
            ))}
          </div>
        </div>
      </div>
    }>
      <ContentsPageContent />
    </Suspense>
  );
}
