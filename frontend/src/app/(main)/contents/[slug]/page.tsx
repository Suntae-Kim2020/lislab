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
import { ShareButton } from '@/components/content/ShareButton';
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

  // Extract body content and styles from HTML
  const getContentInfo = (html: string) => {
    // Check if content has style tags that need isolation
    const hasStyleTag = html.includes('<style');
    const hasFullDocument = html.includes('<!DOCTYPE html>') || html.includes('<html');

    if (hasStyleTag || hasFullDocument) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');

      // Extract all style tags content
      let inlineStyles = '';
      const allStyles = doc.querySelectorAll('style');
      allStyles.forEach((style) => {
        inlineStyles += style.textContent || '';
      });

      // Get body content, removing style tags from it
      const bodyContent = doc.body?.innerHTML || html;
      // Remove style tags from body content since we extracted them
      const cleanedContent = bodyContent.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');

      return {
        content: cleanedContent,
        inlineStyles: inlineStyles
      };
    }
    return {
      content: html,
      inlineStyles: ''
    };
  };

  // Shadow DOM wrapper component for CSS isolation
  const IsolatedContent = ({ html, styles }: { html: string; styles: string }) => {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
      if (containerRef.current) {
        // Clear existing shadow root if any
        const existingShadow = containerRef.current.shadowRoot;
        if (!existingShadow) {
          const shadow = containerRef.current.attachShadow({ mode: 'open' });

          // Transform CSS for Shadow DOM compatibility
          // :root -> :host (CSS variables)
          // body -> .content-body (body styles)
          let transformedStyles = styles
            .replace(/:root\s*\{/g, ':host {')
            .replace(/\bbody\s*\{/g, '.content-body {');

          // Add base styles for typography
          const baseStyles = `
            :host {
              display: block;
              font-family: inherit;
              line-height: 1.7;
            }
            .content-body {
              color: #1f2a37;
              background: #f5f7fb;
            }
          `;

          shadow.innerHTML = `
            <style>${baseStyles}</style>
            ${transformedStyles ? `<style>${transformedStyles}</style>` : ''}
            <div class="content-body">${html}</div>
          `;
        }
      }
    }, [html, styles]);

    return <div ref={containerRef} className="shadow-content-wrapper" />;
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
              <ShareButton
                title={content.title}
                url={typeof window !== 'undefined' ? window.location.href : ''}
              />
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
              // Use Shadow DOM for CSS isolation when content has inline styles
              if (contentInfo.inlineStyles) {
                return (
                  <div ref={contentRef}>
                    <IsolatedContent html={contentInfo.content} styles={contentInfo.inlineStyles} />
                  </div>
                );
              }
              // Use regular rendering for simple content
              return (
                <div
                  ref={contentRef}
                  className="prose prose-slate max-w-none dark:prose-invert"
                  dangerouslySetInnerHTML={{ __html: contentInfo.content }}
                />
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
