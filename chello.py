import mysql.connector
import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

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

    def register(self):
        login = login_window.login_entry.get()
        password = login_window.password_entry.get()

        self.cursor.execute("SELECT * FROM users WHERE uprawnienia = \"2\" ")
        result = self.cursor.fetchall
        if self.cursor.rowcount==0:
            uprawnienia = "2"
        else:
            uprawnienia = "0"
        sql = "INSERT INTO users (login, pass, uprawnienia, avatar, jezykUzytkownika, rodzajSkorkiInterfejsu, portfel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (login, password, uprawnienia, "0", "0", "0", "0")
        self.cursor.execute(sql, val)
        self.connection.commit()
        print("Dodano uzytkownika")


    def login(self):
        login = login_window.login_entry.get()
        password = login_window.password_entry.get()

        self.cursor.execute("SELECT * FROM users WHERE login=%s AND pass=%s", (login, password))
        result = self.cursor.fetchone()

        if result:
            print("Zalogowano")
            login_window.spawn_main_window()
            login_window.withdraw()
        else:
            login_window.login_error_textbox.configure(text_color="black")
            pass



class Interface(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x240")
        self.mainframe= customtkinter.CTkFrame(self, fg_color="#ADD8E6")
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.login_textbox = customtkinter.CTkTextbox(self, fg_color="#ADD8E6")
        self.login_textbox.grid(row=0, column=0)
        self.login_textbox.insert("0.0", "Podaj login i hasło")
        self.login_textbox.configure(state="disabled")
        self.login_textbox.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        self.login_error_textbox = customtkinter.CTkTextbox(self, fg_color="#ADD8E6")
        self.login_error_textbox.grid(row=0, column=0)
        self.login_error_textbox.insert("0.0", "Błędny login lub hasło")
        self.login_error_textbox.configure(state="disabled", text_color="#ADD8E6")
        self.login_error_textbox.place(relx=0.5, rely=1.2, anchor=customtkinter.CENTER)

        self.login_entry = customtkinter.CTkEntry(master=self, placeholder_text="login")
        self.login_entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        self.password_entry = customtkinter.CTkEntry(master=self, placeholder_text="hasło", text_color="White")
        self.password_entry.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

        self.button = customtkinter.CTkButton(master=self, text="Zaloguj", command=conn.login)
        self.button.place(relx=0.5, rely=0.525, anchor=customtkinter.CENTER)

        self.button = customtkinter.CTkButton(master=self, text="Zarejestruj", command=conn.register)
        self.button.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)

    def spawn_main_window(self):
        main_window = Main_Window(self)

class Main_Window(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("800x400")
        self.mainframe= customtkinter.CTkFrame(self, fg_color="#ADD8E6")
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


conn = MySQLConnection('192.166.219.220', '3306', 'niewiadoma', 'niewiadoma', 'Niewiadoma2244;')
conn.connect()

login_window = Interface()
login_window.mainloop()

conn.close()
