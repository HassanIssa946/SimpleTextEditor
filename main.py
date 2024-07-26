import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, messagebox, filedialog
import os
GUI = tk.Tk()
GUI.title("MY EDITOR")
GUI.geometry("700x700")

### MAIN MENU ##############################################
main_menu = tk.Menu()
#INSERTING IMAGES FOR THE MENU
#FILE
file = tk.Menu(main_menu,tearoff=False)
new_icon = tk.PhotoImage(file="icons/new.png")
open_icon = tk.PhotoImage(file="icons/open.png")
save_icon = tk.PhotoImage(file="icons/save.png")
save_as_icon = tk.PhotoImage(file="icons/save_as.png")
exit_icon = tk.PhotoImage(file="icons/exit.png")

#EDIT
edit = tk.Menu(main_menu,tearoff=False)
copy_icon = tk.PhotoImage(file="icons/copy.png")
paste_icon = tk.PhotoImage(file="icons/paste.png")
cut_icon = tk.PhotoImage(file="icons/cut.png")
find_icon = tk.PhotoImage(file="icons/find.png")

#VIEW
view = tk.Menu(main_menu,tearoff=False)
tool_bar_icon = tk.PhotoImage(file="icons/tool_bar.png")
status_bar_icon = tk.PhotoImage(file="icons/status_bar.png")

#Add cascades to each menu item 
main_menu.add_cascade(label="Files",menu=file)
main_menu.add_cascade(label="Edit",menu=edit)
main_menu.add_cascade(label="View",menu=view)
###################################################################
# TOOLBAR #########################################################
tool_bar = ttk.Label(GUI)
tool_bar.pack(side=tk.TOP,fill=tk.X)

#size box
size_var = tk.IntVar()
size_combo = ttk.Combobox(tool_bar,width=15,textvariable=size_var,state="readonly")
size_combo['values'] = tuple(range(5,50,3))
size_combo.grid(row=0,column=1,padx=4)
size_combo.current(3)

#now creating all the buttons
bold_icon = tk.PhotoImage(file='icons/bold.png')
bold_button = ttk.Button(tool_bar,image=bold_icon)
bold_button.grid(row=0,column=2,padx=4)

italic_icon = tk.PhotoImage(file='icons/italic.png')
italic_button = ttk.Button(tool_bar,image=italic_icon)
italic_button.grid(row=0,column=3,padx=4)

underline_icon = tk.PhotoImage(file='icons/underline.png')
underline_button = ttk.Button(tool_bar,image=underline_icon)
underline_button.grid(row=0,column=4,padx=4)

font_color_icon = tk.PhotoImage(file='icons/font_color.png')
font_color_button = ttk.Button(tool_bar,image=font_color_icon)
font_color_button.grid(row=0,column=5,padx=4)
################################################################
#Text Editor ###################################################

#Text Editor
text_editor = tk.Text(GUI)
text_editor.config(wrap='word',relief=tk.FLAT)
text_editor.focus_set()

scroll_bar = tk.Scrollbar(GUI)
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

#font functionalities 

current_font_size = 12
def change_size(GUI):
    global current_font_size
    current_font_size=size_var.get()
    text_editor.configure(font=("Arial",current_font_size))
size_combo.bind('<<ComboboxSelected>>',change_size)    

#buttons functionality
def change_bold():
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal':
        text_editor.configure(font=("Arial", current_font_size, 'bold'))
    if text_property.actual()['weight'] == 'bold':
        text_editor.configure(font=("Arial", current_font_size, 'normal'))
bold_button.configure(command=change_bold)

#italic functionality
def change_italic():
    italic = tk.font.Font(font=text_editor['font'])
    if italic.actual()['slant']=='roman':
        text_editor.configure(font=("Arial", current_font_size, 'italic'))
    if italic.actual()['slant']=='italic':
        text_editor.configure(font=("Arial", current_font_size, 'roman'))
italic_button.configure(command=change_italic)

#underline functionality
def change_underline():
    underline = tk.font.Font(font=text_editor['font'])
    if underline.actual()['underline'] == 0:
        text_editor.configure(font=("Arial", current_font_size, 'underline'))
    if underline.actual()['underline'] == 1:
        text_editor.configure(font=("Arial", current_font_size, 'normal'))
underline_button.configure(command=change_underline)

#color functionality
def color_change():
    color = tk.colorchooser.askcolor()
    text_editor.configure(fg=color[1])
font_color_button.configure(command=color_change)
#End of Text editor##############################################
#Status bar######################################################
status_bar = ttk.Label(GUI, text="Status Bar")
status_bar.pack(side=tk.BOTTOM)

text_changed = False
def changed(event=None):
    global text_changed
    if text_editor.edit_modified():
        text_changed = True
        words = len(text_editor.get(1.0,'end-1c').split())
        characters = len(text_editor.get(1.0,'end-1c')) 
        status_bar.config(text=f"Characters:{characters}  Words : {words} ")
    text_editor.edit_modified(False)

text_editor.bind('<<Modified>>',changed)
#End of status bar####################################################
url = '' 

#new functionality
def new_file(event=None):
    global url
    url = ''
    text_editor.delete(1.0,tk.END)
#file new command
file.add_command(label="New",image=new_icon,compound=tk.LEFT,accelerator="Ctrl+N",command=new_file)

