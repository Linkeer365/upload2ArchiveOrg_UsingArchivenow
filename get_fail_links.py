import os

bad_path=r"D:\upload2ArchiveOrg_UsingArchivenow\ArchiveMePlease\fail_to_upload.txt"
already_path=r"D:\upload2ArchiveOrg_UsingArchivenow\ArchiveMePlease\already_upload.txt"
outer_path=r"D:\upload2ArchiveOrg_UsingArchivenow\ArchiveMePlease\outer_links.txt"

with open(bad_path,"r",encoding="utf-8") as f:
    fst_bad_lines=f.readlines()

# print("fst bad:",fst_bad_lines)

if fst_bad_lines==[]:
    outer_links=[l.strip("\n") for l in open(outer_path,"r",encoding="utf-8").readlines() if l.startswith("http")]
    already_links=[l.strip("\n") for l in open(already_path,"r",encoding="utf-8").readlines() if l.startswith("http")]
    bad_links=list(set(outer_links)-set(already_links))
    if bad_links==[]:
        print("total finished.")
    else:
        bad_links_s="\n".join(bad_links)
        with open(bad_path,"a",encoding="utf-8") as f:
            f.write("\n\n")
            f.write(bad_links_s)
        print("bad links written.")
