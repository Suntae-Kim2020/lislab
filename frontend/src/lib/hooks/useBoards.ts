import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { boardsApi, CreatePostRequest, UpdatePostRequest, CreateReplyRequest } from '../api/boards';

// Get all boards
export function useBoards() {
  return useQuery({
    queryKey: ['boards'],
    queryFn: () => boardsApi.getBoards(),
  });
}

// Get posts by board type
export function usePosts(boardType?: string) {
  return useQuery({
    queryKey: ['posts', boardType],
    queryFn: () => boardType ? boardsApi.getPosts(boardType) : boardsApi.getAllPosts(),
  });
}

// Get a single post
export function usePost(id: number, enabled = true) {
  return useQuery({
    queryKey: ['posts', id],
    queryFn: () => boardsApi.getPost(id),
    enabled: !!id && enabled,
    retry: false, // Don't retry on 404 (deleted posts)
  });
}

// Create a new post
export function useCreatePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreatePostRequest) => boardsApi.createPost(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}

// Update a post
export function useUpdatePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdatePostRequest }) =>
      boardsApi.updatePost(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      queryClient.invalidateQueries({ queryKey: ['posts', variables.id] });
    },
  });
}

// Delete a post
export function useDeletePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => boardsApi.deletePost(id),
    onSuccess: (_, id) => {
      // Remove the deleted post's query to prevent 404 refetch
      queryClient.removeQueries({ queryKey: ['posts', id] });
      // Invalidate list queries only (exclude detail queries with numeric id)
      queryClient.invalidateQueries({
        predicate: (query) => {
          const key = query.queryKey;
          return key[0] === 'posts' && (key.length === 1 || typeof key[1] === 'string');
        }
      });
    },
  });
}

// Create a reply
export function useCreateReply() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ postId, data }: { postId: number; data: CreateReplyRequest }) =>
      boardsApi.createReply(postId, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['posts', variables.postId] });
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}

// Update post status
export function useUpdatePostStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ postId, status }: { postId: number; status: string }) =>
      boardsApi.updateStatus(postId, status),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['posts', variables.postId] });
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}
