import { apiClient } from './client';

export interface TeamMember {
  id: number;
  name: string;
  title: string;
  photo: string | null;
  bio: string;
  order: number;
}

export const teamApi = {
  getMembers: async (): Promise<TeamMember[]> => {
    const response = await apiClient.get<TeamMember[]>('/accounts/team-members/');
    return response.data;
  },
};
