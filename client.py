
from re import L        #Giúp làm việc với biểu thức chính quy 
#(vd: Tìm kiếm chuỗi,...findall(),search(),split(), sub(),...)
import socket           # Thư viện lập trình Socket
from tkinter import *       # Tạo GUI cho chương trình
import tkinter
import time       # Thư viện thời gian
from tkinter import messagebox  # Hiển thị thông báo
from datetime import datetime    # Hiển thị thời gian
import tkinter as tk

#============== Các biến khởi tạo ban đầu================
FORMAT = 'utf8'
now = datetime.now()
DATE = now.strftime("%y_%m_%d")
LARGE_FONT = ("verdana", 13,"bold")

table_number = 0
first_time = True
top_connect = tk.Tk()
order_list = []
#==============================


#===== Xây dựng GUI cho Table Order =====
def screen_connect():
    top_connect.title("Table Order")
    top_connect.geometry("250x200")
    top_connect.configure(bg="bisque2")

    Label(top_connect, text = "Table number",fg='#20639b',bg="bisque2",font='verdana 14 bold').place(relx = 0.18, rely = 0.1)

    input_table_number = tkinter.StringVar()
    e1 = Entry(top_connect, width = 15, textvariable = input_table_number).place(x = 70, y = 80)

    #===== Bấm Order thì hàm này chạy =====
    def client_connect(event = None):     
        global table_number     
        table_number = input_table_number.get()        #Cho phép người dùng nhập
        # nếu giá trị nhập vào khác số nguyên dương thì thông báo lỗi (sử dụng isdigit() trong string)
        if table_number.isdigit() == False:
            messagebox.showinfo("Error", "Vui lòng nhập số bàn")
            return
        
        if table_number == "": 
            messagebox.showinfo('Message ','Bạn chưa nhập số bàn')
            on_closing()
        else:
            client.send(table_number.encode(FORMAT))    #Gửi cho server biết table_number
            time.sleep(0.01)
            msg = client.recv(1024).decode(FORMAT)  #Nhận kiểm tra số bàn từ server
            global first_time
            if msg == "first_time":
                messagebox.showinfo('Message ','Connect first time')

            elif msg == "not_first_time": 
                first_time = False
                messagebox.showinfo('Message ','Connect')
            screen_homepage()
    
    #===== Khi người dùng nhấn nút [X] thì đóng cửa sổ ngắt kết nối đến server =====
    def on_closing():
        client.send("quit".encode(FORMAT))      #Gửi lện server bị thông báo người dùng đóng cửa sổ ngắt kết nối đến server
        client.close()
        top_connect.destroy()

    button_login = Button (top_connect,text="Table Order",bg="#20639b",fg='floral white',height= "1",width="15", activeforeground = "black", activebackground = "blue", command= client_connect)
    button_login.place(x=60,y=120)

    # top_connect.protocol("WM_DELETE_WINDOW", on_closing)
    top_connect.mainloop()


