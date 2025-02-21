from django.contrib import admin
from .models import Feedback
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at")
    search_fields = ("name", "email", "location", "occupation")
    list_filter = ("submitted_at",)


