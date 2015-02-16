#!/usr/bin/python
# -*- coding: utf-8 -*-

import cups
import sys

conn = cups.Connection()

f = open('filetext.txt', 'w')
f.write('blalblabla\n')
f.write('blalblabla\n')
f.write('blalblabla\n')
f.close()

while 1:
#     os.system("clear") 
    print('************************\n')
    print('1 : lister imprimantes \n' )
    print('2 : Ajouter une imprimante \n')
    print('3 : Supprimer une imprimante \n')
    print('4 : imprimer filetext.txt sur Note \n')  
    print('5 : Status imprimante \n')
    print('6 : annuler un job  \n')
    print('7 : lister les job d une imprimante  \n')
    print('8 : deplacer un job \n')
    print('9 : rejeter une imprimante - interdire envoi de job \n')
    print('10 : accepter une imprimante - autoriser envoi de job \n')
    print('0 : quitter \n')
    print('************************\n')
    
    choix = input('choix = ')
    ####################################################################
    #Récupère la liste des imprimantes
    ####################################################################
    if (choix == '1'):
        printers = conn.getPrinters()
        for printer in printers:
#             print (printer, printers[printer]["device-uri"])
            print (printer, printers[printer])

    ####################################################################
    #Ajoute une nouvelle imprimante la liste des imprimantes
    ####################################################################
    elif (choix == '2'):
        name = input('nom imprimante = ')
        uri = input('uri imprimante = ')
        conn.addPrinter(name) # uri vaut null -> SetDevicePrinter permet d'ajouter l'URI de l'imprimante
        conn.setPrinterDevice(name, uri)
        conn.enablePrinter(name) # par défault l'imprimante n'est pas active après création

    ####################################################################
    # Supprimer une imprimante
    ####################################################################
    elif (choix == '3'):
        name = input('nom imprimante = ') # nom de l'imprimante à supprimer et non l'URI
        conn.deletePrinter(name)

    ####################################################################
    # Imprimer
    ####################################################################
    elif (choix == '4'):
        conn.printFile('Note', 'filetext.txt', 'test', {})
    
    ####################################################################
    # Voir les attributs d'une imprimante
    ####################################################################
    elif (choix == '5'):
        name = input('nom imprimante = ')
        print(conn.getPrinterAttributes(name))

    ####################################################################
    # Annuler une tache paramètre = id de la tache (integer) 
    ####################################################################
    elif (choix == '6'):
        jobid = int(input('Job Id à annuler = '))
        conn.cancelJob(jobid)

    ####################################################################
    # Lister les taches - n'affiche pas les taches annulées
    ####################################################################
    elif (choix == '7'):
        dicjob = conn.getJobs()
        for id in dicjob.keys():
            print('JOB_ID = ', str(id))
            print('Etat = ', conn.getJobAttributes(id))
        
    ####################################################################
    # Déplacer une tache vers une autre imprimante - ne prend pas le nom de l'imprimante mais l'URI 
    ####################################################################
    elif (choix == '8'):
        jobid = int(input('Job Id à déplacer = '))
        conn.moveJob('ipp://localhost:631/printers/Note', jobid, 'ipp://localhost:631/printers/Note2')
        
    ####################################################################
    # Rejeter une imprimante - l'envoi d'une tache provoque une exception
    ####################################################################
    elif (choix == '9'):
        name = input('nom imprimante = ')
        conn.rejectJobs(name) # retourne une exception la destination n'accepte pas de tache -> acceptJobs 
    
    ####################################################################
    # Rejeter une imprimante - l'envoi d'une tache est authorisé
    ####################################################################
    elif (choix == '10'):
        name = input('nom imprimante = ')
        conn.acceptJobs(name) 

    elif (choix == '0'):
    
        sys.exit()
    
    input('press enter to continue')

    