#open functionality
def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select File",filetypes=(("Text files","*.txt"),("All files","*.*")))
    try:
        with open(url,'r') as fr:
            text_editor.delete(1.0,tk.END)
            text_editor.insert(1.0,fr.read())
    except FileNotFoundError:
        return
    except:
        return 
    GUI.title(os.path.basename(url))
#open command
file.add_command(label="Open", image=open_icon, compound=tk.LEFT, accelerator="Ctrl+O", command=open_file)
file.add_separator()

#functionality to save a file
def save_file(event=None):
    global url
    try:
        if url:
            content=str(text_editor.get(1.0,tk.END))
            with open(url,'w',encoding='utf-8') as wf:
                wf.write(content)
        else:
            url=filedialog.asksaveasfile(mode='w',defaultextension=".txt",filetypes=(("Text files","*.txt"),("All files","*.*")))
            content=text_editor.get(1.0,tk.END)    
            url.write(content)
            url.close()
    except:
        return
#save command
file.add_command(label="Save", image=save_as_icon, compound=tk.LEFT, accelerator="Ctrl+S", command=save_file)

#save as functionality
def save_as(event=None):
    global url
    try:
        url = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=(("Text files","*.txt"), ("All files","*.*")))
        content = text_editor.get(1.0,tk.END)
        url.write(content)
        url.close()
    except:
        return
#save as command
file.add_command(label="Save As", image=save_as_icon, compound=tk.LEFT, accelerator="Ctrl+S", command=save_as)
file.add_separator()

#Exit command functionality
def exit_fun(event=None):
    global url,text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel("Warning!","Do you want to save your file?")
            if mbox:
                if url:
                    content = str(text_editor.get(1.0,tk.END))
                    with open(url,'w',encoding='utf-8') as wf:
                        wf.write(content)
                        GUI.destroy()
                else:
                    url = filedialog.asksaveasfile(mode='w',defaultextension=".txt",filetypes=(("Text files","*.txt"),("All files","*.*")))
                    content2 = text_editor.get(1.0,tk.END)    
                    url.write(content2)
                    url.close()
                    GUI.destroy()
            elif mbox is False:
                GUI.destroy()
        else:
            GUI.destroy()
    except:
        return
#exit command
file.add_command(label="Exit", image=exit_icon, compound=tk.LEFT, accelerator="Ctrl+Z", command=exit_fun)

#edit commands adding functionality
#find functionality
def find_func(event=None):
    def find():
        word = find_input.get()
        text_editor.tag_remove("match", '1.0', tk.END)
        matches = 0
        if word:
            start_pos = '1.0'
            while True:
                start_pos = text_editor.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_editor.tag_add('match', start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                text_editor.tag_config('match', foreground='red', background='yellow')
            
    def replace():
        word=find_input.get()
        replace_content=replace_input.get()
        content=text_editor.get(1.0, tk.END)
        new_content=content.replace(word, replace_content)
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, new_content)

    find_dialog=tk.Toplevel()
    find_dialog.geometry('450x250+500+200')
    find_dialog.title("Find")
    find_dialog.resizable(0, 0)

    find_frame=ttk.Labelframe(find_dialog, text="Find/Replace")
    find_frame.pack(pady=20)

    #labels
    text_find_label=ttk.Label(find_frame, text="Find: ")
    text_replace_label=ttk.Label(find_frame, text="Replace")
    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)
    #entry boxes
    find_input=ttk.Entry(find_frame, width=30)
    replace_input=ttk.Entry(find_frame, width=30)
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)
    #buttons
    find_button=ttk.Button(find_frame, text="Find", command=find)
    replace_button=ttk.Button(find_frame, text="Replace", command=replace)
    find_button.grid(row=2, column=0, padx=4, pady=4)
    replace_button.grid(row=2, column=1, padx=4, pady=4)



edit.add_command(label="Copy",image=copy_icon,compound=tk.LEFT, accelerator="Ctrl+C", command=lambda:text_editor.event_generate("<Control c>"))
edit.add_command(label="Paste",image=paste_icon,compound=tk.LEFT, accelerator="Ctrl+V", command=lambda:text_editor.event_generate("<Control v>"))
edit.add_command(label="Cut", image=cut_icon, compound=tk.LEFT, accelerator="Ctrl+X", command=lambda:text_editor.event_generate("<Control x>"))
edit.add_separator()

edit.add_command(label="Find", image=find_icon, compound=tk.LEFT, accelerator="Ctrl+F", command=find_func)

#view checkbuttons

show_toolbar = tk.BooleanVar()
show_toolbar.set(True)
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar = False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP, fill=tk.X)
        text_editor.pack(fill=tk.BOTH, expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar = True

def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar = False
    else:
        status_bar.pack(side=tk.BOTTOM)
        show_statusbar = True
 
view.add_checkbutton(label="Status Bar", onvalue=True, offvalue=False, variable=show_statusbar, image=status_bar_icon, compound=tk.LEFT,command=hide_statusbar)
view.add_checkbutton(label="Tool bar", image=tool_bar_icon, onvalue=True, offvalue=False, variable=show_toolbar, compound=tk.LEFT, command=hide_toolbar)

# ********************************************End of Main Menu Functionality*********************************
GUI.config(menu=main_menu)

#binding shortcut keys
GUI.bind('<Control-n>', new_file)
GUI.bind('<Control-o>', open_file)
GUI.bind('<Control-s>', save_file)
GUI.bind('<Control-Alt-s>', save_as)
GUI.bind('<Control-f>', find_func)
GUI.bind('<Control-q>', exit_fun)

GUI.mainloop()