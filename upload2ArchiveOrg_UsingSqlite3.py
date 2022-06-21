import sqlite3
import sys
import time

from datetime import datetime

from archivenow import archivenow

webpage=dict(format_date="",link="",versions=[])

head = len ("https://web.archive.org/web/")
head_str="https://web.archive.org/web/"
date_str_len = len ("20220313143510")

# check change_or_stable

def is_change_or_stable(link):
    change_or_stable="unknown"
    change_types={"linkeer365.github.io"}
    stable_types={"twitter.com"}
    for ct in change_types:
        if ct in link:
            change_or_stable="change"
            return change_or_stable
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

fail_path=""

prom=input("inside or linkeer365[ins/lin]: ")
if prom=="ins":
    with open("./ArchiveMePlease/inside_links.txt","r",encoding="utf-8") as f:
        links=[e.strip("\n") for e in f.readlines() if e!="\n"]
    fail_path="./ArchiveMePlease/inside_links.txt"
elif prom=="lin":
    with open("./ArchiveMePlease/linkeer_links.txt","r",encoding="utf-8") as f:
        links=[e.strip("\n") for e in f.readlines() if e!="\n"]
    fail_path="./ArchiveMePlease/linkeer_links.txt"

conn=sqlite3.connect("./ArchiveMePlease/webpage.db")
cur=conn.cursor()

already_links=[e[0] for e in cur.execute("select link from wp").fetchall()]

items=[]

# links=["https://linkeer365.github.io/Linkeer365ColorfulLife/60380/"]

# def test():
#     raw_date="20210127053440"
#     format_date=get_format_date(raw_date)
#     format_date_obj=datetime.strptime (format_date, "%Y-%m-%d %H:%M:%S")
#     now_obj=datetime.now()
#     time_delta=now_obj-format_date_obj
#     hours=time_delta.seconds/3600
#     if hours<24:
#         print("change: old versions!")
#         print("fail...")

# test()
# sys.exit(0)

fails=[]

with open(r"D:\upload2ArchiveOrg_UsingArchivenow\impossible_links.txt","r",encoding="utf-8") as f:
    impossible_links=[each.strip("\n") for each in f.readlines() if each!="\n"]

already_links.extend(impossible_links)

for idx,link in enumerate(links,1):
    print("第{}个（共{}个）".format(idx,len(links)))
    start_at=time.time()
    change_or_stable=is_change_or_stable(link)
    if "linkeer365.github.io" in link and "\'" in link:
        link=link.replace("\'","")
    # print("type:",change_or_stable)
    if change_or_stable!="change":
        if link in already_links:
            print("ok.")
            continue
        else:
            # print("begin:",link)
            # 因为有些像 b23.tv 这种link，在archive上去的时候会转为 bilibili.com/这种，那这样就不能用所谓的 head/web/raw_date/link 来索引了，必须直接存储archive_link

            archive_link=archivenow.push(link,"ia")[0]
            raw_date=archive_link[head:head+date_str_len]
            if not raw_date.isdigit():
                print("stable: not digit...")
                print("fail...")
                fails.append(link)
                continue
            format_date=get_format_date(raw_date)
            versions=archive_link
            item=(format_date,link,versions)
            cur.execute("insert into wp (format_date,link,versions) values (?,?,?)",item)
    elif change_or_stable=="change":
        if not link in already_links:
            archive_link=archivenow.push(link,"ia")[0]
            raw_date=archive_link[head:head+date_str_len]
            if not raw_date.isdigit():
                print("change: not digit...")
                print("fail...")
                fails.append(link)
                continue
            format_date=get_format_date(raw_date)
            format_date_obj=datetime.strptime (format_date, "%Y-%m-%d %H:%M:%S")
            now_obj=datetime.now()
            time_delta=now_obj-format_date_obj
            hours=time_delta.seconds/3600
            if hours>24:
                print("change: old versions!")
                print("fail...")
                fails.append(link)
                continue
            versions=archive_link
            item=(format_date,link,versions)
            cur.execute("insert into wp (format_date,link,versions) values (?,?,?)",item)
        else:
            already_versions = [e[0] for e in cur.execute ("select versions from wp where link=\"{}\"".format (link)).fetchall ()][0]
            print(already_versions)
            prev_version=already_versions.split(",")[0]
            period=30
            prev_date=prev_version.replace(head_str,"").replace(link,"").replace("/","")
            now_obj=datetime.now()
            print(prev_date)
            prev_obj = datetime.strptime (prev_date, "%Y%m%d%H%M%S")
            duration=now_obj-prev_obj
            days=duration.seconds/(24*3600)
            if days<period:
                print("less than {} days!".format(period))
                continue
            else:
                archive_link = archivenow.push (link, "ia")[0]
                raw_date = archive_link[head:head + date_str_len]
                if not raw_date.isdigit():
                    print("change: not digit...")
                    print("fail...")
                    fails.append(link)
                    continue
                format_date = get_format_date (raw_date)
                format_date_obj=datetime.strptime (format_date, "%Y%m%d%H%M%S")
                now_obj=datetime.now()
                time_delta=now_obj-format_date_obj
                hours=time_delta.seconds/3600
                if hours>24:
                    print("change: old versions!")
                    print("fail...")
                    fails.append(link)
                    continue
                versions=archive_link+","+already_versions
                item = (format_date, link, versions)
                cur.execute ("update wp set format_date={}, versions = {} where link={}".format(item[0],item[2],item[1]))
    conn.commit()
    get_timespent(start_at)
    print("one done.")

fails_s="\n".join(fails)

with open(fail_path,"w",encoding="utf-8") as f:
    f.write(fails_s)





