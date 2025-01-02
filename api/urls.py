from django.urls import path
from api import views

urlpatterns = [
    path("projects/", views.ProjectView.as_view(), name="projects"),
    path("projects/<int:pk>/", views.ProjectView.as_view(), name="project-details"),
    path("contributors/", views.ContributorView.as_view(), name="contributors"),
    path(
        "projects/<int:project_id>/contributors/",
        views.ProjectContributorView.as_view(),
        name="project-contributors",
    ),
    path(
        "projects/<int:project_id>/issues/",
        views.ProjectIssueView.as_view(),
        name="project-issues",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>",
        views.ProjectIssueView.as_view(),
        name="issue-details",
    ),
]
