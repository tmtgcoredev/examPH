from .api import *
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import jwt


def authenticate_user(request):
    # request.session["user_token"] = "user_token"
    request.session.modified = True
    # try:
    #     for key, value in request.session.items():
    #         print('{}: {}'.format(key, value))
                 
    #     try:   
    #         user_token = request.session['user_token'] 
    #         payload = jwt.decode(user_token, API_SECRET_KEY, algorithms=['HS256'])

    #         # SAVE JWT PAYLOAD INTO SESSIONS
    #         for key,value in payload.items():
    #             if key == 'data':
    #                 for key,value in payload['data'].items():
    #                     if request.session[key]:
    #                         pass
    #                     else:
    #                         request.session[key] = value
    #                         request.session.modified = True
    #         return True
        
    #     except jwt.ExpiredSignatureError:
    #         # signout(request)
    #         return False
        
    # except KeyError:
    #     # signout(request)
    #     return False
def home(request):
    template_name = "index.html"
    return render(request, template_name)

def dashboard(request):
    template_name = "main/dashboard.html"
    context = {}  
    authenticate_user(request)
    # user_token = request.session['user_token']
    user_token = APP_TOKEN
    
    all_exams_data = get_exams_list(user_token)
    paginator = Paginator(all_exams_data, 10)
    page = request.GET.get('page')
    
    try:
        exams_data = paginator.page(page)
    except PageNotAnInteger:
        exams_data = paginator.page(1)
    except EmptyPage:
        exams_data = paginator.page(paginator.num_pages)
        
    context['exams_data'] = exams_data  
        
    return render(request, template_name, context)
def exams(request):
    template_name = "main/exams.html"
    context = {}
    authenticate_user(request)
    # user_token = request.session['user_token']
    user_token = APP_TOKEN
    all_exams_data = get_exams_list(user_token)
    paginator = Paginator(all_exams_data, 10)
    page = request.GET.get('page')
    
    try:
        exams_data = paginator.page(page)
    except PageNotAnInteger:
        exams_data = paginator.page(1)
    except EmptyPage:
        exams_data = paginator.page(paginator.num_pages)
        
    context['exams_data'] = exams_data
    
    return render(request, template_name, context)

def podcast(request):
    template_name = "main/podcast.html"
    context = {}
        
    return render(request, template_name, context)

def review(request):
    template_name = "main/review.html"
    context = {}
        
    return render(request, template_name, context)

def leaderboards(request):
    template_name = "main/leaderboards.html"
    context = {}
        
    return render(request, template_name, context)

def sections(request, exam_uuid):
    template_name = "exams/sections.html"
    context = {}  
    authenticate_user(request)
    # user_token = request.session['user_token']
    user_token = APP_TOKEN
    
    all_sections_data = get_sections_list(user_token,exam_uuid)
    paginator = Paginator(all_sections_data, 10)
    page = request.GET.get('page')
    
    try:
        sections_data = paginator.page(page)
    except PageNotAnInteger:
        sections_data = paginator.page(1)
    except EmptyPage:
        sections_data = paginator.page(paginator.num_pages)
        
    context['sections_data'] = sections_data
        
    return render(request, template_name, context)

def items(request, section_uuid):
    template_name = "exams/items.html"
    context = {}  
    authenticate_user(request)
    user_token = APP_TOKEN
    
    all_items_data, items_uuid = get_items_list(user_token, section_uuid)
    items_with_choices = []
    
    for item in all_items_data:
        choices_data = get_choices_list(user_token, item['uuid'])
        labeled_choices = [{'label': chr(65+i), 'data': choice} for i, choice in enumerate(choices_data)]
        item['choices'] = labeled_choices
        items_with_choices.append(item)
    
    paginator = Paginator(items_with_choices, 10)
    page = request.GET.get('page')
    
    try:
        items_data = paginator.page(page)
    except PageNotAnInteger:
        items_data = paginator.page(1)
    except EmptyPage:
        items_data = paginator.page(paginator.num_pages)
        
    context['items_data'] = items_data
    
    return render(request, template_name, context)

def quizzes(request, section_uuid):
    template_name = "exams/quizzes.html"
    choices = []
    context = {}
    authenticate_user(request)
    # user_token = request.session['user_token']
    user_token = APP_TOKEN
    
    all_items_data, items_uuid = get_items_list(user_token,section_uuid)
    index = 0
    for item_uuid in items_uuid:
        choices_data = get_choices_list(user_token,item_uuid)
        choices.append(choices_data)
        index+=1
        char_index = chr(index + 65)
    choices = [item for sublist in choices for item in sublist]
    
    paginator = Paginator(all_items_data, 1)
    page = request.GET.get('page')
    
    try:
        items_data = paginator.page(page)
    except PageNotAnInteger:
        items_data = paginator.page(1)
    except EmptyPage:
        items_data = paginator.page(paginator.num_pages)
        
    context['items_data'] = items_data
    context['choices_data'] = choices
    context['index'] = index
    context['char_index'] = char_index
        
    return render(request, template_name, context)