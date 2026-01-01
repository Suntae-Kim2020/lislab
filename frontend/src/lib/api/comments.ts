import { apiClient } from './client';

export interface Comment {
  id: number;
  content: number;
  author: number;
  author_name: string;
  parent: number | null;
  text: string;
  url_link?: string;
  is_admin_reply: boolean;
  is_hidden: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
  replies: Comment[];
  can_edit: boolean;
  can_delete: boolean;
}

export interface CreateCommentRequest {
  content: number;
  text: string;
  parent?: number | null;
  url_link?: string;
}

export interface UpdateCommentRequest {
  text: string;
  url_link?: string;
}

export const commentsApi = {
  // Get comments for a content
  getComments: async (contentId: number): Promise<Comment[]> => {
    const response = await apiClient.get<{ results: Comment[] }>(`/comments/`, {
      params: { content_id: contentId },
    });
    return response.data.results;
  },

  // Get a single comment
  getComment: async (id: number): Promise<Comment> => {
    const response = await apiClient.get<Comment>(`/comments/${id}/`);
    return response.data;
  },

  // Create a new comment
  createComment: async (data: CreateCommentRequest): Promise<Comment> => {
    const response = await apiClient.post<Comment>('/comments/', data);
    return response.data;
  },

  // Update a comment
  updateComment: async (id: number, data: UpdateCommentRequest): Promise<Comment> => {
    const response = await apiClient.patch<Comment>(`/comments/${id}/`, data);
    return response.data;
  },

  // Delete a comment (soft delete)
  deleteComment: async (id: number): Promise<void> => {
    await apiClient.delete(`/comments/${id}/`);
  },

  // Get user's comments
  getMyComments: async (): Promise<Comment[]> => {
    const response = await apiClient.get<{ results: Comment[] }>('/comments/my-comments/');
    return response.data.results;
  },
};
