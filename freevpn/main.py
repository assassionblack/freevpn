"""
script for download configuration files for openvpn from https://freevpn.me

for download configuration (login, password, ovpn-files, cert-files, key-file):
    run freevpn with argument -p or -pc
:argument:
    -p - for parse site and write username and password into ~/freeVPN/freevpn.txt
    -p -c - for download configuration files into ~/freeVPN/
"""
import os.path
import sys
import zipfile

import bs4
import requests


def parse():
    res = requests.get("https://freevpn.me/accounts/")
    html = res.text
    soup = bs4.BeautifulSoup(html, "html5lib")
    div_span4 = soup.find("div", class_="span4")
    user = ''
    passwd = ''
    for li in div_span4.find_all("li"):
        if li.text.startswith("Username"):
            user = li.text.split()[1]
        if li.text.startswith("Password"):
            passwd = li.text.split()[1]
    return user, passwd, soup.find("a", class_="maxbutton-2 maxbutton maxbutton-downloadbutton").get("href")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        import main

        doc = main.__doc__
        print(doc)
    elif "-p" in sys.argv:
        username, password, link = parse()
        if not os.path.exists(f"/home/{os.getlogin()}/freeVPN/"):
            os.mkdir(f"/home/{os.getlogin()}/freeVPN")
            print("directory ~/freeVPN created")
        with open(f"/home/{os.getlogin()}/freeVPN/freevpn.txt", mode="w", encoding="utf-8") as conf:
            conf.write(f"username: {username}\npassword: {password}")
            print("username and password written")
        if "-c" in sys.argv:
            with open("freevpn.zip", "wb") as zip_f:
                zip_f.write(requests.get(link).content)
            zip_file = zipfile.ZipFile("freevpn.zip")
            zip_file.extractall(f"/home/{os.getlogin()}/freeVPN/")
            os.remove("freevpn.zip")
            print("openvpn configurations written")
