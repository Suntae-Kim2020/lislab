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
  const [subCategory, setSubCategory] = useState<string>('all');
  const [difficulty, setDifficulty] = useState<string>('all');

  // URL 파라미터가 변경될 때 카테고리 업데이트
  useEffect(() => {
    setCategory(categoryParam || 'all');
    setSubCategory('all');
  }, [categoryParam]);

  const { data: contentsData, isLoading } = useContents({
    search,
    category: subCategory !== 'all' ? subCategory : (category === 'all' ? '' : category),
    difficulty: difficulty === 'all' ? '' : difficulty
  });
  const { data: categories } = useCategories();
  const toggleFavoriteMutation = useToggleFavorite();

  // 상위 카테고리 (parent가 자기 자신인 카테고리)
  const parentCategories = Array.isArray(categories)
    ? categories.filter(cat => cat.parent === cat.id)
    : [];

  // 선택된 카테고리의 하위 카테고리
  const selectedCategoryId = Array.isArray(categories)
    ? categories.find(cat => cat.slug === category)?.id
    : undefined;
  const subCategories = selectedCategoryId && Array.isArray(categories)
    ? categories.filter(cat => cat.parent === selectedCategoryId)
    : [];

  // 카테고리 변경 시 하위 카테고리 초기화
  const handleCategoryChange = (value: string) => {
    setCategory(value);
    setSubCategory('all');
  };

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
            <Select value={category} onValueChange={handleCategoryChange}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="카테고리" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">전체</SelectItem>
                {parentCategories.map((cat) => (
                  <SelectItem key={cat.id} value={cat.slug}>
                    {cat.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* 하위 메뉴 드롭박스 - 선택된 카테고리에 하위 카테고리가 있을 때만 표시 */}
            {subCategories.length > 0 && (
              <Select value={subCategory} onValueChange={setSubCategory}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="하위 메뉴" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">전체</SelectItem>
                  {subCategories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.slug}>
                      {cat.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}

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

            {(category !== 'all' || subCategory !== 'all' || difficulty !== 'all' || search) && (
              <Button
                variant="outline"
                onClick={() => {
                  setCategory('all');
                  setSubCategory('all');
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
            <Button variant="outline">이전</Button>
            <Button variant="outline">다음</Button>
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
