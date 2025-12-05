import base64
import hashlib
import os
import random
import re
from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

SECRET_KEY = os.getenv("SECRET_KEY", "SerialQt@2025#Secure")

app = FastAPI(title="Password Generator API")

# Allow same-origin and simple local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def generate_password(target_date: date) -> str:
    """Generate an 8-character password based on date and secret."""
    date_num = target_date.month * 100 + target_date.day
    raw = f"{date_num}{SECRET_KEY}".encode()
    digest = hashlib.sha256(raw).digest()
    encoded = base64.b64encode(digest).decode()
    clean = re.sub(r"[^a-zA-Z0-9]", "", encoded)
    clean = re.sub(r"[O0Il1]", "", clean).upper()
    if len(clean) < 8:
        raise HTTPException(status_code=500, detail="Failed to generate password")
    return clean[:8]


@app.get("/api/password")
def get_password(
    date_str: Optional[str] = Query(
        None, alias="date", description="ISO date, e.g. 2025-12-03"
    ),
    month: Optional[int] = Query(None, ge=1, le=12),
    day: Optional[int] = Query(None, ge=1, le=31),
):
    """
    Generate password for a given date.
    Priority: date param -> month/day -> today.
    """
    if date_str:
        try:
            target = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD)")
    elif month and day:
        try:
            target = date(date.today().year, month, day)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid month/day combination")
    else:
        target = date.today()

    password = generate_password(target)
    return {"date": target.isoformat(), "password": password}


@app.get("/api/background")
def get_background():
    """获取随机背景图片 URL（Picsum 4K）"""
    timestamp = random.randint(1, 100000)
    return {"url": f"https://picsum.photos/3840/2160?random={timestamp}"}


