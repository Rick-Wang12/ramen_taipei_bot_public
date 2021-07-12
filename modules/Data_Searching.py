# -*- coding: utf-8 -*-
import json


def binary_search(data, value, category):
    target_list = []
    q = -1
    if len(data) % 2 == 0:
        q = (len(data) % 2) -1
    else:
        q = (len(data) // 2)
    
    if q == -1: # Not found
        return

    if value in data[q][category]:
        # 找到符合關鍵字的資料，存入list中
        target_list.append(data[q])
  
        # 找尋資料右側是否還有符合的資料，若無，break
        for i in range(q+1, len(data)+1):
            if value in data[i][category]:
                target_list.append(data[i])
            else:
                break

        # 往左找尋資料左側是否還有符合的資料，若無，break
        for i in range(q-1, -1, -1):
            if value in data[i][category]:
                target_list.append(data[i])
            else:
                break

    elif value > data[q][category]:
        binary_search(data[q+1:], target_list, value, category)
    else:
        binary_search(data[:q], target_list, value, category)


def linear_search(data, value, category):
    target_list = []
    for i in range(len(data)):
        if value in data[i][category[0]]:
            target_list.append(data[i])
    return target_list
    

def text_message_format(src_list):
    message = ""
    for i in range(len(src_list)):
        name = src_list[i]["name"] + "\n"
        address = src_list[i]["address"] + "\n"
        soup_type = src_list[i]["type"] + "\n"

        op_time = ""
        for j in range(len(src_list[i]["營業時間"])):
            if j == len(src_list[i]["營業時間"]) - 1:
                op_time += str(src_list[i]["營業時間"][j])
            else:
                op_time += str(src_list[i]["營業時間"][j]) + "\n"

        op_time = op_time.replace("{", "")
        op_time = op_time.replace("}", "")
        op_time = op_time.replace("'", "")
                
        blog = ""
        for k in range(len(src_list[i]["食記連結"])):
            if k == len(src_list[i]["食記連結"]) - 1:
                blog += str(src_list[i]["食記連結"][k])
            else:
                blog += str(src_list[i]["食記連結"][k]) + "\n"
        blog = blog.replace("{", "")
        blog = blog.replace("}", "")
        blog = blog.replace("'", "")

        google_map = src_list[i]["GoogleMap"]
        message += f"店名: {name}地址: {address}\n營業時間:\n{op_time}\n\n類型: {soup_type}\n食記連結:\n{blog}\n\nGoogleMap連結: {google_map}\n\n"
    return message


class SearchingInJson():
    def __init__(self):
        self.json_file_name = "ramen_store.json"
        with open("ramen_store.json") as f:
            self.data = json.load(f) 
       
        self.data = list(self.data)

        # 將資料以店名做排序 (以利後續使用binary search)
        self.data.sort(key = lambda store: (store.get('name', 0)))

        self.data_size = len(self.data)


    def search_name(self, name):
        target_list = linear_search(data = self.data, value = name, category = ["name"])
        if len(target_list) == 0:
            result = "無該店家資料"
        else:
            result = text_message_format(target_list) 
        return result
 
    
    def search_soup_type(self, soup_type):
        # 尚待修正
        target_list = linear_search(data = self.data, value = soup_type, category = ["type"])
        if len(target_list) == 0:
            result = "該地區無該類型之店家"
        else:
            result = text_message_format(target_list) 
        return result


    def search_district(self, district):
        target_list = linear_search(data = self.data, value = district, category = ["district"])
        if len(target_list) == 0:
            result = "無收錄該區店家"
        else:
            result = text_message_format(target_list) 
        return result


    def printallstores(self):
        result = ""
        for i in range(len(self.data)):
            tmp = self.data[i]["name"]
            tmp = tmp.replace("{", "")
            tmp = tmp.replace("}", "")
            tmp = tmp.replace("'", "")
            result += tmp + "\n"
        return result
    
     
        