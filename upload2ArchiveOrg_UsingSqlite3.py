import sqlite3
import sys
import time

from datetime import datetime

from archivenow import archivenow

webpage=dict(format_date="",link="",versions=[])

head = len ("https://web.archive.org/web/")
date_str_len = len ("20220313143510")

# check change_or_stable

def is_change_or_stable(link):
    change_or_stable="unknown"
    change_types={"linkeer365.com"}
    stable_types={"twitter.com"}
    for ct in change_types:
        if ct in link:
            change_or_stable="change"
            return
    for st in stable_types:
        if st in link:
            change_or_stable="stable"
            return change_or_stable
    return change_or_stable

def get_format_date(raw_str):
    # print("raw_str:",raw_str)
    year=raw_str[0:4]
    month=raw_str[4:6]
    day=raw_str[6:8]
    hour=raw_str[8:10]
    min=raw_str[10:12]
    sec=raw_str[12:14]
    date="{}-{}-{} {}:{}:{}".format(year,month,day,hour,min,sec)
    print("date:",date)
    return date

def get_timespent(prev_time):
    now_at=time.time()
    time_spent=now_at-prev_time
    print("用时: {} s".format(time_spent))

# date=get_date("https://web.archive.org/web/20220313143510/https://stackoverflow.com/questions/19477916/python-class-keyword-arguments")
# date_obj=datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
# print(type(date_obj))
# sys.exit(0)

with open("./ArchiveMePlease/inside_links.txt","r",encoding="utf-8") as f:
    links=[e.strip("\n") for e in f.readlines() if e!="\n"]

conn=sqlite3.connect("./ArchiveMePlease/webpage.db")
cur=conn.cursor()

already_links=[e[0] for e in cur.execute("select link from wp").fetchall()]

items=[]

for idx,link in enumerate(links,1):
    print("第{}个（共{}个）".format(idx,len(links)))
    start_at=time.time()
    change_or_stable=is_change_or_stable(link)
    # print("type:",change_or_stable)
    if change_or_stable!="change":
        if link in already_links:
            print("ok.")
            continue
        else:
            archive_link=archivenow.push(link,"ia")[0]
            if link in archive_link:
                raw_date=archive_link[head:head+date_str_len]
                if not raw_date.isdigit():
                    print("fail...")
                    continue
                format_date=get_format_date(raw_date)
                versions=raw_date
                item=(format_date,link,versions)
                cur.execute("insert into wp (format_date,link,versions) values (?,?,?)",item)
            else:
                print("fail...")
                get_timespent(start_at)
                continue
    elif change_or_stable=="change":
        if not link in already_links:
            archive_link=archivenow.push(link,"ia")[0]
            if link in archive_link:
                raw_date=archive_link[head:head+date_str_len]
                if not raw_date.isdigit():
                    print("fail...")
                    continue
                format_date=get_format_date(raw_date)
                versions=raw_date
                item=(format_date,link,versions)
                cur.execute("insert into wp (format_date,link,versions) values (?,?,?)",item)
            else:
                print ("fail...")
                get_timespent(start_at)
                continue
        else:
            already_versions = [e[0] for e in cur.execute ("select versions from wp where link={}".format (link)).fetchall ()]
            prev_version=already_versions.split(",")[0]
            period=10
            now_obj = datetime.strptime (raw_date, "%Y%m%d%H%M%S")
            prev_obj = datetime.strptime (prev_version, "%Y%m%d%H%M%S")
            duration=now_obj-prev_version
            if duration.days<period:
                print("less than {} days!".format(period))
                continue
            else:
                archive_link = archivenow.push (link, "ia")[0]
                if link in archive_link:
                    raw_date = archive_link[head:head + date_str_len]
                    if not raw_date.isdigit():
                        print("fail...")
                        continue
                    format_date = get_format_date (raw_date)
                    versions=raw_date+","+already_versions
                    item = (format_date, link, versions)
                    cur.execute ("update wp set format_date={}, versions = {} where link={}".format(item[0],item[2],item[1]))
                else:
                    print ("fail...")
                    get_timespent (start_at)
                    continue
    conn.commit()
    get_timespent(start_at)
    print("one done.")
    # items.append(item)





