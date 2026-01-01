'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuthStore } from '@/store/authStore';

interface Content {
  id: number;
  title: string;
  slug: string;
  summary: string;
  category: {
    id: number;
    name: string;
    slug: string;
  };
  view_count: number;
  difficulty: string;
  estimated_time: number;
  created_at: string;
  updated_at: string;
}

export default function HomePage() {
  const { isAuthenticated } = useAuthStore();
  const [contents, setContents] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContents = async () => {
      try {
        // 인기 콘텐츠 (조회수 순)와 최신 콘텐츠를 각각 가져오기
        const [popularRes, recentRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/contents/contents/?page_size=6&ordering=-view_count`),
          fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/contents/contents/?page_size=6&ordering=-updated_at`)
        ]);

        const popularData = await popularRes.json();
        const recentData = await recentRes.json();

        // 인기 콘텐츠와 최신 콘텐츠를 합치고 중복 제거
        const allContents = [...popularData.results, ...recentData.results];
        const uniqueContents = Array.from(
          new Map(allContents.map(item => [item.id, item])).values()
        ).slice(0, 9);

        setContents(uniqueContents);
      } catch (error) {
        console.error('Failed to fetch contents:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchContents();
  }, []);

  const getDifficultyLabel = (difficulty: string) => {
    const labels: { [key: string]: string } = {
      'BEGINNER': '초급',
      'INTERMEDIATE': '중급',
      'ADVANCED': '고급'
    };
    return labels[difficulty] || difficulty;
  };

  const getDifficultyColor = (difficulty: string) => {
    const colors: { [key: string]: string } = {
      'BEGINNER': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      'INTERMEDIATE': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      'ADVANCED': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    };
    return colors[difficulty] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="container mx-auto py-6 px-4">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center space-y-4 py-6 text-center">
        <div className="relative w-full max-w-2xl mx-auto p-8 bg-gradient-to-b from-background via-muted/30 to-background rounded-xl">
          <div className="relative">
            <Image
              src="/lis-lab-hero.png"
              alt="LIS Lab - Library & Information Science Learning Platform"
              width={672}
              height={384}
              priority
              className="rounded-lg mx-auto shadow-2xl"
            />
            <div className="absolute inset-0 rounded-lg bg-gradient-to-t from-background/20 via-transparent to-background/20 pointer-events-none"></div>
          </div>
        </div>
        <div className="flex gap-4">
          <Button asChild size="lg">
            <Link href="/contents">콘텐츠 둘러보기</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/register">시작하기</Link>
          </Button>
        </div>
      </section>

      {/* Popular and Recent Contents */}
      <section className="py-12">
        <h2 className="mb-8 text-center text-3xl font-bold">인기 & 최신 학습 콘텐츠</h2>

        {loading ? (
          <div className="text-center text-muted-foreground">로딩 중...</div>
        ) : (
          <>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {contents.map((content) => (
                <Link
                  key={content.id}
                  href={`/contents/${content.slug}`}
                  className="transition-transform hover:scale-105"
                >
                  <Card className="h-full cursor-pointer">
                    <CardHeader>
                      <div className="flex items-center justify-between mb-2">
                        <span className={`text-xs px-2 py-1 rounded ${getDifficultyColor(content.difficulty)}`}>
                          {getDifficultyLabel(content.difficulty)}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          조회 {content.view_count}
                        </span>
                      </div>
                      <CardTitle className="line-clamp-2">{content.title}</CardTitle>
                      <CardDescription>
                        {content.category.name}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground line-clamp-3">
                        {content.summary}
                      </p>
                      {content.estimated_time > 0 && (
                        <p className="text-xs text-muted-foreground mt-2">
                          예상 시간: {content.estimated_time}분
                        </p>
                      )}
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>

            <div className="mt-8 text-center text-sm text-muted-foreground">
              * 콘텐츠 메뉴를 통해서 더 많은 학습자료를 만나세요. ^^
            </div>
          </>
        )}
      </section>

      {/* CTA Section */}
      <section className="flex flex-col items-center justify-center space-y-4 py-12 text-center">
        <h2 className="text-3xl font-bold">지금 시작하세요</h2>
        <p className="max-w-[600px] text-muted-foreground">
          회원가입하고 다양한 교육 콘텐츠를 경험해보세요.
        </p>
        <Button asChild size="lg">
          <Link href="/register">무료 회원가입</Link>
        </Button>
      </section>
    </div>
  );
}
