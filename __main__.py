import asyncio
import os
import platform
import src.core as core


def clear_screen():
    """Clear terminal screen"""
    if(platform.system() == "Windows"):
        os.system("cls")
    elif(platform.system() == "Linux"):
        os.system("clear")


def main():
    """Run the application"""
    clear_screen()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(core.start())
    except KeyboardInterrupt:
        pass


if(__name__ == "__main__"):
    main()
