import curses
import sys
import keyboard
import os

stdscr = curses.initscr()

def clear_terminal():
    stdscr.clear()

def add_text(x,y,text):
    stdscr.addstr(x,y,text)




def main(argv):


    banner = """
__________                         __________.__                
\______   \______  _  __ __________\______   \  | _____  ___.__.
 |     ___/  _ \ \/ \/ // __ \_  __ \     ___/  | \__  \<   |  |
 |    |  (  <_> )     /\  ___/|  | \/    |   |  |__/ __ \\\___  |
 |____|   \____/ \/\_/  \___  >__|  |____|   |____(____  / ____|
                            \/                         \/\/     
"""

    page = "menu"
    key = ""
    menu_option = 0

    program_code = ""


    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    if curses.has_colors():
        curses.start_color()

    caughtExceptions = ""

    while True: 

        try:                          

            if page == "menu":

                stdscr.clear()

                n = 0
                for line in banner.splitlines():
                    stdscr.addstr(n, int((curses.COLS - 64)/2), line)
                    n += 1

                stdscr.addstr(10,int((curses.COLS - len("----------------"))/2),"----------------")

                if menu_option == 0:
                    stdscr.addstr(11,int((curses.COLS - len("> Programs <"))/2),"> Programs <")
                else:
                    stdscr.addstr(11,int((curses.COLS - len("Programs"))/2),"Programs")

                if menu_option == 1:
                    stdscr.addstr(12,int((curses.COLS - len("> Shutdown <"))/2),"> Shutdown <")
                else:
                    stdscr.addstr(12,int((curses.COLS - len("Shutdown"))/2),"Shutdown")

                if menu_option == 2:
                    stdscr.addstr(13,int((curses.COLS - len("> Settings <"))/2),"> Settings <")
                else:
                    stdscr.addstr(13,int((curses.COLS - len("Settings"))/2),"Settings")

                if menu_option == 3:
                    stdscr.addstr(14,int((curses.COLS - len("> Info <"))/2),"> Info <")
                else:
                    stdscr.addstr(14,int((curses.COLS - len("Info"))/2),"Info")

                stdscr.refresh()
                stdscr.keypad(True)
                key = stdscr.getkey()

                if key == "KEY_A2":
                    menu_option = menu_option - 1
                    if menu_option < 0:
                        menu_option = 3
                        
                if key == "KEY_C2":
                    menu_option = menu_option + 1
                    if menu_option > 3:
                        menu_option = 0

                if key == "\n":
                    if menu_option == 0:
                        page = "programs"
                    if menu_option == 1:
                        break
                    if menu_option == 2:
                        page = "setting"
                    if menu_option == 3:
                        page = "info"

                    menu_option = 0
                
            if page == "programs":
                stdscr.clear()

                stdscr.addstr(0,int((curses.COLS - len("[ programs ]"))/2),"[ programs ]")

                n = 0
                for program in os.listdir("programs"):
                    if program.endswith(".py"):

                        if menu_option == n:
                            stdscr.addstr(n + 3,int((curses.COLS - len("> " + program + " <"))/2),"> " + program + " <")
                        else:
                            stdscr.addstr(n + 3,int((curses.COLS - len(program))/2),program)
                        n += 1
                
                stdscr.refresh()
                key = stdscr.getkey()

                if key == "KEY_A2":
                    menu_option = menu_option - 1
                    if menu_option < 0:
                        menu_option = n
                        
                if key == "KEY_C2":
                    menu_option = menu_option + 1
                    if menu_option > n:
                        menu_option = 0

                if key == "\n":
                    program_list = os.listdir("programs")
                    program_code = open(f"programs/{program_list[menu_option]}").read()
                    page = "run"


            if page == "run":

                def key_pressed(key):
                    event = keyboard.read_event()
                    if event.event_type == keyboard.KEY_DOWN and event.name == key:
                        return True
                    else:
                        False


                stdscr.clear()  
                stdscr.keypad(True)

                try:
                    exec(program_code)
                except Exception as err:
                    stdscr.clear()
                    stdscr.addstr(0,0,f"error: {err}")
                    stdscr.refresh()

                stdscr.getkey()
                stdscr.clear()

                page = "programs"

                                            
        except Exception as err:
            caughtExceptions = str(err)
            break


    
    curses.nocbreak()
    curses.echo()
    curses.curs_set(True)
    curses.endwin()

    if "" != caughtExceptions:
        print ("Got error(s) [" + caughtExceptions + "]")

if __name__ == "__main__":
    main(sys.argv[1:])
