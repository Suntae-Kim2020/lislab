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

  // 상단 메뉴와 동일한 순서로 카테고리 정렬
  const categoryOrder = [
    'web-docs',
    'web-technology',
    'search-protocol',
    'standard-specifications',
    'conceptual-model',
    'data-model',
    'metadata',
    'ontology',
    'identifier-reference',
    'overview'
  ];

  // 최상위 카테고리만 필터링하고 순서대로 정렬 (parent === id인 카테고리)
  const topLevelCategories = categoryOrder
    .map(slug => categories?.find(cat => cat.slug === slug && cat.parent === cat.id))
    .filter(Boolean) as Category[];

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-4">
        <div className="space-y-4">
          {topLevelCategories.map((category) => (
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
                allCategories={categories || []}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function CategoryContents({ category, currentPath, allCategories }: {
  category: Category;
  currentPath: string;
  allCategories: Category[];
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
  const childCategories = allCategories.filter(cat => cat.parent === category.id);

  if (childCategories.length === 0 && contents.length === 0) {
    return (
      <div className="ml-3 py-2 text-xs text-muted-foreground">
        콘텐츠 없음
      </div>
    );
  }

  return (
    <div className="mt-1 space-y-2">
      {/* 하위 카테고리가 있으면 하위 카테고리만 표시 */}
      {childCategories.length > 0 ? (
        childCategories.map((childCategory) => (
          <div key={childCategory.id}>
            <Link
              href={`/contents?category=${childCategory.slug}`}
              className="block ml-3 px-2 py-1 text-xs font-medium text-muted-foreground hover:bg-accent transition-colors cursor-pointer rounded-md"
            >
              • {childCategory.name}
            </Link>
            <ChildCategoryContents
              categorySlug={childCategory.slug}
              currentPath={currentPath}
            />
          </div>
        ))
      ) : (
        /* 하위 카테고리가 없으면 현재 카테고리의 콘텐츠 표시 */
        contents.map((content) => {
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
        })
      )}
    </div>
  );
}

function ChildCategoryContents({ categorySlug, currentPath }: {
  categorySlug: string;
  currentPath: string;
}) {
  const { data, isLoading } = useContents({ category: categorySlug });

  if (isLoading) {
    return (
      <div className="ml-5 space-y-1">
        <Skeleton className="h-5 w-full" />
      </div>
    );
  }

  const contents = data?.results || [];

  if (contents.length === 0) {
    return null;
  }

  return (
    <div className="space-y-1">
      {contents.map((content) => {
        const isActive = currentPath === `/contents/${content.slug}`;
        return (
          <Link
            key={content.id}
            href={`/contents/${content.slug}`}
            className={`flex items-start ml-5 px-2 py-1.5 text-xs rounded-md transition-colors ${
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
