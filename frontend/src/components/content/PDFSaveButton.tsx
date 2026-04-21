'use client';

import { Button } from '@/components/ui/button';
import { FileText } from 'lucide-react';

interface PDFSaveButtonProps {
  title: string;
  contentRef: React.RefObject<HTMLDivElement | null>;
  rawHtml?: string;
}

export function PDFSaveButton({ title, contentRef, rawHtml }: PDFSaveButtonProps) {
  const printStyles = `
    @media print {
      @page { margin: 2cm; size: A4; }
      body { margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      /* iOS Safari fix: overflow:hidden clips content during print */
      * { overflow: visible !important; }
      .hero, header, section, main, div { position: static !important; }
      .hero::before, .hero::after { display: none !important; }
    }
    button, .no-print { display: none !important; }
  `;

  const defaultStyles = `
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;
    }
    h1 { font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: #000; }
    h2 { font-size: 1.5rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #ddd; color: #000; }
    h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #000; }
    p { margin: 1rem 0; }
    code { background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 0.9em; }
    pre { background-color: #f5f5f5; padding: 1rem; border-radius: 5px; overflow-x: auto; margin: 1rem 0; }
    pre code { background: none; padding: 0; }
    ul, ol { margin: 1rem 0; padding-left: 2rem; }
    li { margin: 0.5rem 0; }
    table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f5f5f5; font-weight: 600; }
    img { max-width: 100%; height: auto; margin: 1rem 0; }
    .badge { display: inline-block; padding: 4px 8px; margin: 2px; background-color: #e5e7eb; border-radius: 4px; font-size: 0.875rem; }
  `;

  const savePDF = () => {
    const printWindow = window.open('', '', 'width=800,height=600');
    if (!printWindow) {
      alert('팝업이 차단되었습니다. 팝업 차단을 해제해주세요.');
      return;
    }

    if (rawHtml) {
      // Isolated content: use original HTML directly with print styles injected
      const hasFullDoc = rawHtml.includes('<!DOCTYPE') || rawHtml.includes('<html');

      if (hasFullDoc) {
        // Inject print styles into existing document
        const withPrint = rawHtml.replace(
          /<\/head>/i,
          `<style>${printStyles}</style></head>`
        );
        printWindow.document.write(withPrint);
      } else {
        // Parse head-level tags from fragment
        const headTags: string[] = [];
        let bodyContent = rawHtml;
        const patterns = [
          /<meta[^>]*\/?>/gi,
          /<title[^>]*>[\s\S]*?<\/title>/gi,
          /<link[^>]*\/?>/gi,
          /<style[^>]*>[\s\S]*?<\/style>/gi,
        ];
        for (const pattern of patterns) {
          const matches = bodyContent.match(pattern);
          if (matches) {
            headTags.push(...matches);
            bodyContent = bodyContent.replace(pattern, '');
          }
        }

        printWindow.document.write(`<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${title}</title>
${headTags.join('\n')}
<style>${printStyles}</style>
</head><body>${bodyContent}</body></html>`);
      }
    } else {
      // Regular content: clone DOM as before
      if (!contentRef.current) {
        alert('PDF를 생성할 콘텐츠를 찾을 수 없습니다.');
        printWindow.close();
        return;
      }

      const content = contentRef.current.cloneNode(true) as HTMLElement;
      content.querySelectorAll('button').forEach(b => b.remove());

      printWindow.document.write(`<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>${title}</title>
<style>${printStyles}\n${defaultStyles}</style>
</head><body>${content.innerHTML}</body></html>`);
    }

    printWindow.document.close();

    // Wait for fonts/images to load, then print
    setTimeout(() => {
      printWindow.print();
      printWindow.close();
    }, 1000);
  };

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={savePDF}
      title="PDF로 저장 (인쇄)"
    >
      <FileText className="h-4 w-4" />
    </Button>
  );
}
