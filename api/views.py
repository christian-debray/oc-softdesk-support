# from accounts.models import User
from api.models import Project, Contributor, Issue, Comment
from api import serializers
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.serializers import ValidationError


class ProjectView(generics.RetrieveUpdateDestroyAPIView, mixins.ListModelMixin):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get(self, request: Request, *args, **kwargs):
        """
        Read one project or list all projects.

        accepted kwargs:
        pk: int -- id of an existing project to view, update or delete.

        when no pk is specified, lists all existing projects.
        """
        if "pk" in kwargs:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request: Request, *args, **kwargs):
        """Create a new project. Also saves a the project author as a new contributor when creating a new project."""
        # TODO : once authentication is implemented, author = request.user
        serializer = serializers.ProjectSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        if serializer.is_valid():
            project: Project = serializer.save()
            contributor = Contributor(user=project.author, project=project)
            contributor.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = Contributor.objects.all()
    serializer_class = serializers.ContributorSerializer


class ProjectContributorView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.ContributorSerializer
    queryset = Contributor.objects.all()

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return Contributor.objects.filter(project_id=project_id)

    def list(self, request: Request, *args, **kwargs):
        project_id = kwargs.get("project_id")
        queryset = self.get_queryset().filter(project=project_id)
        serializer = serializers.ContributorSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectIssueView(generics.ListCreateAPIView, mixins.RetrieveModelMixin):
    serializer_class = serializers.IssueSerializer
    lookup_url_kwarg = "issue_id"

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return Issue.objects.filter(project_id=project_id)

    def get(self, request: Request, *args, **kwargs):
        if "issue_id" in self.kwargs:
            return self.retrieve(request)
        else:
            return self.list(request)

    def put(self, request: Request, *args, **kwargs):
        """updating/creating an issue: check the assignee is a contributor to the same project"""

    def post(self, request: Request, *args, **kwargs):
        """create a new issue"""
        serializer = serializers.IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.setdefault("project_id", self.kwargs.get("project_id"))
            self.validate_contributor(serializer.validated_data.get("author"))
            # check assignee is a contributor to the same project
            if "assignee" in serializer.validated_data:
                self.validate_contributor(serializer.validated_data.get("assignee"))
            instance = serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def validate_contributor(self, contributor_id: int):
        if Contributor.objects.get(
            project_id=self.kwargs.get("project_id"), pk=contributor_id
        ):
            return True
        else:
            return False


"""from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.models import User, Project

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        filtered_projects = Project.objects.filter(author=user, is_active=True)
        serializer = UserSerializer(user, context={'projects': filtered_projects})
        return Response(serializer.data)
"""
