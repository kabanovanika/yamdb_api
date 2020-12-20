from django.contrib import admin

from .models import Review, Comment, Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')
    search_fields = ('name', )
    list_filter = ('name', )


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')
    search_fields = ('name', )
    list_filter = ('name', )


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', )
    list_filter = ('name', )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'author', 'pk')
    search_fields = ('title_id', )
    list_filter = ('title_id', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date')
    search_fields = ('text', )
    list_filter = ('pub_date', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
