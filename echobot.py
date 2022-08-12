
from cgi import print_arguments
import email
from slixmpp.xmlstream import ElementBase, ET, JID, register_stanza_plugin
from slixmpp import Iq
import socket
import pickle
import sys
from sleekxmpp.exceptions import IqError, IqTimeout
#from slixmpp.exceptions import IqError, IqTimeout
from getpass import getpass
from argparse import ArgumentParser
import logging
import asyncio

import slixmpp

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class EchoBot(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("inicio", self.start)

        # For the users messages
        self.add_event_handler("message", self.message)
        self.add_event_handler("deleteAccount", self.deleteAccount)

        # # For the register management
        # self.register_plugin("xep_0047", {"auto_accept": True})

    async def start(self, event):

        self.send_presence()
        await self.get_roster()

    def message(self, msg):

        if msg['type'] in ('chat', 'normal'):
            print("From: ", msg["from"])
            print("Subject: ", msg["subject"])
            print("Message: ", msg["body"])
            result = 'Mensaje enviado exitosamente'
            # c.send(msg["body"].encode())
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()

    # Delete account management function using sleek exceptions

    def deleteAccount(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full
        resp['register']['remove'] = True

        try:
            resp.send(True)
        except IqError as e:
            print('Could not unregister account: %s' %
                  e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print('No response from server.')
            self.disconnect()


if __name__ == '__main__':

    parser = ArgumentParser(description=EchoBot.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    xmpp = EchoBot(args.jid, args.password)

    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0004')  # Data Forms
    xmpp.register_plugin('xep_0060')  # PubSub
    xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp.register_plugin('xep_0100')  # XMPP Add contact
    xmpp.register_plugin('xep_0030')  # XMPP Delete account
    # xmpp.register_plugin('xep_0256')

    # xmpp.connect()
    # xmpp.process(timeout=10)

    s = socket.socket()
    port = 12345

    s.bind(('', port))
    s.listen(5)
    c, addr = s.accept()

    while True:

        xmpp.connect()

        info = c.recv(1024)
        data = pickle.loads(info)

        loggedIn_option = data['opcion']

        print("Recibido: ", data)
        xmpp.process(timeout=20)
        if(loggedIn_option == "1"):
            xmpp.process(timeout=20)
            print("\nContactos:\n")

            contacts = xmpp.client_roster

            print(contacts.keys())
            data = contacts.keys()
            resu = []

            for key in contacts.keys():
                resu.append(key)

            result = ' '.join(resu)
            c.send(result.encode())

        if(loggedIn_option == "2"):
            xmpp.process(timeout=20)
            to = data['to']
            msg = data['msg']
            result = 'Mensaje enviado exitosamente'
            c.send(result.encode())

            xmpp.send_message(mto=to, mbody=msg, mtype='chat')
            xmpp.process(timeout=20)

        # Add a new users
        elif(loggedIn_option == "3"):

            xmpp.process(timeout=20)
            to = data['to']

            xmpp.send_presence(pto=to, ptype="subscribe",
                               pstatus=None, pfrom=args.jid)

            xmpp.process(timeout=20)

        # # Send a group message
        # elif(loggedIn_option == "4"):
        #     print("Option not implemented in this version")

        # Show other user information
        if (loggedIn_option == "5"):
            contact = data['contact']
            xmpp.process(timeout=20)

            contacts = xmpp.client_roster

            if contact in contacts:
                print('Contacto existente!')
                res = []
                user = contacts[contact]
                # res.append('Correo: ' + user['email'])
                res.append('Correo:'+contact)
                if contacts[contact]['name'] == '':
                    res.append('Nickname:'+'Sin nickname')
                else:
                    res.append('Nickname:'+contacts[contact]['name'])

                friends = contacts[contact]['subscription']
                if friends == 'both':
                    res.append('Suscripcion:'+'Amigo')
                result = ' '.join(res)

                c.send(result.encode())
            else:
                print('Contacto no existente!')
                r = 'Contacto no existente!'
                c.send(r.encode())

        # Set personal message
        if(loggedIn_option == "6"):

            typeStatus = ("unavailable")
            status = ("Llego a casa")
            xmpp.send_presence(pshow=typeStatus, pstatus=status)
            xmpp.process(timeout=20)
            res = 'Status actualizado'
            c.send(res.encode())

        # Log Off
        if(loggedIn_option == "7"):
            xmpp.disconnect()
            print("Logged Off")

            sys.exit()

        # Delete my account
        elif(loggedIn_option == "8"):
            xmpp.deleteAccount()
            print("Account deleted")
            sys.exit()

    c.close()
