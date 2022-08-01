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
            messagebox.showinfo('Message ', 'Account has been registered. Please try again :) ')
            on_closing()

# ===== Xây dựng GUI cho HOMEPAGE =====


def homepage():
    top.destroy()  # xóa cái box loggin
    top2 = Tk()  # tạo box mới (homepage)
    top2.title("Homepage")
    top2.state('zoomed')
    top2.resizable(0, 0)
    top2.configure(bg="bisque2")
    
    

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

        # size của phần hiển thị kết quả
    msg_list = tkinter.Listbox(top2, width=50)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
    msg_total = tkinter.Listbox(top2, width=10)
    msg_total.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

    label_title = tk.Label(msg_list, text="HOME", font=LARGE_FONT, bg="#fff").place(relx=0.5, rely=0)
    label_wel = tk.Label(msg_list, text="Welcome to Food Ordering System Dashboard", font='verdana 10', bg="#fff").place(relx=0.355, rely=0.03)
    label_title = tk.Label(msg_total, text="Thanh toán", font=LARGE_FONT, bg="#fff").place(relx=0.5, rely=0)
    
    frame = Frame(msg_list, bg="bisque2")
    frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.89)

    my_canvas = Canvas(frame, bg="bisque2")
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    # Create scrollbar for msg_list
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=my_canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Configure canvas
    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
    # Create another frame inside the canvas
    second_frame = Frame(my_canvas, bg="bisque2")
    # Add that new frame to a window in the canvas
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    
    # ===== Xây dựng GUI cho thanh toán =====
    image_button1 = PhotoImage(file='./image/food/bamithit1.png')
    button1 = tk.Button(second_frame, image=image_button1, bg="#20639b", width= 190,
                       fg='floral white', height=220)
    button1.grid(row=1, column=0, padx=30, pady=17)

    image_button2 = PhotoImage(file='./image/food/comsuon.png')
    button2 = tk.Button(second_frame,image=image_button2, bg="#20639b", width= 190,
                          fg='floral white', height=220)  
    button2.grid(row=1, column=1, padx=30, pady=17)

    image_button3 = PhotoImage(file='./image/food/bamithit1.png')
    button3 = tk.Button(second_frame,image=image_button3, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button3.grid(row=1, column=2, padx=30, pady=17)

    image_button4 = PhotoImage(file='./image/food/comsuon.png')
    button4 = tk.Button(second_frame,image=image_button4, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button4.grid(row=2, column=0, padx=30, pady=17)

    image_button5 = PhotoImage(file='./image/food/bamithit1.png')
    button5 = tk.Button(second_frame, image=image_button5, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button5.grid(row=2, column=1, padx=30, pady=17)

    image_button6 = PhotoImage(file='./image/food/comsuon.png')
    button6 = tk.Button(second_frame, image=image_button6, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button6.grid(row=2, column=2, padx=30, pady=17)

    image_button7 = PhotoImage(file='./image/drink/cafe.png')
    button7 = tk.Button(second_frame, image=image_button7, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button7.grid(row=3, column=0, padx=30, pady=17)

    image_button8 = PhotoImage(file='./image/drink/capuchino.png')
    button8 = tk.Button(second_frame, image=image_button8, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button8.grid(row=3, column=1, padx=30, pady=17)

    image_button9 = PhotoImage(file='./image/drink/coca.png')
    button9 = tk.Button(second_frame, image=image_button9, bg="#20639b", width= 190,       
                            fg='floral white', height=220)
    button9.grid(row=3, column=2, padx=30, pady=17)

    image_button10 = PhotoImage(file='./image/drink/pepsi.png')
    button10 = tk.Button(second_frame, image=image_button10, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button10.grid(row=4, column=0, padx=30, pady=17)

    image_button11 = PhotoImage(file='./image/drink/nuoc.png')
    button11 = tk.Button(second_frame, image=image_button11, bg="#20639b", width= 190,       
                            fg='floral white', height=220)
    button11.grid(row=4, column=1, padx=30, pady=17)

    image_button12 = PhotoImage(file='./image/drink/cafeden.png')
    button12 = tk.Button(second_frame, image=image_button12, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button12.grid(row=4, column=2, padx=30, pady=17)

    image_button13 = PhotoImage(file='./image/drink/cafesua.png')
    button13 = tk.Button(second_frame, image=image_button13, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button13.grid(row=5, column=0, padx=30, pady=17)

    image_button14 = PhotoImage(file='./image/drink/cafe.png')
    button14 = tk.Button(second_frame, image=image_button14, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button14.grid(row=5, column=1, padx=30, pady=17)

    image_button15 = PhotoImage(file='./image/drink/coca.png')
    button15 = tk.Button(second_frame, image=image_button15, bg="#20639b", width= 190,
                            fg='floral white', height=220)
    button15.grid(row=5, column=2, padx=30, pady=17)




    # Các hình món ăn trong list
    # Món 1
    # Kích thước phần khung hình
    # canvas = Canvas(msg_list, width=178, height=90)
    # canvas.pack()
    # pilImage = Image.open("./image/drink/cafe.png")
    # # Resize của hình món ăn
    # pilImage = pilImage.resize((81, 80)) # độ rộng của phần khung hình
    # image = ImageTk.PhotoImage(pilImage)
    # imagesprite = canvas.create_image(95, 45, image=image)  # tọa độ của hình món ăn
    # canvas.place(x=0, y=0)

    # label_name = tk.Label(msg_list, text="Mì Trộn",font=LARGE_FONT, fg='#20639b', bg='#fff')
    # label_name.place(x=60, y=95)

    # label_price = tk.Label(msg_list, text="Giá: 30.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    # label_price.place(x=10, y=130)

    # label_note = tk.Label(msg_list, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_note.place(x=10, y=155)
    
    # note_food = tk.Entry(msg_list, width=20, bg='#fff')
    # note_food.place(x=53, y= 157)

    # label_amount = tk.Label(msg_list, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_amount.place(x=10, y=177)
    
    # amount_food = tk.Entry(msg_list, width=5, bg='#fff')
    # amount_food.place(x=81, y= 180)

    # button = tk.Button(msg_list, text="ORDER", bg="#20639b", width= 10,
    #                    fg='floral white', height=1)
    # button.place(x=52, y=220)

    # #========== Món 2  ===========
    # canvas1 = Canvas(msg_list, width=176, height=90)
    # canvas1.pack()
    # pilImage1 = Image.open("./image/drink/cafeden.png")
    # pilImage1 = pilImage1.resize((81, 80))  # Resize
    # image1 = ImageTk.PhotoImage(pilImage1)
    # imagesprite1 = canvas1.create_image(95, 45, image=image1)
    # canvas1.place(x=220, y=0)

    # label_name1 = tk.Label(msg_list, text="Cơm chiên",font=LARGE_FONT, fg='#20639b', bg='#fff')
    # label_name1.place(x=260, y=95)

    # label_price1 = tk.Label(msg_list, text="Giá: 35.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    # label_price1.place(x=220, y=130)

    # label_note1 = tk.Label(msg_list, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_note1.place(x=220, y=155)
    
    # note_food1 = tk.Entry(msg_list, width=20, bg='#fff')
    # note_food1.place(x=263, y= 157)

    # label_amount1 = tk.Label(msg_list, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_amount1.place(x=220, y=177)
    
    # amount_food1 = tk.Entry(msg_list, width=5, bg='#fff')
    # amount_food1.place(x=291, y= 180)
    
    # button1 = tk.Button(msg_list, text="ORDER", width = 10,
    #                     bg="#20639b", fg='floral white', height=1)
    # button1.place(x=262, y=220)

    # # Món 3
    # canvas2 = Canvas(msg_list, width=176, height=90)
    # canvas2.pack()
    # pilImage2 = Image.open("./image/drink/cafesua.png")
    # pilImage2 = pilImage1.resize((81, 80))  # Resize
    # image2 = ImageTk.PhotoImage(pilImage2)
    # imagesprite2 = canvas2.create_image(95, 45, image=image2)
    # canvas2.place(x=440, y=0)

    # label_name2 = tk.Label(msg_list, text="Canh gà",
    #                        font=LARGE_FONT, fg='#20639b', bg='#fff')
    # label_name2.place(x=490, y=95)

    # label_price2 = tk.Label(msg_list, text="Giá: 40.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    # label_price2.place(x=440, y=130)

    # label_note2 = tk.Label(msg_list, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_note2.place(x=440, y=155)
    
    # note_food2 = tk.Entry(msg_list, width=20, bg='#fff')
    # note_food2.place(x=483, y= 157)

    # label_amount2 = tk.Label(msg_list, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_amount2.place(x=440, y=177)
    
    # amount_food2 = tk.Entry(msg_list, width=5, bg='#fff')
    # amount_food2.place(x=511, y= 180)

    # button2 = tk.Button(msg_list, text="ORDER", width= 10,
    #                     bg="#20639b", fg='floral white', height=1)
    # button2.place(x=482, y=220)

    # # # Món 4
    # canvas3 = Canvas(msg_list, width=176, height=90)
    # canvas3.pack()
    # pilImage3 = Image.open("./image/drink/capuchino.png")
    # pilImage3 = pilImage3.resize((81, 80))  # Resize
    # image3 = ImageTk.PhotoImage(pilImage3)
    # imagesprite3 = canvas3.create_image(95, 45, image=image3)
    # canvas3.place(x=660, y=0)

    # label_name3 = tk.Label(msg_list, text="Khoai tây lắc",
    #                        font=LARGE_FONT, fg='#20639b', bg='#fff')
    # label_name3.place(x=690, y=95)

    # label_price3 = tk.Label(msg_list, text="Giá: 25.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    # label_price3.place(x=660, y=130)

    # label_note3 = tk.Label(msg_list, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_note3.place(x=660, y=155)
    
    # note_food3 = tk.Entry(msg_list, width=20, bg='#fff')
    # note_food3.place(x=703, y= 157)

    # label_amount3 = tk.Label(msg_list, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_amount3.place(x=660, y=177)
    
    # amount_food3 = tk.Entry(msg_list, width=5, bg='#fff')
    # amount_food3.place(x=731, y= 180)

    # button3 = tk.Button(msg_list, text="ORDER", width= 10,
    #                     bg="#20639b", fg='floral white', height=1)
    # button3.place(x=702, y=220)

    # # # Món 5
    # canvas4 = Canvas(msg_list, width=176, height=90)
    # canvas4.pack()
    # pilImage4 = Image.open("./image/drink/coca.png")
    # pilImage4 = pilImage4.resize((81, 80))  # Resize
    # image4 = ImageTk.PhotoImage(pilImage4)
    # imagesprite4 = canvas4.create_image(95, 45, image=image4)
    # canvas4.place(x=880, y=0)

    # label_name4 = tk.Label(msg_list, text="Gà rán",
    #                        font=LARGE_FONT, fg='#20639b', bg='#fff')
    # label_name4.place(x=930, y=95)

    # label_price4 = tk.Label(msg_list,text="Giá: 30.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    # label_price4.place(x=880, y=130)

    # label_note4 = tk.Label(msg_list, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_note4.place(x=880, y=155)
    
    # note_food4 = tk.Entry(msg_list, width=20, bg='#fff')
    # note_food4.place(x=923, y= 157)

    # label_amount4 = tk.Label(msg_list, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_amount4.place(x=880, y=177)
    
    # amount_food4 = tk.Entry(msg_list, width=5, bg='#fff')
    # amount_food4.place(x=951, y= 180)

    # button4 = tk.Button(msg_list, text="ORDER", width= 10,
    #                     bg="#20639b", fg='floral white', height=1)
    # button4.place(x=922, y=220)

    # # # Món 6
    # canvas5 = Canvas(msg_list, width=176, height=90)
    # canvas5.pack()
    # pilImage5 = Image.open("./image/drink/pepsi.png")
    # pilImage5 = pilImage5.resize((81, 80))  # Resize
    # image5 = ImageTk.PhotoImage(pilImage5)
    # imagesprite5 = canvas5.create_image(95, 45, image=image5)
    # canvas5.place(x=1100, y=0)

    # label_name5 = tk.Label(msg_list, text="Phô mai que",
    #                        font=LARGE_FONT, fg='#20639b', bg='#fff')
    # label_name5.place(x=1120, y=95)

    # label_price5 = tk.Label(msg_list, text="Giá: 15.000đ", font=("Arial bold", 11), fg='#20639b', bg='#fff')
    # label_price5.place(x=1100, y=130)

    # label_note5 = tk.Label(msg_list, text="Note:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_note5.place(x=1100, y=155)
    
    # note_food5 = tk.Entry(msg_list, width=20, bg='#fff')
    # note_food5.place(x=1143, y= 157)

    # label_amount5 = tk.Label(msg_list, text="Số lượng:", font=("verdana", 10), fg='#20639b', bg='#fff')
    # label_amount5.place(x=1100, y=177)
    
    # amount_food5 = tk.Entry(msg_list, width=5, bg='#fff')
    # amount_food5.place(x=1171, y= 180)

    # button5 = tk.Button(msg_list, text="ORDER", width= 10,
    #                     bg="#20639b", fg='floral white', height=1)
    # button5.place(x=1142, y=220)

    # total_name = tk.Label(msg_total, text="Thanh Toán",font=LARGE_FONT, fg='#20639b', bg='#fff')
    # total_name.place(x=420, y=0)

    
    # msg_list.place(x=0, y=120)
    # msg_total.place(x=300, y=300)
    # msg_list1.place(x=240, y=120)
    # msg_list2.place(x=460, y=120)
    # msg_list3.place(x=680, y=120)
    # msg_list4.place(x=900, y=120)
    # msg_list5.place(x=1120, y=120)



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
