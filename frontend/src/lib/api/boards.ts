import { apiClient } from './client';

export interface Board {
  id: number;
  name: string;
  board_type: 'NOTICE' | 'REQUEST' | 'QNA';
  description: string;
  is_active: boolean;
  created_at: string;
}

export interface Post {
  id: number;
  board: number;
  board_name: string;
  board_type: string;
  author: number;
  author_name: string;
  title: string;
  content: string;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'REJECTED' | 'PUBLISHED';
  is_pinned: boolean;
  view_count: number;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
  admin_replies?: PostReply[];
}

export interface PostReply {
  id: number;
  post: number;
  author: number;
  author_name: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface CreatePostRequest {
  board_type: string;
  title: string;
  content: string;
}

export interface UpdatePostRequest {
  title?: string;
  content?: string;
  status?: string;
}

export interface CreateReplyRequest {
  content: string;
}

export const boardsApi = {
  // Get all boards
  getBoards: async (): Promise<Board[]> => {
    const response = await apiClient.get<{ results: Board[] }>('/boards/');
    return response.data.results;
  },

  // Get posts by board type
  getPosts: async (boardType: string): Promise<Post[]> => {
    const response = await apiClient.get<{ results: Post[] }>('/boards/posts/', {
      params: { board_type: boardType },
    });
    return response.data.results;
  },

  // Get all posts (for boards list page)
  getAllPosts: async (): Promise<Post[]> => {
    const response = await apiClient.get<{ results: Post[] }>('/boards/posts/');
    return response.data.results;
  },

  // Get a single post
  getPost: async (id: number): Promise<Post> => {
    const response = await apiClient.get<Post>(`/boards/posts/${id}/`);
    return response.data;
  },

  // Create a new post
  createPost: async (data: CreatePostRequest): Promise<Post> => {
    const response = await apiClient.post<Post>('/boards/posts/', data);
    return response.data;
  },

  // Update a post
  updatePost: async (id: number, data: UpdatePostRequest): Promise<Post> => {
    const response = await apiClient.patch<Post>(`/boards/posts/${id}/`, data);
    return response.data;
  },

  // Delete a post (soft delete)
  deletePost: async (id: number): Promise<void> => {
    await apiClient.delete(`/boards/posts/${id}/`);
  },

  // Create a reply (admin only)
  createReply: async (postId: number, data: CreateReplyRequest): Promise<PostReply> => {
    const response = await apiClient.post<PostReply>(`/boards/posts/${postId}/reply/`, data);
    return response.data;
  },

  // Update status (admin only)
  updateStatus: async (postId: number, status: string): Promise<Post> => {
    const response = await apiClient.post<Post>(`/boards/posts/${postId}/update-status/`, { status });
    return response.data;
  },
};
