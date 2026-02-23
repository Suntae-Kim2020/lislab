from dal import autocomplete
from django.db.models.functions import Collate

from .models import Tag


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Tag.objects.none()

        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs.order_by(Collate('name', 'C'))

    def has_add_permission(self, request):
        return request.user.is_staff

    def create_object(self, text):
        tag, _ = Tag.objects.get_or_create(name=text)
        return tag
