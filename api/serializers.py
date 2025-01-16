from api.models import Project, Contributor, Issue, Comment
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user"]


class DisplayContributorSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()
    project = serializers.IntegerField()


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "title",
            "description",
            "assignee",
            "priority",
            "type",
            "status",
        ]


"""
from rest_framework import serializers
from myapp.models import Project, User

class UserSerializer(serializers.ModelSerializer):
    # Champ personnalisé pour afficher uniquement certains projets
    projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'projects']

    def get_projects(self, obj):
        # Filtrer les projets en fonction d'une condition
        filtered_projects = Project.objects.filter(author=obj, is_active=True)  # Exemple de condition
        return [{"id": project.id, "title": project.title} for project in filtered_projects]
"""


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["issue", "author", "description"]
        read_only_fields = ["uuid"]

    def validate(self, data):
        """Check the comment author is also a contributor to the project"""
        author_contributor = Contributor.objects.get(pk=data.get("author"))
        comment_project = Issue.objects.get(pk=data.get("issue")).project
        if author_contributor.project.pk != comment_project:
            raise serializers.ValidationError(
                "Comment author must be a contributor to the parent project."
            )
