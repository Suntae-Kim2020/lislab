'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePosts } from '@/lib/hooks/useBoards';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Calendar, Eye, Pin, User } from 'lucide-react';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

const boardTypeLabels = {
  NOTICE: '공지사항',
  REQUEST: '콘텐츠 개발 요청',
  QNA: '질의응답',
};

const statusLabels = {
  PENDING: '대기',
  IN_PROGRESS: '진행중',
  COMPLETED: '완료',
  REJECTED: '반려',
  PUBLISHED: '공개',
};

const statusColors = {
  PENDING: 'bg-yellow-100 text-yellow-800',
  IN_PROGRESS: 'bg-blue-100 text-blue-800',
  COMPLETED: 'bg-green-100 text-green-800',
  REJECTED: 'bg-red-100 text-red-800',
  PUBLISHED: 'bg-gray-100 text-gray-800',
};

export default function BoardsPage() {
  const [selectedType, setSelectedType] = useState<string>('all');
  const { data: posts, isLoading } = usePosts(selectedType === 'all' ? undefined : selectedType);

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">게시판</h1>
          <Button asChild>
            <Link href="/boards/new">글쓰기</Link>
          </Button>
        </div>

        <Tabs value={selectedType} onValueChange={setSelectedType} className="mb-6">
          <TabsList>
            <TabsTrigger value="all">전체</TabsTrigger>
            <TabsTrigger value="NOTICE">공지사항</TabsTrigger>
            <TabsTrigger value="REQUEST">콘텐츠 개발 요청</TabsTrigger>
            <TabsTrigger value="QNA">질의응답</TabsTrigger>
          </TabsList>
        </Tabs>

        {isLoading ? (
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
              </Card>
            ))}
          </div>
        ) : posts && posts.length > 0 ? (
          <div className="space-y-3">
            {posts.map((post) => (
              <Link key={post.id} href={`/boards/${post.id}`}>
                <Card className="hover:shadow-md transition-shadow cursor-pointer">
                  <CardHeader>
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          {post.is_pinned && (
                            <Pin className="h-4 w-4 text-primary" />
                          )}
                          <Badge variant="outline">
                            {boardTypeLabels[post.board_type as keyof typeof boardTypeLabels]}
                          </Badge>
                          {post.board_type === 'REQUEST' && (
                            <Badge className={statusColors[post.status as keyof typeof statusColors]}>
                              {statusLabels[post.status as keyof typeof statusLabels]}
                            </Badge>
                          )}
                        </div>
                        <CardTitle className="text-xl mb-2">{post.title}</CardTitle>
                        <CardDescription className="flex items-center gap-4 text-sm">
                          <span className="flex items-center gap-1">
                            <User className="h-3 w-3" />
                            {post.author_name}
                          </span>
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {format(new Date(post.created_at), 'yyyy.MM.dd', { locale: ko })}
                          </span>
                          <span className="flex items-center gap-1">
                            <Eye className="h-3 w-3" />
                            {post.view_count}
                          </span>
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                </Card>
              </Link>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12">
              <p className="text-center text-muted-foreground">
                게시글이 없습니다.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
