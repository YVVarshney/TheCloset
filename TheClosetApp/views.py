from django.http import HttpResponse
# from django.shortcuts import render

# def index(request):
#     return render(request, "index.html")

# def aboutUs(request):
#     return HttpResponse("Welcome to The Closet")
# Create your views here.
from django.shortcuts import render, redirect
from .models import Questions, Option, UserResponse, BodyType, UserBodyMeasurement
from django.urls import reverse

# Home Page
def home(request):
    return render(request, 'quiz.html')

# Display Questions
def quiz(request, questionId = 0):
    quizData = [{
        "question": "Which image do you prefer?",
        "images": [
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            
        ],
    },
    {
        "question": "Which image do you prefer?",
        "images": [
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            'images/index.png',
            
        ],
    }]
    if questionId >= len(quizData):
        return HttpResponse("Quiz completed! Thank you.")

    context = {
        "question": quizData[questionId]["question"],
        "images": quizData[questionId]["images"],
        "questionId": questionId,
    }
    return render(request, "questions.html", context)

def submit_response(request):
    if request.method == "POST":
        selected_image = request.POST.get("selected_image")
        questionId = int(request.POST.get("questionId", 0))
        action = request.POST.get("action")

        # Store user response in session (or save to a database)
        if "responses" not in request.session:
            request.session["responses"] = []
        request.session["responses"].append({"question": questionId, "answer": selected_image})
        request.session.modified = True
        
        if action == "next":
            return redirect(reverse("quiz", kwargs={"questionId": questionId + 1}))
        else:
            return redirect('feedback')

    return redirect("quiz")

# Calculate and Display Results
def results(request):
    user_id = request.session.session_key
    responses = UserResponse.objects.filter(user_id=user_id)
    
    # Count style personality preferences
    style_scores = {}
    for response in responses:
        style = response.selected_option.style_personality
        style_scores[style] = style_scores.get(style, 0) + 1
    
    sorted_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
    top_styles = sorted_styles[:3]

    return render(request, 'results.html', {'top_styles': top_styles})

# Feedback Page
def feedback(request):
    feedbackQuiz = [{
        "question": "Do you find it challenging to select outfits on a daily basis?",
        "option": [
            'Yes',
            'No',
            'Sometimes',
        ],
    },
    {
        "question": "Do you face challenges in selecting outfits for special occasions? (Such as parties, dates, weddings, or business events)",
        "option": [
            'Yes',
            'No',
            
        ],
    }]
    if request.method == "POST":
        feedback.objects.create(
            user_id=request.session.session_key,
            feedback_text=request.POST.get('feedback'),
            rating=int(request.POST.get('rating'))
        )
        return redirect('home')
    return render(request, 'feedback.html')
