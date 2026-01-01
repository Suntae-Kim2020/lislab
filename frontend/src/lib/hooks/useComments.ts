import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { commentsApi, CreateCommentRequest, UpdateCommentRequest } from '@/lib/api/comments';

export function useComments(contentId: number) {
  return useQuery({
    queryKey: ['comments', contentId],
    queryFn: () => commentsApi.getComments(contentId),
    enabled: !!contentId,
  });
}

export function useComment(id: number) {
  return useQuery({
    queryKey: ['comment', id],
    queryFn: () => commentsApi.getComment(id),
    enabled: !!id,
  });
}

export function useCreateComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateCommentRequest) => commentsApi.createComment(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['comments', variables.content] });
    },
  });
}

export function useUpdateComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateCommentRequest }) =>
      commentsApi.updateComment(id, data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['comment', data.id] });
      queryClient.invalidateQueries({ queryKey: ['comments', data.content] });
    },
  });
}

export function useDeleteComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, contentId }: { id: number; contentId: number }) => commentsApi.deleteComment(id),
    onSuccess: (_, variables) => {
      // Invalidate the specific content's comments
      queryClient.invalidateQueries({ queryKey: ['comments', variables.contentId] });
      // Also invalidate my-comments list
      queryClient.invalidateQueries({ queryKey: ['my-comments'] });
    },
  });
}

export function useMyComments() {
  return useQuery({
    queryKey: ['my-comments'],
    queryFn: () => commentsApi.getMyComments(),
  });
}
