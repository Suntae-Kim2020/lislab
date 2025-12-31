import Link from 'next/link';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Heart, Clock, Eye } from 'lucide-react';
import { Content } from '@/lib/api/contents';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

interface ContentCardProps {
  content: Content;
  onToggleFavorite?: (slug: string) => void;
  isAuthenticated?: boolean;
}

const difficultyColors = {
  BEGINNER: 'bg-green-100 text-green-800',
  INTERMEDIATE: 'bg-yellow-100 text-yellow-800',
  ADVANCED: 'bg-red-100 text-red-800',
};

const difficultyLabels = {
  BEGINNER: '초급',
  INTERMEDIATE: '중급',
  ADVANCED: '고급',
};

export function ContentCard({ content, onToggleFavorite, isAuthenticated }: ContentCardProps) {
  return (
    <Card className="flex flex-col h-full transition-shadow hover:shadow-lg">
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            <Link href={`/contents/${content.slug}`}>
              <CardTitle className="line-clamp-2 hover:text-primary cursor-pointer">
                {content.title}
              </CardTitle>
            </Link>
            <CardDescription className="mt-2">
              {content.category_name}
            </CardDescription>
          </div>
          {isAuthenticated && onToggleFavorite && (
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onToggleFavorite(content.slug)}
              className={content.is_favorited ? 'text-red-500 hover:text-red-600' : 'hover:text-gray-600'}
            >
              <Heart
                className={`h-5 w-5 ${content.is_favorited ? 'fill-current' : ''}`}
              />
            </Button>
          )}
        </div>
      </CardHeader>

      <CardContent className="flex-1">
        <p className="text-sm text-muted-foreground line-clamp-3">
          {content.summary}
        </p>

        <div className="mt-4 flex flex-wrap gap-2">
          <Badge className={difficultyColors[content.difficulty]}>
            {difficultyLabels[content.difficulty]}
          </Badge>
          {content.tags.slice(0, 3).map((tag) => (
            <Badge key={tag.id} variant="outline">
              {tag.name}
            </Badge>
          ))}
        </div>
      </CardContent>

      <CardFooter className="text-sm text-muted-foreground">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Eye className="h-4 w-4" />
              <span>{content.view_count}</span>
            </div>
            {content.estimated_time > 0 && (
              <div className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                <span>{content.estimated_time}분</span>
              </div>
            )}
          </div>
          <span className="text-xs">
            {format(new Date(content.created_at), 'yyyy.MM.dd', { locale: ko })}
          </span>
        </div>
      </CardFooter>
    </Card>
  );
}
