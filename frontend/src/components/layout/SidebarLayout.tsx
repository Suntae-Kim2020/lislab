'use client';

import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ContentSidebar } from './ContentSidebar';

export function SidebarLayout({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(true);

  // localStorage에서 사이드바 상태 로드
  useEffect(() => {
    const saved = localStorage.getItem('sidebar-open');
    if (saved !== null) {
      setIsOpen(saved === 'true');
    }
  }, []);

  // 사이드바 상태 변경 시 localStorage에 저장
  const toggleSidebar = () => {
    const newState = !isOpen;
    setIsOpen(newState);
    localStorage.setItem('sidebar-open', String(newState));
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

            {/* 사이드바 콘텐츠 */}
            <div className="flex-1 overflow-hidden">
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
