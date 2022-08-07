from ctypes import sizeof #cho phép bạn sử dụng các lib sẵn có thừ một ngôn ngữ khác (foreign function library)
import os       #cung cấp các chức năng để tương tác với hệ điều hành
                #cho phép chúng ta làm việc với các tập tin và thư mục.
import socket   # Thư viện lập trình Socket
from tkinter.constants import FALSE, S, TRUE    # Thư viện tkinter chứa tất cả các hằng số
from threading import Thread     #cung cấp nhiều hỗ trợ mạnh mẽ và cấp độ cao hơn cho các Thread để triển khai đa luồng
from time import time, sleep    # Thư viện time để làm việc với thời gian
import json             # Thư viện json
from tkinter import *   # Thư viện tkinter (GUI)
from datetime import datetime
import os.path      # Thư viện os.path để kiểm tra tồn tại file

LARGE_FONT = ("verdana", 15, "bold")
now = datetime.now()
# Định dạng ngày/tháng/năm của thời điểm chạy server
DATE = now.strftime("%y_%m_%d")
FORMAT = "utf8"  # Định dạng chuỗi gửi đến client (tiếng việt)

countFood = 0  # Số lượng món ăn có trong menu
Food_Name = []
Food_Price = []

# ====== Chấp nhận kết nối các client ========
def accept_client():
    while True:
        conn, addr = s.accept()
        print("client address:", addr, "đã kết nối")
        try:
            # Tạo luồng cho các client, mỗi luồng một client chạy riêng
            Thread(target=handle_client, args=(conn, addr,)).start()
        except:
            # Nếu bên Client bị ngắt kết nối đột ngột, server sẽ được thông báo
            print("Client", addr, "đã ngưng kết nối do lỗi!!!")
            conn.close()  # Đóng kết nối của Client đó
            return


def menu(conn):
    with open("menu.json", "r", encoding='utf8') as fin:  # Mở file chứa Menu
        data = json.load(fin)
    global countFood
    countFood = 0       # mỗi lần mở server -> reset số lượng món về 0
    for i in data:      # Lặp qua từng món ăn trong menu
        countFood += 1  # Đếm số lượng món ăn
    conn.send(str(countFood).encode(FORMAT))  # Gửi số lượng món ăn đến client
    global Food_Name
    global Food_Price
    Food_Name.clear()
    Food_Price.clear()

    for i in data:
        conn.send(i["Name"].encode(FORMAT))  # Gửi tên món ăn đến client
        Food_Name.append(i["Name"])  # Lưu tên món ăn vào Food_Name
        sleep(0.01)

        conn.send(i["Price"].encode(FORMAT))  # Gửi giá món ăn đến client
        Food_Price.append(i["Price"])  # Lưu giá món ăn vào Food_Price
        sleep(0.01)

        conn.send(i["Note"].encode(FORMAT))  # Gửi ghi chú món ăn đến client
        sleep(0.01)

        conn.send(i["Image"].encode(FORMAT))  # Gửi ghi chú hình ảnh món ăn đến client
        sleep(0.01)
        fin.close()  # Đóng file menu.json


class Food:
    def __init__(self, food_name, food_price, food_count):  # Hàm khởi tạo
        self.food_name = food_name  # Gán tên món ăn vào food_name
        self.food_price = food_price  # Gán giá món ăn vào food_price
        self.food_count = food_count  # Gán số lượng món ăn vào food_count

    def getName(self):  # Hàm lấy tên món ăn
        return self.food_name

    def getPrice(self):  # Hàm lấy giá món ăn
        return self.food_price

    def getCount(self):  # Hàm lấy số lượng món ăn
        return self.food_count

    def dump(self):  # Hàm lưu thông tin món ăn vào file
        return {
            "List order": {
                'Name': self.food_name,
                'Price': self.food_price,
                'Count': self.food_count}
        }


def write_json(new_data, filename):     # Hàm ghi dữ liệu vào file json
    with open(filename, 'r+') as file:
        file_data = json.load(file)     # Đọc dữ liệu từ file json
        # Thêm dữ liệu vào file json
        # chuyển đổi new_data về dạng utf8

        file_data["List Order"].append(new_data)
        # Đặt vị trí hiện tại của file là 0 (đưa con trỏ về đầu file)
        file.seek(0)
        json.dump(file_data, file, indent=5, separators=(
            ", ", ": "))   # Ghi dữ liệu vào file json
        file.close()                         # Đóng file json


