'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Skeleton } from '@/components/ui/skeleton';
import { CommentItem } from './CommentItem';
import { useComments, useCreateComment, useUpdateComment, useDeleteComment } from '@/lib/hooks/useComments';
import { useAuthStore } from '@/store/authStore';
import { MessageSquare } from 'lucide-react';

interface CommentListProps {
  contentId: number;
}

export function CommentList({ contentId }: CommentListProps) {
  const { user, isAuthenticated } = useAuthStore();
  const [newComment, setNewComment] = useState('');

  const { data: comments, isLoading } = useComments(contentId);
  const createCommentMutation = useCreateComment();
  const updateCommentMutation = useUpdateComment();
  const deleteCommentMutation = useDeleteComment();

  const handleSubmitComment = () => {
    if (!newComment.trim()) return;

    createCommentMutation.mutate(
      {
        content: contentId,
        text: newComment,
      },
      {
        onSuccess: () => {
          setNewComment('');
        },
      }
    );
  };

  const handleReply = (parentId: number, text: string) => {
    createCommentMutation.mutate({
      content: contentId,
      text,
      parent: parentId,
    });
  };

  const handleEdit = (id: number, text: string) => {
    updateCommentMutation.mutate({
      id,
      data: { text },
    });
  };

  const handleDelete = (id: number) => {
    if (window.confirm('정말 삭제하시겠습니까?')) {
      deleteCommentMutation.mutate({ id, contentId });
    }
  };

  // Filter out comments that have a parent (they will be shown as nested replies)
  const topLevelComments = comments?.filter((comment) => !comment.parent) || [];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageSquare className="h-5 w-5" />
          댓글 {comments?.length || 0}개
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Comment Form */}
        {isAuthenticated ? (
          <div className="space-y-2 mb-4">
            <Textarea
              placeholder="댓글을 입력하세요..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              className="min-h-[80px]"
            />
            <Button
              onClick={handleSubmitComment}
              disabled={!newComment.trim() || createCommentMutation.isPending}
            >
              {createCommentMutation.isPending ? '작성 중...' : '댓글 작성'}
            </Button>
          </div>
        ) : (
          <div className="mb-4 p-3 bg-muted rounded-lg">
            <p className="text-sm text-muted-foreground text-center">
              댓글을 작성하려면 로그인이 필요합니다.
            </p>
          </div>
        )}

        {/* Comments List */}
        {isLoading ? (
          <div className="space-y-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="space-y-2">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-16 w-full" />
              </div>
            ))}
          </div>
        ) : topLevelComments.length > 0 ? (
          <div className="space-y-2">
            {topLevelComments.map((comment) => (
              <CommentItem
                key={comment.id}
                comment={comment}
                onReply={handleReply}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-muted-foreground">아직 댓글이 없습니다.</p>
            <p className="text-sm text-muted-foreground mt-1">첫 댓글을 작성해보세요!</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
