from cryptography.fernet import Fernet

key = b'rPuxmfV-imRkOA7sXAcCFWCLzl1NCKwifrTpH6KA3X4='
fernet = Fernet(key)
encryptedUsername = b'gAAAAABi9SVug0gzYaps5x4vKcWXzL5T3dHTYKB4fGhB4QAwx4XpovbplHnpmRDhK3VbD9C6OZKjTx-UdRXislq-wqLnUYu42Q=='
encryptedPassword = b'gAAAAABi9SVuBRXULUyblDkTUIn3kUyxWqjkxtTcQ5eE2rN3hUEJFd4Ydbdi5Uwu3aKh1zMX_hYdaag1g8gPZPTn3zraNAGl9g=='


def login():
    username = input('Enter your username : ')
    password = input('Enter your password : ')
    if (username == fernet.decrypt(encryptedUsername).decode() and password == fernet.decrypt(
            encryptedPassword).decode()):
        return True
    else:
        print('Invalid Username or password.')
        return False
