from api.models import Project, Contributor, Issue, Comment
from accounts.models import User
from rest_framework import serializers
import uuid


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "type", "description", "author"]

    def create(self, validated_data):
        # register project author and create a new contributor for this project
        author = User.objects.get(pk=validated_data.get("author"))
        project = Project(
            author=author,
            type=validated_data.get("type"),
            description=validated_data.get("description"),
        )
        project.save()
        contributor = Contributor.objects.get(user=author, project=project)
        contributor.save()


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project"]
        read_only_fields = ["id"]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "project",
            "author",
            "title",
            "description",
            "assignee",
            "priority",
            "type",
            "status",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        """Check the issue author is also a contributor to the project
        """
        author_contributor = Contributor.objects.get(pk=data.get('author'))
        if author_contributor.project.pk != data.get('project'):
            raise serializers.ValidationError("Issue author must be a contributor to the parent project.")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["issue", "author", "description"]
        read_only_fields = ["uuid"]

    def create(self, validated_data):
        """Create a UUID when storing a comment.
        """
        comment = Comment(
            uuid=uuid.uuid4(),
            issue=validated_data.get("issue"),
            author=validated_data.get("author"),
            description=validated_data.get("description"),
        )
        comment.save()
        return comment()

    def validate(self, data):
        """Check the comment author is also a contributor to the project
        """
        author_contributor = Contributor.objects.get(pk=data.get('author'))
        comment_project = Issue.objects.get(pk=data.get('issue')).project
        if author_contributor.project.pk != comment_project:
            raise serializers.ValidationError("Comment author must be a contributor to the parent project.")
