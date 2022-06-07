from django.contrib import admin
from .models import News,Category
from django.utils.safestring import mark_safe

class NewsAdmin(admin.ModelAdmin):
    list_display = ("id","title","created_at","update_at","category","is_published","get_photo","user")
    list_display_links = ("id","title")
    search_fields = ("title","content")
    list_editable = ("is_published","category","user")
    list_filter = ("is_published","category")
    fields = ("title","slug","content","created_at","update_at","category","photo","is_published","get_photo",)
    readonly_fields = ("created_at","update_at","get_photo")
    save_on_top = True
    prepopulated_fields = {"slug":("title",)}


    def get_photo(self,obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='75'>")
        return "Фото не установлено"

    get_photo.short_description = "фото"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","category_name")
    list_display_links = ("id","category_name")
    search_fields = ("category_name",)
    prepopulated_fields = {"slug": ("category_name",)}


admin.site.register(News,NewsAdmin)
admin.site.register(Category,CategoryAdmin)