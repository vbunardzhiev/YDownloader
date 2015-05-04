import tkinter, os, pafy
from tkinter import ACTIVE,filedialog
from tkinter.messagebox import askokcancel


class Application(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.option_add('*Font', 'courier 12')
        self.option_add('*Background', 'light blue')
        self.configure(bg='light blue')
        self.playlists_list = []
        self.url_var =  tkinter.StringVar()
        self.path_var =  tkinter.StringVar()
        self.encode_to_mp3 = tkinter.IntVar()
        self.create_widgets()
        
    def create_widgets(self):
        self.path_entry = tkinter.Entry(self,
                                   textvariable=self.path_var,
                                   width=30)
        self.path_entry.place(relx=1, x=-301, y=24, anchor='ne')

        self.url_entry = tkinter.Entry(self,
                                   textvariable=self.url_var,
                                   width=30)
        self.url_entry.place(relx=1, x=-301, y=70, anchor='ne')

        self.dir_button = tkinter.Button(self, text='dir')
        self.dir_button['command'] = lambda: self.load_path()
        self.dir_button.place(relx=1, x=-560, y=91, anchor='ne')

        self.sync_button = tkinter.Button(self, text='add to synclist')
        self.sync_button['command'] = lambda: self.add_to_sync_list()
        self.sync_button.place(relx=1, x=-300, y=91, anchor='ne')

        self.path_text = tkinter.Label(self, text='dir to download')
        self.path_text.place(relx=1, x=-375, y=0, anchor='ne')

        self.url_text = tkinter.Label(self, text='playlist url')
        self.url_text.place(relx=1, x=-390, y=46, anchor='ne')
        
        self.encode = tkinter.Checkbutton(self,
                                          text="to mp3",
                                          variable=self.encode_to_mp3)
        self.encode.place(relx=1 ,x=-469, y=92, anchor='ne')

        self.info_list = tkinter.Listbox(self)
        self.info_list.config(width=29, activestyle='none', relief='flat')
        self.info_list.config(height=6,
                              bd=5,
                              highlightthickness=0)
        self.info_list.place(relx=1, x=-301, y=123, anchor='ne')


def main():
    root = tkinter.Tk()
    root.title("tubesync")
    root.geometry('305x250')
    root.resizable(width='false', height='false')
    app = Application(root)
    app.pack()
    app.place(bordermode='outside', height=500, width=605)
    root.mainloop()

if __name__ == '__main__':

    main()