#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

class StatusTest(TestCase):
    """
    Classe de test des status de réponse
    """
    def setUp(self):
        self.client = Client()
        
    def test_public(self):
        urls = [{'url' : '/serveurweb/connexion/',
                 'template' : 'serveurweb/connexion.html',
                 'status' : 200},
                {'url' : '/serveurweb/deconnexion/',
                 'template' : 'serveurweb/connexion.html',
                 'status' : 302}]
        
        for elem in urls:
            response = self.client.get(elem['url'])
            self.assertEqual(response.status_code, elem['status'])
            response = self.client.get(elem['url'], follow=True)
            self.assertEqual(response.templates[0].name, elem['template'])
    
    def test_login(self):
        """
        Teste la redirection d'url si login correct
        ???
        response.templates[0].name ne contient pas le template serveurweb/index.html de redirection mais serveurweb/connexion.html
        car la methode authenticate retourne None.
        Il faut rajouter la création d'un user et les urls pour cela
        ???
        """
        
        user = User(username="test", password='test')
        user.save() # la creation de cette manière, authenticate retourne None aussi
        user = User.objects.get(username='test')
        self.assertEqual(user.username, "test")
        response = self.client.post('/serveurweb/connexion/',
                                    {'username':'test', 'password':'test'},
                                    follow=True)
        print('response.templates[0].name = ', response.templates[0].name)
#         self.assertRedirects(response,'/serveurweb/', status_code=302, target_status_code=200, msg_prefix='') #faux response contient l'url de connexion serveurweb/connexion/
        self.assertEqual(response.templates[0].name, '/serveurweb/index.html') #faux response contient le template serveurweb/connexion.html
