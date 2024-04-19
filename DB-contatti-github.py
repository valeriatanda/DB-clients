import tkinter 
import tkcalendar
import tkinter.messagebox
import mysql.connector

#GESTIRE UN DATABASE DI CLIENTI. 
#OGNI CLIENTE E CARATTERIZZATO DA:
#NOME, COGNOME, DATA DI NASCITA, GENERE, EMAIL, TELEFONO.

#L'UTENTE HA LA POSSIBILITA DI:
#AGGIUNGERE UN CLIENTE 
#RIMUOVERE UN CLIENTE 
#SELEZIONARE UN CLIENTE IN BASE AL GENERE 
#SELEZIONARE IL NUMERO DI TELEFONO DI UN CLIENTE (SCRIVENDO NOME E COGNOME)


#CONNESSIONE AL DB
db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "", #nessuna password
        database = "customer_db"
)



cursor = db.cursor() 


def add_customer():
    """
    Estrae le informazioni del cliente, 
    creea un oggetto di tipo cliente,
    lo aggiunge in una lista python 
    e lo aggiunge in un database
    """
    customer_name = name_entry.get().strip().title()
    customer_surname = surname_entry.get().strip().title()
    customer_dateOfBirth = dateOfBirth_entry.get_date()
    customer_gender = select_option.get()
    customer_email = email_entry.get().strip().lower()
    customer_phoneNumber = phoneNumber_entry.get().strip()

    #bisogna fare un controllo (tutti i campi devono essere popolati)
    if (customer_name and customer_surname and customer_dateOfBirth and customer_gender and customer_email and customer_phoneNumber):
        #creare un oggetto customer
        customer = Customer(customer_name, customer_surname, customer_dateOfBirth, customer_gender, customer_email, customer_phoneNumber )
    
        #aggiungere tutti i customer a una lista 
        customers_list.append(customer)
        print(customers_list)


        #creare query per trasferire i dati da python a db
        query = f"INSERT INTO customers(Name, Surname, DateOfBirth, Gender, Email, PhoneNumber) VALUES(%s, %s, %s, %s, %s, %s)"
        valori = (customer_name, customer_surname, customer_dateOfBirth, customer_gender, customer_email, customer_phoneNumber) 
        #eseguire la query
        cursor.execute(query, valori)
        db.commit()  #dare l'ok

        #creare una label of success 
        
        success_label = tkinter.Label(window, text= "Customer added with success", foreground= 'green')
        success_label.grid(row=7, column = 0, columnspan= 2)
    else:
        tkinter.messagebox.showwarning("Error","Please fill all the fields")
        


def remove_customer():
    name_removed = name_entry_rem.get().strip().title()
    surname_removed = surname_entry_rem.get( ).strip().title()
    if name_removed and surname_removed: #se esistono
        #cancellare dal db
        query = f"DELETE FROM customers WHERE Name = %s AND Surname = %s"
        valori = (name_removed, surname_removed)
        cursor.execute(query,valori)
        db.commit()

        #creare una label of success (remove)
       
        success_label = tkinter.Label(window, text= "Customer removed with success", foreground= 'red')
        success_label.grid(row=4, column = 3, columnspan= 2)
    else:
        tkinter.messagebox.showwarning("ERROR!", "Insert both Name and Surname")


