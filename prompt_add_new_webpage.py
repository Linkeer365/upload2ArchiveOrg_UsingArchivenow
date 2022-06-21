import sqlite3

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

conn=sqlite3.connect("./ArchiveMePlease/webpage.db")
cur=conn.cursor()

head_str="https://web.archive.org/web/"
head_len=len(head_str)
date_str_len = len ("20220313143510")

flag=1

while flag==1:
    ask=input("archive link or a no: ")
    if ask.startswith(head_str):
        date_str=ask[head_len:head_len+date_str_len]
        link=ask[head_len+date_str_len+1:]
        archive_link=ask
        print(f"date_str:{date_str}\nori_link:{link}\narchive_link:{archive_link}\n\n")
        date=get_format_date(date_str)
        pack=(date,link,archive_link)
        # insert or replace
        cur.execute("insert or replace into wp (format_date,link,versions) values (?,?,?)",pack)
    elif ask == "no":
        flag=0

conn.commit()
print("done.")