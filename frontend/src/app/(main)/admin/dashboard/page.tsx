'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAdminStatistics } from '@/lib/hooks/useStatistics';
import { useAuthStore } from '@/store/authStore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, FileText, Heart, Eye, TrendingUp, Building2 } from 'lucide-react';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

export default function AdminDashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuthStore();
  const { data: statistics, isLoading, error } = useAdminStatistics();

  useEffect(() => {
    if (!authLoading && (!isAuthenticated || user?.role !== 'ADMIN')) {
      router.push('/');
    }
  }, [isAuthenticated, user, authLoading, router]);

  if (authLoading || isLoading) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Skeleton className="h-12 w-64 mb-8" />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4 text-red-500">오류 발생</h1>
          <p className="text-muted-foreground">통계 데이터를 불러오는데 실패했습니다.</p>
        </div>
      </div>
    );
  }

  if (!statistics || user?.role !== 'ADMIN') {
    return null;
  }

  const { content_statistics, user_statistics } = statistics;

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">관리자 대시보드</h1>
        <p className="text-muted-foreground">시스템 통계 및 현황을 확인하세요.</p>
      </div>

      {/* 주요 지표 카드 */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">전체 회원</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{user_statistics.total_users}</div>
            <p className="text-xs text-muted-foreground mt-1">
              이번 달 +{user_statistics.new_users_this_month}명
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">신규 회원</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{user_statistics.new_users_this_month}</div>
            <p className="text-xs text-muted-foreground mt-1">이번 달</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">인기 콘텐츠</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {content_statistics.top_favorited[0]?.favorite_count || 0}
            </div>
            <p className="text-xs text-muted-foreground mt-1">최다 즐겨찾기</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">조회수</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {content_statistics.top_viewed[0]?.view_count || 0}
            </div>
            <p className="text-xs text-muted-foreground mt-1">최다 조회</p>
          </CardContent>
        </Card>
      </div>

      {/* 차트 및 상세 통계 */}
      <div className="grid gap-6 md:grid-cols-2 mb-8">
        {/* 월별 회원 등록 */}
        <Card>
          <CardHeader>
            <CardTitle>월별 회원 등록</CardTitle>
            <CardDescription>최근 12개월 회원 가입 추이</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={user_statistics.monthly_registrations}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8884d8" name="가입 수" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* 직업별 회원 분포 */}
        <Card>
          <CardHeader>
            <CardTitle>직업별 회원 분포</CardTitle>
            <CardDescription>사용자 유형별 통계</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={user_statistics.users_by_type as any}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry: any) => `${entry.label}: ${entry.count}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {user_statistics.users_by_type.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* 테이블 통계 */}
      <div className="grid gap-6 md:grid-cols-2 mb-8">
        {/* 인기 콘텐츠 - 즐겨찾기 */}
        <Card>
          <CardHeader>
            <CardTitle>인기 콘텐츠 (즐겨찾기)</CardTitle>
            <CardDescription>가장 많이 즐겨찾기된 콘텐츠</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {content_statistics.top_favorited.slice(0, 5).map((content, index) => (
                <div key={content.id} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-muted-foreground">#{index + 1}</span>
                    <span className="text-sm">{content.title}</span>
                  </div>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Heart className="h-3 w-3" />
                    {content.favorite_count}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* 인기 콘텐츠 - 조회수 */}
        <Card>
          <CardHeader>
            <CardTitle>인기 콘텐츠 (조회수)</CardTitle>
            <CardDescription>가장 많이 조회된 콘텐츠</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {content_statistics.top_viewed.slice(0, 5).map((content, index) => (
                <div key={content.id} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-muted-foreground">#{index + 1}</span>
                    <span className="text-sm">{content.title}</span>
                  </div>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Eye className="h-3 w-3" />
                    {content.view_count}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 추가 통계 */}
      <div className="grid gap-6 md:grid-cols-2 mb-8">
        {/* 기관별 회원 수 */}
        <Card>
          <CardHeader>
            <CardTitle>기관별 회원 수</CardTitle>
            <CardDescription>상위 10개 기관</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {user_statistics.users_by_organization.slice(0, 10).map((org, index) => (
                <div key={index} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div className="flex items-center gap-2">
                    <Building2 className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">{org.organization}</span>
                  </div>
                  <span className="text-sm font-medium">{org.count}명</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* 최근 활동 회원 */}
        <Card>
          <CardHeader>
            <CardTitle>최근 활동 회원</CardTitle>
            <CardDescription>최근 로그인한 회원</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {user_statistics.most_active_users.slice(0, 10).map((user) => (
                <div key={user.id} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div>
                    <div className="text-sm font-medium">{user.username}</div>
                    <div className="text-xs text-muted-foreground">{user.email}</div>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {user.last_login ? new Date(user.last_login).toLocaleDateString('ko-KR') : '-'}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 가장 왕성한 활동 회원 */}
      <Card>
        <CardHeader>
          <CardTitle>가장 왕성한 활동 회원</CardTitle>
          <CardDescription>게시글, 답글, 즐겨찾기를 종합한 활동 점수</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {user_statistics.most_active_contributors.slice(0, 10).map((user, index) => (
              <div key={user.id} className="flex items-start gap-4 p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors">
                <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-primary-foreground font-bold flex-shrink-0">
                  {index + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-bold text-base">{user.full_name}</span>
                        <span className="text-sm text-muted-foreground">({user.username})</span>
                        <span className="text-xs text-muted-foreground px-2 py-0.5 bg-muted rounded">
                          {user.user_type === 'STUDENT' ? '학생' :
                           user.user_type === 'PROFESSOR' ? '교수/연구자' :
                           user.user_type === 'JOB_SEEKER' ? '취업준비생' : '기타'}
                        </span>
                      </div>
                      <div className="text-sm text-muted-foreground mb-1">{user.email}</div>
                      <div className="flex items-center gap-1 text-sm text-muted-foreground">
                        <Building2 className="h-3 w-3" />
                        <span>{user.organization}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-center">
                        <div className="font-semibold text-blue-600">{user.post_count}</div>
                        <div className="text-xs text-muted-foreground">게시글</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold text-green-600">{user.reply_count}</div>
                        <div className="text-xs text-muted-foreground">답글</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold text-red-600">{user.favorite_count}</div>
                        <div className="text-xs text-muted-foreground">즐겨찾기</div>
                      </div>
                      <div className="text-center ml-2 pl-2 border-l">
                        <div className="font-bold text-2xl text-primary">{user.activity_score}</div>
                        <div className="text-xs text-muted-foreground">총점</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
