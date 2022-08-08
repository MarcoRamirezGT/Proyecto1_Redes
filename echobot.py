from sqlite3 import Timestamp
from slixmpp.xmlstream import ElementBase, ET, JID, register_stanza_plugin
from slixmpp import Iq
import socket
import pickle

from slixmpp.exceptions import IqError, IqTimeout
from getpass import getpass
from argparse import ArgumentParser
import logging

import slixmpp


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

# Logged in user menu function
def userMenu():
    print("1. Show other users")
    print("2. Send message to a specific user")
    print("3. Add new user")
    print("4. Group message")
    print("5. Show other users information")
    print("6. My personal message")
    print("7. Log off")
    print("8. Delete my account")
    print("Enter Back to go to the last page")

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
   # xmpp.connect()
    s = socket.socket()

    print("Socket successfully created")

    port = 12345

    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen(5)
    print("socket is listening")
    c, addr = s.accept()
    
    while True:
        
        xmpp.connect()
        

        data = c.recv(1024)
        data=pickle.loads(data)
        loggedIn_option=data['opcion']
        
        # data = codecs.encode(pickle.dumps(data), "hex").decode()
        #loggedIn_option = pickle.loads(data)
        print("Recibido: ", data)
        
        # data = codecs.encode(pickle.dumps(data), "hex").decode()
       # loggedIn_option = pickle.loads(data)
        #print("Recibido: ", loggedIn_option)
        
        # To get all the users joined to the chat
        
        if(loggedIn_option == "1"):
            xmpp.process(timeout=10)
            print("\nContactos:\n")
            
            contacts = xmpp.client_roster
            while (len(contacts)==0):
                xmpp.process(timeout=10)
            print(contacts.keys())
            data=contacts.keys()
            resu=[]
            
            
            for key in contacts.keys():
                resu.append(key)
               
                
            
            result=' '.join(resu)
            c.send(result.encode())
            c.close()
            xmpp.process(0)
            
            

        # Send a message to a specific user 
        elif(loggedIn_option == "2"):
            
            # xmpp.process(timeout=10)
            # 
            # xmpp.send_message(mto= user, mbody = message, mtype = 'chat')
            # print("Tu mensaje ha sido enviado")
            # xmpp.process(timeout=15)
            print ('opcion 2')

        # Add a new user
        elif(loggedIn_option == "3"):
            xmpp.process(timeout=10)
            user = input("A quien quieres agregar: ")
            xmpp.send_presence(pto = user, ptype ='subscribe')
            xmpp.process(timeout=10)
        
        # # Send a group message    
        # elif(loggedIn_option == "4"):
        #     print("Option not implemented in this version")

        # # Show other user information   
        # elif(loggedIn_option == "5"):
        #     print("Option not implemented in this version")

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