# fileManager.py
# Created by: Chris Tornow
# Initial Create Date: 07-31-2022
# Class: CIS245-T304 Introduction to Programming
# Detail: File manager tool for creating a file within directory specified
# ------------------------------------------------------------------------------
import cursor
import time
import os
import sys

os.system("")  # enables ansi escape characters in terminal

# ------------------------------------------------------------------------------
# Globals
TOOL_NAME = 'File Manager'


# ------------------------------------------------------------------------------

class SetFont:  # Use for printing text
    # Styles
    BOLD = '\033[1m'
    # Colors
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    MAGENTA = '\033[35m'
    # Remove formatting
    ENDC = '\033[0m'


class ScreenFormatting:

    def print_divide_line():
        '''Print dividing line across screen.'''
        print(25 * "~~~")

    def clear_console():
        '''Clear the full console.'''
        os.system('clear')

    def clear_lines(lines=1):
        '''Clear above x lines in console.'''
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        for n in range(lines):
            print(LINE_UP, end=LINE_CLEAR)

    def print_header():
        '''Print the application header.'''
        ScreenFormatting.print_divide_line()
        welcomeMessage = f"{SetFont.MAGENTA}{SetFont.BOLD}Welcome to the {TOOL_NAME}{SetFont.ENDC}"
        print(f"{welcomeMessage:^85}")  # Print centered
        ScreenFormatting.print_divide_line()

    def print_strobe(message, iterations=3, seconds_message=1, seconds_blink=1):
        '''Print a message with a strobe effect based on variables set.'''
        n = 0
        cursor.hide()  # Hide the cursor
        while n < iterations:
            # Print the message and wait set time
            print(message)
            time.sleep(seconds_message)
            # Clear the line, then wait for blink time
            ScreenFormatting.clear_lines(2)
            print(' ', end='\r')
            time.sleep(seconds_blink)
            ScreenFormatting.clear_lines()
            n += 1
        cursor.show()  # Show the cursor

    def print_typewriter(message, letter_speed=.01):
        '''Print a message with a typewriter effect based on variables set. Letter speed is in seconds'''
        message = str(message)  # Change to string for precaution
        cursor.hide()  # Hide the cursor
        for char in message:
            time.sleep(letter_speed)
            sys.stdout.write(char)
            sys.stdout.flush()
        cursor.show()  # Show the cursor


class UserInteraction:

    def get_user_response_directory():
        inputPass = False
        while inputPass == False:
            userInput = input(f"Enter a {SetFont.GREEN}{SetFont.BOLD}" \
                              f"directory path{SetFont.ENDC}: ")
            # Print a divide line
            ScreenFormatting.print_divide_line()
            inputPass = True
        return userInput

    def get_user_response_filename():
        inputPass = False
        while inputPass == False:
            userInput = input(f"Enter a {SetFont.GREEN}{SetFont.BOLD}" \
                              f"file name{SetFont.ENDC} (*.txt will be applied): ")
            # Print a divide line
            ScreenFormatting.print_divide_line()
            inputPass = True
        return str(userInput) + ".txt"

    def get_user_response_options(message, options=['Y', 'N']):
        inputPass = False
        while inputPass == False:
            options_text = ''
            # Create a string of all the options
            for o in options:
                options_text = options_text + f"{SetFont.CYAN}{SetFont.BOLD}{o}{SetFont.ENDC}" + " | "
            # Remove the end delimiter and format for print
            options_text = options_text.rstrip(' | ')
            print(message, options_text)
            user_input = input().upper()
            ScreenFormatting.print_divide_line()
            # Check if the entered value in options list
            if user_input in options:
                return user_input
                ScreenFormatting.print_divide_line()
                inputPass = True
            else:
                ScreenFormatting.print_divide_line()
                print("Error -- Entered value not an option")
                ScreenFormatting.print_divide_line()

    class User():
        def __init__(self):  # Define a dictionary for user information
            self.user_details = {'Full Name': '', 'Address': '', 'Phone Number': ''}

        def set_full_name(self, full_name):
            self.user_details['Full Name'] = full_name

        def set_address(self, address):
            self.user_details['Address'] = address

        def set_phone_number(self, phone_number):
            self.user_details['Phone Number'] = phone_number

        def pretty_print(self, delimiter=','):
            pretty = "Full Name : " + self.user_details['Full Name'] + delimiter \
                     + "Address : " + self.user_details['Address'] + delimiter \
                     + "Phone Number : " + self.user_details['Phone Number']
            return pretty


