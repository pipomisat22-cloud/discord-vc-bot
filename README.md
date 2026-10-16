# Discord VC Bot 🤖

บอท Discord ที่เข้าห้อง Voice แบบปิดหูปิดไมค์ตลอด

## คำสั่ง
| คำสั่ง | ฟังก์ชัน |
|--------|---------|
| `!join` | เข้าห้องเดียวกับคนพิมพ์ |
| `!join ชื่อห้อง` | เข้าห้องที่ระบุ |
| `!leave` | ออกจากห้อง |
| `!status` | เช็คสถานะ |

## Deploy บน Render

1. Push code นี้ขึ้น GitHub
2. ไปที่ [render.com](https://render.com) → New Web Service
3. เชื่อม GitHub repo
4. ตั้งค่า Environment Variable: `DISCORD_TOKEN` = token ของคุณ
5. Deploy!

## รันในเครื่อง
```bash
pip install -r requirements.txt
python bot.py
```
