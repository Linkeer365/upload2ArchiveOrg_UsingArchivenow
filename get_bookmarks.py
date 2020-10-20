import os
import re

import subprocess

from upload2ArchiveOrg import get_links

# import requests

bookmarks_path=r"C:\Users\linsi\AppData\Local\CentBrowser\User Data\Default\Bookmarks"
bookmarks_save_path=r"D:\ArchiveMePlease\bookmarks.txt"

if os.path.exists(bookmarks_save_path):
	with open(bookmarks_save_path,"r",encoding="utf-8") as f:
		old_bookmarks=[each.strip("\n") for each in f.readlines()]
		old_bookmarks_set=set(old_bookmarks)

folder_name="ArchiveMePlease!"
links=get_links(folder_name)

links=[each for each in links if not each in old_bookmarks_set]

links_s="\n".join(links)

with open(bookmarks_save_path,"a",encoding="utf-8") as f:
	f.write(links_s)
	f.write("\n")

print("written done.")

