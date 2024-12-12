from django.db import models
from accounts.models import User


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = "BACKEND", "Backend"
        FRONTEND = "FRONTEND", "Frontend"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    type = models.CharField(choices=ProjectType, null=False, blank=False, max_length=8)
    description = models.TextField(null=False, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Contributor(models.Model):
    """List contributors to a project:
    Contributors.objects.filter(project=project_id)
    List all Issues posted by a contributor on a project:
    Issue.objects.filter(project=project_id, author=contributor.id)
    List all Issues posted by a user on a project:
    Issue.objects.filter(project=project_id, author__user=username)
    check if a user can post a comment to an issue
    Contributor.objects.get(user__username=username, project=)
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)


class Issue(models.Model):

    class IssuePriority(models.TextChoices):
        LOW = "LOW", "low"
        MEDIUM = "MEDIUM", "medium"
        HIGH = "HIGH", "high"

    class IssueType(models.TextChoices):
        BUG = "BUG", "bug"
        FEATURE = "FEATURE", "feature"
        TASK = "TASK", "task"
    
    class IssueStatus(models.TextChoices):
        TODO = "ToDo", "toDo"
        INPROGRESS = "InProgress", "InProgress"
        FINISHED = "Finished", "Finised"

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(to=Contributor, on_delete=models.CASCADE, null=True, blank=True, related_name="issue_assignee")
    priority = models.CharField(choices=IssuePriority, null=False, max_length=8, default=IssuePriority.MEDIUM)
    type = models.CharField(choices=IssueType, null=False, max_length=8, default=IssueType.BUG)
    status = models.CharField(choices=IssueStatus, null=False, max_length=10, default=IssueStatus.TODO)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Project of a comment:
    """
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
    description = models.TextField(null=False, blank=False)
    uuid = models.CharField(max_length=32, null=False, blank=True)


# class Contributor(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         related_name="project_author"
#     )
#     project = models.ForeignKey(
#         Project, on_delete=models.CASCADE,
#         related_name="project_contributor"
#     )
#     issue = models.ForeignKey(
#         Issue,
#         on_delete=models.CASCADE,
#         related_name="contributor_issue",
#         null=True,
#         blank=True,
#     )
#     comment = models.ForeignKey(
#         Comment,
#         on_delete=models.CASCADE,
#         related_name="contributor_comment",
#         null=True,
#         blank=True,
#     )

#     def __str__(self):
#         return f"{self.user}"