class FileManagement:

    def format_full_filename(path, filename=''):
        path = path.replace("\\", "/")
        path = os.path.join(path, '')  # Make sure slash at end
        full_filepath = os.path.join(os.path.normpath(path), filename)
        return full_filepath

    def check_file_exists(full_filename):
        if os.path.isfile(full_filename):  # Check if file exists
            return True
        else:
            return False

    def check_directory_exists(full_directory):
        if os.path.isdir(full_directory):  # Check if directory exists
            return True
        else:
            return False

    def create_directory(full_directory):
        full_directory = FileManagement.format_full_filename(full_directory)
        if FileManagement.check_directory_exists(full_directory) == False:
            print(f"\t{SetFont.GREEN}{SetFont.BOLD}{full_directory}{SetFont.ENDC} does not exist; creating")
            try:
                os.makedirs(full_directory)
                return True # Create directory was successful
            except:
                return False # Create directory failed
        else:
            print(f"\t{SetFont.GREEN}{SetFont.BOLD}{full_directory}{SetFont.ENDC} exists; do not create")

    def create_file(directory, filename):
        full_filepath = FileManagement.format_full_filename(directory, filename)
        if FileManagement.check_file_exists(full_filepath) == False:
            print(f"\t{SetFont.GREEN}{SetFont.BOLD}{filename}{SetFont.ENDC} does not exist; creating")
            with open(full_filepath, 'w') as fileHandle:
                fileHandle.write("")  # Create the file
        else:
            print(f"\t{SetFont.GREEN}{SetFont.BOLD}{filename}{SetFont.ENDC} exists; do not create")

    def write_to_file(path, filename, write, type_of_write='w'):
        full_filepath = FileManagement.format_full_filename(path, filename)
        with open(full_filepath, type_of_write) as fileHandle:
            fileHandle.write(write)
        print(f"Saved data to {SetFont.GREEN}{SetFont.BOLD}{full_filepath}{SetFont.ENDC}")

    def read_from_file(path, filename, type_of_read='r'):
        full_filepath = FileManagement.format_full_filename(path, filename)
        with open(full_filepath, type_of_read) as fileHandle:
            data = fileHandle.read()
        return data


def main():
    ScreenFormatting.print_header()
    do_until = True
    while do_until:
        # Get the directory from the user
        directory = UserInteraction.get_user_response_directory();
        # Get the filename from the user, the extension will be applied
        filename = UserInteraction.get_user_response_filename();

        # Create the directory; if not exist
        created = FileManagement.create_directory(directory)
        if created == False:
            print(f"\tError -- Directory cannot be created")
            ScreenFormatting.print_divide_line()
            continue
        # Create the file in the created directory
        FileManagement.create_file(directory, filename)

        # Print a divide line
        ScreenFormatting.print_divide_line()

        # Ask user for input details and store
        user = UserInteraction.User()
        user.set_full_name(input("Enter Full Name: "))
        user.set_address(input("Enter Address: "))
        user.set_phone_number(input("Enter Phone Number: "))

        # Print a divide line
        ScreenFormatting.print_divide_line()

        # Save the dictionary of the user to the file
        FileManagement.write_to_file(directory, filename, user.pretty_print())

        # Print from the file to screen
        file_info = FileManagement.read_from_file(directory, filename)
        data_message = "\n\t== Data in file ==\n\t" + file_info.replace(',', '\n\t')
        ScreenFormatting.print_typewriter(data_message, .03)

        # Print a divide line
        print("\n")
        ScreenFormatting.print_divide_line()

        # Get the user response whether data entered is correct
        response = UserInteraction.get_user_response_options("Is this data correct?")

        # Pring to the user whether they are a good person per input
        if response == 'N':
            print("Well, that isn't good...Lying is a bad habit")
        else:
            print('Thank you for confirming!')

        # Just end and not allow another run at this time
        do_until = False


if __name__ == "__main__":
    main()
