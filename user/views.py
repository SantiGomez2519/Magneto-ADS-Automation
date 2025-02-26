from django.shortcuts import render, redirect

# Create your views here.
def login_page(request):
    if request.method == "POST":
        # Aquí puedes agregar la lógica de autenticación
        return redirect('home')  # Nombre de la URL de la otra app
    
    return render(request, 'login.html')
