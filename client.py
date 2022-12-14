# Required LIBRARIES
import socket
import pickle
import sys
import filecmp
import shutil
import shutil


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

# Recv/Send data from the client
while True:
    original = './messages.txt'
    copy = './messages_copy.txt'
    result = filecmp.cmp(original, copy)

    if result == True:
        userMenu()
        loggedIn_option = input("\nQue quieres hacer?: ")
        # Show contacts
        if loggedIn_option == '1':
            data = pickle.dumps({'opcion': '1'})

            s.send(data)
            print('\n')
            print("Lista de usuarios:", s.recv(1024).decode(), '\n')
        # Send private message to a contact
        if loggedIn_option == '2':
            to = input('A quien desea enviarle mensaje:\n')
            msg = input('Mensaje (exit)>>> ')

            data = pickle.dumps({'opcion': '2', 'to': to, 'msg': msg})
            s.send(data)
            # msg = input('Mensaje (exit)>>> ')

            # print("Mensaje enviado!\n")
        # Add a new users
        if loggedIn_option == '3':
            to = input('A quien deseas agregar:\n')
            data = pickle.dumps({'opcion': '3', 'to': to})
            s.send(data)

            print("Usuario agregado!\n")
        # Contact info
        if loggedIn_option == '5':
            contact = input('Cual contacto deseas ver:\n')
            data = pickle.dumps({'opcion': '5', 'contact': contact})
            s.send(data)
            print("\nDatos del contacto:\n", s.recv(1024).decode(), '\n')
        # Change status
        if loggedIn_option == '6':
            # op = input('A cual estado deseas cambiar:\n')
            status = input('Cual es el estado:\n')
            data = pickle.dumps({'opcion': '6', 'status': status})
            s.send(data)
            print(s.recv(1024).decode(), '\n')
        # Close session
        if loggedIn_option == '7':
            data = pickle.dumps({'opcion': '7'})

            try:
                s.send(data)

            except:
                print('Se ha cerrado sesion\n')
                sys.exit()
        # Delete account
        if loggedIn_option == '8':
            data = pickle.dumps({'opcion': '8'})
            try:
                s.send(data)

            except:
                print('Se ha borrado la cuenta\n')
                sys.exit()

        if loggedIn_option == '9':
            data = pickle.dumps({'opcion': '9'})

            text = input('Escribe el mensaje que deseas enviar:\n')
            s.send(data)
            while text != 'exit':

                text = input('Escribe el mensaje que deseas enviar:\n')
    if result == False:

        f = open(original, 'r')
        d = open(copy, 'w')

        data = f.readlines()

        print('Ha ingresado un nuevo mensaje:\n')
        print(data[-1])
        shutil.copyfile(original, copy)
