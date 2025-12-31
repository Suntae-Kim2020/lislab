'use client';

import { useParams, useRouter } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useContent, useToggleFavorite } from '@/lib/hooks/useContents';
import { useAuthStore } from '@/store/authStore';
import { CommentList } from '@/components/features/CommentList';
import { TagSearchModal } from '@/components/content/TagSearchModal';
import { QRCodeButton } from '@/components/content/QRCodeButton';
import { PDFSaveButton } from '@/components/content/PDFSaveButton';
import { Heart, Clock, Eye, Calendar, User, GraduationCap } from 'lucide-react';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

const difficultyLabels = {
  BEGINNER: '초급',
  INTERMEDIATE: '중급',
  ADVANCED: '고급',
};

export default function ContentDetailPage() {
  const params = useParams();
  const slug = params.slug as string;
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const contentRef = useRef<HTMLDivElement>(null);
  const pdfContentRef = useRef<HTMLDivElement>(null);

  const [tagModalOpen, setTagModalOpen] = useState(false);
  const [selectedTag, setSelectedTag] = useState('');

  const { data: content, isLoading } = useContent(slug);
  const toggleFavoriteMutation = useToggleFavorite();

  // Extract body content from full HTML documents and check for inline styles
  const getContentInfo = (html: string) => {
    // Check if this is a full HTML document
    const hasFullDocument = html.includes('<!DOCTYPE html>') || html.includes('<html');

    if (hasFullDocument) {
      // Parse the HTML and extract body content only
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const bodyContent = doc.body?.innerHTML || html;
      // Also get inline styles from head if they exist
      const styleElements = doc.head?.querySelectorAll('style');
      let inlineStyles = '';
      if (styleElements) {
        styleElements.forEach((style) => {
          inlineStyles += style.textContent || '';
        });
      }

      // Scope the inline styles to only apply within .custom-content-wrapper
      // This prevents styles like "body", "h1" from affecting the entire page
      if (inlineStyles) {
        // Remove color-related properties from .code-block to allow global CSS to apply
        inlineStyles = inlineStyles.replace(/\.code-block\s*\{[^}]*\}/g, (match) => {
          // Remove background-color and color properties
          return match
            .replace(/background-color:\s*[^;]+;/g, '')
            .replace(/color:\s*[^;]+;/g, '');
        });

        // Remove colors from code syntax highlighting classes
        inlineStyles = inlineStyles.replace(/\.code-block\s+\.(keyword|string|prefix|uri|comment)\s*\{[^}]*\}/g, '');

        // Replace body selector with .custom-content-wrapper
        inlineStyles = inlineStyles.replace(/\bbody\b/g, '.custom-content-wrapper');
        // Prefix all other selectors with .custom-content-wrapper
        // This is a simplified approach - wrap everything in the scoped class
        inlineStyles = `.custom-content-wrapper { ${inlineStyles} }`;
      }

      return {
        content: bodyContent,
        hasInlineStyles: false, // Disable inline styles to use global CSS
        inlineStyles: ''
      };
    }
    return {
      content: html,
      hasInlineStyles: false,
      inlineStyles: ''
    };
  };

  // Execute scripts in content_html
  useEffect(() => {
    if (content && contentRef.current) {
      const scripts = contentRef.current.querySelectorAll('script');
      const addedScripts: HTMLScriptElement[] = [];

      scripts.forEach((script, index) => {
        try {
          const newScript = document.createElement('script');
          if (script.src) {
            newScript.src = script.src;
            newScript.onerror = () => {
              console.error(`Failed to load script from ${script.src}`);
            };
          } else {
            newScript.textContent = script.textContent;
          }
          newScript.async = false;
          document.body.appendChild(newScript);
          addedScripts.push(newScript);
        } catch (error) {
          console.error(`Error executing script ${index + 1} in ${content.slug}:`, error);
          console.error('Script content:', script.textContent?.substring(0, 200));
        }
      });

      // Cleanup
      return () => {
        addedScripts.forEach((script) => {
          if (script.parentNode) {
            script.parentNode.removeChild(script);
          }
        });
      };
    }
  }, [content]);

  const handleToggleFavorite = () => {
    if (!isAuthenticated) {
      alert('로그인이 필요합니다.');
      return;
    }
    toggleFavoriteMutation.mutate(slug);
  };

  const handleAdvancedLearning = () => {
    router.push('/data-model/rdf');
  };

  const handleTagClick = (tagName: string) => {
    setSelectedTag(tagName);
    setTagModalOpen(true);
  };

  if (isLoading) {
    return (
      <div className="container py-8">
        <Skeleton className="h-12 w-3/4 mb-4" />
        <Skeleton className="h-6 w-1/2 mb-8" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  if (!content) {
    return (
      <div className="container py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">콘텐츠를 찾을 수 없습니다</h1>
          <Button onClick={() => window.history.back()}>돌아가기</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div ref={pdfContentRef} className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-start justify-between gap-4 mb-4">
            <h1 className="text-4xl font-bold">{content.title}</h1>
            <div className="flex gap-2">
              <QRCodeButton title={content.title} />
              <PDFSaveButton title={content.title} contentRef={pdfContentRef} />
              {isAuthenticated && (
                <Button
                  variant={content.is_favorited ? 'default' : 'outline'}
                  size="icon"
                  onClick={handleToggleFavorite}
                  disabled={toggleFavoriteMutation.isPending}
                >
                  <Heart className={content.is_favorited ? 'fill-current' : ''} />
                </Button>
              )}
            </div>
          </div>

          <p className="text-lg text-muted-foreground mb-4">{content.summary}</p>

          <div className="flex flex-wrap gap-2 mb-4">
            <Badge>{difficultyLabels[content.difficulty]}</Badge>
            <Badge variant="outline">{content.category_name}</Badge>
            {content.tags.map((tag) => (
              <Badge
                key={tag.id}
                variant="secondary"
                className="cursor-pointer hover:bg-secondary/80 transition-colors"
                onClick={() => handleTagClick(tag.name)}
              >
                {tag.name}
              </Badge>
            ))}
          </div>

          <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <User className="h-4 w-4" />
              <span>{content.author_name}</span>
            </div>
            <div className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              <span>{format(new Date(content.created_at), 'yyyy년 MM월 dd일', { locale: ko })}</span>
            </div>
            <div className="flex items-center gap-1">
              <Eye className="h-4 w-4" />
              <span>{content.view_count.toLocaleString()}회</span>
            </div>
            {content.estimated_time > 0 && (
              <div className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                <span>약 {content.estimated_time}분</span>
              </div>
            )}
          </div>
        </div>

        {/* Meta Info Cards */}
        <div className="grid gap-4 mb-8 sm:grid-cols-2">
          {content.prerequisites && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">선수 학습</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{content.prerequisites}</p>
              </CardContent>
            </Card>
          )}

          {content.learning_objectives && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">학습 목표</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{content.learning_objectives}</p>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Main Content */}
        <Card>
          <CardContent className="pt-6">
            {(() => {
              const contentInfo = getContentInfo(content.content_html || '');
              return (
                <>
                  {contentInfo.hasInlineStyles && (
                    <style dangerouslySetInnerHTML={{ __html: contentInfo.inlineStyles }} />
                  )}
                  <div
                    ref={contentRef}
                    className={contentInfo.hasInlineStyles ? 'custom-content-wrapper' : 'prose prose-slate max-w-none dark:prose-invert'}
                    dangerouslySetInnerHTML={{ __html: contentInfo.content }}
                  />
                </>
              );
            })()}
          </CardContent>
        </Card>

        {/* Advanced Learning Button for RDF */}
        {(slug === 'rdf' || slug === 'rdf-interactive') && (
          <div className="mt-6 flex justify-center">
            <Button
              size="lg"
              onClick={handleAdvancedLearning}
              className="gap-2 text-lg px-8 py-6"
            >
              <GraduationCap className="h-5 w-5" />
              RDF 심화학습 시작하기
            </Button>
          </div>
        )}

        {/* Footer Info */}
        <div className="mt-8 p-4 bg-muted rounded-lg">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">버전 {content.version}</span>
            <span className="text-muted-foreground">
              최종 수정: {format(new Date(content.updated_at), 'yyyy.MM.dd HH:mm', { locale: ko })}
            </span>
          </div>
        </div>

        {/* Comments Section */}
        <div className="mt-8">
          <CommentList contentId={content.id} />
        </div>
      </div>

      {/* Tag Search Modal */}
      <TagSearchModal
        open={tagModalOpen}
        onOpenChange={setTagModalOpen}
        tagName={selectedTag}
      />
    </div>
  );
}
