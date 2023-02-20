import mysql.connector
import tkinter
import customtkinter
from datetime import datetime
import os

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
            log.write(str(datetime.now()))
            log.write("\n")
            log.write("Connecting to database\n")
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
                log.write("Connected to database\n")

                log.write("Checking if database exists and rebuilding\n")
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
                log.write("Success\n")

        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
            log.write("Error while connecting to database\n")
            log.write(str(e))
            log.write("\n")
            self.connection.rollback()
            self.cursor.close()
            self.connection.close()
            log.close()
            language_file.close()

    def close(self):
        log.write("Closing connection to database\n")
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            log.close()
            language_file.close()

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
        log.write("Added new user\n")

    def login(self):
        login = login_window.login_entry.get()
        password = login_window.password_entry.get()

        self.cursor.execute("SELECT uprawnienia FROM users WHERE login=%s AND pass=%s", (login, password))
        result = self.cursor.fetchone()

        if result:
            log.write("User logged in\n")
            login_window.spawn_main_window()

            if 2 in result:
                login_window.spawn_admin_window()

            

        else:
            log.write("User failed to log in\n")
            login_window.login_error_label.pack(pady=10, padx=10)
            
    def bigUpgrade(self):
        target = login_window.admin_window.BigUpgradeEntry.get()
        self.cursor.execute("SELECT uprawnienia FROM users WHERE login =%s AND login=%s", (target, target))
        result = self.cursor.fetchone()
        if 2 in result:
            print("Error, can't downgrade the SuperAdmin\n")
        else:
            self.cursor.execute("UPDATE users SET uprawnienia = '1' WHERE login=%s AND login=%s", (target, target))
            self.connection.commit()
            log.write("A user has been upgraded to Admin\n")

    def bigDowngrade(self):
        target = login_window.admin_window.BigDowngradeEntry.get()
        self.cursor.execute("SELECT uprawnienia FROM users WHERE login =%s AND login=%s", (target, target))
        result = self.cursor.fetchone()
        if 2 in result:
            print("Error, can't downgrade the SuperAdmin\n")
        else:
            self.cursor.execute("UPDATE users SET uprawnienia = '0' WHERE login=%s AND login=%s", (target, target))
            self.connection.commit()
            log.write("A user has been downgraded to User\n")

    def stankyLeg(self):
        self.cursor.execute("UPDATE users SET uprawnienia = '0' WHERE uprawnienia='2'")

        target = login_window.admin_window.TransferSuperUserEntry.get()
        self.cursor.execute("UPDATE users SET uprawnienia = '2' WHERE login=%s AND login=%s", (target, target))
        self.connection.commit()
        log.write("SuperAdmin has been trasnfered\n")

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
        log.write("Studio name changed\n")

    def addTrack(self):
        name = login_window.main_window.AddTrackNameEntry.get()
        author = login_window.main_window.AddTrackAuthorEntry.get()
        record = login_window.main_window.AddTrackRecordEntry.get()

        self.cursor.execute("SELECT * FROM autor WHERE nazwaAutora='"+author+"'")
        if self.cursor.rowcount == 0:
            self.cursor.execute("INSERT INTO autor(nazwaAutora) values ('"+author+"')")
            self.cursor.execute("SELECT idAutora FROM autor WHERE nazwaAutora='"+author+"'")
            idauthor = self.cursor.fetchone()
        else:
            self.cursor.execute("SELECT idAutora FROM autor WHERE nazwaAutora='"+author+"'")
            idauthor = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM plyta WHERE tytulPlyty='"+record+"'")
        if self.cursor.rowcount == 0:
            self.cursor.execute("INSERT INTO plyta(tytulPlyty) values ('"+record+"') ")
            self.cursor.execute("SELECT idPlyty FROM plyta WHERE tytulPlyty='"+record+"'")
            idrecord = self.cursor.fetchone()
        else:
            self.cursor.execute("SELECT idPlyty FROM plyta WHERE tytulPlyty='"+record+"'")
            idrecord = self.cursor.fetchone()
        int_record = idrecord[0]
        int_author = idauthor[0]
        int_record = str(int_record)
        int_author = str(int_author)
        self.cursor.execute("INSERT INTO utwor (Nazwa, Autor, idPlyta) values ('"+name+"', '"+int_author+"', '"+int_record+"')")
        self.connection.commit()
        log.write("Track added\n")

    def removeTrack(self):
        name = login_window.main_window.AddTrackNameEntry.get()

        self.cursor.execute("DELETE from utwor WHERE Nazwa='"+name+"'")
        self.connection.commit()
        log.write("Track removed\n")

    def assignArtist(self):
        artist = login_window.main_window.AssignArtistEntryAuthor.get()
        record = login_window.main_window.AssignArtistEntryRecord.get()
        self.cursor.execute("SELECT * FROM autor WHERE nazwaAutora='" + artist + "'")
        if self.cursor.rowcount == 0:
            self.cursor.execute("INSERT INTO autor(nazwaAutora) values ('"+artist+"')")
            self.cursor.execute("SELECT idAutora FROM autor WHERE nazwaAutora='" + artist + "'")
            idartist = self.cursor.fetchone()
            strartist = str(idartist)
            self.cursor.execute("Select idPlyty from plyta where tytulPlyty='"+record+"'")
            idrecord = self.cursor.fetchone()
            strrecord = str(idrecord)
            self.cursor.execute("UPDATE utwor SET Autor='"+strartist+"' WHERE idPlyta='"+strrecord+"'")
        else:
            self.cursor.execute("SELECT idAutora FROM autor WHERE nazwaAutora='" + artist + "'")
            idartist = self.cursor.fetchone()
            strartist = str(idartist)
            self.cursor.execute("Select idPlyty from plyta where tytulPlyty='" + record + "'")
            idrecord = self.cursor.fetchone()
            strrecord = str(idrecord)
            self.cursor.execute("UPDATE utwor SET Autor='" + strartist + "' WHERE idPlyta='" + strrecord + "'")

        self.connection.commit()
        log.write("Assigned artist to record\n")

