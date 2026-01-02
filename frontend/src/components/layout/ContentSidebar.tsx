'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FileText } from 'lucide-react';
import { useCategories, useContents } from '@/lib/hooks/useContents';
import { Skeleton } from '@/components/ui/skeleton';
import type { Category } from '@/lib/api/contents';

const difficultyLabels = {
  BEGINNER: '초급',
  INTERMEDIATE: '중급',
  ADVANCED: '고급',
};

export function ContentSidebar() {
  const pathname = usePathname();
  const { data: categories, isLoading } = useCategories();

  if (isLoading) {
    return (
      <div className="space-y-2 p-4">
        <Skeleton className="h-8 w-full" />
        <Skeleton className="h-8 w-full" />
        <Skeleton className="h-8 w-full" />
      </div>
    );
  }

  // 카테고리를 order 순서대로 정렬
  const sortedCategories = (categories || []).sort((a, b) => a.order - b.order);

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-4">
        <div className="space-y-4">
          {sortedCategories.map((category) => (
            <div key={category.id}>
              {/* 카테고리 제목 - 클릭 가능 */}
              <Link
                href={`/contents?category=${category.slug}`}
                className="block px-3 py-2 text-sm font-semibold text-foreground border-b hover:bg-accent transition-colors cursor-pointer"
              >
                {category.name}
              </Link>

              {/* 카테고리의 콘텐츠 */}
              <CategoryContents
                category={category}
                currentPath={pathname}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function CategoryContents({ category, currentPath }: {
  category: Category;
  currentPath: string;
}) {
  const { data, isLoading } = useContents({ category: category.slug });

  if (isLoading) {
    return (
      <div className="ml-3 space-y-1 mt-2">
        <Skeleton className="h-6 w-full" />
        <Skeleton className="h-6 w-full" />
      </div>
    );
  }

  const contents = data?.results || [];

  if (contents.length === 0) {
    return (
      <div className="ml-3 py-2 text-xs text-muted-foreground">
        콘텐츠 없음
      </div>
    );
  }

  return (
    <div className="mt-1 space-y-1">
      {contents.map((content) => {
        const isActive = currentPath === `/contents/${content.slug}`;
        return (
          <Link
            key={content.id}
            href={`/contents/${content.slug}`}
            className={`flex items-start ml-3 px-2 py-1.5 text-xs rounded-md transition-colors ${
              isActive
                ? 'bg-primary text-primary-foreground'
                : 'hover:bg-accent'
            }`}
          >
            <FileText className="h-3 w-3 mr-2 mt-0.5 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="truncate">{content.title}</div>
              <div className="text-[10px] opacity-70 mt-0.5">
                {difficultyLabels[content.difficulty]} · {content.estimated_time}분
              </div>
            </div>
          </Link>
        );
      })}
    </div>
  );
}
