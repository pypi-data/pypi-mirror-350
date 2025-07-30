"""
کتابخانه غیررسمی جستجوی ربات در سرویس بازواستور

این کتابخانه توسط محمدرضا با آیدی :
@python_php
در پیام رسان بله نوشته شده است


در این کتابخانه بجای نام ربات از واژه ی فارسی آن استفاده شده یعنی بازو

پیش نیاز ها :
requests
"""

import requests

BaseURL = "https://api.bazoostore.ir"


def GetBestBots(offset: str | int = 1):
    """برای دریافت بازو هایی که جز برترین بازو ها هستند به کار می رود"""
    try:
        return {
            "ok": True,
            "result": list(
                requests.get(
                    f"{BaseURL}/best",
                    json={
                        "offset": str(offset)
                    }
                ).json()["value"]
            )
        }
    except:
        return {
            "ok": False
        }


def GetNewBots(offset: str | int = 1):
    """برای دریافت بازو هایی که جدیدا به بازو استور اضافه شدند به کار می رود"""
    try:
        return {
            "ok": True,
            "result": list(
                requests.get(
                    f"{BaseURL}/bot",
                    json={
                        "offset": str(offset)
                    }
                ).json()["value"]
            )
        }
    except:
        return {
            "ok": False
        }


def GetRandomBazoo():
    """برای دریافت ربات های تصادفی استفاده می شود"""
    try:
        return {
            "ok": True,
            "result": list(
                requests.get(
                    f"{BaseURL}/random"
                ).json()["value"]
            )
        }
    except:
        return {
            "ok": False
        }


def SearchBazoo(NameBazoo: str, searched_by: str = "name"):
    """
    برای جستجوی ربات در بازو استور به کار می رود

    در صورتی که می خواهید بر اساس توضیحات ، ربات مورد نظرتان را جستجو کنید :
    searched_by = "caption"
    """
    try:
        return {
            "ok": True,
            "result": list(
                requests.post(
                    f"{BaseURL}/search",
                    json={
                        "search_params": str(NameBazoo),
                        "searched_by": str(searched_by)
                    }
                ).json()["value"]
            )
        }
    except:
        return {
            "ok": False
        }


def GetDataBot(UsernameBot: str):
    """برای دریافت اطلاعات یک ربات خاص استفاده می شود"""
    try:
        DataBot = requests.get(
            f"{BaseURL}/random/{UsernameBot}"
        ).json()["value"]
        return {
            "ok": True,
            "result": {
                "id": DataBot[0]["id"],
                "name": DataBot[0]["name"],
                "chat_id": DataBot[0]["chat_id"],
                "username": DataBot[0]["username"],
                "description": DataBot[0]["description"],
                "photo": DataBot[0]["photo"],
                "track_id": DataBot[0]["track_id"],
                "created_at": DataBot[0]["created_at"],
                "average": DataBot[1]["average"],
                "count": DataBot[1]["count"]
            }
        }
    except:
        return {
            "ok": False
        }
