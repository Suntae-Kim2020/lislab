import { apiClient } from './client';

export interface ContentStatistic {
  id: number;
  title: string;
  slug: string;
  favorite_count?: number;
  view_count?: number;
}

export interface UserStatistic {
  id: number;
  username: string;
  email: string;
  user_type: string;
  organization?: string;
  created_at?: string;
  last_login?: string;
}

export interface ActiveContributor {
  id: number;
  username: string;
  full_name: string;
  email: string;
  user_type: string;
  organization: string;
  post_count: number;
  reply_count: number;
  favorite_count: number;
  activity_score: number;
}

export interface MonthlyRegistration {
  month: string;
  count: number;
}

export interface UserTypeCount {
  type: string;
  label: string;
  count: number;
}

export interface OrganizationCount {
  organization: string;
  count: number;
}

export interface AdminStatistics {
  content_statistics: {
    top_favorited: ContentStatistic[];
    top_viewed: ContentStatistic[];
  };
  user_statistics: {
    total_users: number;
    new_users_this_month: number;
    recent_new_users: UserStatistic[];
    monthly_registrations: MonthlyRegistration[];
    users_by_type: UserTypeCount[];
    users_by_organization: OrganizationCount[];
    most_active_users: UserStatistic[];
    most_active_contributors: ActiveContributor[];
  };
}

// 관리자 통계 조회
export const getAdminStatistics = async (): Promise<AdminStatistics> => {
  const response = await apiClient.get<AdminStatistics>('/accounts/statistics/');
  return response.data;
};
