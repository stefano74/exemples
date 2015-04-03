#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        permet de demander l'affichage la MainWindow
        retourne boolean
        """
        pass
    
    def listerModels(self):
        """
        demande la liste des models du serveur
        :return: liste des models du serveur
        :rtype: list of string
        """
        pass
    
    def ajouterModel(self, aModelName, adictModel):
        """
        ajout un model 
        :param aModelName: nom du model
        :type aModelName: string
        :param adictModel: le model à ajouter
        :type adictModel: dictionnaire au format JSON sérialiser par Django serialize JSON
        """
        pass
    
    def modifierModel(self, aModelName, adictModel):
        """
        modifier un model 
        :param aModelName: nom du model
        :type aModelName: string
        :param adictModel: le model à modifier
        :type adictModel: dictionnaire au format Django serialize JSON
        """
        pass

    def supprimerModel(self, aModelName, adictModel):
        """
        supprimer un model 
        :param aModelName: nom du model
        :type aModelName: string
        :param adictModel: le model à supprimer
        :type adictModel: dictionnaire au format Django serialize JSON
        """
        pass

    def listerArticles(self):
        """
        Retourne la liste des articles
        """
        pass
    
    def modifierArticle(self, aid, alibelle, aprix, adate):
        pass
    
    def supprimerArticle(self, alibelle):
        pass
    
    def ajouterArticle(self, alibelle, aprix, adate):
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
            return self.__proxy.listerArticles()
    
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
        logger.debug('resp.status_code = %s', resp.status_code)
        logger.debug('article ajouté = %s', json.loads(resp.json()))

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
        