customers_list = []
class Customer:
    def __init__(self, name, surname, dateOfBirth, gender, email, phoneNumber):
        self.__name = name
        self.__surname = surname
        self.__dateOfBirth = dateOfBirth
        self.__gender = gender
        self.__email = email
        self.__phoneNumber = phoneNumber
    
    def __str__(self):
        return f"Name: {self.__name}, Surname: {self.__surname}, DateOfBirth: {self.__dateOfBirth}, "\
        f"Gender: {self.__gender}, Email: {self.__email}, PhoneNumber: {self.__phoneNumber}"
    
 #metodi getter 
    def getName(self) -> str:
        return self.__name
    
    def getSurname(self) -> str:
        return self.__surname
    
    def getDateOfBirth(self) -> str:
        return self.__dateOfBirth
    
    def getGender(self) -> str:
        return self.__gender
    
    def getEmail(self) -> str:
        return self.__email
    
    def getPhoneNumber(self) -> str:
        return self.__phoneNumber
    

 #metodi setter 
    def setName(self, newName) -> str:
        if isinstance(newName, str):   
            self.__name = newName

    def setSurname(self, newSurname) -> str:
        if isinstance(newSurname, str):
            self.__surname = newSurname

    def setDateOfBirth(self, newDateOfBirth) -> str:
        if isinstance(newDateOfBirth, str):   
            self.__dateOfBirth = newDateOfBirth

    def setGender(self, newGender) -> str:
        if isinstance(newGender, str):
            self.__genre = newGender

    def setEmail(self, newEmail) -> str:
        if isinstance(newEmail, str): 
            self.__email = newEmail

    def setPhoneNumber(self, newPhoneNumber) -> str:
        if isinstance(newPhoneNumber, str): 
            self.__phoneNumber = newPhoneNumber





#CREAZIONE INTERFACCIAA GRAFICA 
window = tkinter.Tk()


#***___ADD SECTION___***
#REALIZZAZIONE DEL WIDGET (label + entry)
#LABEL
name_label = tkinter.Label(window, text = "Name: ")
surname_label = tkinter.Label(window, text = "Surname: ")
dateOfBirth_label = tkinter.Label(window, text = "Date of birth: ")
gender_label = tkinter.Label(window, text = "Gender: ")
email_label = tkinter.Label(window, text = "E.mail: ")
phoneNumber_label = tkinter.Label(window, text = "Phone number: ")
#ENTRY
name_entry = tkinter.Entry(window, borderwidth = 3)
surname_entry = tkinter.Entry(window, borderwidth = 3)
dateOfBirth_entry = tkcalendar.DateEntry(window, borderwidth = 3, width= 17, 
                                     date_pattern="dd/mm/yyyy", year = 2000, month = 11, day = 4 )
#__________calendario
option_list = ["M", "F"]
select_option = tkinter.StringVar(window)
select_option.set("Select an Option")   
gender_entry = tkinter.OptionMenu(window, select_option, *option_list)
#__________
email_entry = tkinter.Entry(window, borderwidth = 3)
phoneNumber_entry = tkinter.Entry(window, borderwidth = 3)
#__________bottoni
button_add = tkinter.Button(window, text = "Add Customer", background="green", foreground= "white", command = add_customer)




#VISUALIZZAZIONE DEL WIDGET NELLA FINESTRA
#LABEL GRID
name_label.grid(row = 0, column = 0)
surname_label.grid(row = 1, column = 0) 
dateOfBirth_label.grid(row = 2, column = 0) 
gender_label.grid(row = 3, column = 0) 
email_label.grid(row = 4, column = 0) 
phoneNumber_label.grid(row = 5, column = 0) 
#ENTRY GRID
name_entry.grid(row = 0, column = 1) 
surname_entry.grid(row = 1, column = 1) 
dateOfBirth_entry.grid(row = 2, column = 1) 
gender_entry.grid(row = 3, column = 1) 
email_entry.grid(row = 4, column = 1) 
phoneNumber_entry.grid(row = 5, column = 1) 
#__________bottoni
button_add.grid(row= 6, column = 0, columnspan= 2)



#***___REMOVE SECTION__***
#LABEL REMOVE
name_label_rem = tkinter.Label(window, text = "Name to remove: ")
surname_label_rem = tkinter.Label(window, text = "Surname to remove: ")
#ENTRY REMOVE
name_entry_rem = tkinter.Entry(window, borderwidth=3)
surname_entry_rem = tkinter.Entry(window, borderwidth=3)
#BOTTONE
button_remove = tkinter.Button(window,text = "Remove Customer", background="red", foreground= "white", command = remove_customer)

#LABEL REMOVE GRID
name_label_rem.grid(row = 0, column = 2)
surname_label_rem.grid(row = 1, column = 2)
#ENTRY REMOVE GRID
name_entry_rem.grid(row = 0, column = 3)
surname_entry_rem.grid(row = 1, column = 3)
#BOTTONE
button_remove.grid(row = 2, column = 2, columnspan= 2)





window.mainloop() 