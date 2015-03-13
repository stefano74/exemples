#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http.response import Http404, HttpResponseRedirect, JsonResponse
import json
from serveurweb.user.forms import ConnexionForm
from django.core.urlresolvers import reverse
from django.shortcuts import render

  
@csrf_exempt
def connexion(request):
    """
    Connexion d'un utilisateur
    """
    if request.method == "POST":
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            data = request.body.decode('utf-8')
            data = json.loads(data)
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    raise Http404("L'utilisateur n'est pas activé.")
            else:
                    raise Http404("L'utilisateur n'existe pas.")
            
            return JsonResponse({})
                    
        else:
            form = ConnexionForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)  # vérifie si les données sont correctes
                if user:  # Si l'objet renvoyé n'est pas None
                    if user.is_active:
                        login(request, user)  # connecte l'utilisateur
#                     else:
#                         raise Http404("L'utilisateur n'est pas activé.")
#                 else: # sinon une erreur sera affichée
#                     raise Http404("L'utilisateur n'existe pas.")
            return HttpResponseRedirect(reverse('index')) # la redirection avec LOGIN_REDIRECT_URL ne fonctionne pas (seulement pour CBV)
    else:   
        form = ConnexionForm()
        return render(request, 'user/connexion.html', locals()) # locals retourne les variables locales dans un dictionnaire

def deconnexion(request):
    """
    deconnexion
    utiliser commande manage.py clearsessions pour supprimer les sessions expirées (2 semaines) de la DB 
    """
    logout(request)
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        return JsonResponse({})
    else:
        return HttpResponseRedirect(reverse('connexion'))
