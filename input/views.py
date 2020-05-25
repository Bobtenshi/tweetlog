from django.shortcuts import render
from django.views.generic import ListView
from .models import Post
from django.http.response import HttpResponse
from .forms import KakikomiForm

def hello_world(request):
    return HttpResponse('Hello World!')

def hello_get_query(request):
    d = {
        'your_name': request.GET.get('your_name')
    }
    return render(request, 'get_query.html', d)

def kakikomi(request):
    if request.method == 'POST':
      f = KakikomiForm(request.POST)
      f = KakikomiForm({
        'name':'Ichiro',
        'email':'foo@bar.com',
        'body': 'Hello, Django Form!'})
      return render(request, 'input/home.html', {'form1': f})

    else:
      f = KakikomiForm()
      return render(request, 'input/home.html', {'form1': f})

#class InputFormView(ListView):
  #model = Post
  #template_name = "input/home.html"
  #template_name = "input/get_query.html"