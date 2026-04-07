'use client';

import { useParams, useRouter } from 'next/navigation';
import { useEffect, useMemo, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useContent, useToggleFavorite } from '@/lib/hooks/useContents';
import { useAuthStore } from '@/store/authStore';
import { CommentList } from '@/components/features/CommentList';
import { LoginRequired } from '@/components/features/LoginRequired';
import { TagSearchModal } from '@/components/content/TagSearchModal';
import { QRCodeButton } from '@/components/content/QRCodeButton';
import { PDFSaveButton } from '@/components/content/PDFSaveButton';
import { ShareButton } from '@/components/content/ShareButton';
import { Heart, Clock, Eye, Calendar, User, GraduationCap, Download } from 'lucide-react';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

const difficultyLabels = {
  BEGINNER: '초급',
  INTERMEDIATE: '중급',
  ADVANCED: '고급',
};

// 텍스트를 줄바꿈과 블릿포인트로 렌더링
function FormattedText({ text }: { text: string }) {
  const lines = text.split('\n').filter(line => line.trim());

  // 블릿포인트로 시작하는 줄이 있는지 확인
  const hasBullets = lines.some(line => /^[-•*]\s/.test(line.trim()));

  if (hasBullets) {
    const bulletItems = lines.filter(line => /^[-•*]\s/.test(line.trim()));
    const regularLines = lines.filter(line => !/^[-•*]\s/.test(line.trim()));

    return (
      <div className="text-sm text-muted-foreground space-y-2">
        {regularLines.length > 0 && (
          <p>{regularLines.join(' ')}</p>
        )}
        <ul className="list-disc list-inside space-y-1">
          {bulletItems.map((line, i) => (
            <li key={i}>{line.replace(/^[-•*]\s/, '')}</li>
          ))}
        </ul>
      </div>
    );
  }

  // 블릿포인트 없으면 줄바꿈만 유지
  return (
    <div className="text-sm text-muted-foreground whitespace-pre-line">
      {text}
    </div>
  );
}

export default function ContentDetailPage() {
  return (
    <LoginRequired>
      <ContentDetailPageInner />
    </LoginRequired>
  );
}

