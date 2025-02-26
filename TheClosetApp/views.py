from django.http import HttpResponse
# from django.shortcuts import render

# def index(request):
#     return render(request, "index.html")

# def aboutUs(request):
#     return HttpResponse("Welcome to The Closet")
# Create your views here.
from django.shortcuts import render, redirect
# from .models import Questions, Option, UserResponse, BodyType, UserBodyMeasurement
from django.urls import reverse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import uuid
from .models import Feedback, UserResponse  # Import the model
import logging
from datetime import datetime
import boto3
from django.conf import settings

s3_client = boto3.client('s3')

quizData = [{
        "question": "What is your go-to color palette for everyday outfits? ",
        "images": [
            'images/QuizOptions/q1o1.jpg',
            'images/QuizOptions/q1o2.jpg',
            'images/QuizOptions/q1o3.jpg',
            'images/QuizOptions/q1o4.jpg',
            'images/QuizOptions/q1o5.jpg',
            'images/QuizOptions/q1o6.jpg',
            'images/QuizOptions/q1o7.jpg',
            'images/QuizOptions/q1o8.jpg',
            'images/QuizOptions/q1o9.jpg',

        ],
        "optionText": [
            "Neutral tones like black, white, beige" ,
            "Soft pastels and floral prints" ,
            "Earthy hues and natural patterns" ,
            "Dark shades and bold accents" ,
            "Vibrant, bold colors with eye-catching prints" ,
            "Clean lines with pops of bright color" ,
            "Metallics, sequins, or bold jewel tones" ,
            "Monochromatic or minimalistic colors" ,
            "A mix of modern patterns and neutrals",

        ],
    },
    {
        "question": "What’s your weekend vibe?",
        "images": [
            'images/QuizOptions/q2o1.jpg',
            'images/QuizOptions/q2o2.jpg',
            'images/QuizOptions/q2o3.jpg',
            'images/QuizOptions/q2o4.jpg',
            'images/QuizOptions/q2o5.jpg',
            'images/QuizOptions/q2o6.jpg',
            'images/QuizOptions/q2o7.jpg',
            'images/QuizOptions/q2o8.jpg',
            'images/QuizOptions/q2o9.jpg',
        ],
        "optionText": [
            "Brunch with friends, sipping lattes, at a classy restaurant." ,
            "A picnic in the park, surrounded by flowers and sunshine." ,
            "Exploring a flea market or crafting something artsy." ,
            "Riding my motorcycle or hitting up a cool underground event." ,
            "Wandering the city streets, finding Insta-worthy spots." ,
            "Lounging at the country club or heading to a bookstore." ,
            "Attending a glamorous party or hitting a chic rooftop bar." ,
            "Shopping for high-end basics or trying out a minimalist café." ,
            "Checking out a modern art gallery or working on my side hustle.",

        ],
    },
    {
      "question": "What shoes are you most drawn to?",
        "images": [
            'images/QuizOptions/q3o1.jpg',
            'images/QuizOptions/q3o2.jpg',
            'images/QuizOptions/q3o3.jpg',
            'images/QuizOptions/q3o4.jpg',
            'images/QuizOptions/q3o5.jpg',
            'images/QuizOptions/q3o6.jpg',
            'images/QuizOptions/q3o7.jpg',
            'images/QuizOptions/q3o8.jpg',
            'images/QuizOptions/q3o9.jpg',
        ],  
        "optionText": [
            "Loafers, classic pumps, or ballet flats – timeless." ,
            "Delicate heels or floral sandals." ,
            "Sandals or cute ankle boots – easy and comfy." ,
            "Combat boots or studded heels – edgy all the way." ,
            "Chunky sneakers or urban-style boots." ,
            "oxfords or preppy loafers." ,
            "High heels that make a statement." ,
            "Sleek ankle boots or designer flats." ,
            "Mules or trendy, versatile sneakers.",

        ],
    },
    {
       "question": "What accesories are you most drawn to?",
        "images": [
            'images/QuizOptions/q4o1.jpg',
            'images/QuizOptions/q4o2.jpg',
            'images/QuizOptions/q4o3.jpg',
            'images/QuizOptions/q4o4.jpg',
            'images/QuizOptions/q4o5.jpg',
            'images/QuizOptions/q4o6.jpg',
            'images/QuizOptions/q4o7.jpg',
            'images/QuizOptions/q4o8.jpg',
            'images/QuizOptions/q4o9.jpg',
        ],  
        "optionText": [
            "Pearl earrings and a classic watch." ,
            "Floral headbands and delicate bracelets." ,
            "Fringe bags, layered necklaces, and quirky rings." ,
            "Studded belts, statement earrings, and bold cuffs." ,
            "oversized sunglasses and quirky jewelry." ,
            "Headbands, structured bags, and subtle necklaces." ,
            "Sparkly earrings, clutches, and standout pieces." ,
            "Minimal necklaces and sleek structured handbags." ,
            "Modern, functional pieces with a chic twist",

        ],
    },
    {
       "question": "What's your favorite type of bag?",
        "images": [
            'images/QuizOptions/q5o1.jpg',
            'images/QuizOptions/q5o2.jpg',
            'images/QuizOptions/q5o3.jpg',
            'images/QuizOptions/q5o4.jpg',
            'images/QuizOptions/q5o5.jpg',
            'images/QuizOptions/q5o6.jpg',
            'images/QuizOptions/q5o7.jpg',
            'images/QuizOptions/q5o8.jpg',
            'images/QuizOptions/q5o9.jpg',
        ], 
        "optionText": [
            "A structured leather tote or satchel." ,
            "A romantic crossbody with floral or vintage details." ,
            "A slouchy hobo bag with fringe or macramé." ,
            "A studded mini backpack or bold clutch." ,
            "A quirky statement bag or oversized tote." ,
            "A polished, preppy shoulder bag." ,
            "A glittery clutch or luxurious designer bag." ,
            "A sleek, minimalist crossbody or top-handle bag." ,
            "A modern geometric bag or multi-functional piece.",

        ],
    },
    {
        "question": "Pick an outfit for a formal setting.",
        "images": [
            'images/QuizOptions/q6o1.jpg',
            'images/QuizOptions/q6o2.jpg',
            'images/QuizOptions/q6o3.jpg',
            'images/QuizOptions/q6o4.jpg',
            'images/QuizOptions/q6o5.jpg',
            'images/QuizOptions/q6o6.jpg',
            'images/QuizOptions/q6o7.jpg',
            'images/QuizOptions/q6o8.jpg',
            'images/QuizOptions/q6o9.jpg',
        ],
        "optionText": [
            "A tailored blazer with trousers or a pencil skirt." ,
            "A soft blouse and a flowy midi skirt." ,
            "A maxi dress with boho accessories that still lok polished." ,
            "Black skinny jeans with a moto jacket or statement heels." ,
            "An oversized blazer with bold sneakers." ,
            "A structured dress with loafers or ballet flats." ,
            "A glamorous jumpsuit or a fitted dress with luxurious details." ,
            "A sleek monochrome outfit with clean lines." ,
            "A trendy co-ord set or a structured power suit.",

        ],
    },
    {
       "question": "Pick your ideal outfit for a nightout.",
        "images": [
            'images/QuizOptions/q7o1.jpg',
            'images/QuizOptions/q7o2.jpg',
            'images/QuizOptions/q7o3.jpg',
            'images/QuizOptions/q7o4.jpg',
            'images/QuizOptions/q7o5.jpg',
            'images/QuizOptions/q7o6.jpg',
            'images/QuizOptions/q7o7.jpg',
            'images/QuizOptions/q7o8.jpg',
            'images/QuizOptions/q7o9.jpg',
        ], 
        "optionText": [
            "A classic little black dress or tailored trousers." ,
            "A romantic dress with soft colors and flowing fabric." ,
            "A boho maxi dress or wide-leg pants with layered jewelry." ,
            "A leather jacket over a bold mini dress." ,
            "A graphic tee with a cool jacket and sneakers. " ,
            "A preppy blazer with fitted jeans or a tailored skirt." ,
            "A sparkling dress with high heels and bold makeup." ,
            "A sleek jumpsuit or modern matching set." ,
            "A trendy outfit with bold accessories to stand out.",

        ],
    },
    {
        "question": "Pick your perfect shopping cart.",
        "images": [
            'images/QuizOptions/q8o1.jpg',
            'images/QuizOptions/q8o2.jpg',
            'images/QuizOptions/q8o3.jpg',
            'images/QuizOptions/q8o4.jpg',
            'images/QuizOptions/q8o5.jpg',
            'images/QuizOptions/q8o6.jpg',
            'images/QuizOptions/q8o7.jpg',
            'images/QuizOptions/q8o8.jpg',
            'images/QuizOptions/q8o9.jpg',
        ],
        "optionText": [
            "I invest in high-quality, timeless pieces." ,
            "I look for romantic patterns and soft fabrics." ,
            "I gravitate toward unique, artisan-made items." ,
            "I hunt for edgy, statement pieces or bold accents." ,
            "I’m always looking for trendy, streetwear-inspired designs." ,
            "I shop at brands with classic, preppy vibes." ,
            "I love luxury brands or anything that sparkles." ,
            "I prefer simple, versatile basics with a polished look." ,
            "I’m drawn to innovative or experimental designs.",

        ],
    },
    {
        "question": "Pick a print or pattern.",
        "images": [
            'images/QuizOptions/q9o1.jpg',
            'images/QuizOptions/q9o2.jpg',
            'images/QuizOptions/q9o3.jpg',
            'images/QuizOptions/q9o4.jpg',
            'images/QuizOptions/q9o5.jpg',
            'images/QuizOptions/q9o6.jpg',
            'images/QuizOptions/q9o7.jpg',
            'images/QuizOptions/q9o8.jpg',
            'images/QuizOptions/q9o9.jpg',
        ],
        "optionText": [
            "Pinstripes or subtle plaid – clean and classic." ,
            "Floral patterns or soft, romantic designs." ,
            "Paisley, tie-dye, or nature-inspired prints." ,
            "Bold, edgy prints like animal prints or abstract patterns." ,
            "Graphic prints or street-style logos." ,
            "Plaid, gingham, or preppy stripes." ,
            "Luxe patterns like metallics or intricate embellishments." ,
            "Minimalistic patterns or solid tones – understated." ,
            "Geometric prints or cutting-edge designs.",

        ],
    },
    {
        "question": "What is your ideal vacation destination?",
        "images": [
            'images/QuizOptions/q10o1.jpg',
            'images/QuizOptions/q10o2.jpg',
            'images/QuizOptions/q10o3.jpg',
            'images/QuizOptions/q10o4.jpg',
            'images/QuizOptions/q10o5.jpg',
            'images/QuizOptions/q10o6.jpg',
            'images/QuizOptions/q10o7.jpg',
            'images/QuizOptions/q10o8.jpg',
            'images/QuizOptions/q10o9.jpg',
        ],
        "optionText": [
            "Vienna, Austria – timeless elegance, grand architecture, and refined culture" ,
            "Tuscany – rolling hills, wine tastings, and romantic villas." ,
            "Bali – serene beaches and boho markets." ,
            "Los Angeles, USA – Gritty city culture, alternative fashion, and urban col" ,
            "New York City – fast-paced urban adventures and trendy neighborhoods" ,
            "The Hamptons, USA – Coastal chic, polo matches, and summer elegance" ,
            "Dubai – luxury shopping, dazzling nightlife, and glamour galore" ,
            "Copenhagen – minimalistic, scandinavian design, and sleek fashion" ,
            "Melbourne, Australia – Creative culture, stylish coffee shops, and progressive fashion",

        ],
    },
    {
        "question": "Describe the vibe you want your outfits to convey.",
        "images": [
            'images/QuizOptions/q11o1.jpg',
            'images/QuizOptions/q11o2.jpg',
            'images/QuizOptions/q11o3.jpg',
            'images/QuizOptions/q11o4.jpg',
            'images/QuizOptions/q11o5.jpg',
            'images/QuizOptions/q11o6.jpg',
            'images/QuizOptions/q11o7.jpg',
            'images/QuizOptions/q11o8.jpg',
            'images/QuizOptions/q11o9.jpg',
        ],
        "optionText": [
            "Timeless and elegant, with pieces that feel polished and professional." ,
            "Soft and delicate, with thoughtful details like lace or florals." ,
            "Relaxed and natural, with flowy silhouettes and an effortless feel." ,
            "Bold and striking, with pieces that grab attention and make a statement." ,
            "Cool and modern, blending casual elements with unique personal touches." ,
            "Polished and put-together, with cordinated and clean designs." ,
            "Luxurious and eye-catching, with dramatic and standout details." ,
            "Simple and refined, with sleek, understated, and structured pieces." ,
            "Experimental and creative, with innovative combinations and fresh ideas.",

        ],
    }
    ]



