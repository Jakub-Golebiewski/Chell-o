## Projekt zbudowany na bazie python 3.7  connector  8.0.31

#Problemy do rozwiązania na później:
# Jak zaznaczasz hasło to się pokazuje

import mysql.connector #connector musi być zainstalowany
from mysql.connector import Error
import tkinter
import customtkinter



try:
    connection = mysql.connector.connect(host='remotemysql.com', #Połącz się z bazą danych
                                         port='3306',
                                         database='kkQ248zGAs',
                                         user='kkQ248zGAs',
                                         password='3dbum5P0FI')
    if connection.is_connected(): #Wyświetl informacje o bazie danych
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor(buffered=True) #Kursor wykonuje polecenia SQL
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
                #Interfejs aplikacji
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")

        app = customtkinter.CTk()
        app.geometry("400x240")
        mainframe= customtkinter.CTkFrame(app, padx=1, pady=1, fg_color="#ADD8E6")
        app.configure(fg_color="#ADD8E6")
        mainframe.grid(column=0, row=0, sticky="nsew")
        app.columnconfigure(0, weight=1)
        app.rowconfigure(0, weight=1)

        login_textbox = customtkinter.CTkTextbox(app, fg_color="#ADD8E6") #Text proszący o login i hasło
        login_textbox.grid(row=0, column=0)
        login_textbox.insert("0.0", "Podaj login i hasło")
        login_textbox.configure(state="disabled")


        login_entry = customtkinter.CTkEntry(master=app, placeholder_text="Login") #Pole login
        login_entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        password_entry = customtkinter.CTkEntry(master=app, placeholder_text="Hasło", text_color="White") #Pole Hasło
        password_entry.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)


        # def Dodaj_przyklad(): #Guzik
        #         sql = "INSERT INTO autor (idAutora, nazwaAutora, fotkaAutora) VALUES (%s, %s, %s)" #Dodaje nowego autora
        #         val = (1, "Tentacooler", "http://pokemonmeme.com/cache/70f8b164/ava2b422db4b70224cd3d.png")
        #         cursor.execute(sql, val)
        #         connection.commit()
        #         print(cursor.rowcount, "Record inserted")
        #
        # button = customtkinter.CTkButton(master=app, text="Dodaj przykładowe dane do bazy danych", command=Dodaj_przyklad)
        # button.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)


        def Login():
             pass#W tym miejscu ma być funkcja logowania. Pobierz login i hasło z login_entry i password_entry.

        button = customtkinter.CTkButton(master=app, text="Zaloguj", command=Login)
        button.place(relx=0.5, rely=0.525, anchor=customtkinter.CENTER)

        def Register():
             #W tym miejscu ma być funkcja Rejestrowania. Pobierz login i hasło z login_entry i password_entry.
            login = login_entry.get()
            password = password_entry.get()
            
            cursor.execute("SELECT * FROM users WHERE uprawnienia = \"2\" ")
            result = cursor.fetchall
            if cursor.rowcount==0:
                uprawnienia = "2"
            else:
                uprawnienia = "0"
            sql = "INSERT INTO users (login, pass, uprawnienia, avatar, jezykUzytkownika, rodzajSkorkiInterfejsu, portfel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (login, password, uprawnienia, "0", "0", "0", "0")
            cursor.execute(sql, val)
            connection.commit()
            print("Dodano uzytkownika")

        button = customtkinter.CTkButton(master=app, text="Zarejestruj", command=Register)
        button.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)


        # def usun_przyklad():
        #         sql = "DELETE FROM autor WHERE idAutora = 1" #Usuwa dane z autora
        #         cursor.execute(sql)
        #         connection.commit()
        #         print(cursor.rowcount, "Records deleted")
        #
        # button = customtkinter.CTkButton(master=app, text="Usuń przykładowe dane", command=usun_przyklad)
        # button.place(relx=0.5, rely=0.775, anchor=customtkinter.CENTER)


        app.mainloop()
                #Inter


        cursor.execute("SELECT * FROM autor") #Wyświetla zawartość tabeli autor
        result = cursor.fetchall()
        for x in result:
            print(x)




except Error as e: #Jak coś się zepsuje to powiedz dlaczego
    print("Error while connecting to MySQL", e)
finally: #Zamknij połączenie na koniec, nawet jak coś się zepsuje
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
