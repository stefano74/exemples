#!/usr/bin/python
# -*- coding: utf-8 -*-

#import python
import xmlrpc.client
import json
import requests
import sys

#################################################################################
#   classe d'interface Proxy
#################################################################################
class Proxy:
    
    def __init__(self, aConnection=None):
        
        self._url = aConnection # protected : simple '_'

    #############################################################################
    # Permet d'afficher la MainWidow
    # Return boolean
    #############################################################################
    def afficherMainWindow(self):
        pass
    
    #############################################################################
    # retourne la liste des articles
    # Return [...]
    #############################################################################
    def listerArticles(self):
        pass
    
    def modifierArticle(self, aid, alibelle, aprix, adate):
        pass
    
    def supprimerArticle(self, alibelle):
        pass
    
    def ajouterArticle(self, alibelle, aprix, adate):
        pass
    

#################################################################################
#   classe Proxy pour serveur de type XMLRPC
#################################################################################
# class ProxyXMLRPC(xmlrpc.client.ServerProxy):
class ProxyXMLRPC(Proxy):

    ADR_XMLRPC  = '/serveurXMLRPC/'

    def __init__(self, aConnection=None):
        super(ProxyXMLRPC, self).__init__(aConnection + self.ADR_XMLRPC)
         
        try:
            self.__proxy = xmlrpc.client.ServerProxy(self._url, verbose=True, allow_none=True) 
        except Exception:
            print("le client XMLRPC n'est pas initialisé !")
            raise Exception
        #Proxy.__init__(self, aConnection)
#         xmlrpc.client.ServerProxy.__init__(self, aConnection, verbose=True)
    
    def afficherMainWindow(self):
        
        return self.__proxy.afficherMainWindow()
    
    def listerArticles(self):

        return self.__proxy.listerArticles()
    
    def modifierArticle(self, aid, alibelle, aprix, adate):
        
        self.__proxy.modifierArticle(aid, alibelle, aprix, adate)
        
    def supprimerArticle(self, aid):
        
        self.__proxy.supprimerArticle(aid)
    
    def ajouterArticle(self, alibelle, aprix, adate):
        
        self.__proxy.ajouterArticle(alibelle, aprix, adate)
        

#################################################################################
#   classe Proxy pour serveur de type REST
#################################################################################
class ProxyREST(Proxy):

    ADR_REST = '/serveurREST/'

    def __init__(self, aConnection=None):
        super(ProxyREST, self).__init__(aConnection + self.ADR_REST)
        
        self.__headers = {'content-type': 'application/json', 'accept': 'application/json'}
        
    def afficherMainWindow(self):
        return True

    def listerArticles(self):

        url = self._url + "articles/"

        resp = requests.get(url=url, headers=self.__headers)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        dicolist = resp.json()
        print('articles reçus = ', dicolist)
        
        result = []
        article = []
        for dico in dicolist:
            article.append(dico['id'])
            article.append(dico['libelle'])
            article.append(dico['prix'])
            article.append(dico['date'])
            result.append(article)
            article = []
        return result

    def modifierArticle(self, aid, alibelle, aprix, adate):
        
        url = self._url + "articles/" + str(aid) + "/"
        
        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.put(url, data=json.dumps(article), headers=self.__headers)
        
        #revoir l'article modifié
        print('resp.text = ', resp.text)
        print('resp.status_code = ', resp.status_code)
        
        resp.raise_for_status()
        
    def supprimerArticle(self, aid):
        
        url = self._url + "articles/" + str(aid) + "/"
        resp = requests.delete(url, headers=self.__headers)

        print("resp = ", resp.text)
        print('resp.status_code = ', resp.status_code)

        resp.raise_for_status()
        
    def ajouterArticle(self, alibelle, aprix, adate):

        url = self._url + "articles/"
        
        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.post(url, data=json.dumps(article), headers=self.__headers)

        #revoir l'article ajouté
        print('resp.text = ', resp.text)
        print('resp.status_code = ', resp.status_code)

        resp.raise_for_status()


#################################################################################
#   classe Proxy pour serveur de type REST
#################################################################################
class ProxyWeb(Proxy):

    ADR_WEB = '/serveurweb/'

    def __init__(self, aConnection=None):
        super(ProxyWeb, self).__init__(aConnection + self.ADR_WEB)
        
        self.__headers = {'content-type': 'application/json', 'accept': 'application/json'}
        
    def afficherMainWindow(self):
        return True

    def listerArticles(self):

        url = self._url + "articles/"

        resp = requests.get(url=url, headers=self.__headers)
        resp.raise_for_status()

        resp.encoding = 'utf-8'
        dicolist = json.loads(resp.json()) # a utiliser si le serveur renvoie le serializer json
#         dicolist = resp.json() # a utiliser si le serveur envoie une liste de dict
        #ATTENTION : les 2 méthodes list de dict ou serializer n ont pas le meme format json

        print('articles reçus = ', dicolist, type(dicolist))
        
        result = []
        article = []
        for dico in dicolist:
            article.append(dico['pk'])
            article.append(dico['fields']['libelle'])
            article.append(dico['fields']['prix'])
            article.append(dico['fields']['date'])
            result.append(article)
            article = []
        return result

    def modifierArticle(self, aid, alibelle, aprix, adate):

        url = self._url + "articles/" + str(aid) + "/"
        
        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.put(url, data=json.dumps(article), headers=self.__headers)
        
        #revoir l'article modifié
        print('article modifié = ', json.loads(resp.json()))
        print('resp.status_code = ', resp.status_code)
        
        resp.raise_for_status()
    
    def supprimerArticle(self, aid):
        
        url = self._url + "articles/" + str(aid) + "/del/"
        resp = requests.delete(url, headers=self.__headers)

        print("resp = ", json.loads(resp.json()))
        print('resp.status_code = ', resp.status_code)

        resp.raise_for_status()
    
    def ajouterArticle(self, alibelle, aprix, adate):

        url = self._url + "articles/add/"
        
        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.post(url, data=json.dumps(article), headers=self.__headers)
#         resp = requests.post(url, data=article, headers=self.__headers)

        #revoir l'article ajouté
        print('article ajouté = ', json.loads(resp.json()))
        print('resp.status_code = ', resp.status_code)

        resp.raise_for_status()
        