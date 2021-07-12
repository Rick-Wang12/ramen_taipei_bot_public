# -*- coding: utf-8 -*-

import sys, os
sys.path.append("..")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])

from modules.Data_Searching import *

def text_message_format(r):
    name = r["name"]
    address = r["address"]

    op_time = ""
    for j in range(len(r["營業時間"])):
        #op_time += "          "
        if j == len(r["營業時間"]) - 1:
            op_time += str(r["營業時間"][j])
        else:
            op_time += str(r["營業時間"][j]) + "\n"
        

    op_time = op_time.replace("{", "")
    op_time = op_time.replace("}", "")
    op_time = op_time.replace("'", "")
            
    blog = ""
    for k in range(len(r["食記連結"])):
        
        if k == len(r["食記連結"]) - 1:
            blog += str(r["食記連結"][k])
        else:
            blog += str(r["食記連結"][k]) + "\n"
    blog = blog.replace("{", "")
    blog = blog.replace("}", "")
    blog = blog.replace("'", "")

    google_map = r["GoogleMap"]
    message = f"店名: {name}\n地址:{address}\n\n營業時間:\n{op_time}\n\n食記連結:\n{blog}\n\nGoogleMap連結: {google_map}\n"
    return message


def test_print_all_data():
    search = SearchingInJson()
    result = search.printallstores()
    print(result)

def test_search_store(name):
    search = SearchingInJson()
    r = search.search_name(name)
    if r != "查無店家資料":
        print(r)
    else:
        print("查無店家資料")

print()
test_search_store("道樂")
print("-" * 100 + "\n")
test_print_all_data()

print()