function ContentDetailPageInner() {
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

  // Check if content needs full isolation (has its own styles/layout)
  const needsIsolation = (html: string) => {
    const hasStyleTag = html.includes('<style');
    const hasFullDocument = html.includes('<!DOCTYPE html>') || html.includes('<html');
    const hasInlineStyles = (html.match(/style\s*=\s*["'][^"']{20,}/g) || []).length >= 3;
    return hasStyleTag || hasFullDocument || hasInlineStyles;
  };

  // Iframe-based isolation - renders original HTML exactly as-is
  const IsolatedContent = ({ html }: { html: string }) => {
    const iframeRef = useRef<HTMLIFrameElement>(null);

    const resizeScript = `<script>
function notifyHeight(){window.parent.postMessage({type:'iframe-resize',height:document.documentElement.scrollHeight},'*')}
new ResizeObserver(notifyHeight).observe(document.body);
window.addEventListener('load',notifyHeight);
notifyHeight();
document.addEventListener('click',function(e){
  var a=e.target.closest('a');
  if(a){
    var href=a.getAttribute('href');
    if(href&&href.startsWith('#')){e.preventDefault();var t=document.getElementById(href.substring(1));if(t)t.scrollIntoView({behavior:'smooth',block:'start'});}
    else if(href&&!href.startsWith('#')&&!href.startsWith('javascript')){e.preventDefault();window.open(href,'_blank');}
  }
});
<\/script>`;

    // Build a proper HTML document from the content
    const fullHtml = useMemo(() => {
      // If content already has full document structure, inject resize script
      if (html.includes('<!DOCTYPE') || html.includes('<html')) {
        if (html.includes('</body>')) {
          return html.replace(/<\/body>/i, resizeScript + '</body>');
        }
        return html + resizeScript;
      }

      // Parse head-level elements (meta, link, style, title) vs body content
      // These tags should go in <head> for proper rendering (fonts, CSS, etc.)
      const headTags: string[] = [];
      let bodyContent = html;

      // Extract <meta>, <title>, <link>, <style> tags that appear before body content
      const headTagRegex = /^(\s*(<(meta|title|link|style)[^>]*(?:\/>|>(?:[\s\S]*?)<\/\3>))\s*)+/i;
      const headMatch = bodyContent.match(headTagRegex);

      if (!headMatch) {
        // Fallback: extract individual head-level tags from anywhere in the content
        const tagPatterns = [
          /<meta[^>]*\/?>/gi,
          /<title[^>]*>[\s\S]*?<\/title>/gi,
          /<link[^>]*\/?>/gi,
          /<style[^>]*>[\s\S]*?<\/style>/gi,
        ];
        for (const pattern of tagPatterns) {
          const matches = bodyContent.match(pattern);
          if (matches) {
            headTags.push(...matches);
            bodyContent = bodyContent.replace(pattern, '');
          }
        }
      } else {
        // Extract matched head tags and remove from body
        const headSection = headMatch[0];
        bodyContent = bodyContent.slice(headSection.length);

        const individualTags = headSection.match(/<(meta|title|link|style)[^>]*(?:\/>|>[\s\S]*?<\/\1>)/gi);
        if (individualTags) {
          headTags.push(...individualTags);
        }
      }

      return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
${headTags.join('\n')}
</head>
<body>
${bodyContent}
${resizeScript}
</body>
</html>`;
    }, [html]);

    useEffect(() => {
      const handleMessage = (e: MessageEvent) => {
        if (e.data?.type === 'iframe-resize' && iframeRef.current) {
          iframeRef.current.style.height = e.data.height + 'px';
        }
      };
      window.addEventListener('message', handleMessage);
      return () => window.removeEventListener('message', handleMessage);
    }, []);

    return (
      <iframe
        ref={iframeRef}
        srcDoc={fullHtml}
        style={{ width: '100%', border: 'none', minHeight: '200px', overflow: 'hidden' }}
        sandbox="allow-scripts allow-popups"
        scrolling="no"
        title="content"
      />
    );
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

  const isIsolated = needsIsolation(content.content_html || '');

  return (
    <>
      {/* Header - always in container */}
      <div className="container mx-auto py-8 px-4">
        <div ref={pdfContentRef} className="max-w-6xl mx-auto">
          <div className="mb-8">
            <div className="flex items-start justify-between gap-4 mb-4">
              <h1 className="text-4xl font-bold">{content.title}</h1>
              <div className="flex gap-2">
                <ShareButton
                  title={content.title}
                  url={typeof window !== 'undefined' ? window.location.href : ''}
                />
                <QRCodeButton title={content.title} />
                <PDFSaveButton title={content.title} contentRef={pdfContentRef} rawHtml={isIsolated ? content.content_html : undefined} />
                {isIsolated && (
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => {
                      const html = content.content_html || '';
                      const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
                      const url = URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = `${content.slug}.html`;
                      a.click();
                      URL.revokeObjectURL(url);
                    }}
                    title="HTML 소스 다운로드"
                  >
                    <Download className="h-4 w-4" />
                  </Button>
                )}
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
              {[...content.tags].sort((a, b) => a.name.localeCompare(b.name)).map((tag) => (
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
            {content.learning_objectives && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">학습 목표</CardTitle>
                </CardHeader>
                <CardContent>
                  <FormattedText text={content.learning_objectives} />
                </CardContent>
              </Card>
            )}

            {content.prerequisites && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">선수 학습</CardTitle>
                </CardHeader>
                <CardContent>
                  <FormattedText text={content.prerequisites} />
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>

      {isIsolated ? (
        <>
          {/* Isolated content: full-width iframe, no container constraint */}
          <div ref={contentRef}>
            <IsolatedContent html={content.content_html || ''} />
          </div>

          {/* Footer and comments back in container */}
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="mt-8 p-4 bg-muted rounded-lg">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">버전 {content.version}</span>
                  <span className="text-muted-foreground">
                    최종 수정: {format(new Date(content.updated_at), 'yyyy.MM.dd HH:mm', { locale: ko })}
                  </span>
                </div>
              </div>

              <div className="mt-8">
                <CommentList contentId={content.id} />
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            {/* Non-isolated content in Card */}
            <Card>
              <CardContent className="pt-6">
                <div
                  ref={contentRef}
                  className="prose prose-slate max-w-none dark:prose-invert"
                  dangerouslySetInnerHTML={{ __html: content.content_html || '' }}
                />
              </CardContent>
            </Card>

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

            <div className="mt-8 p-4 bg-muted rounded-lg">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">버전 {content.version}</span>
                <span className="text-muted-foreground">
                  최종 수정: {format(new Date(content.updated_at), 'yyyy.MM.dd HH:mm', { locale: ko })}
                </span>
              </div>
            </div>

            <div className="mt-8">
              <CommentList contentId={content.id} />
            </div>
          </div>
        </div>
      )}

      {/* Tag Search Modal */}
      <TagSearchModal
        open={tagModalOpen}
        onOpenChange={setTagModalOpen}
        tagName={selectedTag}
      />
    </>
  );
}
