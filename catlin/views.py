import json
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from catlin.models import (
Category, Page, CategoryMap, Comment, LikePage, LikeComment, LikeCategory
)
from users.models import Profile
from .forms import AddCategoryForm, AddPageForm, AddCommentForm
from catlin.search.mysearch import compare_strings


def like_my_model(my_request, entity_model, like_model):
    """
    like_model = LikePage, LikeComment, LikeCategory
    entity_model = Page, Comment, Category
    AJAX post request must contain: entity_id, liketype('L' or 'D')
    returns dict {likes, dislikes}
    """
    entity_id = None
    like_type = None
    not_like_type = 'D'
    like_type_count = 0
    not_like_type_count = 0
    likes = 0
    dislikes = 0
    user = Profile.objects.get(user=my_request.user)
    if my_request.method == "POST":
        entity_id = my_request.POST['entity_id']
        like_type = my_request.POST['liketype']
        if like_type == 'D':
            not_like_type = 'L'
    if entity_id:
        entity_obj = entity_model.objects.get(id=int(entity_id))
        if entity_obj:
            # likes = entity_obj.like_count #
            # dislikes = entity_obj.dislike_count #
            try:
                like_obj = like_model.objects.get(entity=entity_obj, user=user)
                if like_obj.type == like_type:
                    like_obj.delete()
                    like_type_count -= 1
                elif like_obj.type == not_like_type:
                    like_obj.type = like_type
                    like_obj.save()
                    like_type_count += 1
                    not_like_type_count -= 1
            except like_model.DoesNotExist:
                like_obj = like_model(entity=entity_obj, user=user, type=like_type)
                like_obj.save()
                like_type_count += 1
            if like_type == 'L':
                likes += like_type_count
                dislikes += not_like_type_count
            elif like_type == 'D':
                likes += not_like_type_count
                dislikes += like_type_count
            entity_obj.like_count += likes
            entity_obj.dislike_count += dislikes
            entity_obj.save()
            if entity_model == Category and entity_obj.user:
                entity_obj.user.like_count += likes
                entity_obj.user.dislike_count += dislikes
                entity_obj.user.save()
    return {'likes':entity_obj.like_count, 'dislikes':entity_obj.dislike_count}
def get_search_categories(search_string, max_results = 25, threshold = 0):
    search_result_cats = []
    cat_score_list = []
    cat_id_list = []
    category_list = Category.objects.all()

    #Filling cat_score_list, cat_id_list
    for category in category_list:
        cat_score_list.append(compare_strings(search_string, category.title))
        cat_id_list.append(category.id)

    #Collecting matched ids
    for i in range(0, max_results):
        max1 = max(cat_score_list)
        if max1 > threshold:
            index = cat_score_list.index(max1)
            search_result_cats.append(category_list.get(id=cat_id_list[index]))
            cat_score_list[index] = 0
    return search_result_cats

def get_search_pages(search_string, max_results = 25, threshold = 0):
    search_result_pages = []
    page_score_list = []
    page_id_list = []
    page_list = Page.objects.all()
    #Filling page_score_list, page_id_list
    for page in page_list:
        page_score_list.append(compare_strings(search_string, page.title))
        page_id_list.append(page.id)

    #Collecting matched ids
    for i in range(0, max_results):
        max1 = max(page_score_list)
        if max1 > threshold:
            index = page_score_list.index(max1)
            search_result_pages.append(page_list.get(id=page_id_list[index]))
            page_score_list[index] = 0
    return search_result_pages

def get_search_users(search_string, max_results = 25, threshold = 0):
    search_result_users = []
    user_score_list = []
    user_id_list = []
    user_list = Profile.objects.all()
    #Filling page_score_list, page_id_list
    for user in user_list:
        user_score_list.append(compare_strings(search_string, user.user.username))
        user_id_list.append(user.id)

    #Collecting matched ids
    for i in range(0, max_results):
        max1 = max(user_score_list)
        if max1 > threshold:
            index = user_score_list.index(max1)
            search_result_users.append(user_list.get(id=user_id_list[index]))
            user_score_list[index] = 0
    return search_result_users

# Create your views here.
def index(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 5)
    page_no = request.GET.get('page')
    categories = paginator.get_page(page_no)
    context = {
        'categories':categories,
        'heading':'All Linkgroups'
    }
    return render(request, 'catlin/category_list.html', context)

