from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from .forms import AuthForm, ItemForm, GastoForm, UserForm
from .models import Gasto, Item, User

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
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            request.session['user'] = user.pk
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
                return redirect('/itens/list/')
            else:
                return redirect('/itens/list/')
        else:
            form = ItemForm()
            return render(request, 'cad_item.html', {'form':form})
    else:
        return redirect('/user/auth')

def cad_gasto(request):
    try:
        user = valida_login(request.session['user'])
    except:
        user = None
    if user:
        if request.method == 'POST':
            form = GastoForm(request.POST)
            user = User.objects.get(pk=request.session['user'])
            if form.is_valid():
                item = Item.objects.get(descricao=form.cleaned_data.get('items'))
                gasto = form.save(commit=False)
                gasto.id_user = user
                gasto.data = timezone.now()
                gasto.total = gasto.quantidade * item.valor
                gasto.save()
                pass
                return redirect('/gastos/list/')
            else:
                return redirect('/gastos/list/')
        else:
            form = GastoForm()
            itens = Item.objects.filter(id_user=request.session['user'])
            contents = {'form':form, 'itens':itens}
            return render(request, 'cad_gasto.html', {'forms':contents})
    else:
        return redirect('/user/auth/')

def list_gastos(request):
    try:
        user = valida_login(request.session['user'])
    except:
        user = None
    if user:
        gastos = Gasto.objects.filter(id_user=request.session['user'])
        return render(request, 'list_gastos.html', {'gastos':gastos})
    else:
        return redirect('/user/auth/')

def delete_gasto(request, gasto):
    try:
        user = valida_login(request.session['user'])
    except:
        user = None
    if request.method == 'GET':
        if user:
            gasto = Gasto.objects.filter(pk=gasto).delete()
            return redirect('/gastos/list/')
        else:
            return redirect('/gastos/list/')

def edit_gasto(request, gasto):
    try:
        user = valida_login(request.session['user'])
    except:
        user = None
    if request.method == 'POST':
        if user:
            edit_gasto = Gasto.objects.get(pk=gasto)
            form = GastoForm(request.POST, instance=edit_gasto)
            print(form.errors)
            if form.is_valid():
                item = Item.objects.get(descricao=form.cleaned_data['items'])
                gasto = form.save(commit=False)
                gasto.total = gasto.quantidade * item.valor
                gasto.save()
                return redirect('/gastos/list/')
            else:
                return redirect('/gastos/list/')
        else:
            return redirect('/user/auth/')
    elif request.method == 'GET':
        try:
            user = valida_login(request.session['user'])
        except:
            user = None
        if user:
            gasto = Gasto.objects.get(pk=gasto)
            total = str(gasto.total)
            gasto.total = (total).replace(',','.')
            form = GastoForm()
            itens = Item.objects.filter(id_user=request.session['user'])
            contents = {'form':form, 'gasto':gasto, 'itens':itens}
            return render(request, 'edit_gasto.html', {'form':contents})
        else:
            return redirect('/user/auth/')
    else:
        return redirect('/itens/list/')
    

def list_itens(request):
    try:
        user = valida_login(request.session['user'])
    except:
        user = None
    if user:
        itens = Item.objects.filter(id_user=request.session['user'])
        return render(request, 'list_itens.html',{'itens':itens}) 
    else:
        return redirect('/user/auth/')

def delete_item(request, item):
    if request.method == 'GET':
        try:
            user = valida_login(request.session['user'])
        except:
            user = None
        if user:
            item = Item.objects.filter(pk=item).delete()
            return redirect('/itens/list/')
        else:
            return redirect('/itens/list/')
    else:
        return redirect('/itens/list/')

def edit_item(request, item):
    if request.method == 'POST':
        try:
            user = valida_login(request.session['user'])
        except:
            user = None
        if user:
            edit_item = Item.objects.get(pk=item)
            form = ItemForm(request.POST, instance=edit_item)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('/itens/list/')
            else:
                return redirect('/itens/list/')
        else:
            return redirect('/user/auth/')
    elif request.method == 'GET':
        try:
            user = valida_login(request.session['user'])
        except:
            user = None
        if user:
            item = Item.objects.get(pk=item)
            valor = str(item.valor)
            item.valor = (valor).replace(',','.')
            form = ItemForm()
            contents = {'form':form, 'item':item}
            return render(request, 'edit_item.html', {'form':contents})
        else:
            return redirect('/user/auth/')
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
