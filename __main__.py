import src.core as core
import platform
import os


def clear_screen():
    """Clear terminal screen"""
    if(platform.system() == "Windows"):
        os.system("cls")
    elif(platform.system() == "Linux"):
        os.system("clear")


def main():
    """Run the application"""
    clear_screen()

    try:
        core.start()
    except KeyboardInterrupt:
        pass


if(__name__ == "__main__"):
    main()
