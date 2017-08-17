from django.contrib import admin
from .models import Question, Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                       {'fields': ['question_text']}),
        ("Publication Data",      {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInLine]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


#admin.site.site_header = "My administrationzzzzz" # Don't need this because I am changing the header by overriding the base_site.html template in templates/admin/base_site.html


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
