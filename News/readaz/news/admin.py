from django.contrib import admin
from  .models import Category, New


class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'available')
    list_filter = ('available', 'created_at', 'category')
    search_fields = ('title', 'description')

admin.site.register(New, NewAdmin)
admin.site.register(Category)



