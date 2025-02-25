import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import IntegrityError
import markdown
from openai import OpenAI
from django.urls import reverse
from .models import User, Course


api_key = "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"


def create_course_pages():
    for content_file in os.listdir('learnerapp/content'):
        if content_file.endswith('.txt'):
            continue

        with open('learnerapp/content/completed.txt') as completed:
            if content_file in completed.read():
                break

        with open(f'learnerapp/content/{content_file}', 'r') as content_data:
            with open(f'learnerapp/content/completed.txt', 'a') as completed:
                completed.write(content_file+'\n')

            pages = []
            lines = []

            for line in content_data:
                if line.startswith('~'):
                    pages.append(lines)
                    lines = [line]
                else:
                    lines.append(line)

            i=0
            course_folder_name = content_file.split('.')[0]
            os.mkdir(f'learnerapp/content/{course_folder_name}')
            for lines in pages:
                if not lines:
                    continue
                i+=1
                with open(f"learnerapp/content/{course_folder_name}/{i}.txt", "w") as lesson:
                    para = ""
                    for line in lines:
                        para+=line

                    lesson.write(str(para))


def index(request):
    create_course_pages()
    lessons = []
    for folder in os.scandir('learnerapp/content'):
        if folder.is_dir():
            for file2 in os.scandir(f'learnerapp/content/{folder.name}'):
                with open(f'learnerapp/content/{folder.name}/{file2.name}', 'r') as f:
                    lessons.append({
                        'url': f"{folder.name}/{file2.name.split('.')[0]}",
                        'title': markdown.markdown(f.readline()[2:]),
                        'content': markdown.markdown(f.read()),
                        'id': int(file2.name.split('.')[0])
                    })
    return render(request, 'home.html', {
        'lessons': sorted(lessons, key=lambda x: x['id'])
    })


def get_lesson(request, lesson_name, lesson_id):
    with open(f'learnerapp/content/{lesson_name}/{lesson_id}.txt', 'r') as lesson_content:
        content = lesson_content.read().replace('~', "#")
        prompt = f"Don't say anything else just Make the content a bit easier to understand without removing any points and format nicely using markdown: {content}"
        if request.user.is_authenticated:
            user = request.user
            if user.quizzes_attempted >= 5:
                if user.avg_score > 9:
                    prompt = f"Don't say anything else Make the content a bit easier to understand without removing any points and format nicely using markdown in about 150 words: {content}"
                elif user.avg_score > 7:
                    prompt = f"Don't say anything else Make the content easier to understand by including examples without removing any points and format nicely using markdown in about 250 words: {content}"
                elif user.avg_score > 4:
                    prompt = f"Don't say anything else Make the content a simpler and easier to understand by giving real world examples without removing any points and format nicely using markdown in about 300 words: {content}"

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )

            completion = client.chat.completions.create(
                model="google/gemini-2.0-pro-exp-02-05:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            ai_content = completion.choices[0].message.content
        except:
            ai_content = "An error occured"

        return render(request, 'lesson.html', {
            'content': markdown.markdown(ai_content),
            'raw_content': ai_content,
            'lesson_name': lesson_name,
            'lesson_id': lesson_id
        })


@login_required(login_url="/login/")
def get_quiz(request, lesson_name, lesson_id):
    content = ""
    try:
        with open(f'learnerapp/content/{lesson_name}/{lesson_id}.txt', 'r') as f:
            content = f.read()

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        completion = client.chat.completions.create(
            model="google/gemini-2.0-pro-exp-02-05:free",
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a set of 10 question mcq quiz from the course content: {content}. prefix questions with '---' and prefix options with '\n++', if it's the correct option add another prefix '-' to it. Don't add any other unnecessary characters. Each question should have 4 options."
                }
            ]
        )
        ai_content = completion.choices[0].message.content
    except:
        ai_content="An error occured"

    quiz_content = {}

    ai_content = ai_content.split("---")
    print(ai_content)
    for problem in ai_content:
        question = problem.split("\n++")[0]
        options = problem.split("\n++")[1:]
        quiz_content.update({
            question: options[0:5]
        })
    print(quiz_content)
    return render(request, 'quiz.html', {
        'content': quiz_content
    })


@login_required(login_url="/login/")
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url="/login/")
def leaderboard(request):
    users = User.objects.all().order_by('-points')
    return render(request, 'leaderboard.html', {
        'users': users
    })


def chatbot(request):
    return render(request, 'chatbot.html')


@login_required(login_url="/login/")
def submit_quiz(request, score):
    score = int(score)
    user = request.user

    if user.quizzes_attempted < 1:
        user.score1 = score
    elif user.quizzes_attempted < 2:
        user.score2 = score
    elif user.quizzes_attempted < 3:
        user.score3 = score
    elif user.quizzes_attempted < 4:
        user.score4 = score
    elif user.quizzes_attempted < 5:
        user.score5 = score

    if score < 5:
        message = "Please redo the quiz to move ahead"
    else:
        user.score1 = user.score2
        user.score2 = user.score3
        user.score3 = user.score4
        user.score4 = score
        user.avg_score = (user.score1 + user.score2 + user.score3 + user.score4)/4
        user.points += score
        user.level_completed+=1
        if score % 50 is 0:
            user.badges_won += 1
        message = f"You scored{score}"
    user.save()
    return JsonResponse({
        'message': message
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, 'survey_form.html')
    else:
        return render(request, "register.html")


def survey(request):
    if request.method == "POST":
        age = int(request.POST["age"])
        experience_level = int(request.POST["experience_level"])
        if age < 9:
            request.user.avg_score = 3
        elif age < 15:
            request.user.avg_score = 6
        else:
            request.user.avg_score = 8

        if experience_level > 1:
            request.user.avg_score += 1
        elif experience_level > 2:
            request.user.avg_score += 2

    return HttpResponseRedirect(reverse("index"))