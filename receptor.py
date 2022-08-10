import socket
import pickle
s = socket.socket()


# Logged in user menu function
def userMenu():
    print("1. Muestre mis contactos")
    print("2. Mensaje privado")
    print("3. Agregar contacto")
    print("4. Mensaje grupal")
    print("5. Informacion de otros usuarios")
    print("6. Cambiar estado")
    print("7. Cerrar Sesion")
    print("8. Borrar Cuenta")


s = socket.socket()
port = 12345

s.connect(('127.0.0.1', port))


while True:

    userMenu()
    loggedIn_option = input("Que quieres hacer?: ")
    # data_send = pickle.dumps(loggedIn_option)
  #  loggedIn_option=pickle.dumps(loggedIn_option)
    if loggedIn_option == '1':
        data = pickle.dumps({'opcion': '1'})

        s.send(data)
        print('\n')
        print("Lista de usuarios:", s.recv(1024).decode())

    if loggedIn_option == '2':
        to = input('A quien desea enviarle mensaje:\n')
        msg = input('Mensaje >>> ')
        data = pickle.dumps({'opcion': '2', 'to': to, 'msg': msg})
        s.send(data)

        print("Mensaje enviado!\n")

    if loggedIn_option == '3':
        to = input('A quien deseas agregar:\n')
        data = pickle.dumps({'opcion': '3', 'to': to})
        s.send(data)

        print("Usuario agregado!\n")
    if loggedIn_option == '5':
        # to=input('A quien deseas agregar:\n')
        data = pickle.dumps({'opcion': '5'})
        s.send(data)
        while True:
            print(s.recv(1024).decode())

    # , addr = c.accept()
    # data = c.recv(1024)
