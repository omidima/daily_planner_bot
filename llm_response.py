import requests

model_url = f"https://chat.barikalla.com/api/chat/completions"
model_key = "sk-221bb7ead0ea4528b2c056b886734f4a"

def new_program_prompt(targets: str, work: str, sleep: str): 
    return f'''# Context:
    تو یک دستار برنامه ریزی هستی که قراره به من کمک کنی در رابطه با هدف‌های یکماهه‌ای که به تو میدم به صورت روزانه و هدفگذازی هفتگی به من کمک کنی تا در پایان ماه هدف‌های من کامل بشند و به صورت زیر به من نمایش میدهی.

    | نام روز | تسک | هدف | زمان شروع | زمان پایان | توضیحات | اهمیت | 
    | -- | -- | -- | -- | -- | -- |

    کاربر به صورت روزانه گزارشی از فعالیت‌هایش برای تو ارسال میکند که بر اساس آن در صورت نیاز باید برنامه روزانه شخص را تغییر- دهی.

    برخی دستورات نیز برای وجود دارند که در صورتی که کاربر آنها را ارسال کرد باید متناسب با دستوری که نوشته میشود با آن رفتار کنید.

    ## دستورات:
    - done <task name>: با اینکار هدف ماهانه‌ای که تایین شده بود به پایان رسیده است و باید از لیست کارهای روزانه حدف گردد.
    - next week: پیاده‌سازی کردن برنامه روزانه برای هفته جدید.
    - next day: برگرداندن برنامه روز بر اساس نام آن
    - update plan: توضیحاتی برای تغییر در روند برنامه‌ریزی
    - send report: دریافت گزارشی از روند کارهای روزانه، بررسی و برگرداندن برنامه روز بعد

    ## در برنامه‌ریزی این موارد را در نظر بگیر.
    - زمان خواب فرد.
    - میزان زمان کاری
    - کارهایی که در روز باید حتما انجام شود
    - کارهایی که در صورت به اتمام رساندن کارهای مهم روزانه، میتوان آنها را انجام داد تا از برنامه جلو افتاد.

    # Information:
    ## اهداف ماهانه
    {targets}

    ## اطلاعات فردی
    میزان خواب: {sleep}
    میزان ساعات کاری: {work}
    '''

def send_message(history = [], message:str = ""):
    history = []
    history.extend({"role": item.role, "content": item.content}
                    for item in history)

    history.append({"role": "user", "content": message})

    print(f"history len: {len(history)}")

    data = requests.post(model_url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {model_key}"
    }, json={
            "model": "gpt-4-turbo-free",
            "messages": history,
            "temperature": 0.7
        }).json()

    text = data["choices"][0]["message"]["content"]

    return text