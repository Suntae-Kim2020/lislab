import { SidebarLayout } from '@/components/layout/SidebarLayout';

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="h-[calc(100vh-64px-48px)] overflow-hidden">
      <SidebarLayout>{children}</SidebarLayout>
    </div>
  );
}
