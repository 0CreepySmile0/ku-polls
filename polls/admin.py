"""Contains admin views related."""
from django.contrib import admin
from .models import Question, Choice, Vote


class ChoiceInline(admin.TabularInline):
    """Use in QuestionAdmin."""

    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    """Admin can access and manage Question model."""

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information",
         {"fields": ["published_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["__str__", "published_date", "is_published", "can_vote"]
    list_filter = ["published_date"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    """Admin can access and manage Choice model."""

    list_display = ["__str__", "votes", "question"]
    list_filter = ["question"]


class VoteAdmin(admin.ModelAdmin):
    """Admin can access and manage Vote model."""

    fieldsets = [
        ("Vote information", {"fields": ["user", "choice"]}),
    ]
    list_display = ["choice", "user", "question"]
    list_filter = ["user", "choice"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote, VoteAdmin)
