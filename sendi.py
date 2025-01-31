import requests
import random
from io import BytesIO
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message

API_CREATE_QRIS = "https://qris-ku.autsc.my.id/api/create"
QRIS_CODE = "00020101021226670016COM.NOBUBANK.WWW01189360050300000879140214449214512358760303UMI51440014ID.CO.QRIS.WWW0215ID20253689485890303UMI52045411540310053033605802ID5918VPN STORE OK5893096011PROBOLINGGO61056721162070703A0163044F6A"
API_CHECK_PAYMENT = "https://mutasiv2.vercel.app/check-payment"
MERCHANT = "OK589309u"
KEY = "63963571734356150589309OKCTA1E2209D4DFDBD0D0785600B911F1126"

app = Client("my_bot")

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply_text("Masukkan nominal transaksi")

@app.on_message(filters.text & ~filters.command)
def process_amount(client, message: Message):
    try:
        amount = int(message.text)
        random_addition = random.randint(1, 50)
        final_amount = amount + random_addition

        response = requests.get(API_CREATE_QRIS, params={"amount": final_amount, "qrisCode": QRIS_CODE})

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                download_url = data["data"]["download_url"]
                image_response = requests.get(download_url)

                if image_response.status_code == 200:
                    image = Image.open(BytesIO(image_response.content))
                    bio = BytesIO()
                    bio.name = 'qris.png'
                    image.save(bio, 'PNG')
                    bio.seek(0)
                    client.send_photo(chat_id=message.chat.id, photo=bio, caption=f"✅ QRIS berhasil dibuat!\n\n💰 Nominal: {data['data']['formatted_amount']}\n📌 Fee: {random_addition}\n⏳ QRIS berlaku selama 5 menit\n\n🔄 Menunggu pembayaran...")

                    check_payment(client, message.chat.id, final_amount)

                else:
                    message.reply_text("❌ Gagal mengambil gambar QRIS.")
            else:
                message.reply_text(f"❌ Error: {data.get('message', 'Unknown error.')}")
        else:
            message.reply_text("❌ Gagal memproses permintaan. Coba lagi nanti.")
    except ValueError:
        message.reply_text("⚠️ Masukkan angka yang valid!")

def check_payment(client, chat_id, amount):
    response = requests.get(API_CHECK_PAYMENT, params={"merchant": MERCHANT, "key": KEY})

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success" and data["data"]:
            for payment in data["data"]:
                if payment["amount"] == amount:
                    client.send_message(chat_id=chat_id, text="✅ *Pembayaran berhasil diterima!*\n\nTerima kasih atas transaksi Anda.", parse_mode="Markdown")
                    return

if __name__ == "__main__":
    app.run()
