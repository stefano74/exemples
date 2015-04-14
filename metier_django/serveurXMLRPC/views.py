#from django.views.decorators.csrf import csrf_exempt 
# from django.shortcuts import render
# from xmlrpc.server import SimpleXMLRPCDispatcher
# from django.http.response import HttpResponse
import sys
from serveurweb.core.models import Articles
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.core import serializers

##############################################################################
#Retourne la listes des articles de la table articles
##############################################################################
def listerArticles():
	try:
		data = serializers.serialize('json', Articles.objects.order_by('id'))
		return data
# 		for art in Articles.objects.order_by('id'):
# 			resultat.append((art.id, art.libelle, art. prix, str(art.date)))
# 		return resultat
	except:
		print('metier_django.serveurXMLRPC.views.listerArticles Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

##############################################################################
#Retourne la listes des articles de la table articles
##############################################################################
def afficherMainWindow():
	print('metier_django.serveurXMLRPC.views.afficherMainWindow')
	return True

##############################################################################
#Modifie l article de la table articles
##############################################################################
def modifierArticle(aid, alibelle, aprix, adate):
	try:
		art = get_object_or_404(Articles, pk=aid)
		art.libelle = alibelle
		art.prix = aprix
		art.date = adate
		art.save()
	except:
			print ('metier_django.serveurXMLRPC.views.modifierArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

##############################################################################
#supprime l article de la table articles
##############################################################################
def supprimerArticle(aid):
	try:
		get_object_or_404(Articles, pk=aid).delete()
	except:
		print ('metier_django.serveurXMLRPC.views.supprimerArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

##############################################################################
#Ajoute un article à la table articles
##############################################################################
def ajouterArticle(alibelle, aprix, adate):
	try:
		art = Articles(libelle = alibelle, prix = aprix, date=adate)
		art.save()
	except:
		print ('metier_django.serveurXMLRPC.views.ajouterArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
