from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response

from . import serializers
from . import models


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogRetrieveView(RetrieveAPIView):
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        current_pk = int(kwargs.get('pk'))
        status = kwargs.get('status')
        if status == 'undecided':
            pass
        elif status == 'liked':
            status = 'l'
        elif status == 'disliked':
            status = 'd'
        else:
            raise ValueError('{} is not valid status'.format(status))
        if current_pk == -1:
            if status == 'undecided':
                dog = self.queryset.exclude(userdog__user=current_user).first()
            else:
                dog = self.queryset.filter(userdog__user=current_user,
                                           userdog__status=status).first()
            if dog:
                serializer = self.get_serializer(dog)
                return Response(serializer.data)
            else:
                return Response('')
        else:
            if status == 'undecided':
                dog = self.queryset.exclude(
                    userdog__user=current_user).filter(
                    pk__gt=current_pk).first()
            else:
                dog = self.queryset.filter(userdog__user=current_user,
                                           userdog__status=status,
                                           pk__gt=current_pk).first()
            if dog:
                serializer = self.get_serializer(dog)
                return Response(serializer.data)
            else:
                return Response('')


class UserDogUpdateView(UpdateAPIView):
    queryset = models.UserDog.objects.all()

    def update(self, request, *args, **kwargs):
        current_user = request.user
        current_pk = kwargs.get('pk')
        status = kwargs.get('status')
        dog = models.Dog.objects.get(pk=current_pk)
        if status == 'undecided':
            pass
        elif status == 'liked':
            status = 'l'
        elif status == 'disliked':
            status = 'd'
        else:
            raise ValueError('{} is not valid status'.format(status))
        if status == 'undecided':
            self.queryset.filter(user=current_user,
                                 dog=dog).get().delete()
        else:
            self.queryset.update_or_create(user=current_user,
                                           dog=dog,
                                           status=status)
        return Response('')


class UserPrefRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        user = self.request.user
        pref, created = self.queryset.get_or_create(user=user)
        return pref

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
