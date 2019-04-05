import json
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from catlin.models import (
Category, Page, UserProfile, CategoryMap, Comment, LikePage, LikeComment, LikeCategory
)
from .forms import AddCategoryForm, AddPageForm, AddCommentForm

def like_my_model(my_request, entity_model, like_model):
    # like_model = LikePage, LikeComment, LikeCategory
    # entity_model = Page, Comment, Category
    # AJAX post request must contain: entity_id, liketype('L' or 'D')
    # returns dict {likes, dislikes}
    entity_id = None
    like_type = None
    not_like_type = 'D'
    like_type_count = 0
    not_like_type_count = 0
    likes = 0
    dislikes = 0
    user = UserProfile.objects.get(user=my_request.user)
    if my_request.method == "POST":
        entity_id = my_request.POST['entity_id']
        like_type = my_request.POST['liketype']
        if like_type == 'D':
            not_like_type = 'L'
    if entity_id:
        entity_obj = entity_model.objects.get(id=int(entity_id))
        if entity_obj:
            likes = entity_obj.like_count
            dislikes = entity_obj.dislike_count
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
            entity_obj.like_count = likes
            entity_obj.dislike_count = dislikes
            entity_obj.save()
            if entity_model == Category:
                entity_obj.user.like_count = likes
                entity_obj.user.dislike_count = dislikes
                entity_obj.user.save()
    return {'likes':likes, 'dislikes':dislikes}

# Create your views here.
def index(request):
    return render(request, 'catlin/index.html', {})

def category(request, category_id):
    comment_index = 0 #some request object
    no_of_comments = 5 #fixed see more comments
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/cat_not_exist.html', {})
    category.views += 1
    category.save()
    pages = Page.objects.filter(category=category).order_by('-like_count')
    main_comments = Comment.objects.filter(category=category, depth='M').order_by('-last_modified')[comment_index:comment_index+no_of_comments]
    main_comment_form = AddCommentForm()
    context = {
        'category':category,
        'pages':pages,
        'comments':main_comments,
        'main_comment_form':main_comment_form,
    }
    return render(request, 'catlin/category.html', context)

# @login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            user = UserProfile.objects.get(user=request.user)
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

def add_page(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/cat_not_exist.html', {})
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
            return HttpResponseRedirect(reverse('catlin:update_category', args=[category_id]))
    elif request.user != category.user.user:
        return render(request, 'catlin/not_authorised.html',{})
    form = AddPageForm()
    context = {
        'category_id': category_id,
        'form':form,
    }
    return render(request, 'catlin/add_page.html', context)

def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/cat_not_exist.html', {})
    if request.user == category.user.user:
        pages = Page.objects.filter(category=category).order_by('-like_count')
        context = {
        'pages':pages,
        'category':category
        }
        return render(request,'catlin/update_category.html', context)
    return render(request, 'catlin/not_authorised.html',{})

def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'catlin/cat_not_exist.html', {})
    user = category.user
    if request.method == 'POST' and user.user == request.user:
        category.delete()
        user.category_count -= 1
        user.save()
        return HttpResponseRedirect(reverse('catlin:del_cat_successfull'))
    return render(request, 'catlin/not_authorised.html',{})

# @login_required
def add_comment(request):
    if request.method == 'POST':
        type = 'M'
        parent_comment = None
        user = UserProfile.objects.get(user=request.user)
        comment_content = request.POST['comment_content']
        category_id = request.POST['category_id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'catlin/cat_not_exist.html', {})
        if request.POST['type'] == 'N':
            type = 'N'
            try:
                parent_comment = Comment.objects.get(id=request.POST['comment_id'], category=category)
                parent_comment.comment_count += 1
                parent_comment.save()
                print(parent_comment.comment_count)
            except Comment.DoesNotExist:
                return render(request, 'catlin/cat_not_exist.html', {})
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

def search(request):
    return HttpResponse("Search feature coming soon.")

def search_category(request, category_id):
    return HttpResponse("Searching category feature coming soon.")

# @login_required
def like_category(request):
    #add like_category object (test)
    #increment category like_count (test)
    #increment category's owner like_count (test)
    #check if the same user has not disliked, remove dislike add like
    json_context = like_my_model(my_request=request, entity_model=Category, like_model=LikeCategory)
    return JsonResponse(json_context)

def like_page(request):
    json_context = like_my_model(my_request=request, entity_model=Page, like_model=LikePage)
    return JsonResponse(json_context)

def like_comment(request):
    json_context = like_my_model(my_request=request, entity_model=Comment, like_model=LikeComment)
    return JsonResponse(json_context)

def goto_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    page.views += 1
    page.save()
    return redirect(page.url)

def about(request):
    return HttpResponse("Linkspot is a social link sharing platform.")

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

def del_cat_successfull(request):
    return render(request, 'catlin/del_cat_success.html',{})
