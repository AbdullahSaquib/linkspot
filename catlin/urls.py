from django.urls import path
from . import views

app_name = 'catlin'
urlpatterns = [
    path("", views.index, name='index'),
    path("about/", views.about, name='about'),
    path("<int:category_id>/", views.category, name='category'),
    path("new-link-group/", views.add_category, name='add_category'),
    path("<int:category_id>/add-page/", views.add_page, name='add_page'),
    path("<int:category_id>/update/", views.update_category, name='update_category'),
    path("<int:category_id>/delete/", views.delete_category, name='delete_category'),
    path("<int:category_id>/delete-linkgroup-verified/", views.delete_category_verified, name='delete_category_verified'),
    path("add-comment/", views.add_comment, name='add_comment'),
    path("page/<int:page_id>/", views.goto_page, name='goto_page'),
    path("link/<int:page_id>/delete/", views.delete_page, name='delete_page'),
    path("link/<int:page_id>/delete-link-verify/", views.delete_page_verify, name='delete_page_verify'),
    path("search-results/", views.search, name='search'),
    path("<int:category_id>/search/", views.search_category, name='search_category'),
    path("like_category/", views.like_category, name='like_category'),
    # path("dislike_category/", views.dislike_category, name='dislike_category'),
    path("like_page/", views.like_page, name='like_page'),
    # path("dislike_page/", views.dislike_page, name='dislike_page'),
    path("like_comment/", views.like_comment, name='like_comment'),
    # path("dislike_comment/", views.dislike_comment, name='dislike_comment'),
    path("see_replies/", views.see_replies, name='see_replies'),
    path("delete-category-successfull/", views.del_cat_successfull, name='del_cat_successfull'),
]
