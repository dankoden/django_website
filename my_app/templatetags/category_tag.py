from django import template
from my_app.models import Category
from django.db.models import Count,F
from django.core.cache import cache

register = template.Library()

@register.simple_tag()
def get_category():
    category = cache.get('categories')
    if not category:
        category = Category.objects.annotate(cnt = Count('news',filter=F("news__is_published"))).filter(cnt__gt = 0)
        cache.set('categories',category,30)
    return category
