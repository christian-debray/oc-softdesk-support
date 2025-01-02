from api.models import Project, Contributor, Issue, Comment
from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project"]


class DisplayContributorSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()
    project = serializers.IntegerField()


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["issue", "author", "description"]
        read_only_fields = ["uuid"]

    def validate(self, data):
        """Check the comment author is also a contributor to the project
        """
        author_contributor = Contributor.objects.get(pk=data.get('author'))
        comment_project = Issue.objects.get(pk=data.get('issue')).project
        if author_contributor.project.pk != comment_project:
            raise serializers.ValidationError("Comment author must be a contributor to the parent project.")
