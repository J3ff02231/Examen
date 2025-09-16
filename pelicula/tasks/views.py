from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Pelicula
from django.contrib.auth.decorators import login_required
from .forms import PeliculaForm

def signout (request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request,
                      "signin.html",
                      {"form":AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST["username"],
                            password =request.POST["password"])
        if user is None:
            return render(request,
                          "signin.html",
                          {"form":AuthenticationForm(),
                           "error":"Usuario o contraseña incorrecta"})
        else:
            login(request, user)
            return redirect("peliculas")
        
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        return render(request, 
                  "signup.html",
                  {"form":UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("peliculas")

            except IntegrityError:
                return render(request,
                              'signup.html',
                              {"form": UserCreationForm(),
                               "error":"Error al crear el usuario"})
                
        else:
                 return render(request,
                              'signup.html',
                              {"form": UserCreationForm(),
                               "error":"Error, Las contraseñas no coinciden"})
        
def peliculas(request):
    if not request.user.is_authenticated:
        return redirect("signup")
    peliculas = Pelicula.objects.filter(user=request.user)
    return render(request, "peliculas.html", {"peliculas": peliculas})

def crear_pelicula(request):
    if request.method == "GET":
        return render(request, "crear_pelicula.html", {"form": PeliculaForm()})
    else:
        try:
            form = PeliculaForm(request.POST)
            nueva_pelicula = form.save(commit=False)
            nueva_pelicula.user = request.user
            nueva_pelicula.save()
            return redirect("peliculas")
        except ValueError:
            return render(request,
                          "crear_pelicula.html",
                          {"form": PeliculaForm(),
                           "error": "Error al crear la película. Por favor, verifica los datos."})

def editar_pelicula(request, pelicula_id):
    pelicula = Pelicula.objects.get(id=pelicula_id, user=request.user)
    if request.method == "GET":
        form = PeliculaForm(instance=pelicula)
        return render(request, "crear_pelicula.html", {"form": form, "pelicula": pelicula})
    else:
        try:
            form = PeliculaForm(request.POST, instance=pelicula)
            form.save()
            return redirect("peliculas")
        except ValueError:
            return render(request,
                          "crear_pelicula.html",
                          {"form": PeliculaForm(instance=pelicula),
                           "error": "Error al editar la película. Por favor, verifica los datos.",
                           "pelicula": pelicula})

def eliminar_pelicula(request, pelicula_id):
    pelicula = Pelicula.objects.get(id=pelicula_id, user=request.user)
    pelicula.delete()
    return redirect("peliculas")
