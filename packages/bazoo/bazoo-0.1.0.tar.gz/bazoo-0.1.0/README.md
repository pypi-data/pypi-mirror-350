# Bazoo - کتابخانه غیررسمی بازواستور

کتابخانه غیررسمی پایتون برای دسترسی به API بازواستور. این کتابخانه امکان جستجو و دریافت اطلاعات ربات‌ها از سرویس بازواستور را فراهم می‌کند.

## بازواستور چیست؟

بازواستور (BazooStore) یک فروشگاه ربات برای پیام‌رسان بله است که امکان جستجو و استفاده از ربات‌های مختلف را برای کاربران فراهم می‌کند. این کتابخانه به شما امکان دسترسی به API بازواستور را می‌دهد.

## نصب

```bash
pip install bazoo
```

## استفاده

```python
import bazoo

# دریافت برترین ربات‌ها
best_bots = bazoo.GetBestBots(offset=1)
if best_bots["ok"]:
    for bot in best_bots["result"]:
        print(bot["name"])

# جستجوی ربات با نام
search_results = bazoo.SearchBazoo("calculator")
if search_results["ok"]:
    for bot in search_results["result"]:
        print(bot["name"], bot["username"])

# دریافت اطلاعات کامل یک ربات
bot_info = bazoo.GetDataBot("calculator_bot")
if bot_info["ok"]:
    print(bot_info["result"]["description"])
```

## توابع موجود

- `GetBestBots(offset=1)` - دریافت برترین ربات‌ها
- `GetNewBots(offset=1)` - دریافت جدیدترین ربات‌ها
- `GetRandomBazoo()` - دریافت ربات‌های تصادفی
- `SearchBazoo(name, searched_by="name")` - جستجوی ربات (با نام یا توضیحات)
- `GetDataBot(username)` - دریافت اطلاعات کامل یک ربات

## پیش‌نیازها

- Python 3.6+
- کتابخانه Requests

## نویسنده

این کتابخانه توسط حمیدرضا نوشته شده است.

## لایسنس

MIT
