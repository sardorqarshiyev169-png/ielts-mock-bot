# 🎯 IELTS Computer-Delivered Mock Platform & Telegram Bot

Haqiqiy **British Council** va **IDP Computer-Delivered (CD-IELTS)** imtihon muhitini to'liq o'zida mujassam etgan Telegram Mini App va Telegram Bot tizimi.

---

## ✨ Asosiy Imkoniyatlar

1. 💻 **Rasmiy CD-IELTS Interfeysi (Telegram Mini App):**
   - **Split-Screen Ko'rinish:** Chap tomonda akademik matn (Passage) yoki audio pleyer, o'ng tomonda interaktiv savollar.
   - **Savol Turlari:** *True / False / Not Given*, *Multiple Choice*, *Summary / Sentence Completion (Fill in the blanks)*, *Matching Headings*.
   - **Pastki Navigatsiya Palitrasi:** 1 dan 40 gacha savol katakchalari (yechilgan, yechilmagan, `Review` belgisi qo'yilgan).
   - **Matnni Belgilash (Highlighter):** Real imtihondagi kabi matnni sariq rang bilan belgilash va tozalash imkoniyati.
   - **Imtihon Taymeri:** 60:00 daqiqalik teskari sanagich. Vaqt tugaganda avtomatik topshirish.

2. 🎧 **Listening Audio Generatsiyasi (Edge-TTS):**
   - Sun'iy intellekt orqali tabiiy Britaniya (`en-GB-SoniaNeural`, `en-GB-RyanNeural`) va Avstraliya (`en-AU-NatashaNeural`) talaffuzidagi listening audiolari avtomatik generatsiya qilinadi.

3. 🤖 **"O'zi ham topa oladigan" AI Material Finder:**
   - Ixtiyoriy mavzuni kiriting (masalan: *Climate Change, Space Exploration, History of Marine Navigation*) yoki bo'sh qoldiring.
   - Tizim 1 bosishda to'liq 800-1000 so'zli akademik matn, 10-14 ta savol, to'g'ri kalitlar va tahliliy izohlarni (explanations) avtomatik generatsiya qilib bazaga saqlaydi!

4. 📋 **Material Joylash juda oson (Quick Text Import):**
   - Adminlar xohlagan IELTS testini oddiy matn ko'rinishida ko'chirib Mini App ichidagi import oynasiga tashlashi kifoya.
   - Tizim avtomatik savollar, variantlar va javob kalitlarini ajratib oladi.

5. 🏅 **Avtomatik Baholash va IELTS Band Kalkulyatori:**
   - Test topshirilgach, javoblar avtomatik tekshirilib, Cambridge IELTS jadvali bo'yicha **1.0 dan 9.0 gacha Band Score** hisoblanadi.
   - Har bir savol bo'yicha to'g'ri/noto'g'ri tahlili va matndan keltirilgan isbot-izoh ko'rsatiladi.

---

## 🚀 Ishga Tushirish (Qadam-ba-qadam)

### 1-qadam: Sozlamalar (`.env` fayli)
Loyiha papkasidagi `.env` faylini oching va Telegram Bot tokenni kiriting:
```env
BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRstuVWXyz
WEB_HOST=0.0.0.0
WEB_PORT=8080
WEBAPP_URL=http://localhost:8080
ADMIN_IDS=12345678
GEMINI_API_KEY=
```
*(Eslatma: `GEMINI_API_KEY` kiritilmasa ham tizim ichidagi o'rnatilgan aqlli test generatsiyasi to'liq ishlaydi!)*

### 2-qadam: Serverni yoqish
Windowsda loyiha papkasidagi **`start.bat`** faylini ikki marta bosing yoki terminalda:
```bash
py run.py
```
Buyrug'ini bajaring.

Brauzerda darhol ko'rish uchun: **`http://localhost:8080`** manziliga kiring.

---

## 📲 Telegram Bot & Mini App ni ulash

1. Telegramda [@BotFather](https://t.me/BotFather) botiga kiring.
2. `/newbot` buyrug'i orqali yangi bot yarating va tokenni `.env` faylidagi `BOT_TOKEN` ga yozing.
3. BotFather ga `/newapp` buyrug'ini yuboring:
   - Botni tanlang.
   - Mini App nomini yozing (masalan: `IELTS Mock Pro`).
   - Tavsif va rasm kiriting.
   - WebApp URL so'raganda o'zingizning havolangizni yuboring (Masalan: `ngrok http 8080` yoki Cloudflare tunnel orqali olingan HTTPS havola).
4. BotFather ga `/setmenubutton` buyrug'ini yuborib, bot menyu tugmasini Mini App havolasiga ulang.

---

## 📁 Loyiha Tuzilishi

```
ielts-mock-bot-tma/
├── backend/
│   ├── config.py              # Konfiguratsiya va yo'llar
│   ├── database.py            # SQLite ma'lumotlar bazasi (testlar, natijalar)
│   ├── server.py              # Aiohttp REST API va Mini App static host
│   ├── bot.py                 # Aiogram 3 Telegram Bot boshqaruvi
│   ├── material_finder.py     # AI Mock Generator & Tezkor matn importi
│   ├── seed_data.py           # Cambridge formatidagi tayyor mock testlar
│   ├── tts_service.py         # Listening uchun Britaniya/Avstraliya ovozlari
│   └── band_calculator.py     # Rasmiy IELTS Band 1.0 - 9.0 kalkulyatori
├── frontend/
│   ├── index.html             # Telegram Mini App asosiy interfeysi (SPA)
│   ├── css/
│   │   └── style.css          # CD-IELTS highlighter va maxsus stillar
│   └── js/
│       └── app.js             # Mini App to'liq dinamik logikasi va taymer
├── data/
│   ├── audio/                 # Listening audio fayllari
│   └── ielts.db               # SQLite bazasi
├── .env                       # Muhit o'zgaruvchilari
├── run.py                     # Asosiy ishga tushiruvchi dastur
├── start.bat                  # Windows 1-klik ishga tushirish skripti
└── README.md                  # Ushbu qo'llanma
```

---

## 📋 Matndan Tezkor Test Qo'shish Formati (Namuna)

Mini App ichidagi **Materiallar** bo'limida quyidagi formatda matn tashlansa, tizim uni avtomatik testga aylantiradi:

```text
TITLE: Sun'iy Intellekt va Tibbiyot
PASSAGE:
Paragraph A
Sun'iy intellekt tibbiyot diagnostikasida ulkan yutuqlarga erishmoqda...

Paragraph B
Radiologiya sohasida algoritmlar rentgen tasvirlarini 98% aniqlik bilan tahlil qilmoqda...

QUESTIONS:
1. Sun'iy intellekt rentgen tasvirlarini qanday aniqlikda tahlil qiladi?
A) 85%
B) 90%
C) 95%
D) 98%
ANSWER: D
EXPLANATION: Paragraph B matnida 98% aniqlik aniq ko'rsatilgan.

2. Rentgen tahlilini yaxshilash uchun yangi usullar qo'llanilmoqda.
ANSWER: TRUE
EXPLANATION: Paragraph B radiologiya algoritmlari haqida so'z boradi.
```
