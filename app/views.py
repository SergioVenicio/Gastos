from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from .forms import AuthForm, ItemForm, GastoForm, UserForm
from .models import Item, User

def index(request):
    return render(request, 'index.html')

def auth_user(request):
    form = AuthForm(request.POST)
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'], senha=request.POST['senha'])
        except:
                user = None
                return render(request, 'auth_user.html', {'form':form})

        if user is not None:
            request.session['user'] = user.pk
            return redirect('/')
        else:
            return render(request, 'auth_user.html', {'form':form})
    else:
        return render(request, 'auth_user.html', {'form':form})

def logout(request):
    request.session['user'] = None
    return redirect('/')

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

def cad_item(request):
    if request.session['user']:
        valida_login(request.session['user'])
        if request.method == 'POST':
            form = ItemForm(request.POST)
            user = User.objects.get(pk=request.session['user'])
            if form.is_valid():
                item = form.save(commit=False)
                item.id_user = user
                item.save()
                return redirect('/')
            else:
                return redirect('/')
        else:
            form = ItemForm()
            return render(request, 'cad_item.html', {'form':form})
    else:
        return redirect('/user/auth')

def cad_gasto(request):
    if request.session['user']:
        valida_login(request.session['user'])
        if request.method == 'POST':
            form = GastoForm(request.POST)
            user = User.objects.get(pk=request.session['user'])
            if form.is_valid():
                gasto = form.save(commit=False)
                gasto.id_user = user
                gasto.data = timezone.now()
                gasto.save()
                return redirect('/')
            else:
                return redirect('/')
        else:
            form = GastoForm()
            itens = Item.objects.filter(id_user=request.session['user'])
            contents = {'form':form, 'itens':itens}
            return render(request, 'cad_gasto.html', {'forms':contents})
    else:
        return redirect('/user/auth/')

def list_itens(request):
    if valida_login(request.session['user']):    
        itens = Item.objects.filter(id_user=request.session['user'])
        return render(request, 'list_itens.html',{'itens':itens}) 
    else:
        return redirect('/user/auth')

def delete_item(request, item):
    if request.method == 'GET':
        if valida_login(request.session['user']):
            item = Item.objects.filter(pk=item).delete()
            return redirect('/itens/list/')
        else:
            return redirect('/itens/list/')
    else:
        return redirect('/itens/list/')


def valida_login(user):
    try:
        user = User.objects.get(pk=user)
        if user:
            return redirect('/user/auth/')
        else:
            return redirect('/user/auth/')
    except:
        return redirect('/user/auth/')
