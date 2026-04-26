'use client';

import { useState, useEffect, useRef } from 'react';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ContentSidebar } from './ContentSidebar';
import { useIsMobile } from '@/lib/hooks/useIsMobile';

const SCROLL_POSITION_KEY = 'sidebar-scroll-position';

export function SidebarLayout({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(true);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname();
  const isMobile = useIsMobile();

  // 모바일은 기본 닫힘, 데스크톱은 localStorage 우선 (없으면 기본 열림)
  useEffect(() => {
    if (isMobile) {
      setIsOpen(false);
      return;
    }
    const saved = localStorage.getItem('sidebar-open');
    if (saved !== null) {
      setIsOpen(saved === 'true');
    } else {
      setIsOpen(true);
    }
  }, [isMobile]);

  // 모바일에서 라우트가 바뀌면 사이드바 자동 닫기
  useEffect(() => {
    if (isMobile) setIsOpen(false);
  }, [pathname, isMobile]);

  // 스크롤 위치 저장
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      sessionStorage.setItem(SCROLL_POSITION_KEY, String(container.scrollTop));
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [isOpen]);

  // 스크롤 위치 복원 / 활성 항목으로 포커싱
  // - 콘텐츠 상세 경로(/contents/xxx)일 때는 활성 항목이 나타나면 해당 위치로 스크롤
  // - 그 외에는 기존 저장된 스크롤 위치를 복원
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container || !isOpen) return;

    const isContentDetail = /^\/contents\/[^/]+/.test(pathname);

    if (isContentDetail) {
      // 활성 항목이 렌더링되는 즉시 중앙으로 스크롤
      let scrolled = false;
      const scrollToActive = () => {
        if (scrolled) return;
        const active = container.querySelector<HTMLElement>('[data-active="true"]');
        if (active) {
          scrolled = true;
          active.scrollIntoView({ block: 'center', behavior: 'auto' });
          // 저장된 스크롤 위치를 활성 항목 기준으로 업데이트
          sessionStorage.setItem(SCROLL_POSITION_KEY, String(container.scrollTop));
        }
      };

      // 초기 시도
      scrollToActive();

      const observer = new MutationObserver(scrollToActive);
      observer.observe(container, { childList: true, subtree: true });

      const timeout = setTimeout(() => observer.disconnect(), 3000);
      return () => {
        observer.disconnect();
        clearTimeout(timeout);
      };
    }

    // 콘텐츠 상세가 아닐 때는 저장된 스크롤 위치 복원
    const savedPosition = sessionStorage.getItem(SCROLL_POSITION_KEY);
    if (!savedPosition) return;

    const position = parseInt(savedPosition, 10);

    const observer = new MutationObserver(() => {
      if (container.scrollHeight > position) {
        container.scrollTop = position;
      }
    });

    observer.observe(container, { childList: true, subtree: true });
    container.scrollTop = position;

    const timeout = setTimeout(() => observer.disconnect(), 3000);

    return () => {
      observer.disconnect();
      clearTimeout(timeout);
    };
  }, [pathname, isOpen]);

  // 사이드바 상태 변경 시 localStorage에 저장 (데스크톱 환경설정만 영속화)
  const toggleSidebar = () => {
    const newState = !isOpen;
    setIsOpen(newState);
    if (!isMobile) {
      localStorage.setItem('sidebar-open', String(newState));
    }
  };

  return (
    <div className="flex h-full">
      {/* 사이드바 */}
      <aside
        className={`fixed lg:relative inset-y-0 left-0 z-40 w-80 bg-background border-r transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:-translate-x-0 lg:w-0'
        }`}
      >
        {isOpen && (
          <div className="h-full flex flex-col">
            {/* 사이드바 헤더 */}
            <div className="flex items-center justify-between p-4 border-b">
              <h2 className="text-lg font-bold">교육자료 목록</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleSidebar}
                title="사이드바 닫기"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            {/* 사이드바 콘텐츠 - 스크롤 컨테이너 */}
            <div ref={scrollContainerRef} className="flex-1 overflow-y-auto">
              <ContentSidebar />
            </div>
          </div>
        )}
      </aside>

      {/* 메인 콘텐츠 */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* 토글 버튼 (사이드바가 닫혔을 때) */}
        {!isOpen && (
          <div className="p-2 border-b">
            <Button
              variant="outline"
              size="sm"
              onClick={toggleSidebar}
              className="gap-2"
            >
              <Menu className="h-4 w-4" />
              <span className="hidden sm:inline">교육자료 목록 열기</span>
            </Button>
          </div>
        )}

        {/* 페이지 콘텐츠 */}
        <div className="flex-1 overflow-auto">
          {children}
        </div>
      </div>

      {/* 모바일 오버레이 */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={toggleSidebar}
        />
      )}
    </div>
  );
}
