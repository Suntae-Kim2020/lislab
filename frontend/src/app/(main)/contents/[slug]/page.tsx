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
import { Heart, Clock, Eye, Calendar, User, GraduationCap, Download, ArrowLeft } from 'lucide-react';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { useIsMobile } from '@/lib/hooks/useIsMobile';

const difficultyLabels = {
  BEGINNER: '초급',
  INTERMEDIATE: '중급',
  ADVANCED: '고급',
};

// 웹폰트/이미지 지연 로딩 및 vh 단위 콘텐츠에 대응하기 위한 강화된 높이 측정 스크립트.
// 원본 HTML이 이미 iframe-resize postMessage를 쓰고 있으면 주입을 생략한다.
//
// 주의: ResizeObserver(document.body)와 window.resize 리스너는 의도적으로 쓰지 않는다.
// 콘텐츠에 min-height:100vh 같은 vh 단위가 있으면 iframe 리사이즈 → body 크기 변화 →
// 재측정 → 더 큰 높이 전송의 피드백 루프가 발생해 iframe이 무한히 커진다.
// 대신 MutationObserver(실제 DOM 변경), document.fonts.ready(웹폰트),
// 이미지/iframe/video 요소의 load 이벤트(위임), 스케줄된 setTimeout 재측정으로 대응한다.
const HEIGHT_MEASURE_SCRIPT = `<script>
(function(){
  if(window.parent===window) return;
  var lastHeight=0;
  var lastViewport=window.innerHeight;
  var lastViewportChangeAt=0;
  function sendHeight(){
    var vp=window.innerHeight;
    if(vp!==lastViewport){lastViewport=vp;lastViewportChangeAt=Date.now();}
    var h=Math.max(
      document.body.scrollHeight,
      document.documentElement.scrollHeight,
      document.body.offsetHeight,
      document.documentElement.offsetHeight
    );
    if(h===lastHeight||h<=0) return;
    // 뷰포트가 방금 바뀐 직후의 성장은 vh 단위 피드백 루프일 가능성이 높아 스킵
    if(h>lastHeight&&lastHeight>0&&(Date.now()-lastViewportChangeAt)<400) return;
    lastHeight=h;
    window.parent.postMessage({type:'iframe-resize',height:h},'*');
  }
  if(document.readyState==='complete'){sendHeight();}
  else{window.addEventListener('load',sendHeight);}
  var mo=new MutationObserver(sendHeight);
  mo.observe(document.body,{childList:true,subtree:true,characterData:true});
  if(document.fonts&&document.fonts.ready){document.fonts.ready.then(sendHeight);}
  document.addEventListener('load',function(e){
    var t=e.target;
    if(t&&(t.tagName==='IMG'||t.tagName==='IFRAME'||t.tagName==='VIDEO')) sendHeight();
  },true);
  [100,300,800,2000].forEach(function(d){setTimeout(sendHeight,d);});
})();
<\/script>`;

const CLICK_HANDLER_SCRIPT = `<script>
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a');
  if(a){
    var href=a.getAttribute('href');
    if(href&&href.startsWith('#')){e.preventDefault();var t=document.getElementById(href.substring(1));if(t)t.scrollIntoView({behavior:'smooth',block:'start'});}
    else if(href&&!href.startsWith('#')&&!href.startsWith('javascript')){e.preventDefault();window.open(href,'_blank');}
  }
});
<\/script>`;

