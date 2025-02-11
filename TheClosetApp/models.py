from django.db import models

# Model for Style Personality Quiz Questions
class Questions(models.Model):
    text = models.TextField()

class Option(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    style_personality = models.CharField(max_length=50)  # Classic, Romantic, etc.

# User Responses
class UserResponse(models.Model):
    user_id = models.CharField(max_length=255)  # Track user session
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

# Body Type Data
class BodyType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

# User Body Measurements
class UserBodyMeasurement(models.Model):
    user_id = models.CharField(max_length=255)
    shoulders = models.FloatField()
    bust = models.FloatField()
    waist = models.FloatField()
    hips = models.FloatField()
    body_type = models.ForeignKey(BodyType, on_delete=models.SET_NULL, null=True)

# Feedback Form
class Feedback(models.Model):
    user_id = models.CharField(max_length=255)
    feedback_text = models.TextField()
    rating = models.IntegerField()