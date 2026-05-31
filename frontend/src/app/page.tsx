'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, Clock, Search } from 'lucide-react';

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
    <div className="h-full overflow-y-auto">
      <div className="container mx-auto py-4 px-4">
        {/* 검색 바 - 컴팩트 */}
        <form onSubmit={handleSearch} className="max-w-xl mx-auto mb-6">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="콘텐츠 검색... (예: RDF, 메타데이터, MARC)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 h-10"
              />
            </div>
            <Button type="submit" className="h-10 px-6">
              검색
            </Button>
          </div>
        </form>

        {loading ? (
          <div className="text-center text-muted-foreground py-8">로딩 중...</div>
        ) : (
        <>
          {/* 최신 콘텐츠 */}
          <section className="py-4">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="h-5 w-5 text-blue-500" />
              <h2 className="text-xl font-bold">최신 콘텐츠</h2>
            </div>
            {recentContents.length > 0 ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {recentContents.map((content) => (
                  <ContentCard key={content.id} content={content} />
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-center py-8">콘텐츠가 없습니다.</p>
            )}
          </section>

          {/* 인기 콘텐츠 */}
          <section className="py-4">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="h-5 w-5 text-orange-500" />
              <h2 className="text-xl font-bold">인기 콘텐츠</h2>
            </div>
            {popularContents.length > 0 ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {popularContents.map((content) => (
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
        <section className="flex flex-col items-center justify-center space-y-3 py-8 text-center">
          <h2 className="text-2xl font-bold">지금 시작하세요</h2>
          <p className="max-w-[600px] text-muted-foreground text-sm">
            회원가입하고 다양한 교육 콘텐츠를 경험해보세요.
          </p>
          <Button asChild>
            <Link href="/register">무료 회원가입</Link>
          </Button>
        </section>
      </div>
    </div>
  );
}
