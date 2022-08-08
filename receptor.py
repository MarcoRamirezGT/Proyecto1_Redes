import socket
import pickle
s = socket.socket()


# Logged in user menu function
def userMenu():
    print("1. Muestre mis contactos")
    print("2. Mensaje privado")
    print("3. Add new user")
    print("4. Group message")
    print("5. Show other users information")
    print("6. My personal message")
    print("7. Log off")
    print("8. Delete my account")
    print("Enter Back to go to the last page")

s = socket.socket()
port = 12345

s.connect(('127.0.0.1', port))


while True:
   
    
    userMenu()
    loggedIn_option = input("What would you like to do?: ")
    # data_send = pickle.dumps(loggedIn_option)
  #  loggedIn_option=pickle.dumps(loggedIn_option)
    if loggedIn_option=='1':
        data = pickle.dumps({'opcion': '1'})
    
        s.send(data)
        print('\n')
        print ("Lista de usuarios:",s.recv(1024).decode())
        print('\n')
    if loggedIn_option=='2':
        to=input('A quien desea enviarle mensaje:\n')
        msg=input('Mensaje >>> ')
        data = pickle.dumps(  {'to': to, 'msg': msg})

    # , addr = c.accept()
    # data = c.recv(1024)
    