from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(
        '',
        views.home_view,
        name='home'
    ),
    path(
        'like/<int:post_id>/',
        views.like_post,
        name='like_post'
        ),
    path(
        'dislike/<int:post_id>/',
        views.dislike_post,
        name='dislike_post'
        ),
    path(
        'detail/<int:id>/',
        views.post_detail,
        name = 'detail'
    ),
    path(
        'category/<int:category_id>/',
        views.category,
        name = 'category'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)