import json
from tkinter import *
import tkinter as tk
from datetime import datetime

file = open("user.json", "r")
data = json.load(file)
    #in từng username và back_acc trong file json
username = input("Nhập user: ")
bank_acc = input("Nhập bank_acc: ")

for i in range(len(data)):
    if username == data[i]["name"] and bank_acc == data[i]["bank_acc"]:
        print("Đăng nhập thành công")
        break
    else:
        print("Đăng nhập thất bại")
        break
    

file.close()

