from .tweetlog import gettweetlog
from django.shortcuts import render
from django.views.generic import ListView
from django.http.response import HttpResponse
from .forms import NameForm
def tweet(request):
    if request.method == 'POST':
      f = NameForm(request.POST)
      print(request.POST.get('Username'))#username
      try:
        username = request.POST.get('Username')
        gettweetlog(str(username))
        return render(request, 'tweetname/imageshow.html', {'form1': f})
      except:
        return render(request, 'tweetname/error.html', {'form1': f})



    else:
      f = NameForm()
      return render(request, 'tweetname/home.html', {'form1': f})
