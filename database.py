import mysql.connector as mc
import pickle
import numpy as np
from pathlib import Path

def insert(id_cat, array, path,  db):
    # Mmemasukan data fitur ke dataset
    try:
        if db.is_connected():
            cursor = db.cursor()
            # Insert data id_cat, fitur, path 
            sql = "INSERT INTO feature (id_cat, array, path) VALUES (%s, %s, %s)"
            val = (id_cat, pickle.dumps(array), path)
            cursor.execute(sql, val)

            db.commit()

    except mc.Error as e:
        print("Gagal saat menghubungkan ke MySQL", e)       

def select(db, category):
    # Menampilkan dataset
    try:
        if db.is_connected():
            cursor = db.cursor()
            # Menampilkan semua data sesuai id kategori
            sql = f"SELECT array, path FROM feature WHERE id_cat = {category}"
            cursor.execute(sql)
            result = cursor.fetchall()

            # Menampilkan nama kategori dari id_cat
            select_label = f"SELECT label FROM category WHERE id_cat = '{category}'"
            cursor.execute(select_label)
            label = cursor.fetchone()

            features = []
            img_paths = []
            for index in range(len(result)):
                # [index] adalah list dan didalamnya ada tuple [(array, path), (array, path)]
                # [0] di dalam list terdapat kumpulan tuple yang isinya (array, path)

                # Mencari label untuk dijadikan path folder dataset gambar
                img_paths.append(Path(f"./static/dataset/{label[0]}") / (result[index][1]))

                # Me-load binary image
                features.append(pickle.loads(result[index][0]))
                
            
            return np.array(features), img_paths

    except mc.Error as e:
        print("Gagal saat menghubungkan ke MySQL", e)

def check(label, db):
    # Check ketersediaan kategori 
    try:
        if db.is_connected():
            cursor = db.cursor()
            sql = f"SELECT id_cat FROM category WHERE label = '{label}'"
            cursor.execute(sql)

            result = cursor.fetchone()

            return result

    except mc.Error as e:
        print("Gagal saat menghubungkan ke MySQL", e)