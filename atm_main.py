# importing necessary modules
import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox
from pymongo.errors import  ConnectionFailure
import os
from dotenv import load_dotenv
from datetime import datetime
# -------------------------------------------------------

# load data from .env file
load_dotenv()
# get MongoDB URI
mongo_uri = os.getenv('MONGO_URI')
# create client for database
client_db = MongoClient(mongo_uri)
# connect to a database
db = client_db['ATM']
# collection for user's credentials 
user_collection = db['user_data']
# collection consist of actions performed
user_action = db['actions']

# ---------------------------------------------------------------
# create a class 
class ATM(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('300x230')
        self.title("ATM")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3, 4), weight=1)
        self.verified_username = None

    # ---------------------------------------------------- Widgets ------------------------------------------------
        # heading
        ctk.CTkLabel(self, text='Welcome to Python ATM', font=('Georgia',17,'italic'), text_color='#4DFFBE').grid(row=0, column=0,pady=10, padx=10)
        # login button
        ctk.CTkButton(self, text='Login', font=('Arial',12,'bold'), command=self.login_window, text_color='#4DFFBE', fg_color='transparent', border_width=1, border_color='#4DFFBE', hover=True, corner_radius=6).grid(row=1, column=0, pady=10,padx=10)
        # Create account button
        ctk.CTkButton(self, text='Create new account', font=('Arial',12,'bold'), command=self.create_new_account_window, text_color='#4DFFBE', fg_color='transparent', border_width=1, border_color='#4DFFBE', hover=True, corner_radius=6).grid(row=2, column=0, pady=10, padx=10)
        # Quit button
        ctk.CTkButton(self, text='Quit', font=('Arial',12,'bold'), command=self.quit, border_width=1, border_color='#DC3C22', fg_color='transparent', text_color='#DC3C22', hover=True, hover_color='#FF8282',corner_radius=6).grid(row=3, column=0, pady=10, padx=10)
    
    # ------------------------------------------------- functions -------------------------------------------------
    # quit button
    def quit(self):
        self.destroy()
    # ---------------------------------------------------------------------------------------------------------------------
    # function for login
    def login_window(self):
        try:
            if not user_collection.find({}):
                messagebox.showerror("Error","User not found!")
            else:
                messagebox.showinfo("info","login successful!")
                # open main window
                self.main_window()
        except Exception as e:
            messagebox.showerror("Error",f"{str(e)}")
        except ConnectionFailure:
            messagebox.showerror("Error","Connection Failed!")
        except ConnectionError:
            messagebox.showerror("Error","Connection Error")  

    # ----------------------------------------------------- MAIN WINDOW ----------------------------------------------------------
    def main_window(self):
        # close previous window
        self.withdraw()
        # create new window
        self.main = ctk.CTkToplevel()
        self.main.geometry("250x350")
        self.main.title("main window")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure((0,1,2,3), weight=1)
        # ----------------------------------------------------- main window widgets ------------------------------------------------------------------
        # heading
        ctk.CTkLabel(self.main, text='welcome', font=("georgia",18,'italic'), text_color='#4DFFBE').grid(row=0, column=0, padx=10, pady=10)
        frame_2 = ctk.CTkFrame(self.main, width=250, height=300, corner_radius=6, border_width=1, border_color='#4DFFBE')
        frame_2.grid(row=1,column=0, padx=10, pady=10, sticky='ew')
        frame_2.grid_columnconfigure(0, weight=1)
        # depsoit button
        ctk.CTkButton(frame_2, text='Depsoit', command=lambda:self.verify_window(self.deposit_window), corner_radius=6, border_width=1, border_color='#799EFF',fg_color='transparent', hover=True,text_color='#799EFF').grid(row=0, column=0, padx=10, pady=10)
        # withdraw button
        ctk.CTkButton(frame_2, text='Withdraw', command=lambda:self.verify_window(self.withdrawl_window), corner_radius=6, border_color='#FF7D29', fg_color='transparent', hover=True, hover_color='#FFC785',text_color='#FF7D29', border_width=1).grid(row=1, column=0, padx=10, pady=10)
        # show balance button
        ctk.CTkButton(frame_2, text='Show Bal', command=lambda:self.verify_window(self.show_balance_window), corner_radius=6, border_color='#B4E50D', hover=True, hover_color='#78C841',border_width=1, fg_color='transparent', text_color='#B6F500').grid(row=2, column=0, padx=10, pady=10)
        # transaction history button
        ctk.CTkButton(frame_2, text='Transaction History', font=('Arial',12,'bold'), command=lambda:self.verify_window(self.trans_history), text_color='#4DFFBE', fg_color='transparent', border_width=1, border_color='#4DFFBE', hover=True, corner_radius=6).grid(row=3, column=0, pady=10, padx=10)
        # back button
        ctk.CTkButton(frame_2, text='back', command=self.go_back, corner_radius=6, border_width=1, border_color='#DC3C22', hover_color='#FF8282', hover=True, fg_color='transparent', text_color='#DC3C22').grid(row=4, column=0, padx=10, pady=10)
        # ------------------------------------------------- MAIN WINDOW FUNCTIONS -------------------------------------------
    # back button
    def go_back(self):
        self.main.destroy()
        self.deiconify()

        # ----------------------------------------------------- Calulate deposit window -----------------------------------------------------------
    # deposit window
    def deposit_window(self):
        # close the previous window
        self.verify.withdraw()
        # create new window
        new = ctk.CTkToplevel()
        new.geometry("300x200")
        new.title("Deposit amount")   
        new.grid_columnconfigure(0, weight=1)
        new.grid_rowconfigure((0,1,2), weight=1)        
        # -----------------------------------------------------  calculate Deposit Functions ----------------------------------------------------------------
        # cancel button logic
        def cancel():
            new.destroy()
            self.main.deiconify()
        # ------------------------------------------------------------------------------------
        # clear button logic
        def clear():
            amt_entry.delete(0, ctk.END)
        # -------------------------------------------------------------------------------------
        # deposit function logic
        def deposit():
            # get username
            username = self.verified_username
            # get entered amount by user
            amount = amt_entry.get()
            # check for correct entry
            data = user_collection.find_one({"username":username})
            if not amount or not amount.isdigit():
                messagebox.showerror('error','Enter valid amount!')
                return 
                    
            if data:
                try:
                    amount = float(amount)
                    # get balance from the database
                    crt_balanace = float(data.get('balance',0))
                    # calculate the final amunt
                    new_bal = crt_balanace + amount
                    # update the database with new balance
                    result = user_collection.update_one(
                        {'username':username},
                        {"$set":{"balance":new_bal}}
                    )
                    # insert the action performed by user
                    if result.modified_count > 0:
                        messagebox.showinfo('success',f'Rs.{amount} deposited successfully!')
                        # insert the actions performed in user_collection 
                        statement = f'deposited Rs. {amount}'
                        user_action.insert_one({"username":username,"action":statement,"time":datetime.now()})
                        amt_entry.delete(0, ctk.END)
                    else:
                        messagebox.showinfo('info','balance already updated or nothing change.')
                except Exception as e:
                    messagebox.showerror('error',f'{str(e)}')
            else:
                messagebox.showerror('error','user not found.')

        # ------------------------------------------------------- calculate depsoit widgets -----------------------------------------------------------
        # heading
        ctk.CTkLabel(new, text='Deposit Amount', font=('Arial',18,'italic'), text_color='#4DFFBE').grid(row=0, column=0, padx=10, pady=10)
        # frame
        frame_4 = ctk.CTkFrame(new,width=300,height=180, border_color='#4DFFBE', border_width=1)
        frame_4.grid(row=1, column=0, padx=10, pady=10)
        frame_4.grid_columnconfigure((0,1,2), weight=1)
        frame_4.grid_rowconfigure((0,1), weight=1)
        # Enter amount label
        ctk.CTkLabel(frame_4, text='amount', font=('Arial',11,'bold'), text_color='#4DFFBE').grid(row=0, column=0, padx=10, pady=10)
        # amount entry
        amt_entry= ctk.CTkEntry(frame_4, font=('arial',11), width=200, text_color='#4DFFBE')
        amt_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        # Cancel button
        ctk.CTkButton(frame_4, text='Cancel', command=cancel, font=("arial",10,'bold'), fg_color='transparent', hover=True, border_width=1, border_color='#FB4141', hover_color='#FF8282',text_color='#FB4141').grid(row=1, column=0, padx=10, pady=10)
        # clear all button
        ctk.CTkButton(frame_4, text='Clear', command=clear, font=("arial",10,'bold'), fg_color='transparent', hover=True, border_width=1, border_color='#FDF5AA', text_color='#FDF5AA', hover_color='#FFCB61').grid(row=1, column=1, padx=10, pady=10)
        # deposit button
        deposit_btn = ctk.CTkButton(frame_4, text='Deposit', command=deposit, font=("arial",10,'bold'), fg_color='transparent', hover=True, border_width=1, border_color='#B4E50D', text_color='#B4E50D', hover_color='#5E936C')
        deposit_btn.grid(row=1, column=2, padx=10, pady=10)
            
    # ---------------------------------------------------------------- verify window ------------------------------------------------------------------------------
    def verify_window(self,next_action):
        # close the previous window
        self.main.withdraw()
        # create new window
        self.verify = ctk.CTkToplevel()
        self.verify.title('verify')
        self.verify.geometry('550x300')
        #frame:
        frame_3 = ctk.CTkFrame(self.verify, width=500, height=300, corner_radius=6, border_width=2, border_color="#4DFFBE")
        # username entry
        username_entry = ctk.CTkEntry(frame_3, text_color="#4DFFBE", font=("arial",12,'bold'), width=220)
        # password entry
        pwd_entry = ctk.CTkEntry(frame_3, text_color="#4DFFBE", font=("arial",12,'bold'), width=220)
        # pin entry
        pin_entry = ctk.CTkEntry(frame_3, text_color="#4DFFBE", font=("arial",12,'bold'), width=220)

        # ----------------------------------------------------- Verify window function -------------------------------------------------------
        # verify logic for verification
        def verify_logic():
            username = username_entry.get().strip()
            pwd = pwd_entry.get().strip()
            pin = pin_entry.get().strip()
            data = user_collection.find_one({"username" : username,"password" : pwd,"pin" : pin})
                
            if not username or not pwd or not pin:
                messagebox.showerror("Error","Fill data to proceed.")
                return
            try:
                if data :
                    self.verified_username = username
                    messagebox.showinfo('succeess',' ✅ User verified!')
                    next_action() # call the function===================================================
                    username_entry.delete(0, ctk.END)
                    pwd_entry.delete(0, ctk.END)
                    pin_entry.delete(0, ctk.END)
                elif not data:
                    messagebox.showerror("Error"," User not found!")
            except ConnectionFailure:
                messagebox.showerror("error","Connection failure")
            except ConnectionError:
                messagebox.showerror('Error','Connection error.')
        # ------------------------------------------------------------
        # clear btn function
        def clear():
            username_entry.delete(0, ctk.END)
            pwd_entry.delete(0, ctk.END)
            pin_entry.delete(0, ctk.END)
        # ----------------------------------------------------------
        # back function
        def back():
            self.verify.destroy()
            self.main.deiconify()
        # ------------------------------------------------------------  verify window widgets ------------------------------------------------
        # heading
        ctk.CTkLabel(self.verify, text='Verify yourself', font=("Georgia",16,'italic'), text_color="#4DFFBE").grid(row=0, column=0, padx=10, pady=10)
        # frame 
        frame_3.grid(row=1, column=0, padx=10, pady=10)
        frame_3.grid_columnconfigure(0, weight=1)
        frame_3.grid_rowconfigure((0,1,2), weight=1)
        # username label
        ctk.CTkLabel(frame_3, text='username', text_color="#4DFFBE", font=("arial",14,'bold')).grid(row=0, column=0, padx=10, pady=10)
        username_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        # password label
        ctk.CTkLabel(frame_3, text='Password', text_color="#4DFFBE", font=("arial",14,'bold')).grid(row=1, column=0, padx=10, pady=10)
        pwd_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        # PIN Label
        ctk.CTkLabel(frame_3, text='Pin', text_color="#4DFFBE", font=("arial",14,'bold')).grid(row=2, column=0, padx=10, pady=10)
        pin_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
        # clear all button
        ctk.CTkButton(frame_3, text='clear all', font=('Arial',13,'bold'), command=clear, border_width=1, border_color='#F97300', fg_color='transparent', text_color='#F97300', hover_color='#FADA7A',hover=True, corner_radius=6).grid(row=3, column=1,pady=10, padx=20, sticky='ew')
        # back button
        ctk.CTkButton(frame_3, text='back', font=('Arial',13,'bold'), command=back, border_width=1, border_color='#DC3C22', fg_color='transparent', text_color='#DC3C22', hover_color='#FF8282', hover=True, corner_radius=6).grid(row=3, column=0,pady=10, padx=20, sticky='ew')
        # verify button
        ctk.CTkButton(frame_3, text='verify', font=('arial',13,'bold'), command=verify_logic, text_color='#3DC2EC', border_width=1, border_color='#3DC2EC', hover=True, fg_color='transparent').grid(row=3, column=2, padx=10, pady=10, sticky='ew')

    # ----------------------------------------------------------------------- Withdrowl window --------------------------------------------------------
    def withdrawl_window(self):
        # close the previous window
        self.verify.withdraw()
        # create new window for withdrawl
        window = ctk.CTkToplevel()
        window.geometry("300x200")
        window.title("withdraw amount")   
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure((0,1,2), weight=1)

        # ----------------------------------------------------------------- withdrawl functions -----------------------------------------------------------------
        # back button
        def back():
            window.destroy()
            self.verify.deiconify()
        # --------------------------------------
        # clear window
        def clear():
            amt_entry.delete(0, ctk.END)
        # ----------------------------------------
        # withdraw logic
        def withdrawl():
            # get username
            username = self.verified_username
            # get entered amount from user
            amount = amt_entry.get()
            # check if user exists
            data = user_collection.find_one({"username":username})
            if not amount or not amount.isdigit():
                messagebox.showerror("Error","enter valid Amount.")
            if data:
                try:
                    # convert the amount into float data type
                    amount = float(amount)
                    # get balance of user
                    crt_bal = float(data.get('balance',0))
                    if crt_bal < amount:
                        messagebox.showwarning("Funds warning", "Insufficient Funds!")
                    elif int(crt_bal) == 0:
                        messagebox.showwarning("Funds warning","No Funds in your account.")
                    else:
                        # calculate left over amount after withdrawl
                        left_amount = crt_bal - amount
                        # update the database
                        result = user_collection.update_one(
                            {"username":username},
                            {"$set":{'balance':left_amount}}
                        )

                        if result.modified_count > 0:
                            messagebox.showinfo("success",f"Rs.{amount} withdraw successfully.")
                            amt_entry.delete(0, ctk.END)
                            # insert the actions performed in user_collection 
                            statement = f'withdraw Rs. {amount}'
                            user_action.insert_one({"username":username,"action":statement,"time":datetime.now()})
                        else:
                            messagebox.showinfo('info','balance already updated.')
                except Exception as e:
                    messagebox.showerror("Error",f"{str(e)}")
                except ConnectionError:
                    messagebox.showerror("Error","Connection Error!")
                except ConnectionFailure:
                    messagebox.showerror("Error","Network Failed!")
            else:
                messagebox.showerror("error","user does not exist.")
        
        # ---------------------------------------------------------------- withdrawl widgets ------------------------------------------------------------
        # heading
        ctk.CTkLabel(window, text="Withdrwal amount", font=('georgia',16,'italic'), text_color='#4DFFBE').grid(row=0, column=0, padx=10, pady=10)
        # frame
        frame_5 = ctk.CTkFrame(window,width=300,height=180, border_color='#4DFFBE', border_width=1)
        frame_5.grid(row=1, column=0, padx=10, pady=10)
        frame_5.grid_columnconfigure((0,1,2), weight=1)
        frame_5.grid_rowconfigure((0,1), weight=1)   
        #   Enter amount label
        ctk.CTkLabel(frame_5, text='amount', font=('Arial',11,'bold'), text_color='#4DFFBE').grid(row=0, column=0, padx=10, pady=10) 
        # amount entry
        amt_entry= ctk.CTkEntry(frame_5, font=('arial',11), width=200, text_color='#4DFFBE')
        amt_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        # Cancel button
        ctk.CTkButton(frame_5, text='Cancel', command=back, font=("arial",10,'bold'), fg_color='transparent', hover=True, border_width=1, border_color='#FB4141', hover_color='#FADA7A',text_color='#FB4141').grid(row=1, column=0, padx=10, pady=10)
        # clear all button
        ctk.CTkButton(frame_5, text='Clear', command=clear, font=("arial",10,'bold'), fg_color='transparent', hover=True, border_width=1, border_color='#FDF5AA', text_color='#FDF5AA', hover_color='#FFCB61').grid(row=1, column=1, padx=10, pady=10) 
        # withdrow button
        withdraw_btn = ctk.CTkButton(frame_5, text='Withdraw', command=withdrawl, font=("arial",10,'bold'), fg_color='transparent', hover=True, border_width=1, border_color='#B4E50D', text_color='#B4E50D', hover_color='#5E936C')
        withdraw_btn.grid(row=1, column=2, padx=10, pady=10)
        
    # -------------------------------------------------------------- Show balance window -------------------------------------------------------------------
    def show_balance_window(self):
        # get username
        username = self.verified_username
        # find if username is present
        data = s=user_collection.find_one({"username":username})
        # if only username is found
        if data:
            try:
                # fetch amount from specified username
                crt_bal = float(data.get('balance',0))
                # show current balance
                messagebox.showinfo("balance",f"current balance Rs. {crt_bal}")
            except Exception as e:
                messagebox.showerror("error",f"{str(e)}")
            except ConnectionFailure:
                messagebox.showerror("error","Network Failed!")
            except ConnectionError:
                messagebox.showerror('error',"Connection Error!")
        else:
            messagebox.showerror("error","user not found!")
    # ------------------------------------------------------------ New account Window -------------------------------------------------------------------
    # create new account function
    def create_new_account_window(self):
        # withdraw previous window
        self.withdraw()
        # create a new window for creating a new window
        account = ctk.CTkToplevel()
        account.title("create account")
        account.geometry('550x400')
        account.grid_columnconfigure((0,1,2,3), weight=1)
        account.grid_rowconfigure((0,1,2), weight=1)

        # ---------------------------------------------------- create account functions ------------------------------------------------
        # back button
        def back():
            account.destroy()
            self.deiconify()
        # ----------------------------
        # clear button
        def clear_all():
            username_entry.delete(0, ctk.END)
            pwd_entry.delete(0, ctk.END)
            conf_pwd_entry.delete(0, ctk.END)
            pin_entry.delete(0, ctk.END)
        # -------------------------------------
        # create account button
        def create_account():
            # get user data 
            username = username_entry.get()
            pwd = pwd_entry.get()
            conf_pwd = conf_pwd_entry.get()
            pin = pin_entry.get()

            # control flow logic
            # if user clicks button without filling any data
            if not username and not pwd and not conf_pwd and not pin:
                messagebox.showerror("Error", "Fill info to proceed.")
            # if password and confirm password doesn't match
            elif pwd != conf_pwd:
                messagebox.showerror("Error", "Incorrect Password!")
            else:
                try:
                    if len(pwd) > 16:
                        messagebox.showerror('error','password cannot be more than 15 characters long!')
                    elif len(pin) > 5:
                        messagebox.showerror('error','PIN must be 4 characters long!')
                    elif not pin.isdigit():
                        messagebox.showerror('error','PIN must be digit only!')
                    else:
                        user_collection.insert_one({"username":username,"password":pwd,"pin":pin,"balance":0})
                        messagebox.showinfo("info", "Account created successfully!")
                        username_entry.delete(0, ctk.END)
                        pwd_entry.delete(0, ctk.END)
                        conf_pwd_entry.delete(0, ctk.END)
                        pin_entry.delete(0,ctk.END)
                except ConnectionError:
                    messagebox.showerror("Error","Connection Error")
                except ConnectionFailure:
                    messagebox.showerror("Error", "Connection Failed!")
    
    # ---------------------------------------------------- create account widgets -------------------------------------------------
        # heading
        ctk.CTkLabel(account, text='Create Account', font=('georgia',17,'italic'), text_color='#4DFFBE').grid(row=0, column=0, padx=10, pady=10, columnspan=3)
        # frame to hold labels and buttons
        frame_1 = ctk.CTkFrame(account, width=550, height=350, fg_color='#393E46', border_color='#4DFFBE', corner_radius=6, border_width=1)
        frame_1.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky='ew')
        frame_1.grid_columnconfigure((0,1,2,3), weight=1)
        # label for user name
        ctk.CTkLabel(frame_1, text='username', font=('arial',12,'bold'), text_color='#4DFFBE').grid(row=0, column=0, padx=10, pady=10)
        # entry for username
        username_entry = ctk.CTkEntry(frame_1, width=220, text_color='#4DFFBE', font=('arial',11))
        username_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=3)
        # password label
        ctk.CTkLabel(frame_1, text='password', font=('arial',12,'bold'), text_color='#4DFFBE').grid(row=1, column=0, padx=10, pady=10)
        # password entry
        pwd_entry = ctk.CTkEntry(frame_1, width=220, text_color='#4DFFBE', font=('arial',11))
        pwd_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=3)
        # confirm password label
        ctk.CTkLabel(frame_1, text='confirm pwd', font=('arial',12,'bold'), text_color='#4DFFBE').grid(row=2, column=0, padx=10, pady=10)
        # confirm password entry
        conf_pwd_entry = ctk.CTkEntry(frame_1, width=220, text_color='#4DFFBE', font=('arial',11))
        conf_pwd_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=3)
        # set pin label 
        ctk.CTkLabel(frame_1, text='set pin', font=('arial',12,'bold'), text_color='#4DFFBE').grid(row=3, column=0, padx=10, pady=10)
        # set pin button
        pin_entry = ctk.CTkEntry(frame_1, width=220, text_color='#4DFFBE', font=('arial',11))
        pin_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=3)
        # back button
        ctk.CTkButton(frame_1, text='back', font=('Arial',13,'bold'), command=back, border_width=1, border_color='#DC3C22', fg_color='transparent', text_color='#DC3C22', hover_color='#FF8282', hover=True, corner_radius=6).grid(row=4, column=0,pady=10, padx=20, sticky='ew')
        # create account button
        ctk.CTkButton(frame_1, text='create', font=('Arial',13,'bold'), command=create_account, border_width=1, border_color='#3DC2EC', fg_color='transparent', text_color='#3DC2EC', hover=True, corner_radius=6).grid(row=4, column=2,pady=10, padx=20, sticky='ew')
        # clear button
        ctk.CTkButton(frame_1, text='clear all', font=('Arial',13,'bold'), command=clear_all, border_width=1, border_color='#F97300', fg_color='transparent', text_color='#F97300', hover_color='#FADA7A',hover=True, corner_radius=6).grid(row=4, column=1,pady=10, padx=20, sticky='ew')

    # --------------------------------------------------------------------- transaction history window ------------------------------------------------------------
    def trans_history(self):
        # close previous window
        self.verify.withdraw()
        # get username
        username = self.verified_username
        if not username:
            messagebox.showwarning("warning","you must login to view transaction history!")
            return
        # create new window
        history = ctk.CTkToplevel()
        history.title("Transaction history")
        history.geometry("500x400")
        history.grid_columnconfigure(0, weight=1)
        history.grid_rowconfigure((0,1), weight=1)

        # --------------------------------------------------------------- Transc history functions ------------------------------------------------------------------
        def back():
            history.destroy()
            self.verify.deiconify()
        # -------------------------------------------------------------- Trancs history widgets ----------------------------------------------------------------------
        # scrollable frame
        frame_6 = ctk.CTkScrollableFrame(history, width=450, height=300, border_color='#4DFFBE', border_width=2, corner_radius=6)
        frame_6.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        # fetch the transaction history from user_action collection
        try:
            trans_history = list(user_action.find({"username":username}).sort('time',-1))
        except Exception as e:
            messagebox.showerror('error',f'failed to retrieve : {str(e)}')
            return
        if not trans_history:
            messagebox.showerror("error",f"no transaction history found for {username}.")
        else:
            # row counter
            row_counter = 0
            # run a loop through database collection for specific username only
            for data in trans_history:
                time = data.get('time')
                action = data.get('action')
                # format date and time
                if isinstance(time, datetime):
                    formatted_time = time.strftime("%d-%b-%Y %I:%M %p")
                else:
                    formatted_time = "[Invalid time]"
                # creating history text
                text = f"Time: {formatted_time}\nAction: {action}"
                # create a subframe to store the text
                frame_7 = ctk.CTkFrame(frame_6, fg_color='#FEEBF6', width=420, height=150)
                frame_7.grid(row = row_counter, column=0, padx=10, pady=10)
                # label to insert in frame_7
                text_label = ctk.CTkLabel(frame_7, text=text, text_color='black', font=('arial',14,'bold'), justify='left', wraplength=420)
                text_label.grid(row=0, column=0, padx=8, pady=8, sticky='w')
                # increment the row_counter by one
                row_counter += 1

        # back button
        ctk.CTkButton(history, text='Back', command=back, font=('Arial',12,'bold'), width=80, fg_color='#F7374F', hover_color='#FF8282', text_color='black').grid(row=1, column=0, padx=10, pady=10)

    # -------------------------------------------------------------------------- run the app -----------------------------------------------------------------------------------
# create the object
app = ATM()
# run the app
app.mainloop()