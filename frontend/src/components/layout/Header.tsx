'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';

export function Header() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center">
        <div className="flex flex-1 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex flex-col">
            <span className="text-2xl font-bold">LIS Lab</span>
            <span className="text-xs text-muted-foreground">Library & Information Science Learning Platform</span>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-6">
            <DropdownMenu>
              <DropdownMenuTrigger className="text-sm font-medium transition-colors hover:text-primary">
                콘텐츠
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem asChild>
                  <Link href="/contents">전체 콘텐츠</Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=web-docs">웹문서</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=web-technology">웹기술</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=search-protocol">프로토콜</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=standard-specifications">표준규격지침</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=conceptual-model">개념 모델</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=data-model">데이터 모델</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=serialization" className="pl-6">→ 직렬화</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=metadata">메타데이터</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=ontology">온톨로지</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=identifier-reference">식별자와 참조체계</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contents?category=overview">한눈에 보기</Link>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <Link
              href="/contents?category=practice"
              className="text-sm font-medium transition-colors hover:text-primary"
            >
              실습
            </Link>

            <Link
              href="/boards"
              className="text-sm font-medium transition-colors hover:text-primary"
            >
              게시판
            </Link>

            <Link
              href="/about"
              className="text-sm font-medium transition-colors hover:text-primary"
            >
              소개
            </Link>
          </nav>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {isAuthenticated && user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                    <Avatar>
                      <AvatarFallback>
                        {user.username.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium">{user.username}</p>
                      <p className="text-xs text-muted-foreground">{user.email}</p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link href="/my">마이페이지</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/my/favorites">즐겨찾기</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/my/profile">프로필 설정</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/my/mailing-settings">메일링 설정</Link>
                  </DropdownMenuItem>
                  {user.role === 'ADMIN' && (
                    <>
                      <DropdownMenuItem asChild>
                        <Link href="/admin/dashboard">대시보드</Link>
                      </DropdownMenuItem>
                      <DropdownMenuItem asChild>
                        <a href="http://localhost:8000/admin/" target="_blank" rel="noopener noreferrer">
                          관리자 페이지
                        </a>
                      </DropdownMenuItem>
                    </>
                  )}
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={handleLogout}>
                    로그아웃
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <div className="flex items-center space-x-2">
                <Button variant="ghost" asChild>
                  <Link href="/login">로그인</Link>
                </Button>
                <Button asChild>
                  <Link href="/register">회원가입</Link>
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
