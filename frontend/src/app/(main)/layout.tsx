import { SidebarLayout } from '@/components/layout/SidebarLayout';

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="h-full overflow-hidden">
      <SidebarLayout>{children}</SidebarLayout>
    </div>
  );
}
