import os
import csv
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(A, B):
    return dot(A, B)/(norm(A)*norm(B))

db_path = "C:\\Users\\cbseo\\Desktop\\test\\2. DB"
result_path = "C:\\Users\\cbseo\\Desktop\\test\\3. compdeg"

precision = []
recall = []
f1 = []
case_num = [[],[],[],[]]
file_list = os.listdir(db_path)
file_list_db = [file for file in file_list if file.endswith("Database.csv")]
for db_file in file_list_db:
    load_path = db_path + "\\" + db_file
    db_load = pd.read_csv(load_path)
    device_list = set(db_load["device"])
    for test_device in device_list:
        test_db = db_load[(db_load["device"] == test_device)&(db_load["0"] == "step 0")]
        test_indexs = test_db.loc[:, test_db.columns.tolist()[:4]].values 
        test_values = test_db.loc[:, test_db.columns.tolist()[5:]].values
        for db_device in device_list:
            db_db = db_load[(db_load["device"] == db_device)&(db_load["0"] == "step 1")]
            db_indexs = db_db.loc[:, db_db.columns.tolist()[:4]].values
            db_values = db_db.loc[:, db_db.columns.tolist()[5:]].values
            temp_val = []
            row_f = [test_indexs[0][1] +"-"+ db_indexs[0][1],]
            for index_t, value_t in enumerate(test_values):
                line_val = [test_indexs[index_t][3]]
                for index_db, value_db in enumerate(db_values):
                    if(index_t == 0):
                        row_f.append(test_indexs[index_db][3])
                    line_val.append(cosine_similarity(value_t,value_db))
                if(index_t == 0):
                    temp_val.append(row_f)
                temp_val.append(line_val)
            df_comp = pd.DataFrame(temp_val)
            store_path = result_path + "\\" + test_indexs[index_t][0] + "\\" + test_indexs[index_t][1] 
            filename = test_indexs[index_t][0]+"("+test_indexs[index_t][1] +"-"+ db_indexs[index_t][1]+").csv"
            df_comp.to_csv(store_path +"\\"+ filename, sep=',', header = False, index = False)
            print(filename+"---------done")