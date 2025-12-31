'use client';

import { useState } from 'react';
import { Comment } from '@/lib/api/comments';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { MessageSquare, Trash2, Edit, Reply } from 'lucide-react';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { useAuthStore } from '@/store/authStore';

interface CommentItemProps {
  comment: Comment;
  onReply: (parentId: number, text: string) => void;
  onEdit: (id: number, text: string) => void;
  onDelete: (id: number) => void;
  level?: number;
}

export function CommentItem({ comment, onReply, onEdit, onDelete, level = 0 }: CommentItemProps) {
  const { user } = useAuthStore();
  const [isReplying, setIsReplying] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [editContent, setEditContent] = useState(comment.text);

  const isOwner = user?.id === comment.author;
  const isAdmin = user?.role === 'ADMIN';
  const canDelete = isOwner || isAdmin;
  const canEdit = isOwner;

  if (comment.is_deleted) {
    return (
      <div className={`${level > 0 ? 'ml-6 mt-2' : 'mt-2'}`}>
        <div className="p-2 bg-muted/50 rounded-lg border border-dashed">
          <p className="text-sm text-muted-foreground">삭제된 댓글입니다.</p>
        </div>
        {comment.replies && comment.replies.length > 0 && (
          <div className="mt-1">
            {comment.replies.map((reply) => (
              <CommentItem
                key={reply.id}
                comment={reply}
                onReply={onReply}
                onEdit={onEdit}
                onDelete={onDelete}
                level={level + 1}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  if (comment.is_hidden && !isAdmin) {
    return (
      <div className={`${level > 0 ? 'ml-6 mt-2' : 'mt-2'}`}>
        <div className="p-2 bg-muted/50 rounded-lg border border-dashed">
          <p className="text-sm text-muted-foreground">숨김 처리된 댓글입니다.</p>
        </div>
      </div>
    );
  }

  const handleSubmitReply = () => {
    if (replyContent.trim()) {
      onReply(comment.id, replyContent);
      setReplyContent('');
      setIsReplying(false);
    }
  };

  const handleSubmitEdit = () => {
    if (editContent.trim() && editContent !== comment.text) {
      onEdit(comment.id, editContent);
      setIsEditing(false);
    }
  };

  const handleCancelEdit = () => {
    setEditContent(comment.text);
    setIsEditing(false);
  };

  return (
    <div className={`${level > 0 ? 'ml-6 mt-2' : 'mt-2'}`}>
      <div className={`p-3 rounded-lg border ${comment.is_hidden ? 'bg-yellow-50 border-yellow-200' : 'bg-card'}`}>
        {/* Comment Header */}
        <div className="flex items-center justify-between mb-1.5">
          <div className="flex items-center gap-2">
            <span className="font-medium text-sm">{comment.author_name}</span>
            {comment.is_admin_reply && (
              <Badge variant="default" className="text-xs">
                관리자
              </Badge>
            )}
            {comment.is_hidden && isAdmin && (
              <Badge variant="destructive" className="text-xs">
                숨김
              </Badge>
            )}
            <span className="text-xs text-muted-foreground">
              {format(new Date(comment.created_at), 'yyyy.MM.dd HH:mm', { locale: ko })}
            </span>
            {comment.created_at !== comment.updated_at && (
              <span className="text-xs text-muted-foreground">(수정됨)</span>
            )}
          </div>
          <div className="flex items-center gap-1">
            {canEdit && !isEditing && (
              <Button variant="ghost" size="sm" onClick={() => setIsEditing(true)}>
                <Edit className="h-4 w-4" />
              </Button>
            )}
            {canDelete && (
              <Button variant="ghost" size="sm" onClick={() => onDelete(comment.id)}>
                <Trash2 className="h-4 w-4 text-destructive" />
              </Button>
            )}
          </div>
        </div>

        {/* Comment Content */}
        {isEditing ? (
          <div className="space-y-2">
            <Textarea
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              className="min-h-[60px]"
            />
            <div className="flex gap-2">
              <Button size="sm" onClick={handleSubmitEdit}>
                수정
              </Button>
              <Button size="sm" variant="outline" onClick={handleCancelEdit}>
                취소
              </Button>
            </div>
          </div>
        ) : (
          <p className="text-sm whitespace-pre-wrap mb-2">{comment.text}</p>
        )}

        {/* Reply Button */}
        {!isEditing && level < 2 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsReplying(!isReplying)}
            className="text-muted-foreground"
          >
            <Reply className="h-4 w-4 mr-1" />
            답글
          </Button>
        )}

        {/* Reply Form */}
        {isReplying && (
          <div className="mt-2 space-y-2">
            <Textarea
              placeholder="답글을 입력하세요..."
              value={replyContent}
              onChange={(e) => setReplyContent(e.target.value)}
              className="min-h-[60px]"
            />
            <div className="flex gap-2">
              <Button size="sm" onClick={handleSubmitReply}>
                답글 작성
              </Button>
              <Button size="sm" variant="outline" onClick={() => setIsReplying(false)}>
                취소
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Nested Replies */}
      {comment.replies && comment.replies.length > 0 && (
        <div className="mt-1">
          {comment.replies.map((reply) => (
            <CommentItem
              key={reply.id}
              comment={reply}
              onReply={onReply}
              onEdit={onEdit}
              onDelete={onDelete}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}
