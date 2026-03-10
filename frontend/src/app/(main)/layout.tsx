import { SidebarLayout } from '@/components/layout/SidebarLayout';

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div style={{ height: 'calc(100vh - 64px - 48px)' }} className="overflow-hidden">
      <SidebarLayout>{children}</SidebarLayout>
    </div>
  );
}
