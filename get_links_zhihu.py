flag="\n"

outer_links_path=r"D:\upload2ArchiveOrg_UsingArchivenow\ArchiveMePlease\outer_links.txt"
outer_links_path2=r"D:\upload2ArchiveOrg_UsingArchivenow\ArchiveMePlease\outer_links2.txt"

while flag!="q":
    packs=input("question_link,max_page_num\nsep by @ for pagenum or # for question num\n(multiple is ok, split by **)").split("**")
    all_links=[]
    for pack in packs:
        if "@" in pack:
            question_link,max_page_num=pack.split("@")
            question_link=question_link.split("answer")[0]
            max_page_num=int(max_page_num)
        elif "#" in pack:
            question_link,max_num=pack.split("#")
            question_link=question_link.split("answer")[0]
            max_page_num=int(max_num)//20+1 if int(max_num)%20!=0 else int(max_num)/20
        # 结尾的/要丢掉
        question_link=question_link.strip("/")
        question_link+="/answers/updated?page="
        # print("max page:",max_page_num)
        max_page_num=int(max_page_num)
        links=[question_link+str(each) for each in range(1,max_page_num+1)]
        all_links.extend(links)
        
    links_s="\n".join(all_links)
    with open(outer_links_path,"w",encoding="utf-8") as f:
        f.write("\n")
        f.write(links_s)
        f.write("\n")
    
    with open(outer_links_path2,"a",encoding="utf-8") as f:
        f.write("\n")
        f.write(links_s)
        f.write("\n")

    print("one done.")

    flag=input("q for quit. Quit?")

print("all done.")
