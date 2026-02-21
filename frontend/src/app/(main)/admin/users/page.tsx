'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/store/authStore';
import { getUsers, User } from '@/lib/api/auth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Input } from '@/components/ui/input';
import { Users } from 'lucide-react';

const USER_TYPE_LABELS: Record<string, string> = {
  STUDENT: '학생',
  PROFESSOR: '교수/연구자',
  JOB_SEEKER: '취업준비생',
  OTHER: '기타',
};

const ROLE_LABELS: Record<string, string> = {
  GUEST: '비회원',
  USER: '일반회원',
  ADMIN: '관리자',
};

const SOCIAL_LABELS: Record<string, string> = {
  NONE: '일반',
  KAKAO: '카카오',
  GOOGLE: '구글',
  NAVER: '네이버',
};

export default function AdminUsersPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuthStore();
  const [search, setSearch] = useState('');

  const { data: users, isLoading, error } = useQuery({
    queryKey: ['adminUsers'],
    queryFn: getUsers,
    enabled: isAuthenticated && user?.role === 'ADMIN',
  });

  useEffect(() => {
    if (!authLoading && (!isAuthenticated || user?.role !== 'ADMIN')) {
      router.push('/');
    }
  }, [isAuthenticated, user, authLoading, router]);

  if (authLoading || isLoading) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Skeleton className="h-12 w-64 mb-8" />
        <Skeleton className="h-96" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4 text-red-500">오류 발생</h1>
          <p className="text-muted-foreground">사용자 목록을 불러오는데 실패했습니다.</p>
        </div>
      </div>
    );
  }

  if (!users || user?.role !== 'ADMIN') {
    return null;
  }

  const filteredUsers = users.filter((u) => {
    const term = search.toLowerCase();
    const fullName = `${u.last_name}${u.first_name}`.toLowerCase();
    return (
      fullName.includes(term) ||
      u.username.toLowerCase().includes(term) ||
      u.email.toLowerCase().includes(term) ||
      (u.organization || '').toLowerCase().includes(term)
    );
  });

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">사용자 목록</h1>
        <p className="text-muted-foreground">전체 회원 목록을 조회합니다.</p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                전체 회원
                <Badge variant="secondary">{filteredUsers.length}명</Badge>
              </CardTitle>
              <CardDescription>이름, 아이디, 이메일, 소속으로 검색할 수 있습니다.</CardDescription>
            </div>
          </div>
          <Input
            placeholder="검색..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="max-w-sm mt-4"
          />
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[60px]">번호</TableHead>
                <TableHead>이름</TableHead>
                <TableHead>아이디</TableHead>
                <TableHead>이메일</TableHead>
                <TableHead>유형</TableHead>
                <TableHead>소속</TableHead>
                <TableHead>역할</TableHead>
                <TableHead>가입방식</TableHead>
                <TableHead>가입일</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredUsers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={9} className="text-center text-muted-foreground py-8">
                    {search ? '검색 결과가 없습니다.' : '등록된 회원이 없습니다.'}
                  </TableCell>
                </TableRow>
              ) : (
                filteredUsers.map((u, index) => (
                  <TableRow key={u.id}>
                    <TableCell className="text-muted-foreground">{index + 1}</TableCell>
                    <TableCell className="font-medium">
                      {u.last_name || u.first_name
                        ? `${u.last_name}${u.first_name}`
                        : '-'}
                    </TableCell>
                    <TableCell>{u.username}</TableCell>
                    <TableCell>{u.email}</TableCell>
                    <TableCell>
                      <Badge variant="outline">
                        {USER_TYPE_LABELS[u.user_type] || u.user_type}
                      </Badge>
                    </TableCell>
                    <TableCell>{u.organization || '-'}</TableCell>
                    <TableCell>
                      <Badge variant={u.role === 'ADMIN' ? 'default' : 'secondary'}>
                        {ROLE_LABELS[u.role] || u.role}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {SOCIAL_LABELS[u.social_provider || 'NONE'] || u.social_provider}
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {new Date(u.created_at).toLocaleDateString('ko-KR')}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
