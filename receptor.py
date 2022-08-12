import socket
import pickle
import sys
s = socket.socket()


# Logged in user menu function
def userMenu():
    print("1. Muestre mis contactos")
    print("2. Mensaje privado")
    print("3. Agregar contacto")
    print("4. Mensaje grupal")
    print("5. Mostrar detalles de contacto de un usuario")
    print("6. Cambiar estado")
    print("7. Cerrar Sesion")
    print("8. Borrar Cuenta")


s = socket.socket()
port = 12345

s.connect(('127.0.0.1', port))


while True:

    userMenu()
    loggedIn_option = input("\nQue quieres hacer?: ")
    # data_send = pickle.dumps(loggedIn_option)
  #  loggedIn_option=pickle.dumps(loggedIn_option)
    if loggedIn_option == '1':
        data = pickle.dumps({'opcion': '1'})

        s.send(data)
        print('\n')
        print("Lista de usuarios:", s.recv(1024).decode(), '\n')

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
        contact = input('Cual contacto deseas ver:\n')
        data = pickle.dumps({'opcion': '5', 'contact': contact})
        s.send(data)
        print("\nDatos del contacto:\n", s.recv(1024).decode(), '\n')

    if loggedIn_option == '6':
        op = input('A cual estado deseas cambiar:\n')
        data = pickle.dumps({'opcion': '6'})
        s.send(data)
        print(s.recv(1024).decode(), '\n')

    if loggedIn_option == '7':
        data = pickle.dumps({'opcion': '7'})

        try:
            s.send(data)

        except:
            print('Se ha cerrado sesion\n')
            sys.exit()
    if loggedIn_option == '8':
        data = pickle.dumps({'opcion': '8'})
        try:
            s.send(data)

        except:
            print('Se ha borrado la cuenta\n')
            sys.exit()
