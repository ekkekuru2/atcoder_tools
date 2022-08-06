#!/usr/bin/env python3
from datetime import timedelta, timezone
import requests
from bs4 import BeautifulSoup
import datetime
import os
import shutil

print("* Checking for a next AtCoder contest...")
r = requests.get("https://atcoder.jp/contests/")
soup = BeautifulSoup(r.content,"html.parser")
next_date = datetime.datetime.strptime(soup.select_one("#contest-table-upcoming").find("tbody").find("tr").find("td").find("time").contents[0],'%Y-%m-%d %H:%M:%S%z')

if(datetime.datetime.now(timezone(timedelta(hours=+9))).date()==next_date.date()):
    contest_url = str(soup.select_one("#contest-table-upcoming").find("tbody").find("tr").find_all("a")[1].attrs['href'])
    
    contest_name = contest_url.replace("/contests/","")
    print("[",contest_name,"]",next_date)
    
    print("========")

    try:
        ATCODER_ROOT=os.environ["ATCODER_ROOT"]
        ### Create Working Directory
        dir_path = ATCODER_ROOT+next_date.strftime('%Y%m%d')+contest_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("Created directory : ",dir_path)
        else:
            print("Already existed directory : ",dir_path)

        ### Copy Templete File
        if os.path.exists(ATCODER_ROOT+"templete.cpp"):
            if not os.path.exists(dir_path+"/a.cpp"):
                shutil.copy(ATCODER_ROOT+"templete.cpp",dir_path+"/a.cpp")
                print("- Created a.cpp")
            if not os.path.exists(dir_path+"/b.cpp"):
                shutil.copy(ATCODER_ROOT+"templete.cpp",dir_path+"/b.cpp")
                print("- Created b.cpp")
            if not os.path.exists(dir_path+"/c.cpp"):
                shutil.copy(ATCODER_ROOT+"templete.cpp",dir_path+"/c.cpp")
                print("- Created c.cpp")

        print("Launching VSCode...")
        os.system("code "+ATCODER_ROOT)
    except:
        print("***Set $ATCODER_ROOT environment variable for auto directory generation***")


    print("Launching Google Chrome...")
    os.system('chrome --new-window "https://atcoder.jp'+contest_url+'"')
else:
    print("No contest will be held today")
