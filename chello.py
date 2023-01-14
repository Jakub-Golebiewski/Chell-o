import mysql.connector
import tkinter
import customtkinter

class MySQLConnection:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                     port=self.port,
                                                     database=self.database,
                                                     user=self.user,
                                                     password=self.password)
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor(buffered=True)
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database: ", record)

                self.cursor.execute("CREATE DATABASE IF NOT EXISTS niewiadoma DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
                self.cursor.execute("USE niewiadoma")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `autor` (`idAutora` int(11) NOT NULL, `nazwaAutora` text NOT NULL, `fotkaAutora` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `config` (`nazwaPlikuLoga` text NOT NULL, `nazwaStudia` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `daneadresowe` (`idAdresu` int(11) NOT NULL, `samAdres` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `demo` (`idOknaWylaczonego` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `gatunek` (`idGatunku` int(11) NOT NULL, `nazwaGatunku` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `plyta` (`idPlyty` int(11) NOT NULL, `tytulPlyty` text NOT NULL, `dataWydania` datetime NOT NULL, `idGatunku` int(11) NOT NULL, `obrazekOkladki` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `sprzedaneplyty` (`idParagonu` int(11) NOT NULL, `idUsera` int(11) NOT NULL, `idUtworu` int(11) NOT NULL, `idPlyty` int(11) NOT NULL, `dataSprzedazy` datetime NOT NULL, `idAdresu` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `users` (`idUsera` int(16) NOT NULL, `login` varchar(16) NOT NULL, `pass` varchar(16) NOT NULL, `uprawnienia` int(16) NOT NULL, `avatar` int(16) NOT NULL, `jezykUzytkownika` int(16) NOT NULL, `rodzajSkorkiInterfejsu` int(16) NOT NULL, `portfel` varchar(16) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `utwor` (`idUtworu` int(11) NOT NULL, `nazwaUtworu` text NOT NULL, `idAutora` int(11) NOT NULL,`idGatunku` int(11) NOT NULL,`obrazek` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")




        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
            self.connection.rollback()
            self.cursor.close()
            self.connection.close()

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

def Register():
    pass

def Login():
    pass

class Interface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")

        self.geometry("400x240")
        mainframe= customtkinter.CTkFrame(self, fg_color="#ADD8E6")
        mainframe.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        login_textbox = customtkinter.CTkTextbox(self, fg_color="#ADD8E6")
        login_textbox.grid(row=0, column=0)
        login_textbox.insert("0.0", "Podaj login i hasło")
        login_textbox.configure(state="disabled")

#        login_errorbox = customtkinter.CTkTextbox(app, fg_color="#ADD8E6")
#        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
#        login_errorbox.grid(row=1, column=1)
#        login_errorbox.insert("0.0", "Błędny login i hasło, spróbuj ponownie")
#        login_errorbox.configure(state="disabled")


        login_entry = customtkinter.CTkEntry(master=self, placeholder_text="Login")
        login_entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        password_entry = customtkinter.CTkEntry(master=self, placeholder_text="Hasło", text_color="White")
        password_entry.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

        button = customtkinter.CTkButton(master=self, text="Zaloguj", command=Login)
        button.place(relx=0.5, rely=0.525, anchor=customtkinter.CENTER)

        button = customtkinter.CTkButton(master=self, text="Zarejestruj", command=Register)
        button.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)

    def spawn_main_window(self):
        main_window = customtkinter.CTkToplevel(self)
        main_window.geometry("800x400")


conn = MySQLConnection('192.166.219.220', '3306', 'niewiadoma', 'niewiadoma', 'Niewiadoma2244;')
conn.connect()

login_window = Interface()
login_window.mainloop()

conn.close()
