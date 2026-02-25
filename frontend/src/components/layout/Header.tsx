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
import { useMenus } from '@/lib/hooks/useContents';
import type { MenuItem, MenuChild } from '@/lib/api/contents';

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
          <nav className="flex items-center">
            {menus?.map((item, index) => (
              <div key={item.id} className="flex items-center">
                <NavMenuItem item={item} />
                {index < (menus?.length || 0) - 1 && (
                  <span className="mx-4 text-muted-foreground/50">|</span>
                )}
              </div>
            ))}
          </nav>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
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
