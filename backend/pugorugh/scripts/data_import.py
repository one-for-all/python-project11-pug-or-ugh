import os
import django
import sys
import json


sys.path.append('../backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from pugorugh.serializers import DogSerializer


with open('pugorugh/static/dog_details.json', 'r') as file:
    data = json.load(file)
    serializer = DogSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
