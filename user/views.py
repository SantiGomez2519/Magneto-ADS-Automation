from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')  # Si ya está autenticado, lo redirige a la página principal
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirigir a la página principal
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirigir al login después de cerrar sesión
