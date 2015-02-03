#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpc.client
import os
import sys


proxy = xmlrpc.client.ServerProxy('http://localhost:8888')

while 1:
#     os.system("clear") 
    print('************************\n')
    print('1 : lister articles \n' )
    print('2 : ajouter articles \n')
    print('3 : supprimer articles \n')
    print('4 : quitter \n')
    print('************************\n')
    
    choix = input('choix = ')
    
    if (choix == '1'):
        print('\narticles = ', proxy.listerArticles())
    elif (choix == '2'):
        nom = input('Entrez le libelle de l article : ')
        prix = input ('entrez le prix de l article : ')
        proxy.ajouterArticle(nom, prix)
    elif (choix == '3'):
        nom = input('Entrez le nom de l article a supprimer: ')
        proxy.supprimerArticle(nom)
    elif (choix == '4'):
        sys.exit()
    
    input('press enter to continue')
    
    
        
        
        
        
#print(proxy.system.listMethods())
#proxy.ajouterArticle('coca cola', 3.5)
# proxy.supprimerArticle('chocolat')
# print('articles = ', proxy.listerArticles())
