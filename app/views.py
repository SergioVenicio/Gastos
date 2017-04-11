from django.shortcuts import render
from .forms import ItemForm, UserForm
from .models import User

def index(request):
    return render(request, 'index.html')


def cad_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(form.errors)
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

def cad_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        user = request.user
        user = User.objects.get(pk=user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.id_user = user
            item.save()
            return render(request, 'index.html')
        else:
            return render(request, 'index.html')

    else:
        form = ItemForm()
        return render(request, 'cad_item.html', {'form':form})

