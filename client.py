import socket
from tkinter import *
from threading import Thread
import tkinter
import tkinter as tk
import time
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk


now = datetime.now()
DATE = now.strftime("%y_%m_%d")
LARGE_FONT = ("verdana", 13, "bold")

# ===== Bấm Sign in button thì hàm này chạy =====


def client_login(event=None):
    # Cho phép người dùng nhập username va bank_acc
    submittedUsername = username.get()
    submittedBank_account = bank_acc.get()
    if submittedUsername == "" or submittedBank_account == "":
        messagebox.showinfo('Message ', 'Empty. Please try again.')

    else:
        client.send(submittedUsername.encode(FORMAT))
        time.sleep(0.01)

        client.send(submittedBank_account.encode(FORMAT))
        time.sleep(0.01)

        client.send("1".encode(FORMAT))
        msg = client.recv(1024).decode(FORMAT)
        if msg == "Sign in successfully":
            messagebox.showinfo('Message', msg)
            homepage()
        else:
            messagebox.showinfo('Message', 'Sign in failed. Please try again.')


# ===== Bấm Sign up button thì hàm này chạy =====
def client_logup(event=None):
    submittedUsername = username.get()
    submittedBank_account = bank_acc.get()
    if submittedUsername == "" or submittedBank_account == "":
        messagebox.showinfo('Message ', 'Empty. Please try again.')
    else:
        client.send(submittedUsername.encode(FORMAT))
        time.sleep(0.01)
        client.send(submittedBank_account.encode(FORMAT))
        time.sleep(0.01)
        client.send("2".encode(FORMAT))
        msg = client.recv(1024).decode(FORMAT)
        if msg == "Sign up successfully!":
            messagebox.showinfo('Sign up successfully!', 'Your username: ' +
                                submittedUsername + '  & Your bank account: ' + submittedBank_account)
            homepage()
        elif msg == 'Account has been registered':
            messagebox.showinfo(
                'Message ', 'Account has been registered. Please try again :) ')
            on_closing()

# ===== Xây dựng GUI cho HOMEPAGE =====


