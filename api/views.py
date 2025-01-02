from rest_framework import viewsets
from accounts.models import User
from api.models import Project, Contributor, Issue, Comment
from api import serializers
import uuid
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins


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
        """Create a new project. Also saves a the project author as a new contributor when creating a new project.
        """
        # TODO : once authentication is implemented, author = request.user
        serializer = serializers.ProjectSerializer(data=request.data, context=self.get_serializer_context())
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


class ProjectContributorView(generics.ListAPIView):
    serializer_class = serializers.ContributorSerializer
    queryset = Contributor.objects.all()

    def list(self, request: Request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        queryset = self.get_queryset().filter(project=project_id)
        serializer = serializers.ContributorSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectIssueView(generics.ListCreateAPIView, mixins.RetrieveModelMixin):
    serializer_class = serializers.IssueSerializer
    lookup_url_kwarg = "issue_id"

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Issue.objects.filter(project_id=project_id)

    def get(self, request: Request, *args, **kwargs):
        if "issue_id" in self.kwargs:
            return self.retrieve(request
                                 )
        else:
            return self.list(request)
