'use client';

import { useEffect } from 'react';
import { useAuthCheck } from '@/lib/hooks/useAuth';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  useAuthCheck();

  return <>{children}</>;
}
