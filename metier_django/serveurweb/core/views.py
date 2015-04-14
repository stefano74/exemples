#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from serveurweb.core.models import Articles
from serveurweb.core.models import Familles
from django.core import serializers
import json
from serveurweb.core.mixins import JSONResponseMixin
from serveurweb.core.forms import form_article
from django.contrib.contenttypes.models import ContentType

   
#####################################################################################################################
# Page racine
#####################################################################################################################

def index(request):
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        data = serializers.serialize('json', ContentType.objects.filter(app_label="core"))
        return JsonResponse(data, safe=False) # retourne une list de dico ou un str et non un dict
    else:
        context = {'page_titre' : 'serveurweb'}
        return render(request, 'core/index.html', context)

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

    
class AjoutArticle(JSONResponseMixin, generic.CreateView):
    model = Articles
    success_url = reverse_lazy('articles_list')
    
    def post(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_ACCEPT') == 'application/json':
            data = request.body.decode('utf-8')
            data = json.loads(data)
            art = Articles(libelle = data['fields']['libelle'],
                           prix = int(data['fields']['prix']),
                           date=data['fields']['date'],
#                            famille=int(data['fields']['famille']) famille doit = instante de Familles()
                           )
            art.save()
            return self.render_to_json_response([get_object_or_404(Articles, pk=art.id), ]) # le serializer ne prend que QuerySet en param
        else:
            return super(AjoutArticle, self).post(request, *args, **kwargs)

class ModifArticle(JSONResponseMixin, generic.UpdateView):
    
    model = Articles
    success_url = reverse_lazy('articles_list')
    fields = '__all__' # evite le warning RemovedInDjango18Warning: Using ModelFormMixin (base class of ModifArticle) without the 'fields' attribute is deprecated.

    def put(self, *args, **kwargs):
        if self.request.META.get('HTTP_ACCEPT') == 'application/json':
            data = self.request.body.decode('utf-8')
            data = json.loads(data)
            art = get_object_or_404(Articles, pk=data['pk'])
            art.libelle = data['fields']['libelle']
            art.prix = data['fields']['prix']
            art.date = data['fields']['date']
            art.save()
            return self.render_to_json_response([get_object_or_404(Articles, pk=art.id), ]) # le serializer ne prend que QuerySet en param
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
            return render(request, 'core/articles_list.html', {'articles_list': articles_list})
         
def detail_article(request, article_id):
     
    article =get_object_or_404(Articles, pk=article_id)
    form = form_article(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('articles_list'))
    return render(request, 'core/article_detail.html', {'form':form})
 
def supprimer_article(request, article_id): 
     
    article = get_object_or_404(Articles, pk=article_id)
    if request.method == 'POST':
        article.delete()
        return HttpResponseRedirect(reverse('articles_list'))
    return render(request, 'core/articles_confirm_delete.html', {'object': article})
     
 
def ajouter_article(request): 
    form = form_article(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('articles_list'))
    return render(request, 'core/article_detail.html', {'form': form})
    
#####################################################################################################################
# Familles
#####################################################################################################################
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

