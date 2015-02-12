#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.forms.models import ModelForm

from serveurweb.models import Articles
from serveurweb.models import Familles

#####################################################################################################################
# Page racine
#####################################################################################################################
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