# Data
styleMappingData = {
    "File Name": [
        "1_1.png", "1_2.png", "1_3.png", "1_4.png", "1_5.png", "1_6.png", "1_7.png", "1_8.png", "1_9.png",
        "2_1.png", "2_2.png", "2_3.png", "2_4.png", "2_5.png", "2_6.png", "2_7.png", "2_8.png", "2_9.png",
        "3_1.png", "3_2.png", "3_3.png", "3_4.png", "3_5.png", "3_6.png", "3_7.png", "3_8.png", "3_9.png",
        "4_1.png", "4_2.png", "4_3.png", "4_4.png", "4_5.png", "4_6.png", "4_7.png", "4_8.png", "4_9.png",
        "5_1.png", "5_2.png", "5_3.png", "5_4.png", "5_5.png", "5_6.png", "5_7.png", "5_8.png", "5_9.png",
        "6_1.png", "6_2.png", "6_3.png", "6_4.png", "6_5.png", "6_6.png", "6_7.png", "6_8.png", "6_9.png",
        "7_1.png", "7_2.png", "7_3.png", "7_4.png", "7_5.png", "7_6.png", "7_7.png", "7_8.png", "7_9.png",
        "8_1.png", "8_2.png", "8_3.png", "8_4.png", "8_5.png", "8_6.png", "8_7.png", "8_8.png", "8_9.png",
        "9_1.png", "9_2.png", "9_3.png", "9_4.png", "9_5.png", "9_6.png", "9_7.png", "9_8.png", "9_9.png"
    ],
    "Primary": [
        "Classic", "Classic", "Classic", "Classic", "Classic", "Classic", "Classic", "Classic", "Classic",
        "Romantic", "Romantic", "Romantic", "Romantic", "Romantic", "Romantic", "Romantic", "Romantic", "Romantic",
        "Bohemian", "Bohemian", "Bohemian", "Bohemian", "Bohemian", "Bohemian", "Bohemian", "Bohemian", "Bohemian",
        "Edgy", "Edgy", "Edgy", "Edgy", "Edgy", "Edgy", "Edgy", "Edgy", "Edgy",
        "Streetstyle", "Streetstyle", "Streetstyle", "Streetstyle", "Streetstyle", "Streetstyle", "Streetstyle", "Streetstyle", "Streetstyle",
        "Preppy", "Preppy", "Preppy", "Preppy", "Preppy", "Preppy", "Preppy", "Preppy", "Preppy",
        "Glamorous", "Glamorous", "Glamorous", "Glamorous", "Glamorous", "Glamorous", "Glamorous", "Glamorous", "Glamorous",
        "Chic", "Chic", "Chic", "Chic", "Chic", "Chic", "Chic", "Chic", "Chic",
        "Contemporary", "Contemporary", "Contemporary", "Contemporary", "Contemporary", "Contemporary", "Contemporary", "Contemporary", "Contemporary"
    ],
    "Secondary": [
        "", "romantic", "bohemian", "edgy", "streetstyle", "preppy", "glamorous", "chic", "contemporary",
        "", "classic", "bohemian", "edgy", "streetstyle", "preppy", "glamorous", "chic", "contemporary",
        "", "classic", "romantic", "edgy", "streetstyle", "preppy", "glamorous", "chic", "contemporary",
        "", "classic", "romantic", "bohemian", "streetstyle", "preppy", "glamorous", "chic", "contemporary",
        "", "classic", "romantic", "bohemian", "edgy", "preppy", "glamorous", "chic", "contemporary",
        "", "classic", "romantic", "bohemian", "edgy", "streetstyle", "glamorous", "chic", "contemporary",
        "", "classic", "romantic", "bohemian", "edgy", "streetstyle", "preppy", "chic", "contemporary",
        "", "classic", "romantic", "bohemian", "edgy", "streetstyle", "preppy", "glamorous", "contemporary",
        "", "classic", "romantic", "bohemian", "edgy", "streetstyle", "preppy", "glamorous", "chic"
    ],
    "Display Name": [
        "Classic", "Romantic", "Bohemian", "Edgy", "Streetstyle", "Preppy", "Glamorous", "Chic", "Contemporary",
        "Romantic", "Classic", "Bohemian", "Edgy", "Streetstyle", "Preppy", "Glamorous", "Chic", "Contemporary",
        "Bohemian", "Classic", "Romantic", "Edgy", "Streetstyle", "Preppy", "Glamorous", "Chic", "Contemporary",
        "Edgy", "Classic", "Romantic", "Bohemian", "Streetstyle", "Preppy", "Glamorous", "Chic", "Contemporary",
        "Streetstyle", "Classic", "Romantic", "Bohemian", "Edgy", "Preppy", "Glamorous", "Chic", "Contemporary",
        "Preppy", "Classic", "Romantic", "Bohemian", "Edgy", "Streetstyle", "Glamorous", "Chic", "Contemporary",
        "Glamorous", "Classic", "Romantic", "Bohemian", "Edgy", "Streetstyle", "Preppy", "Chic", "Contemporary",
        "Chic", "Classic", "Romantic", "Bohemian", "Edgy", "Streetstyle", "Preppy", "Glamorous", "Contemporary",
        "Contemporary", "Classic", "Romantic", "Bohemian", "Edgy", "Streetstyle", "Preppy", "Glamorous", "Chic"
    ]
}


