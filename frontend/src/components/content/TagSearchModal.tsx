'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Loader2 } from 'lucide-react';

interface Content {
  id: number;
  title: string;
  slug: string;
  summary: string;
  category: {
    name: string;
  };
  difficulty: string;
  estimated_time: number;
}

interface TagSearchModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  tagName: string;
}

const difficultyLabels: Record<string, string> = {
  BEGINNER: '초급',
  INTERMEDIATE: '중급',
  ADVANCED: '고급',
};

const difficultyColors: Record<string, string> = {
  BEGINNER: 'bg-green-100 text-green-800',
  INTERMEDIATE: 'bg-yellow-100 text-yellow-800',
  ADVANCED: 'bg-red-100 text-red-800',
};

export function TagSearchModal({ open, onOpenChange, tagName }: TagSearchModalProps) {
  const router = useRouter();
  const [contents, setContents] = useState<Content[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open && tagName) {
      fetchContentsByTag();
    }
  }, [open, tagName]);

  const fetchContentsByTag = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/contents/by-tag?tag=${encodeURIComponent(tagName)}`);

      if (!response.ok) {
        throw new Error('태그 검색에 실패했습니다.');
      }

      const data = await response.json();
      setContents(data.results || data);
    } catch (err) {
      console.error('Error fetching contents by tag:', err);
      setError('콘텐츠를 불러오는 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleContentClick = (slug: string) => {
    onOpenChange(false);
    router.push(`/contents/${slug}`);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Badge variant="secondary" className="text-base">
              {tagName}
            </Badge>
            <span>태그가 포함된 콘텐츠</span>
          </DialogTitle>
          <DialogDescription>
            '{tagName}' 태그가 포함된 모든 교육 콘텐츠입니다.
          </DialogDescription>
        </DialogHeader>

        <ScrollArea className="max-h-[60vh] pr-4">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          )}

          {error && (
            <div className="text-center py-8 text-destructive">
              {error}
            </div>
          )}

          {!loading && !error && contents.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              '{tagName}' 태그가 포함된 콘텐츠가 없습니다.
            </div>
          )}

          {!loading && !error && contents.length > 0 && (
            <div className="space-y-3">
              {contents.map((content) => (
                <div
                  key={content.id}
                  onClick={() => handleContentClick(content.slug)}
                  className="p-4 border rounded-lg hover:bg-accent hover:border-primary cursor-pointer transition-all"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-base mb-2 line-clamp-1">
                        {content.title}
                      </h3>
                      <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                        {content.summary}
                      </p>
                      <div className="flex items-center gap-2 flex-wrap">
                        <Badge variant="outline" className="text-xs">
                          {content.category.name}
                        </Badge>
                        <Badge
                          className={`text-xs ${
                            difficultyColors[content.difficulty] || 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {difficultyLabels[content.difficulty] || content.difficulty}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {content.estimated_time}분
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {!loading && !error && contents.length > 0 && (
          <div className="text-sm text-muted-foreground text-center pt-2 border-t">
            총 {contents.length}개의 콘텐츠
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
