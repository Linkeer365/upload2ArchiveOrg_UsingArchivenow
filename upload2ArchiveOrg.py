import os
import re
import sys
import shutil
import time
import subprocess

# import requests

bookmarks_path=r"C:\Users\linsi\AppData\Local\CentBrowser\User Data\Default\Bookmarks"

check_url="https://archive.org/"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

output_path=r".\ArchiveMePlease\output.txt"

already_path=r".\ArchiveMePlease\already_upload.txt"

bad_links_path=r".\ArchiveMePlease\fail_to_upload.txt"

# outer_links_path=r".\ArchiveMePlease\outer_links.txt"
outer_links_path=r".\ArchiveMePlease\outer_links.txt"

done_flag=0

def get_links(folder_name):
    bookmarks_path2=bookmarks_path+'2'
    shutil.copy(bookmarks_path,bookmarks_path2)
    with open(bookmarks_path2,"r",encoding="utf-8") as f:
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
    # print(some_link+"\n")
    comm1 = "set http_proxy=socks5://127.0.0.1:10086"
    comm2 = "set https_proxy=socks5://127.0.0.1:10086"

    # comm3="echo done"

    comm4=f"archivenow \"{some_link}\""

    comm=f"{comm1}&&{comm2}&&{comm4} >> {output_path}"

    os.system(comm)

    with open(output_path,"r",encoding="gbk") as f:
        output=f.readlines()
    output_s=output[-1]
    if output_s[0:5]=="Error":
        print("fail!")
        print(some_link)
        with open (bad_links_path, "a", encoding="utf-8") as f:
            f.write(some_link+"\n")
        return False
    elif output_s[0:5]=="https":
        print("success!")
        with open (already_path, "a", encoding="utf-8") as f:
            f.write(some_link+"\n")
        return True


def main():
    # sys.exit(1)
    folder_name="ArchiveMePlease!"
    # 需要使用ArchiveMePlease时再打开
    links=get_links(folder_name)
    # links=[]

    # 外部链接（不想一个个去点击收藏的那种，一次性获取很多链接的那种类型）

    outer_links=[]
    already_links_set=set()

    with open(outer_links_path,"r",encoding="utf-8") as f:
        lines=f.readlines()
        print("lines[-1]:",lines[-1])
        if lines[-1]=='done.\n':
            outer_links=[]
        else:
            outer_links=[each.strip("\n") for each in lines if each.startswith("http")]
            links.extend(outer_links)
    
    if outer_links==[]:
        with open(bad_links_path,"r",encoding="utf-8") as f:
            lines=f.readlines()
            bad_links=[each.strip("\n") for each in lines if each.startswith("http")]
            print("in sec term...")
        if bad_links==[]:
            print("all done.")
            # 只有这里才是安全出口...
            sys.exit(0)
        else:
            links.extend(bad_links)
    elif outer_links!=[]:
        # good_links=[]
        # 如果你是第二次，那么already在之前就已经被读取过了...
        with open(already_path,"r",encoding="utf-8") as f:
            already_links=[each.strip("\n") for each in f.readlines() if each.startswith("http")]
            already_links_set=set(already_links)
    
    open(bad_links_path,"w").close()
    # sys.exit(0)

    # bad_links=[]

    # if set(links) in already_links_set:
    #     print("done.")
    #     sys.exit(0)
    links_len=len(links)
    for idx,each_link in enumerate(links,1):
        a=time.time()
        # # set_proxy()
        if already_links_set!=set():
            if each_link in already_links_set:
                print("already!")
                continue
        # else:
        print(f"第{idx}项 （共{links_len}项）")
        res=upload_one_link(each_link,already_path,bad_links_path)
        b=time.time()
        time_cost=b-a
        print(f"用时:{time_cost}s")
    
    print("next turn.")

    with open(outer_links_path,"a",encoding="utf-8") as f:
        f.write("done.\n")
    # 抛出错误，因为还没有完成最终的任务...
    sys.exit(1)
    

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