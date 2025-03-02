from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html  # Optional: For better display customization
from .models import CustomUser

# Custom Filter for Book Publication Year
class PublishedYearFilter(admin.SimpleListFilter):
    title = _('publication year')
    parameter_name = 'publication_year'

    def lookups(self, request, model_admin):
        Book = apps.get_model('bookshelf', 'Book')
        years = set(book.published_date.year for book in Book.objects.all())
        return [(year, year) for year in sorted(years, reverse=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(published_date__year=self.value())
        return queryset

# Custom Book Admin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_year')  
    list_filter = (PublishedYearFilter,)  
    search_fields = ('title', 'author', 'isbn')

    @admin.display(ordering='published_date', description='Publication Year')
    def publication_year(self, obj):
        return obj.published_date.year


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'date_of_birth', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'date_of_birth', 'profile_photo', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )


# Register the models using a safe method
Book = apps.get_model('bookshelf', 'Book')
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
