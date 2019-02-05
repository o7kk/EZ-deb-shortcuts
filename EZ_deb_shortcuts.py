#!/usr/bin/python3

import os
from getpass import getuser
from operator import itemgetter


def print_instructions(shortcut_descriptor, filename, file_path):
    """Print instructions about making the shortcut
    """

    # get contents of file
    contents = ""
    with open(file_path, "r") as file:
        for line in file:
            contents = contents + line

    print("\nInstructions to make shortcut for [{}]".format(shortcut_descriptor))
    print("\n(1) Go to Desktop and create new file. Name it \"{}\"".format(filename))
    print("\n(2) Edit the file (with text editor of choice) and paste in the following:")
    print(contents)
    print("(3) !IMPORTANT!. Save the file you have just edited. :)")
    print("\n(4) Change the permissions to execute (775 within CMD)")
    print("\n(5) Conveniently access your exciting application, straight from the desktop!")
    return


def copy_shortcut_to_desktop(desktop_dir, filename, file_path, shortcut_name):
    """Copy contents of chosen file and reproduce in user's desktop folder
    """
    # check for an existing shortcut. abort if True
    if os.path.isfile(os.path.join(desktop_dir, filename)):
        print("The shortcut for {} already exists! Aborting.".format(shortcut_name))
        return
    # read shortcut and gather contents
    contents = ""
    with open(file_path, "r") as file:
        for line in file:
            contents = contents + line

    # write contents to new file in desktop folder
    new_file_path = os.path.join(desktop_dir, filename)
    new_file = open(new_file_path, "a")
    new_file.write(contents)
    new_file.close()

    # set permisions for the splendid shortcut!
    os.chmod(new_file_path, 0o775)

    # self descriptive, but a nice message nonetheless
    print("Shortcut to [{}] made and permisions set! We are done here.".format(filename))
    return


def get_name_for_desktop_file(desktop_file):
    """Get the displayed name for the shortcuts
    """
    name = ""
    with open(desktop_file, "r") as file:
        for line in file:
            if "Name=" in line:
                name = line.strip().split("=")[1]
                break
    return name


def main():
    """Script to automatically list and copy shortcuts to the users HOME DIR
    Also gives instructions on how to manually do this task for a different user
    """

    # main static variables
    app_name = "EZ deb shortcuts"
    home_desktop_dir = "/home/{}/Desktop/".format(getuser())  # current user's desktop root
    desktop_item_dir = "/usr/share/applications/"  # path to shortcuts

    # check desktop_item_dir. simply exit the program
    if not os.path.isdir(desktop_item_dir):
        print("\"{}\" Cannot be found".format(desktop_item_dir))
        exit()

    # check for Desktop folder path. imply onscreen instructions
    home_desktop_dir_option = True
    if not os.path.isdir(home_desktop_dir):
        home_desktop_dir_option = False

    # welcome text
    print("{} (by jsephler)".format(app_name))

    if home_desktop_dir_option:
        print("\nCreate shortcut in \"{}\"?".format(home_desktop_dir))
        print("[y|Y] to continue | [o|O] for on-screen instructions | [q|Q] to quit : ")
    else:
        print("{} desktop or home folder not detected... don't worry though!\n".format(getuser()))
        print("[o|O] for on-screen instructions | [q|Q] to quit : ")

    i = ""  # i; control for loop
    opt1 = 0  # opt1 keeps track of selection. used further along

    # input loop; check for bad input & action good input
    while opt1 == 0:
        if i:
            i = input("retry: ")
        else :
            i = input()

        if i in ["y", "Y"]:  # write to user's desktop
            if home_desktop_dir_option:
                opt1 = 1
        elif i in ["o", "O"]:  # onscreen instructions
            opt1 = 2
        elif i in ["q", "Q"]:  # quit
            print("\nQuitting...")
            exit()

    # define a list for all the shortcut items found
    shortcut_list = []

    # get raw file values in "/usr/share/applications"
    _raw_list = os.listdir(desktop_item_dir)

    # iterate through raw list and refine
    for _ in _raw_list:

        # check for .desktop. check last word in split. ignore if not "desktop"
        if not _.strip().split(".")[-1] == "desktop":
            continue

        name = get_name_for_desktop_file(os.path.join(desktop_item_dir, _))

        shortcut_list.append(["",  # number allocation
                              "{0}".format(name),  # name of icon
                              "{0}".format(_),  # actual file name
                              ])

    # sort the list into alpha and re-number the items
    shortcut_list = sorted(shortcut_list, key=itemgetter(1))
    c = 1
    for s in shortcut_list:
        s[0] = c
        c += 1

    print("")  # tidy

    # print numbers and names of desktop items found
    for s in shortcut_list:
        print("({0}) {1}".format(
            s[0],
            s[1]
        ))

    print("")  #tidy

    # the section below gets a good input from the list
    i = ""  # i; control for loop

    # create range from list values to test against input
    n_range = range(1, len(shortcut_list) + 1)

    # user instructions... blah blah
    print("[{0}-{1}] to select | [q|Q] to quit".format(1, len(shortcut_list)))

    # main input l0o0p
    while True:
        if i:
            i = input("Retry: " )
        else:
            i = input()

        if i in ["q", "Q"]:
            print("\nQuitting...")
            exit()
        else:
            try:
                i = int(i)
                if i in n_range:
                    break
                else:
                    i = "0"
                    continue
            except ValueError:
                continue

    s_item = ""

    # get index of list item
    for s in shortcut_list:
        if s[0] == i:
            s_item = s

    # make the dreams in opt1 come true!
    # no seriously. send the items where requested.
    if opt1 == 1:
        copy_shortcut_to_desktop(
                                home_desktop_dir,
                                s_item[2],
                                os.path.join(desktop_item_dir, s_item[2]),
                                s_item[1],
                                )
    elif opt1 == 2:
        print_instructions(s_item[1],
                           s_item[2],
                           os.path.join(desktop_item_dir, s_item[2])
                           )
    print("\nThanks for using {}, please sudo-away safely!".format(app_name))
    exit()


if __name__ == "__main__":
    main()
