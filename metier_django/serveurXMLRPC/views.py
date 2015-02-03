#from django.views.decorators.csrf import csrf_exempt 
# from django.shortcuts import render
# from xmlrpc.server import SimpleXMLRPCDispatcher
# from django.http.response import HttpResponse
import sys
from serveurweb.models import Articles

##############################################################################
#Retourne la listes des articles de la table articles
##############################################################################
def listerArticles():
	try:
		resultat = []
		for art in Articles.objects.order_by('id'):
			resultat.append((art.id, art.libelle, art. prix, str(art.date)))
		return resultat
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
		art = Articles.objects.get(id = aid )
		art.libelle = alibelle
		art.prix = aprix
		art.date = adate
		art.save()
	except:
			print ('metier_django.serveurXMLRPC.views.modifierArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

##############################################################################
#supprime l article de la table articles
##############################################################################
def supprimerArticle(libelle):
	try:
		Articles.objects.get(libelle=libelle).delete()
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
