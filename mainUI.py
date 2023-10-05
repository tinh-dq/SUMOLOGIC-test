import customtkinter as ctk

import WikiPost
import data
import sumoApi
import version


class MainScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Light")

        self.title("Bixby Tool for AppVersionApi and ApiCallCount")
        self.geometry("1200x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.config(padx=5, pady=5)
        self.frame_left = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_left.grid(column=0, row=0, sticky="nswe")
        self.frame_right = ctk.CTkFrame(self, corner_radius=0)
        self.frame_right.grid(column=1, row=0, sticky="nswe")
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=1)

        self.version_btn = ctk.CTkButton(self.frame_left, text="Version", corner_radius=0, height=50,
                                         command=self.show_version)
        self.version_btn.grid(row=0, column=0, sticky="swe")

        self.csv_capture_btn = ctk.CTkButton(self.frame_left, text="CSV and capture", corner_radius=0, height=50,
                                             command=self.show_csv_capture)
        self.csv_capture_btn.grid(row=1, column=0, sticky="swe")

        self.wiki_btn = ctk.CTkButton(self.frame_left, text="Wiki", corner_radius=0, height=50,
                                      command=self.show_wiki)
        self.wiki_btn.grid(row=2, column=0, sticky="swe")
        self.show_version()

    def show_version(self):
        self.clear_content()
        data.reloadInputData()
        self.version_btn.configure(state="disabled")
        self.csv_capture_btn.configure(state="normal")
        self.wiki_btn.configure(state="normal")
        version.VersionScreen(self.frame_right)

    def show_csv_capture(self):
        self.version_btn.configure(state="normal")
        self.csv_capture_btn.configure(state="disabled")
        self.wiki_btn.configure(state="normal")
        self.clear_content()
        sumoApi.MainScreen(self.frame_right)

    def show_wiki(self):
        self.version_btn.configure(state="normal")
        self.csv_capture_btn.configure(state="normal")
        self.wiki_btn.configure(state="disabled")
        self.clear_content()
        WikiPost.MainScreen(self.frame_right)

    def clear_content(self):
        for widget in self.frame_right.winfo_children():
            widget.destroy()


main = MainScreen()
main.mainloop()
