'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, Clock, Search, BookOpen } from 'lucide-react';

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
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');
  const [popularContents, setPopularContents] = useState<Content[]>([]);
  const [recentContents, setRecentContents] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/contents?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  useEffect(() => {
    const fetchContents = async () => {
      try {
        const headers = { 'Accept': 'application/json' };
        const [popularRes, recentRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/contents/contents/?page_size=6&ordering=-view_count`, { headers }),
          fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/contents/contents/?page_size=6&ordering=-created_at`, { headers })
        ]);

        const popularData = await popularRes.json();
        const recentData = await recentRes.json();

        setPopularContents(popularData.results || []);
        setRecentContents(recentData.results || []);
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

  const ContentCard = ({ content }: { content: Content }) => (
    <Link
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
            {content.category?.name}
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
  );

  return (
    <div className="container mx-auto py-6 px-4">
      {/* 히어로 섹션 - 검색 인터페이스 */}
      <section className="py-12 text-center">
        <div className="flex items-center justify-center gap-3 mb-4">
          <BookOpen className="h-10 w-10 text-primary" />
          <h1 className="text-4xl font-bold">LIS Lab</h1>
        </div>
        <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
          문헌정보학 교육 콘텐츠를 검색하고 학습하세요
        </p>

        {/* 검색 폼 */}
        <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                type="text"
                placeholder="콘텐츠 검색... (예: RDF, 메타데이터, MARC)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 h-12 text-lg"
              />
            </div>
            <Button type="submit" size="lg" className="h-12 px-8">
              검색
            </Button>
          </div>
        </form>

        {/* 빠른 링크 */}
        <div className="flex flex-wrap justify-center gap-2 mt-6">
          <span className="text-sm text-muted-foreground">인기 검색어:</span>
          {['RDF', 'MARC', '메타데이터', 'XML', 'SPARQL'].map((tag) => (
            <Button
              key={tag}
              variant="outline"
              size="sm"
              onClick={() => router.push(`/contents?search=${encodeURIComponent(tag)}`)}
            >
              {tag}
            </Button>
          ))}
        </div>
      </section>

      {loading ? (
        <div className="text-center text-muted-foreground py-12">로딩 중...</div>
      ) : (
        <>
          {/* 인기 콘텐츠 */}
          <section className="py-8">
            <div className="flex items-center gap-2 mb-6">
              <TrendingUp className="h-6 w-6 text-orange-500" />
              <h2 className="text-2xl font-bold">인기 콘텐츠</h2>
            </div>
            {popularContents.length > 0 ? (
              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {popularContents.map((content) => (
                  <ContentCard key={content.id} content={content} />
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-center py-8">콘텐츠가 없습니다.</p>
            )}
          </section>

          {/* 최신 콘텐츠 */}
          <section className="py-8">
            <div className="flex items-center gap-2 mb-6">
              <Clock className="h-6 w-6 text-blue-500" />
              <h2 className="text-2xl font-bold">최신 콘텐츠</h2>
            </div>
            {recentContents.length > 0 ? (
              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {recentContents.map((content) => (
                  <ContentCard key={content.id} content={content} />
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-center py-8">콘텐츠가 없습니다.</p>
            )}
          </section>

          <div className="text-center text-sm text-muted-foreground py-4">
            * 상단 메뉴를 통해서 더 많은 학습자료를 만나세요.
          </div>
        </>
      )}

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
