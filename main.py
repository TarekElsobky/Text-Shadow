# Importing modules
import customtkinter as ctk  # Gui library
from arabic_reshaper import reshape
from cryptography.fernet import Fernet  # Encryption library
from os.path import join, dirname  # for making the paths relative


key = b""


# Create new key and use it
def create_key():
    global key
    key = str(Fernet.generate_key())[2:-1]
    root.clipboard_clear()
    root.clipboard_append(key)


# Use already generated key
def set_key():
    global key
    key = output_entry.get().encode()


# Encrypt message using the key
def encrypt(text):
    global key
    if key:
        fernet = Fernet(key)
        return str(fernet.encrypt(bytes(text, "utf-8")))[2:-1]
    else:
        return "Set the key first"


# Decrypt message using the key
def decrypt(text):
    global key
    if key:
        fernet = Fernet(key)
        try:
            return str(fernet.decrypt(bytes(text, "utf-8")))[2:-1]
        except Exception:
            return "Wrong key"
    else:
        return "Set the key first"


# Converting text to binary
def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in encrypt(text))


# Converting binary to text
def binary_to_text(binary):
    return decrypt(''.join(chr(int(byte, 2)) for byte in binary.split()))


# Converting binary to zero width characters 0 => "\u200B", 1 => "\u200C" and " " => "\u200D"
def binary_to_zero_width(binary):
    lista = []
    for bit in binary:
        if bit == '0':
            lista.append("\u200B")
        elif bit == '1':
            lista.append("\u200C")
        elif bit == ' ':
            lista.append("\u200D")
    lista.reverse()
    return lista


# Converting zero width characters to binary "\u200B" => 0, "\u200C" => 1 and "\u200D" => " "
def zero_width_to_binary(text):
    lista = []
    for bit in text:
        if bit == "\u200B":
            lista.append('0')
        elif bit == "\u200C":
            lista.append('1')
        elif bit == "\u200D":
            lista.append(' ')
    return ''.join(lista)  # return the zero-width as text


# Hide the real message into the mask message after the first character
def hide(event=None):
    if key:
        message = message_entry.get()
        mask = mask_entry.get()
        if not mask or not message:  # check if two fields are filled
            pass
        else:
            msg_binary = text_to_binary(message)  # convert message to binary
            msg_hide = binary_to_zero_width(msg_binary)  # convert binary to zero-width characters
            mask_list = list(mask)  # convert mask message to list
            for bit in msg_hide:
                mask_list.insert(1, bit)  # insert the zero-width characters into mask message
            if 1571 <= ord(mask_list[0]) <= 1610:
                set_output_entry(reshape(''.join(mask_list)))
            else:
                set_output_entry(''.join(mask_list))  # show the combined message in the output entry
            if output_entry.get():
                root.clipboard_clear()  # clear the clipboard
                root.clipboard_append(''.join(mask_list))  # copy the combined message
    else:
        set_output_entry("Set the key first")
        output_entry.after(1850, reset_output_entry)  # after 1.85 second clear the output entry


# Extracting the real message from the combined message
def show(event=None):
    message = message_entry.get()
    flag = 0
    for char in message:
        if not char.isalpha() and not char.isdigit():  # check if the message contains zero-width characters
            flag = 1
            break
    if flag:
        msg_binary = zero_width_to_binary(message)  # convert the zero-width characters to binary
        set_output_entry(binary_to_text(msg_binary))  # show the extracted message in the output entry
        output_entry.after(1850, reset_output_entry)  # after 1.85 second clear the output entry
    else:
        set_output_entry("No hidden message")
        output_entry.after(1850, reset_output_entry)  # after 1.85 second clear the output entry


def set_output_entry(output):
    entry_var.set(output)  # show the output in the output entry


def reset_output_entry():
    set_output_entry("")  # clear the output entry


# Clear the entries
def clear(event=None):
    mask_entry.delete(0, len(mask_entry.get()))  # clear the mask entry
    message_entry.delete(0, len(message_entry.get()))  # clear the message entry
    message_entry.focus_set()  # set focus on the message entry


# Change between dark and light mode
def change_mode(event):
    current_mode = ctk.get_appearance_mode()  # get current appearance mode
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")  # set appearance mode to light
    else:
        ctk.set_appearance_mode("Dark")  # set appearance mode to dark


# Perform the hide or show operation based on given argument
def action(event):
    mask = mask_entry.get()
    msg = message_entry.get()
    output = output_entry.get()
    if msg and mask:
        hide()
        clear()
    elif msg and not mask:
        show()
        clear()
    elif output and not msg and not mask:
        set_key()
        output_entry.delete(0, len(output_entry.get()))  # clear the output entry
    if not output and not msg and not mask:
        create_key()
    message_entry.focus_set()  # set focus on message entry


def hide_window(event):
    root.attributes("-alpha", 0)  # make the window invisible


def show_window(event):
    root.attributes("-alpha", 1)  # make the window visible


# Set focus to the output entry
def set_focus():
    output_entry.focus_set()  # set focus on the output entry:


root = ctk.CTk()

entry_var = ctk.StringVar()  # define variable for output entry
mode = ctk.set_appearance_mode("dark")  # set the app mode to dark
theme = ctk.set_default_color_theme("green")  # set the theme to green

root.geometry("500x450+620+230")  # defining the app window width and height, width = 500, height = 450
root.iconbitmap(join(dirname(__file__), "halloween.ico"))  # Set the window icon using relative path
root.title("Text Shadow by Tarek Elsobky")  # set the window title
root.resizable(False, False)  # making the app window not resizable

# Defining and packing frame
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Defining and packing the label to show the app name
label = ctk.CTkLabel(master=frame, text="Text Shadow", font=("Roboto", 24))
label.pack(pady=5, padx=10)

# Defining and packing entry to show the output
output_entry = ctk.CTkEntry(master=frame, textvariable=entry_var)
output_entry.pack(pady=60, padx=10)

# Defining and packing entry where user insert the mask message
mask_entry = ctk.CTkEntry(master=frame, placeholder_text="Mask")
mask_entry.pack(pady=12, padx=10)

# Defining and packing entry where user insert the real message
message_entry = ctk.CTkEntry(master=frame, placeholder_text="Message")
message_entry.pack(pady=12, padx=10)

# Defining and packing button to hide the message into the mask message
hide_button = ctk.CTkButton(master=frame, text="Hide and copy", command=hide)
hide_button.pack(pady=12, padx=10)

# Defining and packing button to extract the real message from the combined message
show_button = ctk.CTkButton(master=frame, text="Show", command=show)
show_button.pack(pady=12, padx=10)

# Defining shortcuts
root.bind('<Control-l>', clear)  # clear the entries
root.bind('<Control-m>', change_mode)  # change the app mode between dark and light
root.bind('<Return>', action)  # perform action depends on the fields
root.bind('<Control-h>', hide_window)  # create shortcut for hiding the window
root.bind('<Control-s>', show_window)  # create shortcut for showing the window
root.after(100, set_focus)

# Start the application
root.mainloop()  # start the app loop

