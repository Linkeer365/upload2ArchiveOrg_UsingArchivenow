import os
import re

import subprocess

# import requests

bookmarks_path=r"C:\Users\linsi\AppData\Local\CentBrowser\User Data\Default\Bookmarks"

check_url="https://archive.org/"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

output_path=r"D:\ArchiveMePlease\output.txt"

already_path=r"D:\ArchiveMePlease\already_upload.txt"

bad_links_path=r"D:\ArchiveMePlease\fail_to_upload.txt"

outer_links_path=r"D:\ArchiveMePlease\outer_links.txt"

def get_links(folder_name):
    with open(bookmarks_path,"r",encoding="utf-8") as f:
        bookmarks=f.readlines()

    idx=len(bookmarks)-1

    pivot1=f"\"name\": \"{folder_name}\""
    pivot2="\"children\""

    flag=2

    while idx!=-1 and flag>0:
        each_line=bookmarks[idx]
        if pivot1 in each_line:
            last_idx=idx
            flag=1
        if flag==1 and pivot2 in each_line:
            fst_idx=idx
            flag=0
        idx-=1

    # print(f"fst_idx:{fst_idx};last_idx:{last_idx}")

    bookmarks_s="".join(bookmarks[fst_idx:last_idx])

    # print(bookmarks_s)

    patt_id="\"name\":\s\"(.*?)\""
    patt_url="\"url\":\s\"(.*?)\""

    ids=re.findall(patt_id,bookmarks_s)
    urls=re.findall(patt_url,bookmarks_s)

    print(f"ids:{ids}")
    print(f"urls:{urls}")

    # return tuple(zip(ids,urls))

    return urls



def set_proxy():
    comm1="set http_proxy=socks5://127.0.0.1:10086"
    comm2="set https_proxy=socks5://127.0.0.1:10086"
    os.system(comm1)
    os.system(comm2)

def upload_one_link(some_link,already_path,bad_links_path):
    comm1 = "set http_proxy=socks5://127.0.0.1:10086"
    comm2 = "set https_proxy=socks5://127.0.0.1:10086"

    comm3="echo done"

    comm4=f"archivenow \"{some_link}\""

    comm=f"{comm1}&&{comm2}&&{comm3}&&{comm4} >> {output_path}"

    os.system(comm)

    with open(output_path,"r",encoding="gbk") as f:
        output=f.readlines()
    output_s=output[-1]
    if output_s[0:5]=="Error":
        print("fail!")
        with open (bad_links_path, "a", encoding="utf-8") as f:
            f.write(some_link+"\n")
        return False
    elif output_s[0:5]=="https":
        print("success!")
        with open (already_path, "a", encoding="utf-8") as f:
            f.write(some_link+"\n")
        return True


def main():
    folder_name="ArchiveMePlease!"
    links=get_links(folder_name)

    # 外部链接（不想一个个去点击收藏的那种，一次性获取很多链接的那种类型）

    outer_links=[]

    with open(outer_links_path,"r",encoding="utf-8") as f:
        outer_links=[each.strip("\n") for each in f.readlines()]
    
    links.extend(outer_links)


    # if requests.get(check_url,headers=headers,timeout=10).status_code==200:
    #     print("connection good!")
    # else:
    #     print("connection bad!")
    cnt=0

    # good_links=[]
    already_links=[]
    with open(already_path,"r",encoding="utf-8") as f:
        already_links=[each.strip("\n") for each in f.readlines()]
        already_links_set=set(already_links)

    # bad_links=[]

    for each_link in links:
        # set_proxy()
        if each_link in already_links_set:
            print("already!")
            continue
        else:
            res=upload_one_link(each_link,already_path,bad_links_path)
            # if not res:
            #     bad_links.append(each_link)
            # else:
            #     already_links_set.add(each_link)


    #     comm1 = "set http_proxy=socks5://127.0.0.1:10086"
    #     comm2 = "set https_proxy=socks5://127.0.0.1:10086"

    #     comm3="echo done"

    #     comm4=f"archivenow \"{each_link}\""

    #     comm=f"{comm1}&&{comm2}&&{comm3}&&{comm4} >> {output_path}"

    #     os.system(comm)

    #     with open(output_path,"r",encoding="utf-8") as f:
    #         output=f.readlines()
    #     output_s=output[-1]
    #     if output_s[0:5]=="Error":
    #         print("fail!")
    #         pass
    #     elif output_s[0:5]=="https":
    #         print("success!")
    #         with open (already_path, "a", encoding="utf-8") as f:
    #             f.write(each_link+"\n")
    #         # good_links.append(each_link)
    #         # subprocess.run(comm,capture_output=True)
    #         # print(r)
    # # good_links_s="\n".join(good_links)

if __name__ == '__main__':
    main()



    # print(repr(patt))
    # # 这里必须要有re.S去使得.能匹配全部字符（包括分隔符在内）
    # finds=re.findall(patt,bookmarks_s,re.S)
    #
    # for idx,each in enumerate(finds):
    #     print(each)
    #     print("Idx:",idx)

# print(get_links("Web Archiving相关"))