class Interface(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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

        self.geometry("400x800")
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

        self.AddTrackLabel = customtkinter.CTkLabel(master=self.mainframe, text="Zarządzaj utworami", font=("Arial", 12))
        self.AddTrackLabel.pack(pady=10, padx=10)
        self.AddTrackNameEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="Nazwa utworu")
        self.AddTrackNameEntry.pack(pady=3, padx=10)
        self.AddTrackAuthorEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="Autor")
        self.AddTrackAuthorEntry.pack(pady=3, padx=10)
        self.AddTrackRecordEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="Płyta")
        self.AddTrackRecordEntry.pack(pady=3, padx=10)
        self.AddTrackButton = customtkinter.CTkButton(master=self.mainframe, text="Dodaj", command=conn.addTrack)
        self.AddTrackButton.pack(pady=3, padx=10)
        self.RemoveTrackButton = customtkinter.CTkButton(master=self.mainframe, text="Usuń", command=conn.removeTrack)
        self.RemoveTrackButton.pack(pady=3, padx=10)
        
        self.AssignArtistLabel = customtkinter.CTkLabel(master=self.mainframe, text="Dodaj autora do płyty", font=("Arial", 12))
        self.AssignArtistLabel.pack(pady=10, padx=10)
        self.AssignArtistEntryAuthor = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="Autor")
        self.AssignArtistEntryAuthor.pack(pady=3, padx=10)
        self.AssignArtistEntryRecord = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="Płyta")
        self.AssignArtistEntryRecord.pack(pady=3, padx=10)

        self.AssignArtistButton = customtkinter.CTkButton(master=self.mainframe, text="Dodaj", command=conn.assignArtist)
        self.AssignArtistButton.pack(pady=3, padx=10)


class Admin_Window(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("800x400")
        self.mainframe = customtkinter.CTkFrame(master=self)
        self.mainframe.pack(pady=20, padx=60, fill="both", expand=True)

        self.BigUpgradeLabel = customtkinter.CTkLabel(master=self.mainframe, text="Podnieś uprawnienia użytkownika do Admin", font=("Arial", 12))
        self.BigUpgradeLabel.pack(pady=10, padx=10)
        self.BigUpgradeEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="Nazwa użytkownika")
        self.BigUpgradeEntry.pack(pady=3, padx=10)
        self.BigUpgradeButton = customtkinter.CTkButton(master=self.mainframe, text="Podnieś", command=conn.bigUpgrade)
        self.BigUpgradeButton.pack(pady=3, padx=10)

        self.BigDowngradeLabel = customtkinter.CTkLabel(master=self.mainframe, text="Obniż uprawnienia użytkownika do User", font=("Arial", 12))
        self.BigDowngradeLabel.pack(pady=10, padx=10)
        self.BigDowngradeEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="Nazwa użytkownika")
        self.BigDowngradeEntry.pack(pady=3, padx=10)
        self.BigDowngradeButton = customtkinter.CTkButton(master=self.mainframe, text="Obniż", command=conn.bigDowngrade)
        self.BigDowngradeButton.pack(pady=3, padx=10)

        self.TransferSuperUserLabel = customtkinter.CTkLabel(master=self.mainframe, text="Przekaż uprawnienia SuperAdmin", font=("Arial", 12))
        self.TransferSuperUserLabel.pack(pady=10, padx=10)
        self.TransferSuperUserEntry = customtkinter.CTkEntry(master=self.mainframe, placeholder_text="nazwa użytkownika")
        self.TransferSuperUserEntry.pack(pady=3, padx=10)
        self.TransferSuperUserButton = customtkinter.CTkButton(master=self.mainframe, text="Przekaż", command=conn.stankyLeg)
        self.TransferSuperUserButton.pack(pady=3, padx=10)

class TranslationManager:
    def __init__(self, lang):
        self.lang = lang
        self.translations = {}

    def load_translations(self):
        translations_file = os.path.join(os.path.dirname(__file__), f"{self.lang}.txt")

        with open(translations_file, "r", encoding="utf-8") as f:
            for line in f:
                key, value = line.strip().split("=")
                self.translations[key.strip()] = value.strip()

    def get_translation(self, key):
        return self.translations.get(key, key)


log = open("log.txt", "a")
language_file = open('lang.txt', 'a+')
language_file.seek(0)
language = language_file.read()
print(language)

os.makedirs("lang",exist_ok=True)

conn = MySQLConnection('192.166.219.220', '3306', 'niewiadoma', 'niewiadoma', 'Niewiadoma2244;')
conn.connect()

login_window = Interface()
login_window.mainloop()

conn.close()
log.close()
language_file.close()
