from django.http import HttpResponse
from django.template import loader

def members(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())
# Here we are configuring the views of our app to load what's in our index.html
