from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views


api_router = DefaultRouter()
api_router.register(r'projects', viewset=views.ProjectViewSet, basename='project')
api_router.register(r'contributors', viewset=views.ContributorViewSet, basename='contributor')
api_router.register(r'issue', viewset=views.IssueViewSet, basename='issue')
api_router.register(r'comment', viewset=views.CommentViewSet, basename='comment')
urlpatterns = [
    path('', include(api_router.urls))
]
