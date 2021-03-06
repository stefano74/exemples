#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 18 mars 2015

@author: stefano

Module de connexion au serveur par type de proxy

'''

#import python
import xmlrpc.client
import json
import requests
from clientPyQt import constantes
import logging

logger = logging.getLogger(__name__)

class Proxy:
    """
        classe d'interface Proxy
    """    
    def __init__(self, aConnection=None, aApplication=None):
        
        self._serveur = aConnection # protected : simple '_'
        self._url = aConnection + aApplication # protected : simple '_'

    def connecter(self, aUsername, aPassword):
        """
        connecter au serveur
        :param aUsername: login utilisateur
        :type aUsername: string 
        :param aPassword: mot de passe utilisateur
        :type aPassword: string 
        """
        return True # retourne tjs vrai si pas de gestion des utilisateurs
    
    def deconnecter(self):
        """
        deconnecter du serveur
        """
        return True # retourne tjs vrai si pas de gestion des utilisateurs

    def afficherMainWindow(self):
        """
            Demande l'autorisation de l'affichage MainWindow
            
            :rtype: boolean
        """
        pass
    
    def listerModels(self):
        """
        demande la liste des models du serveur
        :return: liste des models du serveur
        :rtype: list of dict
        """
        dictModels = {}
        dictModels['fields'] = {'name': 'articles'}
        listModels = []
        listModels.append(dictModels)
        
        return listModels
    
    def listerModel(self, aModelName):
        """
        récupère la liste d'objets du model
        :return: liste de dictionnaire au format JSON Django serializer
        :rtype: [{},]
        """
    
        return self.listerArticles()
    
    def ajouterModel(self, aModelName, adictModel):
        """
        ajout un model 
        :param aModelName: nom du model
        :type aModelName: string
        :param adictModel: le model à ajouter
        :type adictModel: dictionnaire au format JSON sérialiser par Django serialize JSON
        """
        
        self.ajouterArticle(adictModel['fields']['libelle'],
                            adictModel['fields']['prix'],
                            adictModel['fields']['date'])
    
    def modifierModel(self, aModelName, adictModel):
        """
        modifier un model 
        :param aModelName: nom du model
        :type aModelName: string
        :param adictModel: le model à modifier
        :type adictModel: dictionnaire au format Django serialize JSON
        """
        self.modifierArticle(adictModel['pk'],
                             adictModel['fields']['libelle'],
                             adictModel['fields']['prix'],
                             adictModel['fields']['date'])

    def supprimerModel(self, aModelName, adictModel):
        """
        supprimer un model 
        :param aModelName: nom du model
        :type aModelName: string
        :param adictModel: le model à supprimer
        :type adictModel: dictionnaire au format Django serialize JSON
        """
        self.supprimerArticle(adictModel['pk'])

    def listerArticles(self):
        """
            Demande la liste des articles
            
            :return: liste des articles
            :rtype: dict
            
            .. seealso:: modifierArticle(), supprimerArticle(), ajouterArticle()
            .. warning:: retourne tous les articles au format JSON pour serveurweb
            .. note:: serveurweb retourne le dictionaire des articles sérialisé au format Django
            .. todo:: A implémenter dans les classe dérivant de Proxy         
        """
        pass
    
    def modifierArticle(self, aid, alibelle, aprix, adate):
        """
            Modifie les champs d'un article
            
            :param aid: id de l'article à modifier
            :type aid: int
            :param alibelle: libellé de l'article à modifier
            :type alibelle: str
            :param aprix: prix de l'article à modifier
            :type aprix: str
            :param adate: date de l'article à modifier
            :type adate: str
        """
        pass
    
    def supprimerArticle(self, aid):
        """
            Supprime les champs d'un article
            
            :param aid: id de l'article à supprimer
            :type aid: int
        """
        pass
    
    def ajouterArticle(self, alibelle, aprix, adate):
        """
            Ajoute les champs d'un article
            
            :param aid: id de l'article à ajouter
            :type aid: int
            :param alibelle: libellé de l'article à ajouter
            :type alibelle: str
            :param aprix: prix de l'article à ajouter
            :type aprix: str
            :param adate: date de l'article à ajouter
            :type adate: str
        """
        pass
    

class ProxyXMLRPC(Proxy):
    """
        Classe Proxy XMLRPC
    """

    def __init__(self, aConnection=None):
        super(ProxyXMLRPC, self).__init__(aConnection, constantes.ADR_XMLRPC)
         
        try:
            self.__proxy = xmlrpc.client.ServerProxy(self._url, verbose=True, allow_none=True) 
        except Exception as e:
            logger.exception(e)
            raise Exception("le client XMLRPC n'est pas initialisé !")
    
    def afficherMainWindow(self):
        try:
            return self.__proxy.afficherMainWindow()

        except Exception as e:
            logger.exception(e)
            raise e
        
    
    def listerArticles(self):
        try:
            resp = self.__proxy.listerArticles()
            lstModel = json.loads(resp)
            
            logger.debug('liste articles = %s', lstModel)
            
            return lstModel
    
        except Exception as e:
            logger.exception(e)
            raise e
    
    def modifierArticle(self, aid, alibelle, aprix, adate):
        try:
            self.__proxy.modifierArticle(aid, alibelle, aprix, adate)
        
        except Exception as e:
            logger.exception(e)
            raise e

    def supprimerArticle(self, aid):
        try:
            self.__proxy.supprimerArticle(aid)

        except Exception as e:
            logger.exception(e)
            raise e
    
    def ajouterArticle(self, alibelle, aprix, adate):
        try:
            self.__proxy.ajouterArticle(alibelle, aprix, adate)
        except Exception as e:
            logger.exception(e)
            raise e
        

class ProxyREST(Proxy):
    """
        Classe Proxy pour serveurREST
    """

    def __init__(self, aConnection=None):
        super(ProxyREST, self).__init__(aConnection, constantes.ADR_REST)
        
        self.__headers = {'content-type': 'application/json', 'accept': 'application/json'}
        
    def afficherMainWindow(self):
        return True

    def listerArticles(self):

        url = self._url + "articles/"

        resp = requests.get(url=url, headers=self.__headers)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        dicolist = resp.json()
        logger.debug('articles reçus = %s', dicolist)
        
        # formatage du dico reçu au format Django Json serializer
        result = []
        jsonDico = {} 
        for dico in dicolist:
            jsonDico['pk'] = dico['id']
            del dico['id']
            jsonDico['fields'] = dico
            result.append(jsonDico)
            jsonDico = {}
        
        logger.debug('articles reçus après formattage Django Json serializer = %s', result)
        return result

    def modifierArticle(self, aid, alibelle, aprix, adate):
        
        url = self._url + "articles/" + str(aid) + "/"
        
        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.put(url, data=json.dumps(article), headers=self.__headers)
        
        #revoir l'article modifié
        logger.debug('article modifié = %s', resp.text)
        logger.debug('resp.status_code = %s', resp.status_code)
        
        resp.raise_for_status()
        
    def supprimerArticle(self, aid):
        
        url = self._url + "articles/" + str(aid) + "/"
        resp = requests.delete(url, headers=self.__headers)

        logger.debug("resp = %s", resp.text)
        logger.debug('resp.status_code = %s', resp.status_code)

        resp.raise_for_status()
        
    def ajouterArticle(self, alibelle, aprix, adate):

        url = self._url + "articles/"
        
        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.post(url, data=json.dumps(article), headers=self.__headers)

        #revoir l'article ajouté
        logger.debug('resp.text = %s', resp.text)
        logger.debug('resp.status_code = %s', resp.status_code)

        resp.raise_for_status()


class ProxyWeb(Proxy):
    """
        Classe Proxy pour serveurweb
    """

    def __init__(self, aConnection=None):
        super(ProxyWeb, self).__init__(aConnection, constantes.ADR_WEB)
        

        self.__headers = {'content-type'    : 'application/json',
                          'accept'          : 'application/json',
                          }
        
        self.__cookies = None    # cookies pour id session Django

    def connecter(self, aUsername, aPassword):
        
        resp = requests.post(self._url + 'user/connexion/', data=json.dumps({'username': aUsername, 'password': aPassword}), headers=self.__headers)

        logger.debug('resp.status_code = %s', resp.status_code)
        
        if resp.status_code == 200:
            self.__cookies = dict(resp.cookies) # cookies contient sessionid et csrftoken
            self.__headers['X-CSRFToken'] = self.__cookies['csrftoken']
            logger.debug('cookies = %s', self.__cookies)
            return True
        else:
            return False
    
    def deconnecter(self):

        url = self._url + "user/deconnexion/"
        self.__headers['Referer'] = url

        resp = requests.post(url, headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()
        
        logger.debug('resp.status_code = %s', resp.status_code)
        
        if resp.status_code == 200:
            self.__cookies = None
            return True
        else:
            return False

    def afficherMainWindow(self):
        return True

    def listerArticles(self):

        url = self._url + "articles/"
        
        resp = requests.get(url=url, headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()

        resp.encoding = 'utf-8'
        dicolist = json.loads(resp.json()) # a utiliser si le serveur renvoie le serializer json
#         dicolist = resp.json() # a utiliser si le serveur envoie une liste de dict
        #ATTENTION : les 2 méthodes list de dict ou serializer n ont pas le meme format json

        logger.debug('articles reçus = %s', dicolist)
        
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
        
        self.__headers['Referer'] = url

        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.put(url, data=json.dumps(article), headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()
                
        #Dans le retour de la requête je renvoie l'article modifié
        logger.debug('resp.status_code = %s', resp.status_code)
        logger.debug('article modifié = %s', json.loads(resp.json()))
        
    def supprimerArticle(self, aid):
        
        url = self._url + "articles/" + str(aid) + "/del/"
        self.__headers['Referer'] = url
        
        resp = requests.delete(url, headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()

        logger.debug('resp.status_code = %s', resp.status_code)
        logger.debug("resp = %s", json.loads(resp.json())) #réponse vide

    
    def ajouterArticle(self, alibelle, aprix, adate):

        url = self._url + "articles/add/"
        self.__headers['Referer'] = url

        article = {'libelle': alibelle, 'prix': str(aprix), 'date': str(adate)}
        resp = requests.post(url, data=json.dumps(article), headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()

        #Dans le retour de la requête je renvoie l'article ajouté
        logger.debug(_('resp.status_code = %s'), resp.status_code)
        logger.debug(_('article ajouté = %s'), json.loads(resp.json()))

    def listerModels(self):
        """
        demande la liste des models du serveur
        :return: liste des models du serveur
        :rtype: list of string
        """
        try:
            resp = requests.get(self._url, headers=self.__headers, cookies=self.__cookies)
            resp.raise_for_status()
    
            resp.encoding = 'utf-8'
            lstModels = json.loads(resp.json())
    
            logger.debug('liste des models  = %s', lstModels)
            
            return lstModels

        except Exception as e:
            logger.exception(e)
            raise e

    def listerModel(self, aModelName):

        url = self._url + aModelName + "/"
        
        resp = requests.get(url=url, headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()

        resp.encoding = 'utf-8'
        dicolist = json.loads(resp.json()) # a utiliser si le serveur renvoie le serializer json
#         dicolist = resp.json() # a utiliser si le serveur envoie une liste de dict
        #ATTENTION : les 2 méthodes list de dict ou serializer n ont pas le meme format json

        logger.debug('articles reçus = %s', dicolist)
        
        return dicolist

    def ajouterModel(self, aModelName, adictModel):
        url = self._url + aModelName + "/add/"
        self.__headers['Referer'] = url

        resp = requests.post(url, data=json.dumps(adictModel), headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()

        #Dans le retour de la requête je renvoie l'article ajouté
        logger.debug('resp.status_code = %s', resp.status_code)
        logger.debug('article ajouté = %s', json.loads(resp.json()))
    
    def modifierModel(self, aModelName, adictModel):
        url = self._url + aModelName + "/" + str(adictModel['pk']) + "/"
        self.__headers['Referer'] = url

        resp = requests.put(url, data=json.dumps(adictModel), headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()
                
        #Dans le retour de la requête je renvoie l'article modifié
        logger.debug('resp.status_code = %s', resp.status_code)
        logger.debug('article modifié = %s', json.loads(resp.json()))

    def supprimerModel(self, aModelName, adictModel):
        url = self._url + aModelName + "/" + str(adictModel['pk']) + "/del/"
        self.__headers['Referer'] = url
        
        resp = requests.delete(url, headers=self.__headers, cookies=self.__cookies)
        resp.raise_for_status()

        logger.debug('resp.status_code = %s', resp.status_code)
        logger.debug("resp = %s", json.loads(resp.json())) #réponse vide
        