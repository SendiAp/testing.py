import qrcode
from pyrogram import Client, filters

API_ID = '20211998'
API_HASH = 'beeeebe74c0c467c47c6ac4a1c9d75b5'
BOT_TOKEN = '7829549841:AAG4XR8ZlkJUpkmZPQCu6Df25Xz5H73HpVY'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

import requests
from pyrogram import Client, filters

@app.on_message(filters.command("qris"))
def send_qris(client, message):
    create_qris_url = "https://qris-ku.autsc.my.id/api/create?amount=5000&qrisCode=00020101021126670016COM.NOBUBANK.WWW01189360050300000879140214522563481268110303UMI51440014ID.CO.QRIS.WWW0215ID20253689702290303UMI5204541153033605802ID5927SENDI ADININGTIAS OK21790706006BEKASI61051711162070703A01630407DE"

    response = requests.get(create_qris_url)

    if response.status_code == 200:
        data = response.json()
        download_url = data.get("data", {}).get("download_url")

        if download_url:
            qr_image_response = requests.get(download_url)

            if qr_image_response.status_code == 200:
                qr_image_path = "qris.png"
                with open(qr_image_path, 'wb') as f:
                    f.write(qr_image_response.content)

                client.send_photo(chat_id=message.chat.id, photo=qr_image_path, caption="QRIS Dinamis Anda dengan Jumlah Rp 5.000")
            else:
                client.send_message(chat_id=message.chat.id, text="Gagal mengunduh gambar QRIS. Silakan coba lagi nanti.")
        else:
            client.send_message(chat_id=message.chat.id, text="Tidak dapat menemukan URL gambar QRIS.")
    else:
        client.send_message(chat_id=message.chat.id, text="Gagal membuat QRIS. Silakan coba lagi nanti.")
        
@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(message.chat.id, "Selamat datang! Kirim /qris untuk mendapatkan QRIS dinamis.")

if __name__ == "__main__":
    app.run()
