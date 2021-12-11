from django.shortcuts import render

from django.http import (
    Http404,
    HttpResponseRedirect
)

from .models import Shortener
from django import forms
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.decorators import api_view

class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={
            "class": "form-control form-control-lg",
            "placeholder": "masukin URL buat dipendekin",
            "style": "text-align: center;",
        },
    ))

    class Meta:
        model = Shortener
        fields = ('long_url',)

class ShortenerNoForm(serializers.ModelSerializer):
    class Meta:
        model = Shortener
        fields = ('long_url',)


def home_view(request):
    template = 'index.html'
    context = {}
    context['form'] = ShortenerForm()
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
            shortened_object = used_form.save()
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url
            context['new_url'] = new_url
            context['long_url'] = long_url
            return render(request, template, context)
        context['errors'] = used_form.errors
        return render(request, template, context)


def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
    except:
        raise Http404('link rusak gan')


class DipendekinAPI(APIView):
    # source: https://stackoverflow.com/questions/63169994/problem-sending-information-using-post-method-in-django-rest-framework
    def post(self, request):
        context = {}
        used_form = ShortenerNoForm(data=request.data, many=False)
        if used_form.is_valid():
            shortened_object = used_form.save()
            short_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url
            context['long_url'] = long_url
            context['short_url'] = short_url
            return Response(context, status=status.HTTP_201_CREATED)
        context['errors'] = used_form.errors
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({
            'Message': 'GET method is allowed, but doesn\'t return anything except this message of how to usage this API, use POST method instead to get shorted links',
            'Usage': {
                "Method": "POST",
                "Media Type": "application/json",
                "Body": {
                    "long_url": "enter your URL here"
                },
                "Return": {
                        "long_url": "enter your URL here",
                        "short_url": "shorted URL"
                }
            }
        })

