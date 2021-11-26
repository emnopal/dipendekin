from django.shortcuts import render

from django.http import (
    Http404,
    HttpResponseRedirect
)

from .models import Shortener

from django import forms


class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg",
               "placeholder": "masukin URL buat dipendekin",
               "style": "text-align: center;"}
    ))

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

        # If URL is valid
        if used_form.is_valid():
            shortened_object = used_form.save()
            new_url = request.build_absolute_uri(
                '/') + shortened_object.short_url
            long_url = shortened_object.long_url
            context['new_url'] = new_url
            context['long_url'] = long_url
            return render(request, template, context)

        # Else
        context['errors'] = used_form.errors

        return render(request, template, context)


def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
    except:
        raise Http404('link rusak gan')
