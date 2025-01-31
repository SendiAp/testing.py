import qrcode
from pyrogram import Client, filters

API_ID = '20211998'
API_HASH = 'beeeebe74c0c467c47c6ac4a1c9d75b5'
BOT_TOKEN = '7829549841:AAG4XR8ZlkJUpkmZPQCu6Df25Xz5H73HpVY'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("qris"))
def send_qris(client, message):
    qris_data = (
        "00020101021126670016COM.NOBUBANK.WWW01189360050300000879140214522563481268110303UMI"
        "51440014ID.CO.QRIS.WWW0215ID20253689702290303UMI5204541153033605802ID5927SENDIADININGTIAS"
        "OK21790706006BEKASI61051711162070703A01630407DE5403ID10.000"
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qris_data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image_path = "qris.png"
    qr_image.save(qr_image_path)

    client.send_photo(chat_id=message.chat.id, photo=qr_image_path, caption="QRIS Dinamis Anda dengan Jumlah 10.000 IDR")

@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(message.chat.id, "Selamat datang! Kirim /qris untuk mendapatkan QRIS dinamis.")

if __name__ == "__main__":
    app.run()
