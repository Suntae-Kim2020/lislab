import { SidebarLayout } from '@/components/layout/SidebarLayout';

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="h-[calc(100vh-theme(spacing.16)-theme(spacing.12))] overflow-hidden">
      <SidebarLayout>{children}</SidebarLayout>
    </div>
  );
}
