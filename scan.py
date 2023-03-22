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
    st.title("SCAN")

    # Membuat kolom untuk menampilkan data barang dan menambahkan barang
    col1, col2 = st.columns(2)

    # # Menambahkan barang dengan kuantitasnya ke dalam database
    # col1.header("Tambah Barang")
    # id_barang = col1.text_input(
    #     "ID Barang", help="Masukan ID barang", value="", placeholder="ID barang")
    # nama_barang = col1.text_input(
    #     "Nama Barang", help="Masukan nama barang", value="", placeholder="Nama barang")
    # kuantitas_stok = col1.number_input("Kuantitas Stok", value=0)

    # if col1.button("Tambahkan Barang"):
    #     add_item_to_db(cursor, connection, id_barang,
    #                    nama_barang, kuantitas_stok)
    #     generate_qr_code(cursor, connection, id_barang, nama_barang)
    #     col1.success(
    #         "Berhasil menambahkan barang ke dalam database!", icon="✅")

    #     # Mengembalikan value dari input field menjadi kosong
    #     nama_barang = ""
    #     kuantitas_stok = 0

    # # Menampilkan data barang yang ada di dalam database
    # col2.header("Daftar Barang")
    # data_barang = read_item_from_db(cursor, connection)
    # col2.dataframe(data_barang, width=500)

    # Membuat kolom untuk QR Code dan QR Code Scanner
    col1, col2 = st.columns(2)

    # Membuat kolom untuk qr code scanner dan mengurangi stok barang
    col1.header("QR Code Scanner")

    # Menggunakan opencv untuk mengambil gambar dari webcam
    run = col1.checkbox('Run')
    camera = cv2.VideoCapture(0)

    if run:
        st.write('Running')
        while True:
            # Capture frame-by-frame
            ret, frame = camera.read()

            # Convert the image to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Create a QR code detector
            detector = cv2.QRCodeDetector()

            # Detect the QR code in the image
            data, bbox, _ = detector.detectAndDecode(gray)

            # Draw the bounding box around the QR code
            if bbox is not None:
                cv2.polylines(frame, [bbox.astype(int)],
                              True, (255, 0, 0), thickness=1)

            cv2.putText(frame, data, (10, 450), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)

            if update_item_in_db(cursor, connection, data):
                col1.success("terdeteksi!")
                interval = 0
                while interval < 100000000:
                    interval += 1

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                st.write('Stopped')
                break

    # # Menampilkan QR Code
    # col2.header("QR Code")
    # id_barang = col2.text_input(
    #     "ID Barang", help="Akan digunakan untuk memunculkan gambar  QR Code", value="", placeholder="Masukan ID barang untuk menampilkan QR Code-nya")
    # if col2.button("Tampilkan QR Code"):
    #     path = read_qr_image_path_from_db(cursor, connection, id_barang)
    #     (qr_path,) = path
    #     col2.image(str(qr_path))
    #     col2.help("QR Code akan terlihat jika ID barang yang dimasukan benar")


# Run the Streamlit app
if __name__ == "__main__":
    main()
