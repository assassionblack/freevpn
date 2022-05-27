"""
script for download configuration files for openvpn from https://freevpn.me
:argument:
    -p - for parse site, write username and password and download config files
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
    print("script for download configuration files for openvpn from https://freevpn.me")
    if "-p" in sys.argv:
        username, password, link = parse()
        if not os.path.exists(f"/home/{os.getlogin()}/freeVPN/"):
            os.mkdir(f"/home/{os.getlogin()}/freeVPN")
            print("directory ~/freeVPN created")
        with open(f"/home/{os.getlogin()}/freeVPN/freevpn.txt", mode="w", encoding="utf-8") as conf:
            conf.write(f"{username}\n{password}")
            print("username and password written")
        with open("freevpn.zip", "wb") as zip_f:
            zip_f.write(requests.get(link).content)
        zip_file = zipfile.ZipFile("freevpn.zip")
        zip_file.extractall(f"/home/{os.getlogin()}/freeVPN/")
        os.remove("freevpn.zip")
        print("openvpn configurations written")

        print("commands for run openvpn:")
        dir0 = f"/home/{os.getlogin()}/freeVPN"
        dir1 = os.listdir(f"/home/{os.getlogin()}/freeVPN")[2]
        dir0 = f"{dir0}/{dir1}"
        dir1 = os.listdir(dir0)[0]
        dir0 = f"{dir0}/{dir1}"
        dir1 = os.listdir(f'{dir0}')
        servers = []
        for server in dir1:
            if server.startswith("Server"):
                servers.append(f"{dir0}/{server}")
        with open(f"/home/{os.getlogin()}/freeVPN/commands.txt", mode="w", encoding="utf-8") as comm:
            for server in servers:
                command = f"sudo openvpn --config '{server}' " \
                          f"--auth-user-pass /home/{os.getlogin()}/freeVPN/freevpn.txt " \
                          f"--auth-nocache"
                comm.write(f"{command}\n")
                print(f"\t{command}")
        print("commands for running openvpn written in freeVPN/commands.txt")
    else:
        print("for download configuration (login, password, ovpn-files, cert-files, key-file):\n"
              "\trun freevpn with argument -p")