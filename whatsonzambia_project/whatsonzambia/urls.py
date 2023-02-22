from django.urls import path, include
from .views import(
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostCreateFeatureView,
    PostDetailFeatureView,
    PostDeleteFeatureView,
    PostUpdateFeatureView,
    UserPostListView,
) 
from . import views

urlpatterns = [
    path('', views.home, name='whatsonzambia-home'),
    path('user/<str:email>', UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name='whatsonzambia-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('feature/<int:pk>/', PostDetailFeatureView.as_view(), name='feature-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new-feature/', PostCreateFeatureView.as_view(), name='post-create-feature'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/update-feature/', PostUpdateFeatureView.as_view(), name='feature-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/delete-feature/', PostDeleteFeatureView.as_view(), name='feature-delete'),
    path('like/<int:pk>', views.postLike, name='post_like'),
    path('ft_like/<int:pk>', views.featureLike, name='feature_like'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('ft_hitcount/', include(('hitcount.urls', 'hitcount'), namespace='ft_hitcount')),
    path('category/<str:cats>/', views.CategoryView, name='category'),

]
