import customtkinter

class CustomFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title = title
        self.create_label(title)

    def create_label(self, text):
        self.label = customtkinter.CTkLabel(self, text=text, font=("Arial", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="w")

class InputFrame(CustomFrame):
    def __init__(self, master, title, label_text):
        super().__init__(master, title)
        self.entry_label = customtkinter.CTkLabel(self, text=label_text)
        self.entry_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")
        self.entry = customtkinter.CTkEntry(self)
        self.entry.grid(row=1, column=1, padx=10, pady=(5, 0), sticky="w")

    def get_value(self):
        return self.entry.get()

class DoubleInputFrame(CustomFrame):
    def __init__(self, master, title, label_text1, label_text2):
        super().__init__(master, title)
        
        self.entry_label1 = customtkinter.CTkLabel(self, text=label_text1)
        self.entry_label1.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")
        self.entry1 = customtkinter.CTkEntry(self)
        self.entry1.grid(row=1, column=1, padx=10, pady=(5, 0), sticky="w")

        self.entry_label2 = customtkinter.CTkLabel(self, text=label_text2)
        self.entry_label2.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="w")
        self.entry2 = customtkinter.CTkEntry(self)
        self.entry2.grid(row=2, column=1, padx=10, pady=(5, 0), sticky="w")

    def get_values(self):
        return self.entry1.get(), self.entry2.get()

class ValuePrinterFrame(CustomFrame):
    def __init__(self,master,title):
        super().__init__(master,title)
        
        self.output_label = customtkinter.CTkLabel(app, text="Value will appear here")
        self.output_label.pack(pady=20)
        
