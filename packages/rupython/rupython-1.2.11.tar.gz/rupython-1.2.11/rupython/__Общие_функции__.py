import os as ОС
import sys as Система

def Заменить_ключи_в_словаре(словарь, замены):
    новый = {}
    for н, з in словарь.items():
        новый.setdefault(замены[н] if н in замены.keys() else н, з)
    return новый

def Ожидать_нажатие_клавиши(сообщение):
    if ОС.name == 'nt':
        import msvcrt
        print('\n' + сообщение)
        msvcrt.getch()
    else:
        import tty
        import termios
        print('\n' + сообщение)
        fd = Система.stdin.fileno()
        старые_настройки = termios.tcgetattr(fd)
        try: tty.setraw(fd); Система.stdin.read(1)
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, старые_настройки)