# 名人名言 + 牛马语录（100条）
QUOTES = [
    # 经典名言（30条）
    {"text": "生活不是等待暴风雨过去，而是学会在雨中跳舞。", "author": "尼采"},
    {"text": "世上只有一种英雄主义，就是在认清生活真相之后依然热爱生活。", "author": "罗曼·罗兰"},
    {"text": "你的时间有限，不要浪费在重复别人的生活上。", "author": "乔布斯"},
    {"text": "成功不是终点，失败也不是末日，重要的是继续前进的勇气。", "author": "丘吉尔"},
    {"text": "人生就像骑自行车，想保持平衡就得往前走。", "author": "爱因斯坦"},
    {"text": "千里之行，始于足下。", "author": "老子"},
    {"text": "天行健，君子以自强不息。", "author": "周易"},
    {"text": "路漫漫其修远兮，吾将上下而求索。", "author": "屈原"},
    {"text": "知之者不如好之者，好之者不如乐之者。", "author": "孔子"},
    {"text": "黑夜无论怎样悠长，白昼总会到来。", "author": "莎士比亚"},
    {"text": "不要等待机会，而要创造机会。", "author": "林肯"},
    {"text": "宝剑锋从磨砺出，梅花香自苦寒来。", "author": "古训"},
    {"text": "海纳百川，有容乃大。", "author": "林则徐"},
    {"text": "业精于勤，荒于嬉；行成于思，毁于随。", "author": "韩愈"},
    {"text": "读书破万卷，下笔如有神。", "author": "杜甫"},
    {"text": "三人行，必有我师焉。", "author": "孔子"},
    {"text": "学而不思则罔，思而不学则殆。", "author": "孔子"},
    {"text": "己所不欲，勿施于人。", "author": "孔子"},
    {"text": "人生自古谁无死，留取丹心照汗青。", "author": "文天祥"},
    {"text": "长风破浪会有时，直挂云帆济沧海。", "author": "李白"},
    {"text": "会当凌绝顶，一览众山小。", "author": "杜甫"},
    {"text": "不积跬步，无以至千里。", "author": "荀子"},
    {"text": "生于忧患，死于安乐。", "author": "孟子"},
    {"text": "穷则独善其身，达则兼济天下。", "author": "孟子"},
    {"text": "书山有路勤为径，学海无涯苦作舟。", "author": "韩愈"},
    {"text": "纸上得来终觉浅，绝知此事要躬行。", "author": "陆游"},
    {"text": "少壮不努力，老大徒伤悲。", "author": "汉乐府"},
    {"text": "静以修身，俭以养德。", "author": "诸葛亮"},
    {"text": "勿以恶小而为之，勿以善小而不为。", "author": "刘备"},
    {"text": "老骥伏枥，志在千里。", "author": "曹操"},
    # 牛马语录（70条）
    {"text": "今天工作不努力，明天努力找工作。", "author": "打工人"},
    {"text": "累吗？累就对了，舒服是留给有钱人的。", "author": "牛马"},
    {"text": "打工可能会少活十年，不打工你一天也活不下去。", "author": "社畜"},
    {"text": "没有困难的工作，只有勇敢的牛马。", "author": "职场"},
    {"text": "上班的心情比上坟还沉重。", "author": "打工人"},
    {"text": "工资就像大姨妈，一个月来一次，一周就没了。", "author": "牛马"},
    {"text": "我不是在上班，就是在上班的路上。", "author": "社畜"},
    {"text": "别人上班挣钱，我上班赔钱，比如交通费、餐费、咖啡钱。", "author": "打工人"},
    {"text": "职场如战场，我是炮灰。", "author": "牛马"},
    {"text": "我命由我不由天，加班由老板说了算。", "author": "社畜"},
    {"text": "早起的鸟儿有虫吃，早起的虫儿被鸟吃，我是虫。", "author": "打工人"},
    {"text": "干不完的活，睡不够的觉，永远在线的微信。", "author": "牛马"},
    {"text": "世上无难事，只要肯放弃。", "author": "摸鱼人"},
    {"text": "钱没挣到，班没少上，觉没少熬，头发没少掉。", "author": "打工人"},
    {"text": "有一种饿叫做老板觉得你不饿，有一种累叫老板觉得你不累。", "author": "社畜"},
    {"text": "每天醒来第一句，先给自己打个气：今天也要努力搬砖！", "author": "牛马"},
    {"text": "生活不止眼前的苟且，还有下个月的房租。", "author": "打工人"},
    {"text": "周一到周四不想上班，周五在等下班。", "author": "社畜"},
    {"text": "要是没有买房的压力，谁愿意做一辈子牛马。", "author": "牛马"},
    {"text": "人生就是起起落落落落落落落落……", "author": "打工人"},
    {"text": "打工人打工魂，打工都是人上人。", "author": "牛马"},
    {"text": "老板的心思你别猜，猜来猜去也白猜。", "author": "社畜"},
    {"text": "加班加点，只为那点碎银几两。", "author": "牛马"},
    {"text": "敢上九天揽月，敢下五洋捉鳖，但不敢迟到早退。", "author": "社畜"},
    {"text": "不是工作需要我，而是我需要工作。", "author": "牛马"},
    {"text": "上班就是为了下班，下班就是为了明天上班。", "author": "社畜"},
    {"text": "我为公司流过血，公司让我随时撤。", "author": "打工人"},
    {"text": "爱情诚可贵，自由价更高，若为工资故，两者皆可抛。", "author": "牛马"},
    {"text": "年年打工年年愁，天天加班何时休。", "author": "社畜"},
    {"text": "生容易，活容易，生活不容易。", "author": "打工人"},
    {"text": "上班如上坟，心情特别沉。", "author": "牛马"},
    {"text": "人在曹营心在汉，身在工位魂在床。", "author": "社畜"},
    {"text": "干最多的活，挨最多的骂，拿最少的钱。", "author": "打工人"},
    {"text": "老板说今晚不加班，我感动哭了，然后他说明天补上。", "author": "牛马"},
    {"text": "我不是想躺平，我是真的累了。", "author": "社畜"},
    {"text": "工作使我快乐，如果不快乐，一定是工作还不够多。", "author": "打工人"},
    {"text": "生活以痛吻我，我却报之以上班。", "author": "牛马"},
    {"text": "别问我为什么这么努力，因为我想换个地方当牛马。", "author": "社畜"},
    {"text": "努力不一定成功，但不努力一定很舒服。", "author": "摸鱼人"},
    {"text": "每月总有那么30几天不想上班。", "author": "打工人"},
    {"text": "我上班就是为了钱，别跟我谈理想，我的理想是不上班。", "author": "牛马"},
    {"text": "上班一条虫，下班一条龙，周末回笼觉。", "author": "社畜"},
    {"text": "这个月工资到手，发现又可以交房租了。", "author": "打工人"},
    {"text": "当你觉得累的时候，想想你还没工作会更累。", "author": "牛马"},
    {"text": "都说三百六十行，行行出状元，我怎么行行都不行。", "author": "社畜"},
    {"text": "不怕同事是学霸，就怕同事放暑假。", "author": "打工人"},
    {"text": "贫穷限制了我的想象力，工资限制了我的购买力。", "author": "牛马"},
    {"text": "有时候真想躺平，但一想到房贷，算了继续卷。", "author": "社畜"},
    {"text": "曾经我以为我能改变世界，现在世界改变了我。", "author": "打工人"},
    {"text": "梦想是要有的，万一实现了呢？算了先上班吧。", "author": "牛马"},
    {"text": "人生没有白走的路，每一步都算加班。", "author": "社畜"},
    {"text": "今天又是元气满满的一天，谁信呢？", "author": "打工人"},
    {"text": "我不是懒，我只是在节省能量。", "author": "摸鱼人"},
    {"text": "加油打工人！月底还有信用卡等着你呢。", "author": "牛马"},
    {"text": "工作虐我千百遍，我待工作如初恋，因为穷。", "author": "社畜"},
    {"text": "你问我为什么眼里常含泪水？因为加班加得深沉。", "author": "打工人"},
    {"text": "别跟我说底层逻辑顶层设计，我只想准时下班。", "author": "牛马"},
    {"text": "人活着就是为了上班，上班是为了有钱活着。", "author": "社畜"},
    {"text": "工资是负债的唯一来源。", "author": "打工人"},
    {"text": "今天也是没有被开除的一天呢，值得庆祝。", "author": "牛马"},
    {"text": "世界那么大我想去看看，钱包那么小哪也去不了。", "author": "社畜"},
    {"text": "愿你出走半生，归来仍是牛马。", "author": "打工人"},
    {"text": "我的人生巅峰就是每个月发工资那一秒。", "author": "牛马"},
    {"text": "如果你觉得生活很难，那是因为你没钱。", "author": "真理"},
    {"text": "上班苦上班累，上班还得交社保。", "author": "社畜"},
    {"text": "我不想上班，只想躺着数钱，可惜没钱可数。", "author": "打工人"},
    {"text": "成年人的崩溃，往往从周一早上开始。", "author": "牛马"},
    {"text": "别人的周末是休息，我的周末是缓刑。", "author": "社畜"},
    {"text": "小时候觉得最难的是作业，长大了发现那叫快乐。", "author": "打工人"},
    {"text": "我的钱包比我的脸还干净。", "author": "牛马"},
]


@app.get("/api/quote")
def get_quote():
    """获取随机名人名言"""
    return random.choice(QUOTES)


# Serve static frontend
app.mount("/", StaticFiles(directory=".", html=True), name="static")