imageToFileNameData = {
    "FileName": [
        "1_1.png", "1_2.png", "1_3.png", "1_4.png", "1_5.png", "1_6.png", "1_7.png", "1_8.png", "1_9.png",
        "2_1.png", "2_2.png", "2_3.png", "2_4.png", "2_5.png", "2_6.png", "2_7.png", "2_8.png", "2_9.png",
        "3_1.png", "3_2.png", "3_3.png", "3_4.png", "3_5.png", "3_6.png", "3_7.png", "3_8.png", "3_9.png",
        "4_1.png", "4_2.png", "4_3.png", "4_4.png", "4_5.png", "4_6.png", "4_7.png", "4_8.png", "4_9.png",
        "5_1.png", "5_2.png", "5_3.png", "5_4.png", "5_5.png", "5_6.png", "5_7.png", "5_8.png", "5_9.png",
        "6_1.png", "6_2.png", "6_3.png", "6_4.png", "6_5.png", "6_6.png", "6_7.png", "6_8.png", "6_9.png",
        "7_1.png", "7_2.png", "7_3.png", "7_4.png", "7_5.png", "7_6.png", "7_7.png", "7_8.png", "7_9.png",
        "8_1.png", "8_2.png", "8_3.png", "8_4.png", "8_5.png", "8_6.png", "8_7.png", "8_8.png", "8_9.png",
        "9_1.png", "9_2.png", "9_3.png", "9_4.png", "9_5.png", "9_6.png", "9_7.png", "9_8.png", "9_9.png"
    ],
    "ImageToMap": [
        "Classic_1.png", "Classic_Romantic.png", "Classic_Bohemian.png", "Classic_Edgy.png",
        "Classic_Streetstyle.png", "Classic_Preppy.png", "Classic_Glamorous.png", "Classic_Chic.png",
        "Classic_Contemporary.png", "Romantic_1.png", "Romantic_Classic.png", "Romantic_Bohemian.png",
        "Romantic_Edgy.png", "Romantic_Streetstyle.png", "Romantic_Preppy.png", "Romantic_Glamorous.png",
        "Romantic_Chic.png", "Romantic_Contemporary.png", "Bohemian_1.png", "Bohemian_Classic.png",
        "Bohemian_Romantic.png", "Bohemian_Edgy.png", "Bohemian_Streetstyle.png", "Bohemian_Preppy.png",
        "Bohemian_Glamorous.png", "Bohemian_Chic.png", "Bohemian_Contemporary.png", "Edgy_1.png",
        "Edgy_Classic.png", "Edgy_Romantic.png", "Edgy_Bohemian.png", "Edgy_Streetstyle.png",
        "Edgy_Preppy.png", "Edgy_Glamorous.png", "Edgy_Chic.png", "Edgy_Contemporary.png",
        "Streetstyle_1.png", "Streetstyle_Classic.png", "Streetstyle_Romantic.png", "Streetstyle_Bohemian.png",
        "Streetstyle_Edgy.png", "Streetstyle_Preppy.png", "Streetstyle_Glamorous.png", "Streetstyle_Chic.png",
        "Streetstyle_Contemporary.png", "Preppy_1.png", "Preppy_Classic.png", "Preppy_Romantic.png",
        "Preppy_Bohemian.png", "Preppy_Edgy.png", "Preppy_Streetstyle.png", "Preppy_Glamorous.png",
        "Preppy_Chic.png", "Preppy_Contemporary.png", "Glamorous_1.png", "Glamorous_Classic.png",
        "Glamorous_Romantic.png", "Glamorous_Bohemian.png", "Glamorous_Edgy.png", "Glamorous_Streetstyle.png",
        "Glamorous_Preppy.png", "Glamorous_Chic.png", "Glamorous_Contemporary.png", "Chic_1.png",
        "Chic_Classic.png", "Chic_Romantic.png", "Chic_Bohemian.png", "Chic_Edgy.png", "Chic_Streetstyle.png",
        "Chic_Preppy.png", "Chic_Glamorous.png", "Chic_Contemporary.png", "Contemporary_1.png",
        "Contemporary_Classic.png", "Contemporary_Romantic.png", "Contemporary_Bohemian.png",
        "Contemporary_Edgy.png", "Contemporary_Streetstyle.png", "Contemporary_Preppy.png",
        "Contemporary_Glamorous.png", "Contemporary_Chic.png"
    ]
}

