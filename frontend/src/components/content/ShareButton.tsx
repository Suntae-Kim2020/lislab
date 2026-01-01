'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Share2, MessageCircle, Copy, Check } from 'lucide-react';

interface ShareButtonProps {
  title: string;
  url: string;
}

export function ShareButton({ title, url }: ShareButtonProps) {
  const [copied, setCopied] = useState(false);

  // Web Share API 사용 (모바일에서 문자, 카카오톡 등 네이티브 공유)
  const handleNativeShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: title,
          text: `${title} - LIS Lab`,
          url: url,
        });
      } catch (error) {
        // 사용자가 취소한 경우 무시
        if ((error as Error).name !== 'AbortError') {
          console.error('Share failed:', error);
        }
      }
    }
  };

  // 카카오톡 공유
  const handleKakaoShare = () => {
    if (typeof window !== 'undefined' && window.Kakao) {
      if (!window.Kakao.isInitialized()) {
        window.Kakao.init(process.env.NEXT_PUBLIC_KAKAO_APP_KEY || '');
      }

      window.Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
          title: title,
          description: 'LIS Lab 교육 콘텐츠',
          imageUrl: 'https://lislab-frontend-326272454487.asia-northeast3.run.app/lis-lab-hero.png',
          link: {
            mobileWebUrl: url,
            webUrl: url,
          },
        },
        buttons: [
          {
            title: '콘텐츠 보기',
            link: {
              mobileWebUrl: url,
              webUrl: url,
            },
          },
        ],
      });
    } else {
      alert('카카오톡 SDK를 로드할 수 없습니다.');
    }
  };

  // URL 복사
  const handleCopyUrl = async () => {
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Copy failed:', error);
      alert('URL 복사에 실패했습니다.');
    }
  };

  // 모바일에서 Web Share API 지원 시 바로 네이티브 공유
  if (typeof navigator !== 'undefined' && navigator.share) {
    return (
      <Button
        variant="outline"
        size="icon"
        onClick={handleNativeShare}
        title="공유하기"
      >
        <Share2 className="h-5 w-5" />
      </Button>
    );
  }

  // 데스크톱에서는 드롭다운 메뉴로 옵션 제공
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon" title="공유하기">
          <Share2 className="h-5 w-5" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={handleKakaoShare}>
          <MessageCircle className="mr-2 h-4 w-4" />
          카카오톡으로 공유
        </DropdownMenuItem>
        <DropdownMenuItem onClick={handleCopyUrl}>
          {copied ? (
            <>
              <Check className="mr-2 h-4 w-4 text-green-600" />
              복사됨!
            </>
          ) : (
            <>
              <Copy className="mr-2 h-4 w-4" />
              URL 복사
            </>
          )}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

// 카카오 SDK 타입 선언
declare global {
  interface Window {
    Kakao: any;
  }
}