def users_categories(request, username):
    try:
        author = Profile.objects.get(user__username = username)
    except Profile.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'user'})
    category_list = Category.objects.filter(user=author)
    paginator = Paginator(category_list, 5)
    page_no = request.GET.get('page')
    categories = paginator.get_page(page_no)
    context = {
        'categories':categories,
        'heading': 'Linkgroups of '+ username,
    }
    return render(request, 'catlin/category_list.html', context)

def category(request, category_id):
    comment_index = 0 #some request object
    no_of_comments = 5 #fixed see more comments
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'category'})
    category.views += 1
    category.save()
    pages = Page.objects.filter(category=category).order_by('-like_count')[:5]
    main_comments = Comment.objects.filter(category=category, depth='M').order_by('-last_modified')[comment_index:comment_index+no_of_comments]
    main_comment_form = AddCommentForm()
    context = {
        'category':category,
        'pages':pages,
        'comments':main_comments,
        'main_comment_form':main_comment_form,
    }
    return render(request, 'catlin/category.html', context)

def category_pages(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'category'})
    page_list = Page.objects.filter(category=category)
    paginator = Paginator(page_list, 5)
    page_no = request.GET.get('page')
    pages = paginator.get_page(page_no)
    context = {
        'pages':pages,
        'heading':category.title,
        'type':'category pages',
    }
    return render(request, 'catlin/page_list.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            user = Profile.objects.get(user=request.user)
            cat = Category(
                title = form.cleaned_data['title'],
                summary = form.cleaned_data['summary'],
                user = user,
            )
            user.category_count += 1
            user.save()
            cat.save()
            return HttpResponseRedirect(reverse('catlin:update_category', args=[cat.id]))
    else:
        form = AddCategoryForm()
    context = {
    'form':form,
    }
    return render(request,'catlin/add_category.html', context)

@login_required
def add_page(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'category'})
    if request.method == 'POST' and request.user == category.user.user:
        form = AddPageForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            page = Page(
                title = form.cleaned_data['title'],
                summary = form.cleaned_data['summary'],
                url = form.cleaned_data['url'],
                category = category
                )
            page.save()
            category.page_count += 1
            category.save()
            return HttpResponseRedirect(reverse('catlin:update_category', args=[category_id]))
    elif request.user != category.user.user:
        return render(request, 'catlin/not_authorised.html',{})
    form = AddPageForm()
    context = {
        'category_id': category_id,
        'form':form,
    }
    return render(request, 'catlin/add_page.html', context)

@login_required
def delete_page(request, page_id):
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'page'})
    user = page.category.user
    if user.user == request.user:
        return render(request, 'catlin/verify_page_delete.html', {'page':page})
    return render(request, 'catlin/not_authorised.html',{})

@login_required
def delete_page_verify(request, page_id):
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'page'})
    category = page.category
    user = category.user
    if user.user == request.user and request.method=='POST':
        page.delete()
        category.page_count -= 1
        category.save()
        messages.success(request, "The link was deleted successfully.")
        return redirect('catlin:update_category', category_id=category.id)
    return render(request, 'catlin/not_authorised.html',{})

@login_required
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'category'})
    if request.user == category.user.user:
        pages = Page.objects.filter(category=category).order_by('-like_count')
        context = {
        'pages':pages,
        'category':category
        }
        return render(request,'catlin/update_category.html', context)
    return render(request, 'catlin/not_authorised.html',{})

@login_required
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'category'})
    user = category.user
    if user.user == request.user:
        return render(request, 'catlin/verify_category_delete.html', {'category':category})
    return render(request, 'catlin/not_authorised.html')

