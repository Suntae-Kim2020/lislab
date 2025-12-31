'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { usePost, useUpdatePost } from '@/lib/hooks/useBoards';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Skeleton } from '@/components/ui/skeleton';
import { ArrowLeft } from 'lucide-react';

export default function EditPostPage() {
  const params = useParams();
  const router = useRouter();
  const id = parseInt(params.id as string);
  const { user, isAuthenticated } = useAuthStore();

  const { data: post, isLoading } = usePost(id);
  const updatePostMutation = useUpdatePost();

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    if (post) {
      setTitle(post.title);
      setContent(post.content);
    }
  }, [post]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || !content.trim()) {
      alert('제목과 내용을 입력해주세요.');
      return;
    }

    updatePostMutation.mutate(
      {
        id,
        data: { title, content },
      },
      {
        onSuccess: () => {
          router.push(`/boards/${id}`);
        },
        onError: (error) => {
          alert('게시글 수정에 실패했습니다.');
          console.error(error);
        },
      }
    );
  };

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">로그인이 필요합니다</h1>
          <Button onClick={() => router.push('/login')}>로그인하기</Button>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-3xl mx-auto">
          <Skeleton className="h-12 w-3/4 mb-4" />
          <Skeleton className="h-96 w-full" />
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">게시글을 찾을 수 없습니다</h1>
          <Button onClick={() => router.push('/boards')}>목록으로</Button>
        </div>
      </div>
    );
  }

  const isAuthor = user?.id === post.author;
  const isAdmin = user?.role === 'ADMIN';

  if (!isAuthor && !isAdmin) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">수정 권한이 없습니다</h1>
          <Button onClick={() => router.push(`/boards/${id}`)}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            돌아가기
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-3xl mx-auto">
        <Button
          variant="outline"
          onClick={() => router.push(`/boards/${id}`)}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          돌아가기
        </Button>

        <Card>
          <CardHeader>
            <CardTitle>게시글 수정</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="title">제목</Label>
                <Input
                  id="title"
                  placeholder="제목을 입력하세요"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="content">내용</Label>
                <Textarea
                  id="content"
                  placeholder="내용을 입력하세요"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  className="min-h-[300px]"
                  required
                />
              </div>

              <div className="flex gap-2">
                <Button type="submit" disabled={updatePostMutation.isPending}>
                  {updatePostMutation.isPending ? '수정 중...' : '수정하기'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => router.push(`/boards/${id}`)}
                >
                  취소
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
