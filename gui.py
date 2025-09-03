from tkinter import *
# from PIL import ImageTk, Image
from tkinter import filedialog
import pandas as pd
from pathlib import Path
from decklist_test import get_decklist_from_collection, decklist_moxfield

green = pd.read_csv('c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv')

def handle_action(event = None):
    # print("Action triggered")
    return()

def _on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")


root = Tk()

## Having the enter key work for highlighted button ##
def handle_enter_key(event):
    focused_widget = root.focus_get()
    focused_widget.invoke()
root.bind("<Return>", handle_enter_key)

container = Frame(root)
canvas = Canvas(container, width = 500, height = 400, bg = 'grey')
canvas.bind_all("<MouseWheel>", _on_mousewheel)
vscrollbar = Scrollbar(container, orient='vertical', command = canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e:canvas.configure( scrollregion=canvas.configure(scrollregion=canvas.bbox("all"))))

canvas.create_window(0,0, window = scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=vscrollbar.set)
container.grid(row= 0, column=0, sticky='nsew')
# canvas.grid(row = 1, columns = 1, sticky='nsew')
canvas.grid(row = 1, column = 0)
# canvas.bind("<Configure>", resize_frame)
vscrollbar.grid(row=0, column=0, sticky = 'nse')


## Load in a file ## 

root.title("Deck List Comparison")
# root.rowconfigure(1, weight=1)
# root.columnconfigure(1, weight=1)
# root.filename = filedialog.askopenfilename(initialdir='c:/Users/Moose/OneDrive/Pictures', title = "select a file", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))

# my_label = Label(root, text = root.filename).pack()
# my_image = ImageTk.PhotoImage(Image.open(root.filename))
# my_image_label = Label(image = my_image).pack()

def resize_frame(event):
    event.width
    event.height
    # self._canvas.itemconfig(self._frame_id, height=e.height, width=e.width)

def decklist_load():
    # global decklist 
    # global canvas
    root.filename = filedialog.askopenfilename(initialdir='c:/Users/Moose/OneDrive/Documents/magic_project', title = "select a file")#, filetypes=(("all files", "*.*")))
    
    # Have the label only be the deck list name, not the full path
    # Find where the last '/' is in the path. After that character will be the file name. 
    # Take only the final index. This is where the last slash is. 
    slash_ind = [i for i, letter in enumerate(root.filename) if letter == '/'][-1]
    # Set the deck name as the file path from that index onward. 
    # Set up to the last 4 digits to get rid of ".txt". This won't work for all file types necessarily, but works for now. 
    deck_name = root.filename[slash_ind + 1:-4]
    my_label = Label(root, text = deck_name).grid(row = 1, column=0, columnspan=2)


    ## The way the function works right now, I think we'll have to load in the decklist and then immediately do the table
    # Don't currently need to save decklist as a global variable

    # Save the pandas dataframe as a global variable that can be used elsewhere.     
    # decklist = decklist_moxfield(root.filename)
    #printing will later be set by a checkbox. Hard code it here because it will change the shape of the table. 
    enough_cards, not_enough_cards, cards_not_in_collection = get_decklist_from_collection(green, root.filename, printing = False)
    print(enough_cards)
    print(not_enough_cards)
    # Set up tags on coloring
    # Length of dataframes
    enough_tag = len(enough_cards['Name'])
    not_enough_tag = len(not_enough_cards['Name'])
    not_in_tag = len(cards_not_in_collection['Name'])
    row_number = enough_tag + not_enough_tag + not_in_tag

    # container = Frame(root)
    # canvas = Canvas(container, width = 500, height = 400, bg = 'grey')
    # canvas.bind_all("<MouseWheel>", _on_mousewheel)
    # vscrollbar = Scrollbar(container, orient='vertical', command = canvas.yview)
    # scrollable_frame = Frame(canvas)

    # scrollable_frame.bind("<Configure>", lambda e:canvas.configure( scrollregion=canvas.configure(scrollregion=canvas.bbox("all"))))

    # canvas.create_window(0,0, window = scrollable_frame, anchor='nw')
    # canvas.configure(yscrollcommand=vscrollbar.set)

    # For now just do if there are enough or not. Don't worry about set or ID
    # That will be for later. 
    table_headers = ['Name', "Decklist Quantity", "Collection Quantity"]#, "Set Code", 'Collector Number']
    for test_row in range(0, row_number):
        for header_to_create in table_headers:
            current_entry = Entry(scrollable_frame, justify='center')
            if test_row == 0:
                current_entry.insert(0, header_to_create)
                current_entry.configure(state='disabled', disabledbackground='grey', disabledforeground='white')
                current_entry.grid(row = test_row, column=table_headers.index(header_to_create), sticky = 'snew')
            else:
                if test_row < enough_tag + 1:
                    color = 'green'
                    current_entry.insert(0, list(enough_cards[header_to_create])[test_row - 1])
                if test_row > enough_tag and test_row < not_enough_tag + enough_tag + 1:
                    color = 'yellow'
                    current_entry.insert(0, list(not_enough_cards[header_to_create])[test_row - enough_tag - 1])
                if test_row > not_enough_tag + enough_tag:
                    color = 'white'
                    if header_to_create =='Name':
                        current_entry.insert(0, list(cards_not_in_collection['Name'])[test_row - enough_tag - not_enough_tag])
                    if header_to_create == 'Decklist Quantity':
                        current_entry.insert(0, list(cards_not_in_collection['Quantity'])[test_row - enough_tag - not_enough_tag])
                    if header_to_create == "Collection Quantity":
                        current_entry.insert(0, '0')
                current_entry.configure(state='disabled', disabledbackground=color, disabledforeground='black')
                current_entry.grid(row = test_row, column=table_headers.index(header_to_create), sticky = 'snew')
                    

    # container.grid(sticky='nsew')
    # # canvas.grid(row = 1, columns = 1, sticky='nsew')
    # canvas.grid()
    # canvas.bind("<Configure>", resize_frame)
    # vscrollbar.grid(row=0, column=0, sticky = 'nse')


my_btn = Button(root, text = "Open", command = decklist_load).grid(row = 0, column=0, sticky='n')

# # height = 5 
# # width = 5
# # for i in range(100):
# #     if i < 3:
# #         color = 'red'
# #     else:
# #         color = 'white'
# #     for j in range(4):
# #         b = Label(root, text = "test", bg = color)
# #         b.grid(row = i + 1, column=j)

# # scrollbar = Scrollbar(root, orient = "vertical")

# ## Create a table to populate with the 

# ## Check boxes ##
# # root.title("Image viewer")
# # root.geometry("400x400")

# # var = StringVar()

# # c = Checkbutton(root, text = "Check this", variable=var, onvalue = "On", offvalue='Off')
# # c.deselect()
# # c.pack()

# # # myLabel = Label(root, text = var.get()).pack()

# # def show():
# #     myLabel = Label(root, text = var.get()).pack()

# # myButton = Button(root, text = "show", command = show).pack()

root.mainloop()