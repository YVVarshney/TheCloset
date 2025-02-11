from django.http import HttpResponse
# from django.shortcuts import render

# def index(request):
#     return render(request, "index.html")

# def aboutUs(request):
#     return HttpResponse("Welcome to The Closet")
# Create your views here.
from django.shortcuts import render, redirect
from .models import Questions, Option, UserResponse, BodyType, UserBodyMeasurement

# Home Page
def home(request):
    return render(request, 'quiz.html')

# Display Questions
def quiz(request):
    context = [{
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
    return render(request, "questions.html", context)

def submit_response(request):
    if request.method == "POST":
        selected_image = request.POST.get("selected_image")
        if selected_image:
            return HttpResponse(f"You selected: {selected_image}")
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

    return render(request, 'templates/results.html', {'top_styles': top_styles})

# Feedback Page
def feedback(request):
    if request.method == "POST":
        feedback.objects.create(
            user_id=request.session.session_key,
            feedback_text=request.POST.get('feedback'),
            rating=int(request.POST.get('rating'))
        )
        return redirect('home')
    return render(request, 'templates/feedback.html')