logging.basicConfig(
    filename=f"wellInformedLog{datetime.now().date()}.log", level=logging.INFO
)
formatter = logging.Formatter("%(levelname)s - %(message)s - %(Time)s")

# Create DataFrame
styleMappingDataDf = pd.DataFrame(styleMappingData)

stylesNoData = {
    "StyleNo": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Style": [
        "Classic", "Romantic", "Bohemian", "Edgy", "Streetstyle",
        "Preppy", "Glamorous", "Chic", "Contemporary"
    ]
}

stylesDf = pd.DataFrame(stylesNoData)

imageToFileNameDataDf = pd.DataFrame(imageToFileNameData)
# Home Page
def home(request):
    request.session.flush()
    return render(request, 'home.html')

# Display Questions
def quiz(request, questionId = 0):
    if questionId >= len(quizData):
        return HttpResponse("Quiz completed! Thank you.")

    context = {
        "question": quizData[questionId]["question"],
        "images": quizData[questionId]["images"],
        "optionTexts":quizData[questionId]["optionText"],
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
            return render(request, "measurementQuiz.html")

    return redirect("quiz")

def measurementQuiz(request):
    if request.method == "POST":
        sex = request.POST.get("sex")
        age = request.POST.get("age")
        waist = request.POST.get("waist")
        bust = request.POST.get("bust")
        shoulder = request.POST.get("shoulder")
        hip = request.POST.get("hip")
        
        bodyType = determine_body_type(shoulder=int(shoulder), bust=int(bust), waist=int(waist), hip = int(hip))
        
        return redirect(reverse("results", kwargs={"bodyType": bodyType}))
    
    return render(request, "measurementQuiz.html")
# Calculate and Display Results
def results(request, bodyType="Not in Calculations"):
    if 'user_id' not in request.session:
        request.session['user_id'] = str(uuid.uuid4())  # Generate a unique ID
    user_id = request.session['user_id']
    
    # responses = UserResponse.objects.filter(user_id=user_id)
    responses = request.session["responses"]
    try:
        styleScoresDf = pd.DataFrame(responses)
        # Count style personality preferences
        styleScoresDf = styleScoresDf.groupby('answer').agg(len)
        styleScoresDf= styleScoresDf.reset_index()
        styleScoresDf.columns=["StyleNo", "Count"]
        styleScoresDf = styleScoresDf.sort_values(by="Count", ascending=False)
        styleScoresDf = styleScoresDf.head(3)

        styleScoresDf["StyleNo"] = styleScoresDf["StyleNo"].astype(int)
        styleScoresDf["StyleNo"] = styleScoresDf["StyleNo"].apply(lambda x :x +1)
        styleScoresDf["Style"] = styleScoresDf["StyleNo"].map(stylesDf.set_index("StyleNo")["Style"])
        styleScoresDf= styleScoresDf.reset_index(drop=True)
    except Exception as e:
        logging.error(f"Exception Occured{e} \n responses: {responses}")    
    logging.info(f"styleScoresDf ", extra=styleScoresDf)
    style1 = styleScoresDf.iloc[0]["Style"]
    styleNoImageToMap1 = f"{styleScoresDf.iloc[0]['Style']}_1.png"
    styleNoImage1 = imageToFileNameDataDf[imageToFileNameDataDf["ImageToMap"] == styleNoImageToMap1]["FileName"].iloc[0]
    styleNoPercentage1 = f"{round(styleScoresDf.iloc[0]['Count']*100/11,1)}"
    if len(styleScoresDf)>1:
        style2 = styleScoresDf.iloc[1]["Style"]
        styleNoImageToMap2 = f"{styleScoresDf.iloc[0]['Style']}_{styleScoresDf.iloc[1]['Style']}.png"
        styleNoImage2 = imageToFileNameDataDf[imageToFileNameDataDf["ImageToMap"] == styleNoImageToMap2]["FileName"]
        styleNoImage2 = styleNoImage2.iloc[0]
        styleNoPercentage2 = f"{round(styleScoresDf.iloc[1]['Count']*100/11,1)}"
    else:
        style2 = "Not Identified"
        styleNoPercentage2 = "0"
        styleNoImage2 = ""
    if len(styleScoresDf)>2:
        style3 = styleScoresDf.iloc[2]["Style"]
        styleNoImageToMap3 = f"{styleScoresDf.iloc[0]['Style']}_{styleScoresDf.iloc[2]['Style']}.png"
        styleNoImage3 = imageToFileNameDataDf[imageToFileNameDataDf["ImageToMap"] == styleNoImageToMap3]["FileName"].iloc[0]
        styleNoPercentage3 = f"{round(styleScoresDf.iloc[2]['Count']*100/11,1)}"
    else:
        style3 = "Not Identified"
        styleNoPercentage3 = "0"
        styleNoImage3 = ""

    UserResponse.objects.create(
            user_id=user_id,
            responses=responses
        )

    styleCards = [
        {   
            "image": generate_presigned_url(styleNoImage1),  # Path to the image in the static folder
            "styleTitle": style1,
            "percentage": styleNoPercentage1
        },
        {
            "image": generate_presigned_url(styleNoImage2),  # Path to the image in the static folder
            "styleTitle": style2,
            "percentage": styleNoPercentage2
        },
        {
            "image": generate_presigned_url(styleNoImage3),  # Path to the image in the static folder
            "styleTitle": style3,
            "percentage": styleNoPercentage3
        }
    ]
    if bodyType is None:
        bodyTypeDict = {"text":"Body type does not fit predefined categories. Please recheck your input measurements and try again.",
                        "bodyTypeImage":f"images/BodyType/NoFit.png"}
    else:
        bodyTypeDict = {"text":bodyType,
                        "bodyTypeImage":f"images/BodyType/{bodyType}.png"}
    context = {
        "styleCards": styleCards,
        "bodyType": bodyTypeDict
    }
    logging.info(f"{context}")

    return render(request, "results.html", context)

# Feedback Page
def feedback(request):
    return render(request, 'feedback.html')

@csrf_exempt  # Temporarily disable CSRF for testing (use proper CSRF handling in production)
def submit_feedback(request):
    if request.method == 'POST':
        # Retrieve form data

        user_id = request.session['user_id']  # Retrieve the session-based user ID
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        location = request.POST.get('location')
        occupation = request.POST.get('occupation')
        style_personality_accuracy = request.POST.get('style_personality_accuracy')
        clothing_suggestions_accuracy = request.POST.get('clothing_suggestions_accuracy')
        style_personality_thoughts = request.POST.get('style_personality_thoughts')
        body_type_accuracy = request.POST.get('body_type_accuracy')
        body_type_suggestions_accuracy = request.POST.get('body_type_suggestions_accuracy')
        body_type_thoughts = request.POST.get('body_type_thoughts')
        outfit_challenge = request.POST.get('outfit_challenge')
        quiz_improvements = request.POST.getlist('features')  # Since checkboxes return multiple values
        quiz_improvements_other = request.POST.get('other_features')
        styling_service = request.POST.get('styling_service')
        styling_service_price = request.POST.get('styling_service_price')
        final_thoughts = request.POST.get('comments')

        # Save the feedback to the database
        feedback = Feedback.objects.create(
            user_id=user_id,
            name=name,
            email=email,
            age=age if age else None,  # Handle empty fields properly
            location=location,
            occupation=occupation,
            style_personality_accuracy=style_personality_accuracy,
            clothing_suggestions_accuracy=clothing_suggestions_accuracy,
            style_personality_thoughts=style_personality_thoughts,
            body_type_accuracy=body_type_accuracy,
            body_type_suggestions_accuracy=body_type_suggestions_accuracy,
            body_type_thoughts=body_type_thoughts,
            outfit_challenge=outfit_challenge,
            quiz_improvements=quiz_improvements,  # JSONField stores a list
            quiz_improvements_other=quiz_improvements_other,
            styling_service=styling_service,
            styling_service_price=styling_service_price,
            final_thoughts=final_thoughts,
        )

        return render(request, 'thankyou.html')
    else:
        return HttpResponse("Invalid request method.")
    
# Function to calculate the body type based on the input measurements
def determine_body_type(shoulder, bust, waist, hip):
    # Ensure measurements are valid and not zero
    if shoulder <= 0 or bust <= 0 or waist <= 0 or hip <= 0:
        return "Measurements must be greater than zero."

    # Calculate percentage differences
    shoulder_bust_diff = abs(shoulder - bust) / max(shoulder, bust)
    bust_hip_diff = abs(bust - hip) / max(bust, hip)
    shoulder_hip_diff = abs(shoulder - hip) / max(shoulder, hip)

    if (
        shoulder_bust_diff <= 0.05
        and (waist >= bust * 0.75)
    ):
        return "Rectangle"
    elif (
        hip > max(shoulder, bust) * 1.05
    ) and hip > waist:
        return "Pear"
    elif waist >= hip:
        if shoulder > hip * 1.05:
            return "InvertedTriangle"
        elif bust > hip * 1.05:
            return "InvertedTriangle"
    elif (
        bust_hip_diff <= 0.05
        and (waist <= bust * 0.75 or waist <= hip * 0.75)
    ):
        return "Hourglass"
    elif (
        (hip >= shoulder * 0.95 or hip >= bust * 0.95)
        and waist >= bust
    ):
        return "Apple"
    else:
        return None



# @staticmethod
def generate_presigned_url(path, expiration=3600):
    s3 = boto3.client(
            's3',
            region_name='ap-south-1',  # Mumbai region
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'managed-documents',
                'Key': f'ImageData/{path}',
                # 'Content-Disposition': 'inline',
                'ResponseContentDisposition': 'inline',
            },
            ExpiresIn=expiration
        )
        print(url)
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None