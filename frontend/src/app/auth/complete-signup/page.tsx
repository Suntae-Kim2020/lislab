'use client';

import { Suspense, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { completeSocialSignup } from '@/lib/api/social-auth';

function CompleteSocialSignupForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const userId = searchParams.get('user_id');

  const [formData, setFormData] = useState({
    email: '',
    user_type: 'STUDENT' as 'STUDENT' | 'PROFESSOR' | 'JOB_SEEKER' | 'OTHER',
    organization: '',
    phone: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!userId) {
      setError('사용자 정보를 찾을 수 없습니다.');
      return;
    }

    // 필수 필드 검증
    if (!formData.email) {
      setError('이메일은 필수 입력 항목입니다.');
      return;
    }

    // 이메일 형식 검증
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('올바른 이메일 형식을 입력해주세요.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await completeSocialSignup({
        user_id: parseInt(userId),
        email: formData.email,
        user_type: formData.user_type,
        organization: formData.organization || undefined,
        phone: formData.phone || undefined,
      });

      // 완료 후 메인 페이지로 이동
      router.push('/');
    } catch (err: any) {
      console.error('Complete signup error:', err);
      setError(err.response?.data?.error || '정보 저장에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };


  if (!userId) {
    return (
      <div className="container flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>오류</CardTitle>
            <CardDescription>사용자 정보를 찾을 수 없습니다.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/login')} className="w-full">
              로그인 페이지로 이동
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container flex items-center justify-center min-h-screen py-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>추가 정보 입력</CardTitle>
          <CardDescription>
            서비스 이용을 위해 추가 정보를 입력해주세요. 모든 필수 항목을 입력해야 합니다.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">이메일 *</Label>
              <Input
                id="email"
                type="email"
                placeholder="example@email.com"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                required
              />
              <p className="text-xs text-muted-foreground">
                신규 콘텐츠 등록 알림을 받을 이메일 주소입니다.
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="user_type">사용자 구분 *</Label>
              <Select
                value={formData.user_type}
                onValueChange={(value: any) =>
                  setFormData({ ...formData, user_type: value })
                }
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="사용자 구분을 선택하세요" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="STUDENT">학생</SelectItem>
                  <SelectItem value="PROFESSOR">교수/연구자</SelectItem>
                  <SelectItem value="JOB_SEEKER">취업준비생</SelectItem>
                  <SelectItem value="OTHER">기타</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="organization">소속기관 (선택)</Label>
              <Input
                id="organization"
                type="text"
                placeholder="예: 한국대학교"
                value={formData.organization}
                onChange={(e) =>
                  setFormData({ ...formData, organization: e.target.value })
                }
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone">연락처 (선택)</Label>
              <Input
                id="phone"
                type="tel"
                placeholder="예: 010-1234-5678"
                value={formData.phone}
                onChange={(e) =>
                  setFormData({ ...formData, phone: e.target.value })
                }
              />
            </div>

            <Button
              type="submit"
              disabled={loading}
              className="w-full"
            >
              {loading ? '저장 중...' : '완료'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

export default function CompleteSocialSignupPage() {
  return (
    <Suspense fallback={
      <div className="container flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-lg">로딩 중...</p>
        </div>
      </div>
    }>
      <CompleteSocialSignupForm />
    </Suspense>
  );
}
