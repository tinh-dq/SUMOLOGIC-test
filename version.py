import data
import customtkinter as ctk


class VersionScreen:
    def __init__(self, master):
        self.frame_content = ctk.CTkFrame(master)
        self.frame_content.grid(row=0, column=0, stick='nswe')
        for _ in range(4):
            self.frame_content.grid_rowconfigure(_, minsize=32)
        self.frame_content.grid_columnconfigure(1, minsize=100)
        self.frame_content.grid_columnconfigure(2, weight=1)
        self.frame_content.grid_rowconfigure(5, weight=1)
        self.frame_content.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.frame_content, text="Report time:").grid(row=0, column=0, sticky='w')
        self.report_time_entry = ctk.CTkEntry(self.frame_content)
        self.report_time_entry.insert(0, data.inp['report_time'])
        self.report_time_entry.grid(row=0, column=1, sticky='we')

        ctk.CTkLabel(self.frame_content, text="Install time:").grid(row=1, column=0, sticky='e')
        self.install_time_start = ctk.CTkEntry(self.frame_content)
        self.install_time_start.insert(0, data.inp['install_time'][0])
        self.install_time_start.grid(row=1, column=1, sticky='we')
        self.install_time_end = ctk.CTkEntry(self.frame_content)
        self.install_time_end.insert(0, data.inp['install_time'][1])
        self.install_time_end.grid(row=1, column=2, sticky='w', padx=5)

        ctk.CTkLabel(self.frame_content, text="ACT test time:").grid(row=2, column=0, sticky='e')
        self.test_time_start = ctk.CTkEntry(self.frame_content)
        self.test_time_start.insert(0, data.inp['test_time'][0])
        self.test_time_start.grid(row=2, column=1, sticky='we')
        self.test_time_end = ctk.CTkEntry(self.frame_content)
        self.test_time_end.insert(0, data.inp['test_time'][1])
        self.test_time_end.grid(row=2, column=2, sticky='w', padx=5)

        ctk.CTkLabel(self.frame_content, text="Binary:").grid(row=3, column=0, sticky='e')
        self.binary_version = ctk.CTkEntry(self.frame_content)
        self.binary_version.insert(0, data.inp['binary'][1])
        self.binary_version.grid(row=3, column=1, sticky='we')
        self.binary_link = ctk.CTkEntry(self.frame_content)
        self.binary_link.insert(0, data.inp['binary'][0])
        self.binary_link.grid(row=3, column=2, sticky='we', padx=5)

        ctk.CTkLabel(self.frame_content, text="user-id:").grid(row=4, column=0, sticky='e')
        self.user_id = ctk.CTkEntry(self.frame_content)
        self.user_id.insert(0, data.inp['user_id'])
        self.user_id.grid(row=4, column=1, sticky='we')

        self.frame_market = ctk.CTkFrame(self.frame_content)
        self.frame_market.grid(row=5, column=0, columnspan=3, sticky='nswe', padx=5, pady=5)
        self.frame_sqe = ctk.CTkFrame(self.frame_content)
        self.frame_sqe.grid(row=6, column=0, columnspan=3, sticky='nswe', padx=5, pady=5)

        ctk.CTkButton(self.frame_content, text='Save', command=self.save_version).grid(row=7, column=0, columnspan=3)

        # frame_market
        self.frame_market.grid_columnconfigure(2, weight=1)
        ctk.CTkLabel(self.frame_market, text="Market version").grid(row=0, column=0, columnspan=3, sticky='nswe')
        ctk.CTkLabel(self.frame_market, text="service-id").grid(row=1, column=0)
        ctk.CTkLabel(self.frame_market, text="Client").grid(row=2, column=0)
        ctk.CTkLabel(self.frame_market, text="Wakeup").grid(row=3, column=0)
        ctk.CTkLabel(self.frame_market, text="Dictation").grid(row=4, column=0)

        self.service_id_market = ctk.CTkEntry(self.frame_market)
        self.service_id_market.insert(0, data.inp['market']['service_id'])
        self.service_id_market.grid(row=1, column=1, columnspan=2, sticky='we')

        self.client_market_version = ctk.CTkEntry(self.frame_market)
        self.client_market_version.insert(0, data.inp['market']['client'][0])
        self.client_market_version.grid(row=2, column=1, sticky='we')
        self.client_market_link = ctk.CTkEntry(self.frame_market)
        self.client_market_link.insert(0, data.inp['market']['client'][1])
        self.client_market_link.grid(row=2, column=2, sticky='nswe')

        self.wakeup_market_version = ctk.CTkEntry(self.frame_market)
        self.wakeup_market_version.insert(0, data.inp['market']['wakeup'][0])
        self.wakeup_market_version.grid(row=3, column=1, sticky='we')
        self.wakeup_market_link = ctk.CTkEntry(self.frame_market)
        self.wakeup_market_link.insert(0, data.inp['market']['wakeup'][1])
        self.wakeup_market_link.grid(row=3, column=2, sticky='nswe')

        self.dictation_market_version = ctk.CTkEntry(self.frame_market)
        self.dictation_market_version.insert(0, data.inp['market']['dictation'][0])
        self.dictation_market_version.grid(row=4, column=1, sticky='we')
        self.dictation_market_link = ctk.CTkEntry(self.frame_market)
        self.dictation_market_link.insert(0, data.inp['market']['dictation'][1])
        self.dictation_market_link.grid(row=4, column=2, sticky='nswe')

        # frame_sqe
        self.frame_sqe.grid_columnconfigure(2, weight=1)
        ctk.CTkLabel(self.frame_sqe, text="SQE version").grid(row=0, column=0, columnspan=3, sticky='nswe')
        ctk.CTkLabel(self.frame_sqe, text="service-id").grid(row=1, column=0)
        ctk.CTkLabel(self.frame_sqe, text="Client").grid(row=2, column=0)
        ctk.CTkLabel(self.frame_sqe, text="Wakeup").grid(row=3, column=0)
        ctk.CTkLabel(self.frame_sqe, text="Dictation").grid(row=4, column=0)

        self.service_id_sqe = ctk.CTkEntry(self.frame_sqe)
        self.service_id_sqe.insert(0, data.inp['sqe']['service_id'])
        self.service_id_sqe.grid(row=1, column=1, columnspan=2, sticky='we')

        self.client_sqe_version = ctk.CTkEntry(self.frame_sqe)
        self.client_sqe_version.insert(0, data.inp['sqe']['client'][0])
        self.client_sqe_version.grid(row=2, column=1, sticky='we')
        self.client_sqe_link = ctk.CTkEntry(self.frame_sqe)
        self.client_sqe_link.insert(0, data.inp['sqe']['client'][1])
        self.client_sqe_link.grid(row=2, column=2, sticky='nswe')

        self.wakeup_sqe_version = ctk.CTkEntry(self.frame_sqe)
        self.wakeup_sqe_version.insert(0, data.inp['sqe']['wakeup'][0])
        self.wakeup_sqe_version.grid(row=3, column=1, sticky='we')
        self.wakeup_sqe_link = ctk.CTkEntry(self.frame_sqe)
        self.wakeup_sqe_link.insert(0, data.inp['sqe']['wakeup'][1])
        self.wakeup_sqe_link.grid(row=3, column=2, sticky='nswe')

        self.dictation_sqe_version = ctk.CTkEntry(self.frame_sqe)
        self.dictation_sqe_version.insert(0, data.inp['sqe']['dictation'][0])
        self.dictation_sqe_version.grid(row=4, column=1, sticky='we')
        self.dictation_sqe_link = ctk.CTkEntry(self.frame_sqe)
        self.dictation_sqe_link.insert(0, data.inp['sqe']['dictation'][1])
        self.dictation_sqe_link.grid(row=4, column=2, sticky='nswe')

    def save_version(self):
        _inp = {
            "user_id": self.user_id.get(),
            "install_time": [
                self.install_time_start.get(),
                self.install_time_end.get()
            ],
            "test_time": [
                self.test_time_start.get(),
                self.test_time_end.get()
            ],
            "report_time": self.report_time_entry.get(),
            "model": self.binary_version.get()[0:5],
            "binary": [
                self.binary_link.get(),
                self.binary_version.get()
            ],
            "market": {
                "service_id": self.service_id_market.get(),
                "client": [
                    self.client_market_version.get(),
                    self.client_market_link.get()
                ],
                "wakeup": [
                    self.wakeup_market_version.get(),
                    self.wakeup_market_link.get()
                ],
                "dictation": [
                    self.dictation_market_version.get(),
                    self.dictation_market_link.get()
                ]
            },
            "sqe": {
                "service_id": self.service_id_sqe.get(),
                "client": [
                    self.client_sqe_version.get(),
                    self.client_sqe_link.get()
                ],
                "wakeup": [
                    self.wakeup_sqe_version.get(),
                    self.wakeup_sqe_link.get()
                ],
                "dictation": [
                    self.dictation_sqe_version.get(),
                    self.dictation_sqe_link.get()
                ]
            }
        }
        # print(_inp)
        data.writeInputData(_inp)
        data.reloadInputData()


if __name__ == "__main__":
    window = ctk.CTk()
    window.title('Bixby SUMOLOGIC')
    window.geometry('390x320')
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    content = VersionScreen(window)
    window.mainloop()
