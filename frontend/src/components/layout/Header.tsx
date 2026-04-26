'use client';

import Link from 'next/link';
import { useState } from 'react';
import { Menu, X, ChevronDown } from 'lucide-react';
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
import { useMenus } from '@/lib/hooks/useContents';
import type { MenuItem, MenuChild } from '@/lib/api/contents';

function MobileNavItem({ item, onClose }: { item: MenuItem; onClose: () => void }) {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = item.children && item.children.length > 0;

  if (!hasChildren) {
    return (
      <Link
        href={item.url}
        onClick={onClose}
        className="block px-3 py-3 text-sm font-medium rounded hover:bg-muted"
        {...(item.open_in_new_tab ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
      >
        {item.name}
      </Link>
    );
  }

  return (
    <div>
      <button
        onClick={() => setExpanded((v) => !v)}
        className="flex items-center justify-between w-full px-3 py-3 text-sm font-medium rounded hover:bg-muted"
      >
        <span>{item.name}</span>
        <ChevronDown className={`h-4 w-4 transition-transform ${expanded ? 'rotate-180' : ''}`} />
      </button>
      {expanded && (
        <div className="pl-3 mt-1 space-y-1 border-l ml-3">
          {item.url && item.url !== '#' && (
            <Link
              href={item.url}
              onClick={onClose}
              className="block px-3 py-2 text-sm text-muted-foreground rounded hover:bg-muted"
            >
              전체 보기
            </Link>
          )}
          {item.children.map((child: MenuChild) => (
            <Link
              key={child.id}
              href={child.url}
              onClick={onClose}
              className="block px-3 py-2 text-sm text-muted-foreground rounded hover:bg-muted"
              {...(child.open_in_new_tab ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
            >
              {child.name}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

function NavMenuItem({ item }: { item: MenuItem }) {
  const hasChildren = item.children && item.children.length > 0;

  if (!hasChildren) {
    return (
      <Link
        href={item.url}
        className="text-sm font-medium transition-colors hover:text-primary"
        {...(item.open_in_new_tab ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
      >
        {item.name}
      </Link>
    );
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="text-sm font-medium transition-colors hover:text-primary">
        {item.name}
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        {item.url && item.url !== '#' && (
          <>
            <DropdownMenuItem asChild>
              <Link href={item.url}>전체 보기</Link>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
          </>
        )}
        {item.children.map((child: MenuChild) => (
          <DropdownMenuItem key={child.id} asChild>
            <Link
              href={child.url}
              {...(child.open_in_new_tab ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
            >
              {child.name}
            </Link>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export function Header() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();
  const { data: menus } = useMenus();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <>
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center">
        <div className="flex flex-1 items-center justify-between gap-2">
          {/* Logo */}
          <Link href="/" className="flex flex-col min-w-0">
            <span className="text-xl md:text-2xl font-bold whitespace-nowrap">LIS Lab</span>
            <span className="hidden md:block text-xs text-muted-foreground">Library & Information Science Learning Platform</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center">
            {menus?.map((item, index) => (
              <div key={item.id} className="flex items-center">
                <NavMenuItem item={item} />
                {index < (menus?.length || 0) - 1 && (
                  <span className="mx-4 text-muted-foreground/50">|</span>
                )}
              </div>
            ))}
          </nav>

          {/* Right side */}
          <div className="flex items-center space-x-2 md:space-x-4">
            {/* Mobile hamburger */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(true)}
              aria-label="메뉴 열기"
            >
              <Menu className="h-5 w-5" />
            </Button>

            {isAuthenticated && user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                    <Avatar>
                      <AvatarFallback>
                        {(user.first_name || user.username).charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium">{user.first_name || user.username}</p>
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
                    <DropdownMenuItem asChild>
                      <Link href="/admin/dashboard">대시보드</Link>
                    </DropdownMenuItem>
                  )}
                  {(user.role === 'ADMIN' || user.is_staff) && (
                    <DropdownMenuItem
                      onClick={() => {
                        const token = localStorage.getItem('access_token');
                        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
                        window.open(`${baseUrl}/admin-login/?token=${token}`, '_blank');
                      }}
                    >
                      관리자 페이지
                    </DropdownMenuItem>
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
                <Button asChild className="hidden sm:inline-flex">
                  <Link href="/register">회원가입</Link>
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>

    {/* Mobile drawer — header 바깥에 두어야 backdrop-filter containing block에 갇히지 않음 */}
    {mobileMenuOpen && (
      <>
        <div
          className="fixed inset-0 z-[60] bg-black/50 md:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
        <aside className="fixed top-0 right-0 z-[70] h-full w-72 max-w-[85vw] bg-background border-l shadow-lg md:hidden overflow-y-auto">
          <div className="flex items-center justify-between p-4 border-b">
            <span className="font-semibold">메뉴</span>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setMobileMenuOpen(false)}
              aria-label="메뉴 닫기"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
          <nav className="p-2">
            {menus?.map((item) => (
              <MobileNavItem key={item.id} item={item} onClose={() => setMobileMenuOpen(false)} />
            ))}
            {!isAuthenticated && (
              <Link
                href="/register"
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-3 mt-2 text-sm font-medium rounded bg-primary text-primary-foreground text-center sm:hidden"
              >
                회원가입
              </Link>
            )}
          </nav>
        </aside>
      </>
    )}
    </>
  );
}