@login_required
def delete_category_verified(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/not_exist.html', {'type':'category'})
    user = category.user
    if user.user == request.user and request.method=='POST':
        category.delete()
        user.category_count -= 1
        user.save()
        messages.success(request, "The linkgroup was deleted successfully.")
        return redirect('catlin:index')
    return render(request, 'catlin/not_authorised.html',{})

@login_required
def add_comment(request):
    if request.method == 'POST':
        type = 'M'
        parent_comment = None
        user = Profile.objects.get(user=request.user)
        comment_content = request.POST['comment_content']
        category_id = request.POST['category_id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'catlin/not_exist.html', {'type':'category'})
        if request.POST['type'] == 'N':
            type = 'N'
            try:
                parent_comment = Comment.objects.get(id=request.POST['comment_id'], category=category)
                parent_comment.comment_count += 1
                parent_comment.save()
                print(parent_comment.comment_count)
            except Comment.DoesNotExist:
                return render(request, 'catlin/not_exist.html', {'type':'category'})
        print(user, parent_comment,type, comment_content, category_id)
        comment = Comment(
            content = comment_content,
            user = user,
            category = category,
            parent_comment = parent_comment,
            depth=type,
        )
        comment.save()
        category.comment_count += 1
        category.save()
        try:
            parent_comment_count = parent_comment.comment_count
        except:
            parent_comment_count = 0
        context = {
            'id':comment.id,
            'content':comment.content,
            'username':comment.user.user.username,
            'last_modified':comment.last_modified,
            'like_count':comment.like_count,
            'dislike_count':comment.dislike_count,
            'parent_comment_count':parent_comment_count
        }
    else :
        return render(request, 'catlin/not_authorised.html',{})
    return JsonResponse(context)

def search_pages(request):
    search_string = request.GET['search_string']
    page_list = get_search_pages(search_string, max_results=10, threshold = 0.25)
    paginator = Paginator(page_list, 5)
    page_no = request.GET.get('page')
    pages = paginator.get_page(page_no)
    context = {
        'pages':pages,
        'heading':search_string,
        'type':'page search',
    }
    return render(request, 'catlin/page_list.html', context)

def search(request):
    search_string = request.GET['search_string']
    category_list = get_search_categories(search_string, max_results=10, threshold = 0.25)
    paginator = Paginator(category_list, 5)
    page_no = request.GET.get('page')
    categories = paginator.get_page(page_no)
    context = {
        'categories': categories,
        'heading':search_string,
        'type':'category search',
    }
    return render(request, 'catlin/search.html', context)

def search_users(request):
    search_string = request.GET['search_string']
    user_list = get_search_users(search_string, max_results=10, threshold = 0.25)
    paginator = Paginator(user_list, 5)
    page_no = request.GET.get('page')
    users = paginator.get_page(page_no)
    context = {
        'users': users,
        'heading':search_string,
        'type':'users search',
    }
    return render(request, 'catlin/user_list.html', context)

@login_required
def like_category(request):
    #add like_category object (test)
    #increment category like_count (test)
    #increment category's owner like_count (test)
    #check if the same user has not disliked, remove dislike add like
    json_context = like_my_model(my_request=request, entity_model=Category, like_model=LikeCategory)
    return JsonResponse(json_context)

@login_required
def like_page(request):
    json_context = like_my_model(my_request=request, entity_model=Page, like_model=LikePage)
    return JsonResponse(json_context)

@login_required
def like_comment(request):
    json_context = like_my_model(my_request=request, entity_model=Comment, like_model=LikeComment)
    return JsonResponse(json_context)

def goto_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    page.views += 1
    page.save()
    return redirect(page.url)

def about(request):
    return render(request, 'catlin/about.html')

def see_replies(request):
    main_comment_id = request.GET['main_comment_id']
    nested_comments = get_list_or_404(Comment, parent_comment__id=main_comment_id)
    likes = []
    dislikes = []
    usernames = []
    nc_ids = []
    last_modifieds = []
    contents = []
    if nested_comments:
        for comment in nested_comments:
            likes.append(comment.like_count)
            dislikes.append(comment.dislike_count)
            usernames.append(comment.user.user.username)
            nc_ids.append(comment.id)
            last_modifieds.append(comment.last_modified)
            contents.append(comment.content)
    json_context1 = {
    'likes':likes,
    'dislikes':dislikes,
    'usernames':usernames,
    'nc_ids':nc_ids,
    'last_modifieds':last_modifieds,
    'contents': contents
    }
    return JsonResponse(json_context1)

@login_required
def del_cat_successfull(request):
    return render(request, 'catlin/not_exist.html', {'type':'category'})

def latest_categories(request):
    category_list = Category.objects.all().order_by('-last_modified')
    paginator = Paginator(category_list, 5)
    page_no = request.GET.get('page')
    categories = paginator.get_page(page_no)
    context = {
        'categories':categories,
        'heading':'Latest Linkgroups'
    }
    return render(request, 'catlin/category_list.html', context)

def most_liked_categories(request):
    category_list = Category.objects.all().order_by('-like_count')
    paginator = Paginator(category_list, 5)
    page_no = request.GET.get('page')
    categories = paginator.get_page(page_no)
    context = {
        'categories':categories,
        'heading':'Most Liked Linkgroups'
    }
    return render(request, 'catlin/category_list.html', context)

def search_users_page(request):
    user_list = Profile.objects.all().order_by('-category_count')
    paginator = Paginator(user_list, 5)
    page_no = request.GET.get('page')
    users = paginator.get_page(page_no)
    context = {
        'users': users,
        'heading':'All Users',
        'type':'users search',
    }
    return render(request, 'catlin/user_list.html', context)
