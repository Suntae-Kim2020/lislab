'use client';

import { useQuery } from '@tanstack/react-query';
import * as statisticsApi from '@/lib/api/statistics';

// 관리자 통계 조회
export function useAdminStatistics() {
  return useQuery({
    queryKey: ['adminStatistics'],
    queryFn: statisticsApi.getAdminStatistics,
    staleTime: 1000 * 60 * 5, // 5분
  });
}
