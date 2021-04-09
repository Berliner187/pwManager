import sys

STR_TYPE = str # type: type
RUNNING_PYTHON_2 = sys.version_info[0] == 2  # type: bool
if RUNNING_PYTHON_2:
    STR_TYPE = unicode # Ignore the pyflakes warning on this line.


import tty, termios


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def mask_password(prompt, mask='*'):
    entered_password = []
    sys.stdout.write(prompt)
    sys.stdout.flush()
    while True:
        key = ord(getch())
        if key == 13:
            sys.stdout.write('\n')
            return ''.join(entered_password)
        elif key in (8, 127): # Backspace/Del key erases previous output.
            if len(entered_password) > 0:
                # Erases previous character.
                sys.stdout.write('\b \b') # \b doesn't erase the character, it just moves the cursor back.
                sys.stdout.flush()
                entered_password = entered_password[:-1]
        elif 0 <= key <= 31:
            # Do nothing for unprintable characters.
            # TODO: Handle Esc, F1-F12, arrow keys, home, end, insert, del, pgup, pgdn
            pass
        else:
            # Key is part of the password; display the mask character.
            char = chr(key)
            sys.stdout.write(mask)
            sys.stdout.flush()
            entered_password.append(char)