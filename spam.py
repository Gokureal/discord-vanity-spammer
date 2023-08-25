import aiohttp, asyncio, os, sys, time

os.system("cls" if os.name == "nt" else "clear")

token = "token gir"
hook = "webhook"
guild = "server id"
list = ["vanit1","vanity2","vanity3"]#virgül ve "" içindekilerle beraber silersen/eklersen url ekleyip silebilirsin
delay = 0

async def notify(session, url, jsonxd):
    async with session.post(url, json=jsonxd) as response:
        return response.status

async def claim(session, url, jsonxd):
    async with session.patch(url, json=jsonxd) as response:
        return response.status

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status, response.text, response.json()

async def main():
    os.system("cls" if os.name == "nt" else "clear")
    async with aiohttp.ClientSession(headers={"Authorization": token, "X-Audit-Log-Reason": "olmaz"}, connector=None) as session:
        async with session.get("https://canary.discord.com/api/v9/users/@me") as response:
          if response.status in (200, 201, 204):
            user = await response.json()
            id = user["id"]
            username = user["username"]
            print("Logged in as {} | {}".format(username, id))
          elif response.status == 429:
            print("[-] Connection failed to discord websocket, this ip is rate limited")
            sys.exit()
          else:
            await notify(session, hook, {"content": "@everyone failed to connect to discord websocket."})
            print("Bad Auth")
            sys.exit()
        for x in range(100000):
            for vanity in list:
                idk, text, jsonxd = await fetch(session, 'https://canary.discord.com/api/v9/invites/%s' % vanity)
                if idk == 404:
                    idk2 = await claim(session, 'https://canary.discord.com/api/v9/guilds/%s/vanity-url' % (guild), {"code": vanity})
                    if idk2 in (200, 201, 204):
                        await notify(session, hook, {"content": "@everyone baba koydu %s" % vanity})
                        sys.exit()
                    else:
                        await notify(session, hook, {"content": "alınmaya çalışılan url: %s | status: vxnity url deneniyor." % str(list)})
                        sys.exit()
                elif idk == 200:
                    print("[+] deneniyor.: %s | Vanity: %s" % (x, vanity))
                    await asyncio.sleep(delay)
                    continue
                elif idk == 429:
                    #print()
                    await notify(session, hook, {"content": "rate limit yedik ananı"})
                    print("[-] Rate Limited")
                    if 'retry_after' in text:
                      time.sleep(int(jsonxd['retry_after']))
                    else:
                      sys.exit()                 
                else:
                    print("[-] Unknown Error")
                    sys.exit()


loop = asyncio.get_event_loop()
loop.run_until_complete(main()) 
#olmaz#0/Goku