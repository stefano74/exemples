#!/usr/bin/env python

"""
Classe de routage pour l'utilisation des bases Postgres et SQLite
"""
#Classe routeur pour Postgres
class PostgresRouter(object):
    def db_for_read(self, model, **hints):

        return 'postgres'

    def db_for_write(self, model, **hints):
       
        return 'postgres'

    def allow_relation(self, obj1, obj2, **hints):

        return True

    def allow_migrate(self, db, model):

        return True

#Classe routeur pour SQLite
class SqliteRouter(object):
    def db_for_read(self, model, **hints):

        return 'sqlite'

    def db_for_write(self, model, **hints):
       
        return 'sqlite'

    def allow_relation(self, obj1, obj2, **hints):

        return True

    def allow_migrate(self, db, model):

        return True
