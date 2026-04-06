'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FileText } from 'lucide-react';
import { useCategories, useContents } from '@/lib/hooks/useContents';
import { Skeleton } from '@/components/ui/skeleton';
import type { Category, SubCategory } from '@/lib/api/contents';

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
    <div className="p-4">
      <div className="space-y-4">
        {sortedCategories.map((category) => (
          <CategorySection
            key={category.id}
            category={category}
            currentPath={pathname}
          />
        ))}
      </div>
    </div>
  );
}

// 카테고리 섹션 - 콘텐츠나 하위 카테고리가 있는 경우에만 렌더링
function CategorySection({ category, currentPath }: {
  category: Category;
  currentPath: string;
}) {
  const { data, isLoading } = useContents({ category: category.slug, includeChildren: true });

  // 로딩 중이면 스켈레톤 표시
  if (isLoading) {
    return (
      <div>
        <Skeleton className="h-8 w-full mb-2" />
        <Skeleton className="h-6 w-3/4 ml-3" />
      </div>
    );
  }

  const totalContents = data?.results?.length || 0;
  const hasChildren = category.children && category.children.length > 0;

  // 콘텐츠도 없고 하위 카테고리도 없으면 렌더링하지 않음
  if (totalContents === 0 && !hasChildren) {
    return null;
  }

  return (
    <div>
      {/* 카테고리 제목 - 클릭 가능 */}
      <Link
        href={`/contents?category=${category.slug}`}
        className="block px-3 py-2 text-sm font-semibold text-foreground border-b hover:bg-accent transition-colors cursor-pointer"
      >
        {category.name}
      </Link>

      {/* 카테고리의 직접 콘텐츠 */}
      <CategoryContents
        category={category}
        currentPath={currentPath}
      />

      {/* 하위 카테고리 */}
      {hasChildren && (
        <div className="ml-3">
          {category.children
            .sort((a, b) => a.order - b.order)
            .map((sub) => (
              <SubCategorySection
                key={sub.id}
                subCategory={sub}
                currentPath={currentPath}
              />
            ))}
        </div>
      )}
    </div>
  );
}

// 하위 카테고리 섹션 - 콘텐츠가 있는 경우에만 렌더링
function SubCategorySection({ subCategory, currentPath }: {
  subCategory: SubCategory;
  currentPath: string;
}) {
  const { data, isLoading } = useContents({ category: subCategory.slug });

  if (isLoading) {
    return null; // 하위 카테고리는 로딩 중 스켈레톤 생략
  }

  const contents = data?.results || [];

  // 콘텐츠가 없으면 렌더링하지 않음
  if (contents.length === 0) {
    return null;
  }

  return (
    <div>
      <Link
        href={`/contents?category=${subCategory.slug}`}
        className="block px-3 py-1.5 text-xs font-medium text-muted-foreground border-l-2 border-muted hover:bg-accent hover:text-foreground transition-colors cursor-pointer"
      >
        {subCategory.name}
      </Link>
      <ContentList
        contents={contents}
        currentPath={currentPath}
        isSubCategory
      />
    </div>
  );
}

// URL 디코딩 + Unicode 정규화 함수 - 한글 slug 비교를 위해
function normalizeSlug(str: string): string {
  try {
    // URL 인코딩된 경우 디코딩 (%ED%95%9C%EA%B8%80 -> 한글)
    const decoded = decodeURIComponent(str);
    // Unicode NFC 정규화 (NFD -> NFC 변환)
    return decoded.normalize('NFC');
  } catch {
    // 이미 디코딩되었거나 유효하지 않은 경우 정규화만 수행
    return str.normalize('NFC');
  }
}

function ContentList({ contents, currentPath, isSubCategory = false }: {
  contents: Array<{
    id: number;
    title: string;
    slug: string;
    difficulty: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
    estimated_time: number;
  }>;
  currentPath: string;
  isSubCategory?: boolean;
}) {
  const mlClass = isSubCategory ? 'ml-4' : 'ml-3';

  if (contents.length === 0) {
    return null;
  }

  // currentPath를 NFC로 정규화
  const normalizedCurrentPath = normalizeSlug(currentPath);

  return (
    <div className="mt-1 space-y-1">
      {contents.map((content) => {
        // 양쪽 모두 NFC로 정규화하여 비교
        const isActive = normalizedCurrentPath === normalizeSlug(`/contents/${content.slug}`);
        return (
          <Link
            key={content.id}
            href={`/contents/${content.slug}`}
            data-active={isActive ? 'true' : undefined}
            className={`flex items-start ${mlClass} px-2 py-1.5 text-xs rounded-md transition-colors ${
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

function CategoryContents({ category, currentPath }: {
  category: Category;
  currentPath: string;
}) {
  const { data, isLoading } = useContents({ category: category.slug });

  if (isLoading) {
    return null;
  }

  const contents = data?.results || [];

  return (
    <ContentList
      contents={contents}
      currentPath={currentPath}
    />
  );
}
