#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from serveurweb.models import Articles
from serveurweb.models import Familles
from django.http.response import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.forms.models import ModelForm
from datetime import date

# Create your views here.

def index(request):
    context = {'page_titre' : 'serveurweb'}
    
    return render(request, 'serveurweb/index.html', context)

#####################################################################################################################
# Articles
#####################################################################################################################

class articles(generic.ListView):
    def get_queryset(self):
        return Articles.objects.all()

class form_article(ModelForm):
    class Meta:
        model = Articles
        
def detail_article(request, article_id):
    try:
        article = Articles.objects.get(pk=article_id)
    except article.DoesNotExist:
        raise Http404("l'article n'existe pas")

    if request.method == 'GET':
        form = form_article(instance=article)
        return render(request, 'serveurweb/article_detail.html', {'form': form, 'article_id': article.id})
    
    elif request.method == 'POST':
        form = form_article(request.POST, instance=article)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('articles_list'))

def supprimer_article(request, article_id): 
    try:
        article = Articles.objects.get(pk=article_id)
    except article.DoesNotExist:
        raise Http404("l'article n'existe pas")
    article.delete()
    return HttpResponseRedirect(reverse('articles_list'))

def ajouter_article(request): 
    article = Articles.objects.create(libelle='', prix=0, date=date.today(), famille=Familles.objects.get(pk=1))

    if request.method == 'GET':
        form = form_article(instance=article)
        return render(request, 'serveurweb/article_detail.html', {'form': form, 'article_id': article.id})
    
    elif request.method == 'POST':
        form = form_article(request.POST, instance=article)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('articles_list'))

#####################################################################################################################
# Familles
#####################################################################################################################

class form_famille(ModelForm):
    class Meta:
        model = Familles
    
class familles(generic.ListView):
        def get_queryset(self):
            return Familles.objects.order_by('id')

class detail_famille(generic.DetailView):
    model = Familles

class ajouter_famille(generic.CreateView):
    model = Familles
    success_url = reverse_lazy('familles_list')

class modifier_famille(generic.UpdateView):
    model = Familles
    success_url = reverse_lazy('familles_list')

class supprimer_famille(generic.DeleteView):
    model = Familles
    success_url = reverse_lazy('familles_list')    

