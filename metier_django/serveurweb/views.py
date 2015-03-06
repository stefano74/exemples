#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, JsonResponse, Http404,\
    HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.forms.models import ModelForm

from serveurweb.models import Articles
from serveurweb.models import Familles
from django.core import serializers
import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django import forms


class JSONResponseMixin(object):
    """
    classe de réponse en JSON
    """

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            safe=False,
            **response_kwargs
        )

    def get_data(self, context):
        """
        utilise le sérialiseur JSON de Django pour l'envoi
        """
        return serializers.serialize('json', context)

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    
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
        return render(request, 'serveurweb/connexion.html', locals()) # locals retourne les variables locales dans un dictionnaire

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
    
#####################################################################################################################
# Page racine
#####################################################################################################################

def index(request):
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        return JSONResponseMixin.render_to_json_response({})
    else:
        context = {'page_titre' : 'serveurweb'}
        return render(request, 'serveurweb/index.html', context)

#####################################################################################################################
# Articles : solution CBV
#####################################################################################################################
class articles(JSONResponseMixin, generic.ListView):
    def get_queryset(self):
        return Articles.objects.all()

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
#         if self.request.GET.get('format') == 'json': # marche pas
        if self.request.META.get('HTTP_ACCEPT') == 'application/json':
            return self.render_to_json_response(self.get_queryset())
        else:
            return super(articles, self).render_to_response(context)

class form_article(ModelForm):
    class Meta:
        model = Articles
        
class AjoutArticle(JSONResponseMixin, generic.CreateView):
    model = Articles
    success_url = reverse_lazy('articles_list')
    
    def post(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_ACCEPT') == 'application/json':
            data = request.body.decode('utf-8')
            data = json.loads(data)
            art = Articles(libelle = data['libelle'], prix = data['prix'], date=data['date'])
            art.save()
            return self.render_to_json_response([get_object_or_404(Articles, pk=art.id), ]) # le serializer ne prend que QuerySet en param
        else:
            return super(AjoutArticle, self).post(request, *args, **kwargs)

class ModifArticle(JSONResponseMixin, generic.UpdateView):
    
    model = Articles
    success_url = reverse_lazy('articles_list')

    def put(self, *args, **kwargs):
        if self.request.META.get('HTTP_ACCEPT') == 'application/json':
            data = self.request.body.decode('utf-8')
            data = json.loads(data)
            art = get_object_or_404(Articles, pk=kwargs['pk'])
            art.libelle = data['libelle']
            art.prix = data['prix']
            art.date = data['date']
            art.save()
            return self.render_to_json_response([get_object_or_404(Articles, pk=kwargs['pk']), ]) # le serializer ne prend que QuerySet en param
        else:
            return generic.UpdateView.put(self, *args, **kwargs)

class SuppressionArticle(JSONResponseMixin, generic.DeleteView):
    model = Articles
    success_url = reverse_lazy('articles_list')
    
    def delete(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_ACCEPT') == 'application/json':
            art = get_object_or_404(Articles, pk=kwargs['pk'])
            art.delete()
            return self.render_to_json_response({}) # ne renvoie aucune donnée
        else:
            return generic.DeleteView.delete(self, request, *args, **kwargs)
        
#####################################################################################################################
# Articles : solution FBV 
# URLs à modifier !!!
#####################################################################################################################
# avec exemple reponse JSON        
def list_articles(request):
     
    articles_list = Articles.objects.all()
    if request.method == 'GET':
        print(request.META.get('HTTP_ACCEPT'))
        print('DATA = ', articles_list, type(articles_list))
        if request.META.get('HTTP_ACCEPT') == 'application/json':
#             data = list(Articles.objects.all().values()) # list de dict 
            data = serializers.serialize('json', articles_list)
            return JsonResponse(data, safe=False) # retourne une list de dico ou un str et non un dict
        else:
            return render(request, 'serveurweb/articles_list.html', {'articles_list': articles_list})
         
def detail_article(request, article_id):
     
    article =get_object_or_404(Articles, pk=article_id)
    form = form_article(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('articles_list'))
    return render(request, 'serveurweb/article_detail.html', {'form':form})
 
def supprimer_article(request, article_id): 
     
    article = get_object_or_404(Articles, pk=article_id)
    if request.method == 'POST':
        article.delete()
        return HttpResponseRedirect(reverse('articles_list'))
    return render(request, 'serveurweb/articles_confirm_delete.html', {'object': article})
     
 
def ajouter_article(request): 
    form = form_article(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('articles_list'))
    return render(request, 'serveurweb/article_detail.html', {'form': form})
    
#####################################################################################################################
# Familles
#####################################################################################################################

class form_famille(ModelForm):
    class Meta:
        model = Familles
    
class familles(generic.ListView):
        def get_queryset(self):
            return Familles.objects.order_by('id')
       
class ajouter_famille(generic.CreateView):
    model = Familles
    success_url = reverse_lazy('familles_list')

class modifier_famille(generic.UpdateView):
    model = Familles
    success_url = reverse_lazy('familles_list')

class supprimer_famille(generic.DeleteView):
    model = Familles
    success_url = reverse_lazy('familles_list')    

