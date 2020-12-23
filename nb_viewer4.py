"""
Allow the preview of a python notebook.
"""
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import json
from tkinter import messagebox

class Window(Frame):

    def __init__(self, master=None):
        
        Frame.__init__(self, master)                  
        self.master = master
        self.init_window()

    
    def init_window(self):
        
        self.master.title("Notebook")
        self.grid(column=0,row=0)
        self.createMenu()
        self.createButons() 
        self.a()
        
    def createMenu(self):
        
        menu = Menu(self.master)
        self.master.config(menu=menu)
        fileMenu = Menu(menu)        
        fileMenu.add_command(label="Exit", command=self.exit_func)
        menu.add_cascade(label="File", menu=fileMenu)
        editMenu = Menu(menu) 
        editMenu.add_command(label="Undo") 
        menu.add_cascade(label="Edit", menu=editMenu)

    def createButons(self):
        
        quitButton = Button(self, text="Exit",command=self.exit_func) 
        quitButton.grid(row=1,column=3,sticky=W+E+N+S)
        openButton = Button(self, text="Open",command=self.open_func) 
        openButton.grid(row=1,column=0,sticky=W+E+N+S)
        saveButton = Button(self, text="Save",command=self.save_as_func) 
        saveButton.grid(row=1,column=1,sticky=W+E+N+S)
        saveAsButton = Button(self, text="Save as",command=self.exit_func) 
        saveAsButton.grid(row=1,column=2,sticky=W+E+N+S)
        
    def save_as_func(self):
        
        temp=[elem.get(1.0, END) for elem in self.texts]
        temp="".join(temp)
        fN=filedialog.asksaveasfilename(initialdir = "./",
                                                title = "Select file",
                                                filetypes = (("Pythonfiles",
                                                              "*.py"),
                                                             ("all files","*.*")))
        
        aFile=open(fN,'w')
        print(temp)
        aFile.write(temp)
        aFile.close()

    def createTextArea(self):
        
        self.txt = scrolledtext.ScrolledText(self,width=80,height=30)
        self.txt.grid(columnspan=6, sticky=E)

    
    def exit_func(self):
        exit()

    def open_func(self):
        myFile = filedialog.askopenfilename(filetypes = (("Notebooks","*.ipynb"),
                                                 ("all files","*.*")))
        codeOnly=messagebox.askyesno("","Display only codes?") 
        
        with open(myFile) as handle:
            self.d = json.loads(handle.read())

        canvas = Canvas(self,width=780,height=480)
        scroll_y = Scrollbar(self, orient="vertical", command=canvas.yview)

        frame = Frame(canvas,width=760,height=460)
        self.texts=[]
        
        for ind,elem in enumerate(self.d['cells']):            
            if (not codeOnly) or elem['cell_type']=='code':            
                self.texts.append(scrolledtext.ScrolledText(frame,
                                                            width=140,
                                                            height=4))
                self.texts[-1].grid(columnspan=4, sticky=E)
                for ind2, elem2 in enumerate(elem['source']):                    
                        self.texts[-1].insert(INSERT, elem2)
                     
        # put the frame in the canvas        
        canvas.create_window(0, 0, anchor='nw', window=frame)
        
        # make sure everything is displayed  
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox('all'), 
                         yscrollcommand=scroll_y.set)
                         
        canvas.grid(column=0,row=2,columnspan=4,rowspan=5, sticky=EW)
         
        scroll_y.grid(column=5, row=2,rowspan=5,sticky=NS)


        
    def a(self):
        pass
        

        

root = Tk()
root.geometry("800x500") 
app = Window(root) 
root.mainloop()  

