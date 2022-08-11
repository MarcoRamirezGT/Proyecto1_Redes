import py_compile
import sys
import subprocess
import os

from getpass import getpass
from slixmpp.clientxmpp import ClientXMPP
import xmpp
from xmpp import debug
import logging
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout


def createUser():
    print(' ')
    print('Crear un usuario: ')
    new_user = input('username@alumchat.fun:  ')
    new_password = input('password:  ')
    user = new_user
    password = new_password
    jid = xmpp.JID(user)
    print(jid)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()
    if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):

        return True
    else:
        return False


cmd = 'python echobot.py -d -j'

menu = True
while menu is True:

    print('================================================')
    print('================================================')
    print('==========BIENVENIDO AL CHAT XMPP===============')
    print('================================================')
    print('================================================')

    op = input('Que desea hacer:\n1.Login\n2.Register\n3.Salir\n>>> ')

    if op == '1':
        user = input('Ingrese su usuario (user@alumchat.fun)\n>>>')
        p = '-p'
        password = getpass('Clave:\n>>> ')
        res = cmd+' '+user+' '+p+' '+password

        list_files = subprocess.run(res)
    elif op == '2':
        print('Registro')
        createUser()

    else:
        print('Gracias por usar el chat\n')
        menu = False
