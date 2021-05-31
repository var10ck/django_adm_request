from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Document, ADMRequest, StoryRecord, Conclusion, \
    ConclusionType, Investigation


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ADMRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ADMRequest
        fields = ['number', 'date', 'slug', 'amount', 'comment', 'file']


class ADMRequestViewSet(viewsets.ModelViewSet):
    queryset = ADMRequest.objects.all()
    serializer_class = ADMRequestSerializer


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'slug', 'file', 'created', 'updated']


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created')
    serializer_class = DocumentSerializer


class InvestigationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Investigation
        fields = ['adm_request', 'description', 'result', 'documents', 'created', 'updated']


class InvestigationViewSet(viewsets.ModelViewSet):
    queryset = Investigation.objects.all().order_by('-updated')
    serializer_class = InvestigationSerializer


class ConclusionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conclusion
        fields = ['number', 'conclusion_type', 'description',
                  'created', 'updated', 'payoff_required', 'document']


class ConclusionViewSet(viewsets.ModelViewSet):
    queryset = Conclusion.objects.all().order_by('-updated')
    serializer_class = ConclusionSerializer


class ConclusionTypeSerializer(serializers.HyperlinkedModelSerializer):
    model = ConclusionType
    fields = ['name', 'description', 'created', 'updated']