import pymysql
from tkinter import *

# Veritabanı bağlantı bilgilerini güncelleyin
host = 'localhost'
user = 'root'
password = 'Tedarik25'
database = 'deneme'

# Butonun tıklanma olayı
def button_clicked():
    # Veritabanına bağlan
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    # Tablodan en büyük ilk 5 skoru sorgula
    query = "SELECT score FROM skortablosu1 ORDER BY score DESC LIMIT 5"
    cursor.execute(query)
    result = cursor.fetchall()

    # Skorları bir liste içinde sakla
    scores = [row[0] for row in result]

    # Sonuçları projede göster
    # Örneğin, bir label üzerine yazdırabilirsiniz
    result_label.configure(text="\n".join(map(str, scores)))

    # Bağlantıyı kapat
    cursor.close()
    conn.close()

# Pencere oluştur
window = Tk()

# Butonu oluştur
button = Button(window, text="Skorları Göster", command=button_clicked)
button.pack()

# Sonuçların gösterileceği bir label oluştur
result_label = Label(window, text="")
result_label.pack()

# Pencereyi çalıştır
window.mainloop()