import os
import subprocess as sp

paths = {
    'notes': "/System/Applications/Notes.app/Contents/MacOS/Notes",
    'discord': "/Applications/Discord.app/Contents/MacOS/Discord",
    'calculator': "/System/Applications/Calculator.app/Contents/MacOS/Calculator",
    'photo_booth': "/System/Applications/Photo Booth.app/Contents/MacOS/Photo Booth"
}


def open_notes():
    os.system(paths['notes'])


def open_discord():
    os.system(paths['discord'])


def open_terminal():
    os.system('start cmd')


def open_photobooth():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    sp.Popen(paths['calculator'])