#===== Xây dựng GUI cho HOMEPAGE =====
def screen_homepage():
    def screen_order_food():
        top_homepage.destroy()       #xóa cái box screen_homepage
        msg = "menu"
        client.send(msg.encode(FORMAT))
        msg = client.recv(1024).decode(FORMAT)
        count = int(msg)
        global food_name
        global food_price
        global food_note
        global food_image
        food_name = []
        food_price = []
        food_note = []
        food_image = []
        for i in range(count):
            msg = client.recv(1024).decode(FORMAT)
            food_name.append(msg)
            msg = client.recv(1024).decode(FORMAT)
            food_price.append(msg)
            msg = client.recv(1024).decode(FORMAT)
            food_note.append(msg)
            msg = client.recv(1024).decode(FORMAT)
            food_image.append(msg)

        entry = {}
        label = {}
        
        top_order_food = tk.Tk()
        top_order_food.title("Menu")
        top_order_food.state('zoomed')
        
        Label(top_order_food, text = "STT",fg='#20639b',font='verdana 15 bold ').grid(row=0, column=0, padx = 30, pady = 30)
        Label(top_order_food, text = "TÊN MÓN",fg='#20639b',font='verdana 15 bold ').grid(row=0, column=1, padx = 30, pady = 30)
        Label(top_order_food, text = "GIÁ TIỀN",fg='#20639b',font='verdana 15 bold ').grid(row=0, column=2, padx = 30, pady = 30)
        Label(top_order_food, text = "NOTE",fg='#20639b',font='verdana 15 bold ').grid(row=0, column=3, padx = 85, pady = 30)
        Label(top_order_food, text = "SỐ LƯỢNG",fg='#20639b',font='verdana 15 bold ').grid(row=0, column=4, padx = 40, pady = 30)
        Label(top_order_food, text = "HÌNH ẢNH",fg='#20639b',font='verdana 15 bold ').grid(row=0, column=5, padx = 70, pady = 30)

        
        frame = Frame(top_order_food)
        frame.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.7)
        canvas = Canvas(frame)
        canvas.pack(side="left", fill="both", expand=1)

        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        second_frame = Frame(frame)
        canvas.create_window((0, 0), window=second_frame, anchor="nw")
        x = 1
        y = 1
        z = 1
        t = 1
        g = 1
        stt = 1
        while (stt <= len(food_name)):
            lbName = Label(second_frame, text=stt,font='verdana 12')
            lbName.grid(row=g, column=0, padx = 30)
            stt += 1
            g += 1

        for Name in food_name:
            e = Entry(second_frame,font='verdana 14',width=10)
            e.grid(row=x, column=4, padx = 30)
            entry[Name] = e

            lbName = Label(second_frame, text=Name,font='verdana 12')
            lbName.grid(row=x, column=1, padx = 30)
            label[Name] = lbName
            x += 1

        for Price in food_price:
            lbPrice = Label(second_frame, text=Price,font='verdana 12')
            lbPrice.grid(row=y, column=2, padx = 50)
            label[Price] = lbPrice
            y += 1

        for Note in food_note:
            lbNote = Label(second_frame, text=Note,font='verdana 12')
            lbNote.grid(row=z, column=3, padx = 30)
            label[Note] = lbNote
            z += 1

        for Img in food_image:
            photo = PhotoImage(file=Img)
            lbImage = Label(second_frame, image = photo, text=Img)
            lbImage.image = photo
            lbImage.grid(row=t, column=5, padx = 80)
            t += 1
            
        def print_all_entries():
            #================== HÀM HỦY ĐƠN HÀNG ==================
            def cancel_order():
                pay.destroy()
                order_list.clear()
            #================== THANH TOÁN BẰNG TIỀN MẶT ===========================
            def pay_cash():
                Label(pay, text="Payment: Cash",fg='#20639b',bg="bisque2",font='verdana 15 bold ').place(relx = 0.1, rely = 0.57)
                Label(pay, text="Nhập số tiền hiện có: ",fg='#20639b',bg="bisque2",font='verdana 11 bold ',width=30).place(relx = 0.06, rely = 0.63)
                cash = Entry(pay)
                cash.place(relx = 0.15, rely = 0.7)
                #================== hàm lấy số tiền hiện có ==================
                def get_money():
                    temp = cash.get()
                    # nếu giá trị nhập vào khác số nguyên dương thì thông báo lỗi (sử dụng isdigit() trong string)
                    if temp.isdigit() == False:
                        messagebox.showerror("Error", "Vui lòng nhập số tiền [0-9]")
                    else:
                        if temp == "":
                            messagebox.showinfo('Message ','Bạn chưa nhập gì !!!Vui lòng nhập số tiền hiện có')
                        else:
                            current_money = int(temp)
                            if current_money < int(total):
                                messagebox.showinfo('Message ','Số tiền không đủ ')
                            else:
                                msg = "order"
                                client.send(msg.encode(FORMAT))
                                for i in range(len(order_list)):
                                    client.send(order_list[i].encode(FORMAT))
                                    time.sleep(0.01)

                                remain = int(current_money) - int(total)
                                Label(pay, text="Tiền dư: " + str(format(remain, ',d')) + " VNĐ",fg='#20639b',bg="bisque2",font='verdana 13 bold ').place(relx = 0.4, rely = 0.78)
                                messagebox.showinfo('Message ','Thanh toán thành công')
                                pay.destroy()
                            
                Button(pay, text="Thanh toán", command=get_money).place(relx = 0.38, rely = 0.698)

            #================== THANH TOÁN BẰNG THẺ ==================
            def pay_card():
                Label(pay, text="Payment: Card",fg='#20639b',bg="bisque2",font='verdana 15 bold ').place(relx = 0.1, rely = 0.57)
                Label(pay, text="Nhập số thẻ: ",fg='#20639b',bg="bisque2",font='verdana 11 bold ',width=30).place(relx = 0.06, rely = 0.63)
                card = Entry(pay)
                card.place(relx = 0.15, rely = 0.7)
                #================== hàm lấy số thẻ  ==================
                def get_card():
                    temp = card.get()   # lấy số thẻ từ Entry
                    # nếu giá trị nhập vào khác số nguyên dương thì thông báo lỗi (sử dụng isdigit() trong string)
                    if temp.isdigit() == False:
                        messagebox.showinfo('Error ','Vui lòng nhập số thẻ [0-9]')
                    else:
                        if temp == "":
                            messagebox.showinfo('Message ','Bạn chưa nhập gì !!!Vui lòng nhập số thẻ 10 số')
                        else:
                            length = str(temp)  # kiểm tra số thẻ nhập = 10 hay không
                            if len(length) != 10 :
                                messagebox.showinfo('Message ','Vui lòng nhập số thẻ 10 số')
                            else:
                                msg = "order"
                                client.send(msg.encode(FORMAT))
                                for i in range(len(order_list)):
                                    client.send(order_list[i].encode(FORMAT))
                                    time.sleep(0.01)
                                messagebox.showinfo('Message ','Thanh toán thành công')
                                pay.destroy()

                Button(pay, text="Thanh toán", command=get_card).place(relx = 0.38, rely = 0.698)
            
            #================== CỬA SỔ CHỌN MÓN ĂN ==================
            for name in food_name:
                 # nếu giá trị '' thì gán lại thành 0
                if entry[name].get() == '':
                    entry[name].insert(0, '0')
                # nếu giá trị nhập vào khác số nguyên dương thì thông báo lỗi (sử dụng isdigit() trong string)
                if entry[name].get().isdigit() == False:
                    messagebox.showinfo('Message ','Vui lòng nhập số lượng món ăn. Xin cảm ơn!')
                    order_list.clear()
                    return
                else:
                    order_list.append(entry[name].get())     # lưu số lượng món ăn vào order_list
            # print (order_list)

            # ================== TÍNH TỔNG TIỀN ==================
            total = 0
            for i in range(len(order_list)):
                total += int(order_list[i]) * int(food_price[i]) # tính tổng tiền của món ăn
            if total == 0:
                messagebox.showinfo('Message ','Bạn chưa chọn món ăn nào. Vui lòng chọn món. Xin cảm ơn!')
                total = 0
                order_list.clear()
                return
            # print ('Tổng tiền:', total)

            #================== TẠO CỬA SỔ THANH TOÁN ==================
            top_order_food.destroy()
            pay = tk.Tk()
            pay.title("Payment")
            pay.geometry("600x600")
            pay.configure(bg="bisque2")
            Label(pay, text="Thanh toán",fg='#20639b',bg="bisque2",font='verdana 20 bold ').place(relx = 0.35, y = 15)
            #================== tạo frame hiển thị món đã đặt và scrollbar ==================
            frame = Frame(pay, bg="bisque2")
            frame.place(relx = 0, rely = 0.2, relwidth = 1, relheight = 0.3)
            scrollbar = Scrollbar(frame)
            scrollbar.pack(side=RIGHT, fill=Y)
            listbox = Listbox(frame, yscrollcommand=scrollbar.set,font='Arial 13 ',fg='#000', bg="bisque2")
            listbox.place(relx = 0, rely = 0, relwidth = 0.97, relheight = 1)    
            scrollbar.config(command=listbox.yview)

            #================== HIỂN THỊ MÓN ĐÃ ĐẶT RA MÀN HÌNH PAYMENT ==================
            count = 1   # biến đếm số món ăn đã đặt vào màn hình
            for i in range(len(order_list)):
                if order_list[i] == '0':         # nếu order_list[i] = 0 thì không hiển thị món ăn này
                    continue
                price = str(format(int(food_price[i]), ',d'))       # chuyển đổi giá trị thành chuỗi với dấu phẩy thập phân (5000 -> 5,000)
                temp_total = str(format(int(order_list[i]) * int(food_price[i]), ',d'))

                listbox.insert(END, str(count) + '.' + ' ' + food_name[i] + ':    ' + order_list[i] + ' x ' + price + " = " + temp_total)
                count += 1

            #================== tạo button thanh toán và hàm thanh toán ==================
            Label(pay, text="Tổng tiền:",fg='#e60000',bg="bisque2",font='verdana 14 ').place(relx = 0.1, rely = 0.5)
            #================== hiển thị tổng tiền với đơn vị vnđ ==================
            Label(pay, text=str(format(total, ',d')) + " VNĐ",fg='#e60000',bg="bisque2",font='verdana 14 bold').place(relx = 0.3, rely = 0.5)
            Button(pay, text="Tiền mặt",bg="#20639b",fg='floral white',height= "1",width="15", activeforeground = "black", activebackground = "blue", command = pay_cash).place(relx = 0.2, rely = 0.85)
            Button(pay, text="Thẻ",bg="#20639b",fg='floral white',height= "1",width="15", activeforeground = "black", activebackground = "blue", command=pay_card).place(relx = 0.4, rely = 0.85)
            Button(pay, text="Hủy",bg="#20639b",fg='floral white',height= "1",width="15", activeforeground = "black", activebackground = "blue", command= cancel_order).place(relx = 0.6, rely = 0.85)
            Label(pay, text="Thank you for your order",fg='#20639b',bg="bisque2",font='verdana 12 ').place(relx = 0.35, rely = 0.95)

        #================== Button ORDER ==================
        b = Button(top_order_food, text="ORDER",bg="#20639b",fg='floral white',font='Arial 13 bold',height= "2", width="20", command=print_all_entries)
        b.place(relx = 0.32, rely = 0.9)

        top_order_food.mainloop()

    #================== CỬA SỔ ORDER FOOD ==================
    top_connect.destroy()       #xóa cái box screen_connect
    global table_number     
    top_homepage = tk.Tk()         #tạo box mới (homepage)
    title = "HOME - TABLE " + str(table_number)
    top_homepage.title(title)
    top_homepage.geometry("300x300")
    top_homepage.configure(bg="bisque2")
    
    button_order = Button (top_homepage,text="Order food",bg="#20639b",fg='floral white',height= "2", width="25", activeforeground = "black", activebackground = "blue", command= screen_order_food)
    button_order.place(relx=0.2,rely=0.4)
        
    top_homepage.mainloop()
    


HOST = "127.0.0.1" 
SERVER_PORT = 8030
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tạo socket
client.connect( (HOST, SERVER_PORT) )
screen_connect()