def homepage():
    top.destroy()  # xóa cái box loggin
    top2 = Tk()  # tạo box mới (homepage)
    top2.title("Homepage")
    top2.geometry("1350x650")
    top2.configure(bg="bisque2")
    label_title = tk.Label(
        top2, text="HOME", font=LARGE_FONT, fg='#20639b', bg="bisque2")
    label_wel = tk.Label(top2, text="Welcome to Food Ordering System Dashboard",
                         fg='#20639b', bg="bisque2", font='verdana 10 ')
    key_search = tkinter.StringVar()
    key_search2 = tkinter.StringVar()
    key_search.set(DATE)
    key_search2.set("Mì")
    entry_search = tk.Entry(top2, width=37, bg='light yellow', textvariable=key_search)
    entry_search2 = tk.Entry(top2, width=37, bg='light yellow', textvariable=key_search2)
    # ===== Bấm Button SEARCH thì hàm này chạy =====
    def search():
        key = key_search.get()
        key_search.set(DATE)
        key2 = key_search2.get()
        client.send(key.encode(FORMAT))
        client.send(key2.encode(FORMAT))
        key_search.set("Food")
        key_search2.set("")
        if key == "quit" or key2 == "quit":
            client.close()
            top2.destroy()

    # ===== Luồng Receive =====
    def receive():
        while True:
            try:
                msg = client.recv(4080).decode(FORMAT)
                if msg == 'quit':
                    messagebox.showinfo('Message ', 'Sever has stopped ')
                    client.close()
                    top2.destroy()
                line = "-----------------------------"
                mess = msg.split("\n")
                msg_list.insert(tkinter.END, mess[0])
                msg_list.insert(tkinter.END, mess[1])
                msg_list.insert(tkinter.END, mess[2])
                msg_list.insert(tkinter.END, mess[3])
                msg_list.insert(tkinter.END, mess[4])
                msg_list.insert(tkinter.END, line)
            except OSError:
                break

    receive_thread = Thread(target=receive)
    receive_thread.start()

    # Xây dựng Console Application cho Client
    button_search = tk.Button(top2, text="SEARCH", bg="#20639b", fg='floral white', height=2)
    button_search['command'] = search

    # size của phần hiển thị kết quả
    msg_list = tkinter.Listbox(top2, height=16, width=30)
    msg_list1 = tkinter.Listbox(top2, height=16, width=30)
    msg_list2 = tkinter.Listbox(top2, height=16, width=30)
    msg_list3 = tkinter.Listbox(top2, height=16, width=30)
    msg_list4 = tkinter.Listbox(top2, height=16, width=30)
    msg_list5 = tkinter.Listbox(top2, height=16, width=30)

    # Các hình món ăn trong list
    # Món 1
    # Kích thước phần khung hình
    canvas = Canvas(msg_list, width=178, height=90)
    canvas.pack()
    pilImage = Image.open("./logo.png")
    # Resize của hình món ăn
    pilImage = pilImage.resize((81, 80), Image.ANTIALIAS) # độ rộng của phần khung hình
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(95, 45, image=image)  # tọa độ của hình món ăn
    canvas.place(x=0, y=0)

    label_name = tk.Label(msg_list, text="Mì Trộn",font=LARGE_FONT, fg='#20639b', bg='#fff')
    label_name.place(x=60, y=95)

    label_price = tk.Label(msg_list, text="Giá: 30.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    label_price.place(x=10, y=130)

    label_note = tk.Label(msg_list, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_note.place(x=10, y=155)
    
    note_food = tk.Entry(msg_list, width=20, bg='#fff')
    note_food.place(x=53, y= 157)

    label_amount = tk.Label(msg_list, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_amount.place(x=10, y=177)
    
    amount_food = tk.Entry(msg_list, width=5, bg='#fff')
    amount_food.place(x=81, y= 180)

    button = tk.Button(msg_list, text="ORDER", bg="#20639b", width= 10,
                       fg='floral white', height=1)
    button.place(x=52, y=220)

    #========== Món 2  ===========
    canvas1 = Canvas(msg_list1, width=176, height=90)
    canvas1.pack()
    pilImage1 = Image.open("./logo.png")
    pilImage1 = pilImage1.resize((81, 80), Image.ANTIALIAS)  # Resize
    image1 = ImageTk.PhotoImage(pilImage1)
    imagesprite1 = canvas1.create_image(95, 45, image=image1)
    canvas1.place(x=0, y=0)

    label_name1 = tk.Label(msg_list1, text="Cơm chiên",font=LARGE_FONT, fg='#20639b', bg='#fff')
    label_name1.place(x=40, y=95)

    label_price1 = tk.Label(msg_list1, text="Giá: 35.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    label_price1.place(x=10, y=130)

    label_note1 = tk.Label(msg_list1, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_note1.place(x=10, y=155)
    
    note_food1 = tk.Entry(msg_list1, width=20, bg='#fff')
    note_food1.place(x=53, y= 157)

    label_amount1 = tk.Label(msg_list1, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_amount1.place(x=10, y=177)
    
    amount_food1 = tk.Entry(msg_list1, width=5, bg='#fff')
    amount_food1.place(x=81, y= 180)
    button1 = tk.Button(msg_list1, text="ORDER", width = 10,
                        bg="#20639b", fg='floral white', height=1)
    button1.place(x=52, y=220)

    # Món 3
    canvas2 = Canvas(msg_list2, width=176, height=90)
    canvas2.pack()
    pilImage2 = Image.open("./logo.png")
    pilImage2 = pilImage1.resize((81, 80), Image.ANTIALIAS)  # Resize
    image2 = ImageTk.PhotoImage(pilImage2)
    imagesprite2 = canvas2.create_image(95, 45, image=image2)
    canvas2.place(x=0, y=0)

    label_name2 = tk.Label(msg_list2, text="Canh gà",
                           font=LARGE_FONT, fg='#20639b', bg='#fff')
    label_name2.place(x=50, y=95)

    label_price2 = tk.Label(msg_list2, text="Giá: 40.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    label_price2.place(x=10, y=130)

    label_note2 = tk.Label(msg_list2, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_note2.place(x=10, y=155)
    
    note_food2 = tk.Entry(msg_list2, width=20, bg='#fff')
    note_food2.place(x=53, y= 157)

    label_amount2 = tk.Label(msg_list2, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_amount2.place(x=10, y=177)
    
    amount_food2 = tk.Entry(msg_list2, width=5, bg='#fff')
    amount_food2.place(x=81, y= 180)

    button2 = tk.Button(msg_list2, text="ORDER", width= 10,
                        bg="#20639b", fg='floral white', height=1)
    button2.place(x=52, y=220)

    # Món 4
    canvas3 = Canvas(msg_list3, width=176, height=90)
    canvas3.pack()
    pilImage3 = Image.open("./logo.png")
    pilImage3 = pilImage3.resize((81, 80), Image.ANTIALIAS)  # Resize
    image3 = ImageTk.PhotoImage(pilImage3)
    imagesprite3 = canvas3.create_image(95, 45, image=image3)
    canvas3.place(x=0, y=0)

    label_name3 = tk.Label(msg_list3, text="Khoai tây lắc",
                           font=LARGE_FONT, fg='#20639b', bg='#fff')
    label_name3.place(x=30, y=95)

    label_price3 = tk.Label(msg_list3, text="Giá: 25.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    label_price3.place(x=10, y=130)

    label_note3 = tk.Label(msg_list3, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_note3.place(x=10, y=155)
    
    note_food3 = tk.Entry(msg_list3, width=20, bg='#fff')
    note_food3.place(x=53, y= 157)

    label_amount3 = tk.Label(msg_list3, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_amount3.place(x=10, y=177)
    
    amount_food3 = tk.Entry(msg_list3, width=5, bg='#fff')
    amount_food3.place(x=81, y= 180)

    button3 = tk.Button(msg_list3, text="ORDER", width= 10,
                        bg="#20639b", fg='floral white', height=1)
    button3.place(x=52, y=220)

    # Món 5
    canvas4 = Canvas(msg_list4, width=176, height=90)
    canvas4.pack()
    pilImage4 = Image.open("./logo.png")
    pilImage4 = pilImage4.resize((81, 80), Image.ANTIALIAS)  # Resize
    image4 = ImageTk.PhotoImage(pilImage4)
    imagesprite4 = canvas4.create_image(95, 45, image=image4)
    canvas4.place(x=0, y=0)

    label_name4 = tk.Label(msg_list4, text="Gà rán",
                           font=LARGE_FONT, fg='#20639b', bg='#fff')
    label_name4.place(x=60, y=95)

    label_price4 = tk.Label(msg_list4,text="Giá: 30.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    label_price4.place(x=10, y=130)

    label_note4 = tk.Label(msg_list4, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_note4.place(x=10, y=155)
    
    note_food4 = tk.Entry(msg_list4, width=20, bg='#fff')
    note_food4.place(x=53, y= 157)

    label_amount4 = tk.Label(msg_list4, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_amount4.place(x=10, y=177)
    
    amount_food4 = tk.Entry(msg_list4, width=5, bg='#fff')
    amount_food4.place(x=81, y= 180)

    button4 = tk.Button(msg_list4, text="ORDER", width= 10,
                        bg="#20639b", fg='floral white', height=1)
    button4.place(x=52, y=220)

    # Món 6
    canvas5 = Canvas(msg_list5, width=176, height=90)
    canvas5.pack()
    pilImage5 = Image.open("./logo.png")
    pilImage5 = pilImage5.resize((81, 80), Image.ANTIALIAS)  # Resize
    image5 = ImageTk.PhotoImage(pilImage5)
    imagesprite5 = canvas5.create_image(95, 45, image=image5)
    canvas5.place(x=0, y=0)

    label_name5 = tk.Label(msg_list5, text="Phô mai que",
                           font=LARGE_FONT, fg='#20639b', bg='#fff')
    label_name5.place(x=30, y=95)

    label_price5 = tk.Label(msg_list5, text="Giá: 15.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    label_price5.place(x=10, y=130)

    label_note5 = tk.Label(msg_list5, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_note5.place(x=10, y=155)
    
    note_food5 = tk.Entry(msg_list5, width=20, bg='#fff')
    note_food5.place(x=53, y= 157)

    label_amount5 = tk.Label(msg_list5, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    label_amount5.place(x=10, y=177)
    
    amount_food5 = tk.Entry(msg_list5, width=5, bg='#fff')
    amount_food5.place(x=81, y= 180)

    button5 = tk.Button(msg_list5, text="ORDER", width= 10,
                        bg="#20639b", fg='floral white', height=1)
    button5.place(x=52, y=220)

    label_title.pack()
    label_wel.pack()
    Label(top2, text="Loại đồ ăn:", fg='#20639b',
          bg="bisque2", font='verdana 10 ').place(x=20, y=60)
    Label(top2, text="Tên món", fg='#20639b', bg="bisque2",
          font='verdana 10 ').place(x=20, y=90)
    entry_search.place(x=150, y=60)
    entry_search2.place(x=150, y=90)
    button_search.place(x=410, y=61)
    msg_list.place(x=20, y=120)
    msg_list1.place(x=240, y=120)
    msg_list2.place(x=460, y=120)
    msg_list3.place(x=680, y=120)
    msg_list4.place(x=900, y=120)
    msg_list5.place(x=1120, y=120)

    def on_closing2():
        client.send("quit".encode(FORMAT))
        client.close()
        top2.destroy()
    top2.protocol("WM_DELETE_WINDOW", on_closing2)
    top2.mainloop()


# ===== Khi người dùng nhấn nút [X] thì đóng cửa sổ ngắt kết nối đến server =====
def on_closing():
    client.send("quit".encode(FORMAT))
    client.close()
    top.destroy()


# ===== Xây dựng GUI cho LOGIN =====
top = Tk()
top.title("Client")
top.geometry("300x200")
top.configure(bg="bisque2")

Label(top, text="Username", fg='#20639b', bg="bisque2",
      font='verdana 10 ').place(x=20, y=40)
Label(top, text="Bank account", fg='#20639b',
      bg="bisque2", font='verdana 10 ').place(x=20, y=80)
username = tkinter.StringVar()
bank_acc = tkinter.StringVar()
e1 = Entry(top, width=25, textvariable=username).place(x=120, y=40)
e2 = Entry(top, width=25, textvariable=bank_acc).place(x=120, y=80)

button_login = Button(top, text="Sign in", bg="#20639b", fg='floral white', height="1",
                      width="15", activeforeground="black", activebackground="blue", command=client_login)
button_login.place(x=100, y=120)
button_logup = Button(top, text="Sign up", bg="#20639b", fg='floral white', height="1",
                      width="15", activeforeground="black", activebackground="blue", command=client_logup)
button_logup.place(x=100, y=160)

top.protocol("WM_DELETE_WINDOW", on_closing)

# ================================

# hostip = input("Please input ip address: ")
HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, SERVER_PORT))
top.mainloop()
