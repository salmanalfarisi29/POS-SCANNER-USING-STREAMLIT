import pymysql
import streamlit as st
import cv2
import qrcode


def generate_qr_code(cursor, connection, id, item_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = "./" + item_name + ".png"
    img.save(filename)
    add_qr_image_path_to_db(cursor, connection, id, filename)


def connect_to_db(port, user, password, database):
    connection = pymysql.connect(
        host="localhost", port=port, user=user, passwd=password, database=database)
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def add_qr_image_path_to_db(cursor, connection, id, qr_image_path):
    query = "UPDATE stok_barang SET qr_image_path = %s WHERE id_barang = %s;"
    cursor.execute(query, (qr_image_path, id))
    connection.commit()


def read_qr_image_path_from_db(cursor, connection, id) -> tuple:
    query = "SELECT qr_image_path FROM stok_barang WHERE id_barang = %s;"
    cursor.execute(query, (id))
    return cursor.fetchone()


def read_item_from_db_by_id(cursor, connection, id) -> tuple:
    query = "SELECT stok FROM stok_barang WHERE id_barang = %s;"
    cursor.execute(query, (id))
    return cursor.fetchone()


def add_item_to_db(cursor, connection, id, item_name, stock_quantity):
    query = "INSERT INTO stok_barang (id_barang, nama, stok) VALUES (%s, %s, %s);"
    cursor.execute(query, (id, item_name, stock_quantity))
    connection.commit()


def update_item_in_db(cursor, connection, id) -> bool:
    stok_tp = read_item_from_db_by_id(cursor, connection, id)
    if stok_tp is None:
        return False
    (stok, ) = stok_tp
    if int(stok) == 0:
        return False
    stok -= 1
    query = "UPDATE stok_barang SET stok = %s WHERE id_barang = %s;"
    cursor.execute(query, (stok, id))
    connection.commit()
    return True


def delete_item_from_db(cursor, connection, id):
    query = "DELETE FROM stok_barang WHERE id_barang = %s;"
    cursor.execute(query, (id))
    connection.commit()


def read_item_from_db(cursor, connection):
    query = "SELECT id_barang, nama, stok FROM stok_barang;"
    cursor.execute(query)
    return cursor.fetchall()
 
def main():
    connection, cursor = connect_to_db(3306, "root", "", "dbpenjualan")
    # st.title("INPUT BARANG")

    # Membuat kolom untuk menampilkan data barang dan menambahkan barang
    col1, col2 = st.columns(2)
 
 # Menampilkan data barang yang ada di dalam database
    col1.header("Daftar Barang")
    data_barang = read_item_from_db(cursor, connection)
    col1.dataframe(data_barang, width=500)

# Run the Streamlit app
if __name__ == "__main__":
    main()

