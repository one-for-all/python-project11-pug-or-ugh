import os
import django
import sys
from pugorugh.serializers import DogSerializer
import json


sys.path.append('../backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


with open('pugorugh/static/dog_details.json', 'r') as file:
    data = json.load(file)
    serializer = DogSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