// 모바일에서 iframe 없이 직접 렌더할 때 사용. <!DOCTYPE>, <html>, <head>, <body>
// 래퍼만 벗겨내고 <style>, <link>, <meta> 등 head 자식 태그는 그대로 둔다.
// (브라우저는 div 내부의 <style>도 전역 적용하므로 LIS UI에 약간의 스타일 누출 가능)
function unwrapHtmlDocument(html: string): string {
  let r = html.replace(/<!DOCTYPE[^>]*>/gi, '');
  r = r.replace(/<\/?html[^>]*>/gi, '');
  r = r.replace(/<head[^>]*>([\s\S]*?)<\/head>/gi, '$1');
  r = r.replace(/<\/?body[^>]*>/gi, '');
  return r;
}

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
  const isMobile = useIsMobile();

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

    // Build a proper HTML document from the content
    const fullHtml = useMemo(() => {
      // 업로더가 자체 iframe-resize 코드를 넣었으면 높이 측정 스크립트는 생략해 충돌 방지.
      const injectedScripts =
        (html.includes('iframe-resize') ? '' : HEIGHT_MEASURE_SCRIPT) +
        CLICK_HANDLER_SCRIPT;

      // If content already has full document structure, inject scripts before </body>
      if (html.includes('<!DOCTYPE') || html.includes('<html')) {
        if (html.includes('</body>')) {
          return html.replace(/<\/body>/i, injectedScripts + '</body>');
        }
        return html + injectedScripts;
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
${injectedScripts}
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
        // 신뢰 가능한 자체 콘텐츠라 allow-same-origin 유지 (Chrome의 sandbox 경고는 의도된 트레이드오프)
        sandbox="allow-scripts allow-same-origin allow-popups"
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

  if (isMobile) {
    return (
      <>
        {/* 모바일 풀스크린 오버레이 — 헤더/사이드바/푸터 위로 덮음 */}
        <div className="fixed inset-0 z-50 bg-background overflow-y-auto">
          {/* Floating 뒤로 버튼 */}
          <button
            onClick={() => router.back()}
            className="fixed top-3 left-3 z-10 inline-flex items-center justify-center h-10 w-10 rounded-full bg-background/85 backdrop-blur shadow-md border hover:bg-background"
            aria-label="뒤로"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>

          {/* 제목/요약/메타 */}
          <div ref={pdfContentRef} className="px-4 pt-16 pb-6">
            <h1 className="text-2xl font-bold mb-2 leading-tight">{content.title}</h1>
            {content.summary && (
              <p className="text-base text-muted-foreground mb-4 leading-relaxed">{content.summary}</p>
            )}

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

            <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-muted-foreground mb-4">
              <span className="flex items-center gap-1"><User className="h-3.5 w-3.5" />{content.author_name}</span>
              <span className="flex items-center gap-1"><Calendar className="h-3.5 w-3.5" />{format(new Date(content.created_at), 'yyyy.MM.dd', { locale: ko })}</span>
              <span className="flex items-center gap-1"><Eye className="h-3.5 w-3.5" />{content.view_count.toLocaleString()}회</span>
              {content.estimated_time > 0 && (
                <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" />약 {content.estimated_time}분</span>
              )}
            </div>

            <div className="flex flex-wrap gap-2">
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

            {(content.learning_objectives || content.prerequisites) && (
              <div className="grid gap-3 mt-6">
                {content.learning_objectives && (
                  <Card>
                    <CardHeader className="pb-2"><CardTitle className="text-base">학습 목표</CardTitle></CardHeader>
                    <CardContent><FormattedText text={content.learning_objectives} /></CardContent>
                  </Card>
                )}
                {content.prerequisites && (
                  <Card>
                    <CardHeader className="pb-2"><CardTitle className="text-base">선수 학습</CardTitle></CardHeader>
                    <CardContent><FormattedText text={content.prerequisites} /></CardContent>
                  </Card>
                )}
              </div>
            )}
          </div>

          {/* 콘텐츠 본문 — 모바일은 iframe 없이 직접 렌더 (vh 자연스럽게 동작) */}
          <div
            ref={contentRef}
            className={isIsolated ? 'content-mobile-isolated' : 'prose prose-slate max-w-none dark:prose-invert px-4'}
            dangerouslySetInnerHTML={{
              __html: isIsolated
                ? unwrapHtmlDocument(content.content_html || '')
                : content.content_html || '',
            }}
          />

          {/* 본문 아래 액션·메타·댓글 */}
          <div className="px-4 py-6 space-y-6">
            {(slug === 'rdf' || slug === 'rdf-interactive') && (
              <div className="flex justify-center">
                <Button size="lg" onClick={handleAdvancedLearning} className="gap-2">
                  <GraduationCap className="h-5 w-5" />
                  RDF 심화학습 시작하기
                </Button>
              </div>
            )}

            <div className="p-3 bg-muted rounded-lg text-xs text-muted-foreground flex items-center justify-between">
              <span>버전 {content.version}</span>
              <span>최종 수정: {format(new Date(content.updated_at), 'yyyy.MM.dd HH:mm', { locale: ko })}</span>
            </div>

            <CommentList contentId={content.id} />
          </div>
        </div>

        <TagSearchModal
          open={tagModalOpen}
          onOpenChange={setTagModalOpen}
          tagName={selectedTag}
        />
      </>
    );
  }

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