def order(conn, table_number):      # Hàm đặt bàn
    list = []                   # Tạo list chứa thông tin món ăn đặt bàn từ client
    # list_order chứa thông tin hoàn tất (bao gồm: tên món ăn, giá, số lượng)
    list_order = []
    total_money = 0         # Tạo biến để lưu tổng tiền đơn hàng
    for i in range(countFood):
        msg = conn.recv(1024).decode(FORMAT)
        list.append(msg)        # Thêm thông tin món ăn vào list
    count = 0
    for i in list:
        if i == '0':        # nếu list[i] = 0 thì bỏ qua
            count += 1
            continue
        # Lấy tên món ăn từ Food_Name theo vị trí count
        food_name = Food_Name[count]
        food_price = Food_Price[count]
        food_count = int(i)
        # Tính tổng tiền của món ăn (giá * số lượng)
        total_money += int(food_price) * food_count
        # Thêm thông tin món ăn vào list_order
        list_order.append(Food(food_name, food_price, food_count))
        count += 1

    current_time = datetime.now().strftime('%Y-%m-%d%H:%M:%S')  # Lấy thời gian hiện tại
    file_name = str(table_number) + '.json' # Tên file json của bàn đã đặt
    with open(file_name, "w") as file_write:        # Ghi dữ liệu vào file ordered.json
        json.dump({
            'Table': table_number,
            'List Order': [],
            'Total': total_money,
            'Time': current_time,
            'Status': "unfinished"}, file_write, indent=5, separators=(", ", ": ")) # separators=(", ", ": ") để có dấu phẩy trong file json. Ngăn Python thêm các khoảng trắng ở cuối
        file_write.close()                                                          # indent=5 để có khoảng trắng (thụt lề) trong file json -> hiển thị đẹp mắt hơn

    for i in list_order:
        
        x = {'Name': i.getName(), 'Price': i.getPrice(), 'Count': i.getCount()}     # Lấy thông tin món ăn vào dict x
        write_json(x, file_name)

# ====== Nhận số bàn từ client ======
def handle_client(conn, addr):
    try:
        table_number = conn.recv(1024).decode(FORMAT)       # Nhận số bàn từ client
        if table_number == "quit":
            print("------------> User quit")
            conn.close()

        # check table xem có trống hay không
        checkTableNumber(conn, table_number)

        # ===== Nếu người dùng nhập chữ "quit" vào ô "Table" thì sẽ thoát chương trình
        def receive_stop():
            receive = input()
            if input == 'quit':
                conn.send(receive.encode(FORMAT))
        stop_thread = Thread(target=receive_stop)
        stop_thread.start()

        while True:
            msg = conn.recv(1024).decode(FORMAT)
            if msg == "menu":                          # Nhận menu
                menu(conn)                          # Gửi menu
            elif msg == "order":                  # Nhận đặt bàn
                order(conn, table_number)       # Gửi đặt bàn
            else:
                msg2 = conn.recv(1024).decode(FORMAT)   
    except:
        print("Client", addr, "đã ngưng kết nối do lỗi!!!")
        return


def checkTableNumber(conn, table_number):
    file_name = str(table_number) + '.json' # Tên file json của bàn đã đặt
    file_exists = os.path.exists(file_name)     # Kiểm tra file json của bàn đã đặt tồn tại hay chưa
    if file_exists == True:             # Nếu tồn tại
        message = "not_first_time"      
        conn.send(message.encode(FORMAT))   # Gửi lời nhắn "not_first_time"
    else:
        if (table_number != "quit" and table_number != ""): # Nếu không là "quit" và không rỗng
            x = {"table_number": table_number}
            with open(file_name, "w") as file_write:
                json.dump(x, file_write)
        message = "first_time"
        conn.send(message.encode(FORMAT))


# =====Khai báo HOST và PORT cho server=====
HOST = "127.0.0.1"
SERVER_PORT = 8030

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, SERVER_PORT))

# Hàm main
if __name__ == "__main__":
    s.listen(5)
    print("SERVER RUNNING")
    print("server:", HOST, SERVER_PORT)
    print("Chờ kết nối từ các client...")
    ACCEPT_THREAD = Thread(target=accept_client)    # Tạo thread nhận kết nối từ client
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    s.close()
