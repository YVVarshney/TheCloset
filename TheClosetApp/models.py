from django.db import models

class Feedback(models.Model):
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)

    style_personality_accuracy = models.IntegerField()
    clothing_suggestions_accuracy = models.IntegerField()
    style_personality_thoughts = models.TextField(blank=True, null=True)

    body_type_accuracy = models.IntegerField()
    body_type_suggestions_accuracy = models.IntegerField()
    body_type_thoughts = models.TextField(blank=True, null=True)

    outfit_challenge = models.CharField(max_length=255)
    quiz_improvements = models.JSONField(blank=True, null=True)  # Store multiple selections
    quiz_improvements_other = models.TextField(blank=True, null=True)

    styling_service = models.CharField(max_length=255)
    styling_service_price = models.CharField(max_length=255)

    final_thoughts = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically set submission time

    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'} - {self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        db_table = "theclosetapp_feedback"  # Use lowercase

class UserResponse(models.Model):
    user_id = models.CharField(max_length=255)  # Store session-based user ID
    responses = models.JSONField()  # Store responses in JSON format
    submitted_at = models.DateTimeField(auto_now_add=True)  # Store submission time

    def __str__(self):
        return f"Response from User {self.user_id} - {self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        db_table = "theclosetapp_userresponse"  # Use lowercase