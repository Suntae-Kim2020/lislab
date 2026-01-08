'use client';

import { Suspense, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { completeSocialSignup } from '@/lib/api/social-auth';
import { useAuthStore } from '@/store/authStore';

function CompleteSocialSignupForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { user, setUser } = useAuthStore();
  const userId = searchParams.get('user_id');
  const provider = searchParams.get('provider');

  // URL 파라미터에서 소셜 로그인 정보 가져오기
  const prefillEmail = searchParams.get('email') || '';
  const prefillName = searchParams.get('name') || '';
  const prefillPhone = searchParams.get('phone') || '';

  const [formData, setFormData] = useState({
    first_name: prefillName,
    email: prefillEmail,
    user_type: 'STUDENT' as 'STUDENT' | 'PROFESSOR' | 'JOB_SEEKER' | 'OTHER',
    organization: '',
    phone: prefillPhone,
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
    if (!formData.first_name) {
      setError('이름은 필수 입력 항목입니다.');
      return;
    }

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
      const response = await completeSocialSignup({
        user_id: parseInt(userId),
        first_name: formData.first_name,
        email: formData.email,
        user_type: formData.user_type,
        organization: formData.organization || undefined,
        phone: formData.phone || undefined,
      });

      // authStore 업데이트 (수정된 사용자 정보 반영)
      if (user && response.user) {
        setUser({
          ...user,
          first_name: response.user.first_name,
          email: response.user.email,
          user_type: response.user.user_type,
          organization: response.user.organization || '',
          phone: response.user.phone || '',
        });
      }

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
            {prefillName && (
              <span className="block mb-1 font-medium text-foreground">
                안녕하세요, {prefillName}님!
              </span>
            )}
            서비스 이용을 위해 추가 정보를 입력해주세요.
            {provider === 'naver' && prefillEmail && (
              <span className="block mt-1 text-green-600">
                네이버 계정 정보가 자동으로 입력되었습니다.
              </span>
            )}
            {provider === 'google' && prefillEmail && (
              <span className="block mt-1 text-blue-600">
                구글 계정 정보가 자동으로 입력되었습니다.
              </span>
            )}
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
              <Label htmlFor="first_name">이름 *</Label>
              <Input
                id="first_name"
                type="text"
                placeholder="이름을 입력하세요"
                value={formData.first_name}
                onChange={(e) =>
                  setFormData({ ...formData, first_name: e.target.value })
                }
                required
              />
              {provider === 'naver' && prefillName && (
                <p className="text-xs text-green-600">
                  네이버에서 가져온 이름입니다. 필요시 수정 가능합니다.
                </p>
              )}
            </div>

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
