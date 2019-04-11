from django.urls import path
from . import views

app_name = 'catlin'
urlpatterns = [
    path("", views.index, name='index'),
    path("about/", views.about, name='about'),
    path("<int:category_id>/", views.category, name='category'),
    path("<int:category_id>/all-links/", views.category_pages, name='category_pages'),
    path("user/<str:username>/", views.users_categories, name='users_categories'),
    path("new-link-group/", views.add_category, name='add_category'),
    path("<int:category_id>/add-link/", views.add_page, name='add_page'),
    path("<int:category_id>/update/", views.update_category, name='update_category'),
    path("<int:category_id>/delete/", views.delete_category, name='delete_category'),
    path("<int:category_id>/delete-linkgroup-verified/", views.delete_category_verified, name='delete_category_verified'),
    path("add-comment/", views.add_comment, name='add_comment'),
    path("page/<int:page_id>/", views.goto_page, name='goto_page'),
    path("link/<int:page_id>/delete/", views.delete_page, name='delete_page'),
    path("link/<int:page_id>/delete-link-verify/", views.delete_page_verify, name='delete_page_verify'),
    path("linkgroup-search/", views.search, name='search'),
    path("link-search/", views.search_pages, name='search_pages'),
    path("like_category/", views.like_category, name='like_category'),
    path("like_page/", views.like_page, name='like_page'),
    path("like_comment/", views.like_comment, name='like_comment'),
    path("see_replies/", views.see_replies, name='see_replies'),
    path("delete-linkgroup-successfull/", views.del_cat_successfull, name='del_cat_successfull'),
    path("latest-linkgroups/", views.latest_categories, name='latest_categories'),
    path("most-liked-linkgroups/", views.most_liked_categories, name='most_liked_categories'),
    path("users-results/", views.search_users, name='search_users'),
    path("search-users/", views.search_users_page, name='search_users_page'),
]
