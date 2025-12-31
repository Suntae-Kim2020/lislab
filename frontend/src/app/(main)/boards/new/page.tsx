'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCreatePost } from '@/lib/hooks/useBoards';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ArrowLeft } from 'lucide-react';

const boardTypes = [
  { value: 'NOTICE', label: '공지사항', adminOnly: true },
  { value: 'REQUEST', label: '콘텐츠 개발 요청', adminOnly: false },
  { value: 'QNA', label: '질의응답', adminOnly: false },
];

export default function NewPostPage() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuthStore();
  const [boardType, setBoardType] = useState('REQUEST');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const createPostMutation = useCreatePost();

  const isAdmin = user?.role === 'ADMIN';

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || !content.trim()) {
      alert('제목과 내용을 입력해주세요.');
      return;
    }

    createPostMutation.mutate(
      {
        board_type: boardType,
        title,
        content,
      },
      {
        onSuccess: (data) => {
          router.push(`/boards/${data.id}`);
        },
        onError: (error) => {
          alert('게시글 작성에 실패했습니다.');
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
          <p className="text-muted-foreground mb-4">
            게시글을 작성하려면 로그인이 필요합니다.
          </p>
          <Button onClick={() => router.push('/login')}>
            로그인하기
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
          onClick={() => router.push('/boards')}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          목록으로
        </Button>

        <Card>
          <CardHeader>
            <CardTitle>게시글 작성</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="boardType">게시판 선택</Label>
                <Select value={boardType} onValueChange={setBoardType}>
                  <SelectTrigger id="boardType">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {boardTypes.map((type) => {
                      if (type.adminOnly && !isAdmin) return null;
                      return (
                        <SelectItem key={type.value} value={type.value}>
                          {type.label}
                        </SelectItem>
                      );
                    })}
                  </SelectContent>
                </Select>
              </div>

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
                <Button type="submit" disabled={createPostMutation.isPending}>
                  {createPostMutation.isPending ? '작성 중...' : '작성하기'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => router.push('/boards')}
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
