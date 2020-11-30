flag="\n"
while flag!="q":
	packs=input("question_link,max_page_num,sep by @(multiple is ok, split by **)").split("**")
	for pack in packs:
		question_link,max_page_num=pack.split("@")
		max_page_num=int(max_page_num)
		question_link+="/answers/updated?page="

		links=[question_link+str(each) for each in range(1,max_page_num+1)]
		links_s="\n".join(links)

		outer_links_path="D:\win2vultr\outer_links.txt"
		outer_links_path2="D:\win2vultr\outer_links2.txt"

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
