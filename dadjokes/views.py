"""
views.py
Xinxu Chen (chenxin@bu.edu)

Defines the views for the dadjokes app.
"""

import random
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer


def show_random(request):
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()

    joke = random.choice(jokes) if jokes else None
    picture = random.choice(pictures) if pictures else None

    context = {
        'joke': joke,
        'picture': picture,
    }
    return render(request, 'dadjokes/random.html', context)


def show_all_jokes(request):
    jokes = Joke.objects.all()
    context = {
        'jokes': jokes,
    }
    return render(request, 'dadjokes/show_all_jokes.html', context)


def show_joke(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    context = {
        'joke': joke,
    }
    return render(request, 'dadjokes/show_joke.html', context)


def show_all_pictures(request):
    pictures = Picture.objects.all()
    context = {
        'pictures': pictures,
    }
    return render(request, 'dadjokes/show_all_pictures.html', context)


def show_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    context = {
        'picture': picture,
    }
    return render(request, 'dadjokes/show_picture.html', context)


@api_view(['GET'])
def api_show_random(request):
    jokes = Joke.objects.all()
    joke = random.choice(jokes) if jokes else None

    if joke is None:
        return Response({'message': 'No jokes found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def api_show_all_jokes(request):
    if request.method == 'GET':
        jokes = Joke.objects.all()
        serializer = JokeSerializer(jokes, many=True)
        return Response(serializer.data)

    serializer = JokeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_show_joke(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET'])
def api_show_all_pictures(request):
    pictures = Picture.objects.all()
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_show_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)


@api_view(['GET'])
def api_show_random_picture(request):
    pictures = Picture.objects.all()
    picture = random.choice(pictures) if pictures else None

    if picture is None:
        return Response({'message': 'No pictures found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PictureSerializer(picture)
    return Response(serializer.data)