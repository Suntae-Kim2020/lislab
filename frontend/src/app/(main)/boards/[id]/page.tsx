'use client';

import { useParams, useRouter } from 'next/navigation';
import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { usePost, useCreateReply, useUpdateReply, useDeleteReply, useDeletePost } from '@/lib/hooks/useBoards';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Calendar, Eye, User, ArrowLeft, Pencil, Trash2, X, Check } from 'lucide-react';
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

export default function PostDetailPage() {
  const params = useParams();
  const router = useRouter();
  const queryClient = useQueryClient();
  const id = parseInt(params.id as string);
  const { user, isAuthenticated } = useAuthStore();
  const [replyContent, setReplyContent] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  const [editingReplyId, setEditingReplyId] = useState<number | null>(null);
  const [editingReplyContent, setEditingReplyContent] = useState('');

  const { data: post, isLoading } = usePost(id, !isDeleting);
  const createReplyMutation = useCreateReply();
  const updateReplyMutation = useUpdateReply();
  const deleteReplyMutation = useDeleteReply();
  const deletePostMutation = useDeletePost();

  const handleCreateReply = () => {
    if (!replyContent.trim()) return;

    createReplyMutation.mutate(
      {
        postId: id,
        data: { content: replyContent },
      },
      {
        onSuccess: () => {
          setReplyContent('');
        },
      }
    );
  };

  const handleDelete = () => {
    if (window.confirm('정말 삭제하시겠습니까?')) {
      // Disable query to prevent refetch
      setIsDeleting(true);
      deletePostMutation.mutate(id, {
        onSuccess: () => {
          router.push('/boards');
        },
      });
    }
  };

  const handleEditReply = (replyId: number, content: string) => {
    setEditingReplyId(replyId);
    setEditingReplyContent(content);
  };

  const handleCancelEditReply = () => {
    setEditingReplyId(null);
    setEditingReplyContent('');
  };

  const handleSaveReply = () => {
    if (!editingReplyContent.trim() || !editingReplyId) return;

    updateReplyMutation.mutate(
      {
        postId: id,
        replyId: editingReplyId,
        data: { content: editingReplyContent },
      },
      {
        onSuccess: () => {
          setEditingReplyId(null);
          setEditingReplyContent('');
        },
      }
    );
  };

  const handleDeleteReply = (replyId: number) => {
    if (window.confirm('답변을 삭제하시겠습니까?')) {
      deleteReplyMutation.mutate({ postId: id, replyId });
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <Skeleton className="h-12 w-3/4 mb-4" />
          <Skeleton className="h-6 w-1/2 mb-8" />
          <Skeleton className="h-96 w-full" />
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">게시글을 찾을 수 없습니다</h1>
          <Button onClick={() => router.push('/boards')}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            목록으로
          </Button>
        </div>
      </div>
    );
  }

  const isAuthor = user?.id === post.author;
  const isAdmin = user?.role === 'ADMIN';

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-4xl mx-auto">
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
            <div className="flex items-center gap-2 mb-4">
              <Badge variant="outline">
                {boardTypeLabels[post.board_type as keyof typeof boardTypeLabels]}
              </Badge>
              {post.board_type === 'REQUEST' && (
                <Badge className={statusColors[post.status as keyof typeof statusColors]}>
                  {statusLabels[post.status as keyof typeof statusLabels]}
                </Badge>
              )}
            </div>
            <CardTitle className="text-3xl mb-4">{post.title}</CardTitle>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <User className="h-4 w-4" />
                {post.author_name}
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                {format(new Date(post.created_at), 'yyyy년 MM월 dd일 HH:mm', { locale: ko })}
              </span>
              <span className="flex items-center gap-1">
                <Eye className="h-4 w-4" />
                {post.view_count}
              </span>
            </div>
          </CardHeader>
          <CardContent>
            <div className="prose prose-slate max-w-none dark:prose-invert whitespace-pre-wrap">
              {post.content}
            </div>

            {(isAuthor || isAdmin) && (
              <div className="flex gap-2 mt-6 pt-6 border-t">
                {isAuthor && (
                  <>
                    <Button
                      variant="outline"
                      onClick={() => router.push(`/boards/${id}/edit`)}
                    >
                      수정
                    </Button>
                    <Button
                      variant="destructive"
                      onClick={handleDelete}
                      disabled={deletePostMutation.isPending}
                    >
                      삭제
                    </Button>
                  </>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Admin Replies */}
        {post.admin_replies && post.admin_replies.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-4">관리자 답변</h3>
            <div className="space-y-4">
              {post.admin_replies.map((reply) => (
                <Card key={reply.id} className="bg-blue-50 dark:bg-blue-950">
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Badge>관리자</Badge>
                        <span>{reply.author_name}</span>
                        <span>·</span>
                        <span>{format(new Date(reply.created_at), 'yyyy.MM.dd HH:mm', { locale: ko })}</span>
                        {reply.updated_at !== reply.created_at && (
                          <span className="text-xs">(수정됨)</span>
                        )}
                      </div>
                      {isAdmin && editingReplyId !== reply.id && (
                        <div className="flex gap-1">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEditReply(reply.id, reply.content)}
                          >
                            <Pencil className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteReply(reply.id)}
                            disabled={deleteReplyMutation.isPending}
                          >
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        </div>
                      )}
                    </div>
                    {editingReplyId === reply.id ? (
                      <div className="space-y-3">
                        <Textarea
                          value={editingReplyContent}
                          onChange={(e) => setEditingReplyContent(e.target.value)}
                          className="min-h-[100px]"
                        />
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            onClick={handleSaveReply}
                            disabled={!editingReplyContent.trim() || updateReplyMutation.isPending}
                          >
                            <Check className="h-4 w-4 mr-1" />
                            {updateReplyMutation.isPending ? '저장 중...' : '저장'}
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={handleCancelEditReply}
                          >
                            <X className="h-4 w-4 mr-1" />
                            취소
                          </Button>
                        </div>
                      </div>
                    ) : (
                      <div className="prose prose-slate max-w-none dark:prose-invert whitespace-pre-wrap">
                        {reply.content}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Admin Reply Form */}
        {isAdmin && (
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>관리자 답변 작성</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Textarea
                  placeholder="답변 내용을 입력하세요..."
                  value={replyContent}
                  onChange={(e) => setReplyContent(e.target.value)}
                  className="min-h-[150px]"
                />
                <Button
                  onClick={handleCreateReply}
                  disabled={!replyContent.trim() || createReplyMutation.isPending}
                >
                  {createReplyMutation.isPending ? '작성 중...' : '답변 작성'}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
