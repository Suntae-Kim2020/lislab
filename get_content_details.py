from apps.contents.models import Content
import json

c = Content.objects.get(slug='web-lis-dev')

content_data = {
    'title': c.title,
    'slug': c.slug,
    'summary': c.summary,
    'content_html': c.content_html,
    'category': c.category.slug if c.category else None,
    'tags': [tag.slug for tag in c.tags.all()],
    'status': c.status,
    'version': c.version,
    'estimated_time': c.estimated_time,
    'difficulty': c.difficulty,
    'prerequisites': c.prerequisites,
    'learning_objectives': c.learning_objectives,
    'meta_description': c.meta_description,
    'meta_keywords': c.meta_keywords,
}

print(json.dumps(content_data, ensure_ascii=False, indent=2))
