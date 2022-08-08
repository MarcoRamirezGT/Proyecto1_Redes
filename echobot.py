
from slixmpp.xmlstream import ElementBase, ET, JID, register_stanza_plugin
from slixmpp import Iq
import socket
import pickle

from slixmpp.exceptions import IqError, IqTimeout
from getpass import getpass
from argparse import ArgumentParser
import logging

import slixmpp

s = socket.socket()
    
    
print("Socket successfully created")

port = 12345

s.bind(('', port))
print("socket binded to %s" % (port))
s.listen(5)
print("socket is listening")
c, addr = s.accept()


class EchoBot(slixmpp.ClientXMPP):

    def __init__(self, jid, password,option):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        
        if option=='1':
            self.add_event_handler("session_start", self.start)
            self.add_event_handler("inicio", self.start)
           
        elif option=='2':
            self.add_event_handler("register", self.register)
            self.add_event_handler("session_start", self.sessionStart)
        else:
            print('Ingrese una opciona valida\n')
         # For the users messages
        self.add_event_handler("message", self.message)

        # For the register management
        self.register_plugin("xep_0047", {"auto_accept": True})

    async def start(self, event):
        
        self.send_presence()
        await self.get_roster()
        
    
    def message(self, msg):
       
        if msg['type'] in ('chat', 'normal'):
            print("From: ", msg["from"])
            print("Subject: ", msg["subject"])
            print("Message: ", msg["body"])
            result='Mensaje enviado exitosamente'
            c.send(msg["body"].encode())
            #msg.reply("Thanks for sending\n%(body)s" % msg).send()
            
    # Register management function using sleek exceptions
    def register(self, iq):
        serverResponse = self.Iq()
        serverResponse["type"] = "set"
        serverResponse["register"]["username"] = self.boundjid.user
        serverResponse["register"]["password"] = self.password

        try:
            serverResponse.send(now=True)
            logging.info("Account created!: %s!" % self.boundjid)
        except IqError as e:
            logging.error("It was imposible to create the account: %s" %
                    e.iq["error"]["text"])
            self.disconnect()
        except IqTimeout:
            logging.error("Server response took longer than wanted, try again.")
            self.disconnect()
            
    
    # Delete account management function using sleek exceptions
    def deleteAccount(self):
        serverResponse = self.Iq()
        serverResponse["type"] = "set"
        serverResponse["from"] = self.boundjid.user
        serverResponse["register"] = ""
        serverResponse["register"]["remove"] = ""
        print(serverResponse)
        try:
            serverResponse.send(now=True)
            logging.info("Account deleted %s!" % self.boundjid)
        except IqError as e:
            logging.error("It was imposible to delete the account: %s" %
                    e.iq["error"]["text"])
            self.disconnect()
        except IqTimeout:
            logging.error("Server response took longer than wanted, try again.")
            self.disconnect()


def initialMenu():
    
    print("-------------------------------------------------")
    print("           Proyecto1!")
    print("Enter the number of your choice:")
    print("1. Log in")
    print("2. Sign in")
    print("-------------------------------------------------")


if __name__ == '__main__':
    
    
    # initialMenu()
    initialOption = '1'#input("What would you like to do? (1 or 2): ")
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

    xmpp = EchoBot(args.jid, args.password,initialOption)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0100') # XMPP Add contact
   # xmpp.connect()
    
    while True:
        
        xmpp.connect()
        

        info = c.recv(1024)
        data=pickle.loads(info)
       
        loggedIn_option=data['opcion']
        
        print("Recibido: ", data)
       
        if(loggedIn_option == "1"):
            xmpp.process(timeout=10)
            print("\nContactos:\n")
            
            contacts = xmpp.client_roster
            
            print(contacts.keys())
            data=contacts.keys()
            resu=[]
            
            
            for key in contacts.keys():
                resu.append(key)
               
                
            
            result=' '.join(resu)
            c.send(result.encode())
          

        if(loggedIn_option == "2"):
            
            xmpp.process(timeout=10)
            to=data['to']
            msg=data['msg']  
            result='Mensaje enviado exitosamente'
            c.send(result.encode())          
            xmpp.send_message(mto= to, mbody = msg, mtype = 'chat')
            xmpp.process(timeout=10)

        # Add a new users
        elif(loggedIn_option == "3"):
            xmpp.process(timeout=15)
            to=data['to']
            
            xmpp.send_presence(pfrom=args.jid, ptype="subscribed", pto=to)
            xmpp.process(timeout=15)
        
        # # Send a group message    
        # elif(loggedIn_option == "4"):
        #     print("Option not implemented in this version")

        # Show other user information   
        if (loggedIn_option == "5"):
            xmpp.process()
            xmpp.message()
              
            

        # Set personal message    
        elif(loggedIn_option == "6"):
            personal = input("Cual es tu mensaje personal: ")
            status = input("Cual es tu nueo estado: ")
            xmpp.makePresence(pfrom=xmpp.jid, pstatus=status, pshow=personal)

        # Log Off    
        elif(loggedIn_option == "7"):
            print("Logged Off")
            xmpp.disconnect()
            break   

        # Delete my account
        elif(loggedIn_option == "8"):   
            print("Account deleted")
            xmpp.deleteAccount()
            xmpp.disconnect()

        # Go back
        elif(loggedIn_option == "Back"):   
            print("Option not implemented in this version")
    c.close()