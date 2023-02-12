import mysql.connector
import tkinter
import customtkinter

customtkinter.set_appearance_mode("Dark")
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

        self.cursor.execute("SELECT uprawnienia FROM users WHERE login=%s AND pass=%s", (login, password))
        result = self.cursor.fetchone()

        if result:
            print("Zalogowano")
            print(result)
            login_window.spawn_main_window()

            if 2 in result:
                login_window.spawn_admin_window()

            

        else:
            login_window.login_error_label.pack(pady=10, padx=10)
            
    def bigUpgrade(self):
        target = login_window.admin_window.BigUpgradeEntry.get()
        self.cursor.execute("SELECT uprawnienia FROM users WHERE login =%s AND login=%s", (target, target))
        result = self.cursor.fetchone()
        if 2 in result:
            print("Error, can't downgrade the SuperAdmin")
        else:
            self.cursor.execute("UPDATE users SET uprawnienia = '1' WHERE login=%s AND login=%s", (target, target))
            self.connection.commit()

    def bigDowngrade(self):
        target = login_window.admin_window.BigDowngradeEntry.get()
        self.cursor.execute("SELECT uprawnienia FROM users WHERE login =%s AND login=%s", (target, target))
        result = self.cursor.fetchone()
        if 2 in result:
            print("Error, can't downgrade the SuperAdmin")
        else:
            self.cursor.execute("UPDATE users SET uprawnienia = '0' WHERE login=%s AND login=%s", (target, target))
            self.connection.commit()

    def stankyLeg(self):
        self.cursor.execute("UPDATE users SET uprawnienia = '0' WHERE uprawnienia='2'")

        target = login_window.admin_window.TransferSuperUserEntry.get()
        self.cursor.execute("UPDATE users SET uprawnienia = '2' WHERE login=%s AND login=%s", (target, target))
        self.connection.commit()

    def fetchStudioName(self):
        self.cursor.execute("SELECT * FROM config")
        result = self.cursor.fetchone()
        string_result = str(result)
        trimmed_result = string_result.replace("(", "")
        trimmed_result = trimmed_result.replace(")", "")
        trimmed_result = trimmed_result.replace("'", "")
        trimmed_result = trimmed_result.replace(",", "")
        trimmed_result = trimmed_result.replace("0", "")
        return trimmed_result

    def studioRename(self):
        target = login_window.main_window.StudioRenameEntry.get()
        self.cursor.execute("UPDATE config SET nazwaStudia=%s WHERE id=%s", (target, "0"))
        self.connection.commit()

class Interface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Logowanie")
        self.geometry("500x340")
        self.mainframe = customtkinter.CTkFrame(master=self)
        self.mainframe.pack(pady=20, padx=60, fill="both", expand=True)

        self.login_label = customtkinter.CTkLabel(master=self.mainframe, text="Podaj login i hasło", font=("Arial", 12))
        self.login_label.pack(pady=10, padx=10)

        self.login_entry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="login")
        self.login_entry.pack(pady=3, padx=10)

        self.password_entry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="hasło", show="*")
        self.password_entry.pack(pady=3, padx=10)

        self.login_button = customtkinter.CTkButton(master=self.mainframe, text="Zaloguj", command=conn.login)
        self.login_button.pack(pady=3, padx=10)

        self.register_button = customtkinter.CTkButton(master=self.mainframe, text="Zarejestruj", command=conn.register)
        self.register_button.pack(pady=3, padx=10)

        self.login_error_label = customtkinter.CTkLabel(master=self.mainframe, text="Błędny login lub hasło", font=("Arial", 12))
        

    def spawn_main_window(self):
        self.main_window = Main_Window(self)

    def spawn_admin_window(self):
        self.admin_window = Admin_Window(self)


class Main_Window(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(conn.fetchStudioName())
        self.geometry("800x400")
        self.mainframe = customtkinter.CTkFrame(master=self)
        self.mainframe.pack(pady=20, padx=60, fill="both", expand=True)

        self.username = login_window.login_entry.get()
        self.WelcomeMessage = "Witaj " + self.username
        self.WelcomeMessageLabel = customtkinter.CTkLabel(master=self.mainframe, text=self.WelcomeMessage, font=("Arial", 16))
        self.WelcomeMessageLabel.pack(pady=10, padx=10)

        self.fetchedName = conn.fetchStudioName()
        self.studioName = customtkinter.CTkLabel(master=self.mainframe, text=self.fetchedName, font=("Arial", 24))
        self.studioName.pack(pady=10, padx=10)

        self.StudioRenameLabel = customtkinter.CTkLabel(master=self.mainframe, text="Zmień nazwę studia", font=("Arial", 12))
        self.StudioRenameLabel.pack(pady=10, padx=10)
        self.StudioRenameEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="nowa nazwa")
        self.StudioRenameEntry.pack(pady=3, padx=10)
        self.StudioRenameButton = customtkinter.CTkButton(master=self.mainframe, text="Zmień", command=conn.studioRename)
        self.StudioRenameButton.pack(pady=3, padx=10)


class Admin_Window(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Administracja")
        self.geometry("800x400")
        self.mainframe = customtkinter.CTkFrame(master=self)
        self.mainframe.pack(pady=20, padx=60, fill="both", expand=True)

        self.BigUpgradeLabel = customtkinter.CTkLabel(master=self.mainframe, text="Podnieś uprawnienia użytkownika do Admin", font=("Arial", 12))
        self.BigUpgradeLabel.pack(pady=10, padx=10)
        self.BigUpgradeEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="nazwa użytkownika")
        self.BigUpgradeEntry.pack(pady=3, padx=10)
        self.BigUpgradeButton = customtkinter.CTkButton(master=self.mainframe, text="Podnieś", command=conn.bigUpgrade)
        self.BigUpgradeButton.pack(pady=3, padx=10)

        self.BigDowngradeLabel = customtkinter.CTkLabel(master=self.mainframe, text="Obniż uprawnienia użytkownika do User", font=("Arial", 12))
        self.BigDowngradeLabel.pack(pady=10, padx=10)
        self.BigDowngradeEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="nazwa użytkownika")
        self.BigDowngradeEntry.pack(pady=3, padx=10)
        self.BigDowngradeButton = customtkinter.CTkButton(master=self.mainframe, text="Obniż", command=conn.bigDowngrade)
        self.BigDowngradeButton.pack(pady=3, padx=10)

        self.TransferSuperUserLabel = customtkinter.CTkLabel(master=self.mainframe, text="Przekaż uprawnienia SuperAdmin", font=("Arial", 12))
        self.TransferSuperUserLabel.pack(pady=10, padx=10)
        self.TransferSuperUserEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="nazwa użytkownika")
        self.TransferSuperUserEntry.pack(pady=3, padx=10)
        self.TransferSuperUserButton = customtkinter.CTkButton(master=self.mainframe, text="Przekaż", command=conn.stankyLeg)
        self.TransferSuperUserButton.pack(pady=3, padx=10)



conn = MySQLConnection('192.166.219.220', '3306', 'niewiadoma', 'niewiadoma', 'Niewiadoma2244;')
conn.connect()

login_window = Interface()
login_window.mainloop()

conn.close()
