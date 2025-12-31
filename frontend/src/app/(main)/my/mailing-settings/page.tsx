'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Checkbox } from '@/components/ui/checkbox';
import { Skeleton } from '@/components/ui/skeleton';
import { useAuthStore } from '@/store/authStore';
import { Mail, Check, AlertCircle } from 'lucide-react';

interface Category {
  id: number;
  name: string;
  slug: string;
  parent?: number;
}

interface MailingPreference {
  id: number;
  enabled: boolean;
  frequency: 'IMMEDIATE' | 'WEEKLY' | 'MONTHLY';
  all_categories: boolean;
  selected_categories: Array<{ id: number; name: string; slug: string }>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function MailingSettingsPage() {
  const router = useRouter();
  const { isAuthenticated, token } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [categories, setCategories] = useState<Category[]>([]);
  const [preferences, setPreferences] = useState<MailingPreference>({
    id: 0,
    enabled: false,
    frequency: 'WEEKLY',
    all_categories: false,
    selected_categories: []
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchData();
  }, [isAuthenticated]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all categories (handle pagination)
      let allCategories: Category[] = [];
      let nextUrl: string | null = `${API_BASE_URL}/api/contents/categories/?page_size=100`;

      while (nextUrl) {
        const categoriesRes = await fetch(nextUrl);

        if (!categoriesRes.ok) {
          throw new Error(`카테고리 조회 실패 (${categoriesRes.status})`);
        }

        const categoriesData = await categoriesRes.json();

        if (Array.isArray(categoriesData)) {
          allCategories = categoriesData;
          break;
        } else {
          allCategories = [...allCategories, ...(categoriesData.results || [])];
          nextUrl = categoriesData.next;
        }
      }

      setCategories(allCategories);

      // Fetch mailing preferences
      const prefsRes = await fetch(`${API_BASE_URL}/api/accounts/mailing-preferences/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!prefsRes.ok) {
        throw new Error(`메일링 설정 조회 실패 (${prefsRes.status})`);
      }

      const prefsData = await prefsRes.json();
      setPreferences(prefsData);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(err instanceof Error ? err.message : '데이터 로딩 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setError(null);
      setSaved(false);

      const selectedCategoryIds = preferences.selected_categories.map(c => c.id);

      const response = await fetch(`${API_BASE_URL}/api/accounts/mailing-preferences/${preferences.id}/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          enabled: preferences.enabled,
          frequency: preferences.frequency,
          all_categories: preferences.all_categories,
          selected_category_ids: selectedCategoryIds,
        }),
      });

      if (!response.ok) {
        throw new Error('설정 저장 실패');
      }

      const data = await response.json();
      setPreferences(data);
      setSaved(true);

      // Hide success message after 3 seconds
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error('Error saving preferences:', err);
      setError(err instanceof Error ? err.message : '설정 저장 중 오류가 발생했습니다.');
    } finally {
      setSaving(false);
    }
  };

  const toggleCategory = (category: Category) => {
    const isSelected = preferences.selected_categories.some(c => c.id === category.id);

    if (isSelected) {
      setPreferences({
        ...preferences,
        selected_categories: preferences.selected_categories.filter(c => c.id !== category.id)
      });
    } else {
      setPreferences({
        ...preferences,
        selected_categories: [...preferences.selected_categories, {
          id: category.id,
          name: category.name,
          slug: category.slug
        }]
      });
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-8 px-4 max-w-4xl">
        <Skeleton className="h-12 w-64 mb-6" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">메일링 설정</h1>
        <p className="text-muted-foreground">
          새로운 콘텐츠 업데이트를 이메일로 받아보세요
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-destructive/10 text-destructive rounded-lg flex items-center gap-2">
          <AlertCircle className="h-5 w-5" />
          <p>{error}</p>
        </div>
      )}

      {saved && (
        <div className="mb-6 p-4 bg-green-50 text-green-800 rounded-lg flex items-center gap-2">
          <Check className="h-5 w-5" />
          <p>설정이 저장되었습니다</p>
        </div>
      )}

      <div className="space-y-6">
        {/* Enable/Disable Mailing */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Mail className="h-5 w-5" />
              메일링 수신 설정
            </CardTitle>
            <CardDescription>
              이메일 알림을 받으시려면 활성화해주세요
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <Switch
                id="enabled"
                checked={preferences.enabled}
                onCheckedChange={(checked) => setPreferences({ ...preferences, enabled: checked })}
              />
              <Label htmlFor="enabled" className="cursor-pointer">
                {preferences.enabled ? '메일링 활성화됨' : '메일링 비활성화됨'}
              </Label>
            </div>
          </CardContent>
        </Card>

        {/* Frequency */}
        {preferences.enabled && (
          <Card>
            <CardHeader>
              <CardTitle>발송 빈도</CardTitle>
              <CardDescription>
                이메일을 얼마나 자주 받으시겠습니까?
              </CardDescription>
            </CardHeader>
            <CardContent>
              <RadioGroup
                value={preferences.frequency}
                onValueChange={(value) => setPreferences({ ...preferences, frequency: value as any })}
              >
                <div className="flex items-center space-x-2 mb-3">
                  <RadioGroupItem value="IMMEDIATE" id="immediate" />
                  <Label htmlFor="immediate" className="cursor-pointer">
                    즉시 (콘텐츠 발행 시)
                  </Label>
                </div>
                <div className="flex items-center space-x-2 mb-3">
                  <RadioGroupItem value="WEEKLY" id="weekly" />
                  <Label htmlFor="weekly" className="cursor-pointer">
                    <span className="font-semibold">주간 다이제스트</span> (월요일, 추천)
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="MONTHLY" id="monthly" />
                  <Label htmlFor="monthly" className="cursor-pointer">
                    월간 다이제스트 (매월 1일)
                  </Label>
                </div>
              </RadioGroup>
            </CardContent>
          </Card>
        )}

        {/* Category Selection */}
        {preferences.enabled && (
          <Card>
            <CardHeader>
              <CardTitle>상위 카테고리</CardTitle>
              <CardDescription>
                관심 있는 상위 카테고리를 선택하세요
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2 mb-4 p-4 bg-muted rounded-lg">
                <Checkbox
                  id="all-categories"
                  checked={preferences.all_categories}
                  onCheckedChange={(checked) => setPreferences({
                    ...preferences,
                    all_categories: checked as boolean
                  })}
                />
                <Label htmlFor="all-categories" className="cursor-pointer font-semibold">
                  전체 상위 카테고리 구독
                </Label>
              </div>

              {!preferences.all_categories && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {categories
                    .filter(category => category.parent === category.id)
                    .map((category) => (
                      <div key={category.id} className="flex items-center space-x-2">
                        <Checkbox
                          id={`cat-${category.id}`}
                          checked={preferences.selected_categories.some(c => c.id === category.id)}
                          onCheckedChange={() => toggleCategory(category)}
                        />
                        <Label htmlFor={`cat-${category.id}`} className="cursor-pointer">
                          {category.name}
                        </Label>
                      </div>
                    ))}
                </div>
              )}

              {!preferences.all_categories && preferences.selected_categories.length > 0 && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-800 mb-2">
                    <strong>선택된 카테고리:</strong>
                  </p>
                  <p className="text-sm text-blue-700">
                    {preferences.selected_categories.map(c => c.name).join(', ')}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Save Button */}
        <div className="flex justify-end gap-3">
          <Button variant="outline" onClick={() => router.push('/my')}>
            취소
          </Button>
          <Button onClick={handleSave} disabled={saving}>
            {saving ? '저장 중...' : '설정 저장'}
          </Button>
        </div>
      </div>
    </div>
  );
}
