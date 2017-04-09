from django.shortcuts import render
from .forms import UserForm

def index(request):
    return render(request, 'index.html')


def cad_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return render(request, 'index.html')
        else:
            return render(request, 'index.html')

    else:
        form = UserForm()
        return render(request, 'cad_user.html', {'form':form})

def list_user(request, user):
    return render(request, 'index.html')
