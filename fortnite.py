"""
MIT License

Copyright (c) 2019 Oli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

try:
    import fortnitepy
    from fortnitepy.errors import Forbidden
    import BenBotAsync, asyncio, datetime, os, json, livejson, aiohttp, logging, sys, random, functions, warnings, requests, aiofiles
    import time as sleep
    from colorama import init
    init(autoreset=True)
    from colorama import Fore, Back, Style
    from pathlib import Path
    from zipfile import ZipFile as zipopen
except ModuleNotFoundError:
    print(Fore.RED + f'[FORTNITEPY] [N/A] [ERROR] Failed to import 1 or more modules, run "INSTALL PACKAGES.bat".')
    exit()
with livejson.File("settings.json",pretty=True,sort_keys=True,indent=4) as f:
    data = f
    for value in data.values():
        if value == "":
            value = None
        if value == 'true':
            value = True
        if value == 'false':
            value = False
GITHUB_BASE = "https://raw.githubusercontent.com/xMistt/fortnitepy-bot/"
MASTER_ZIP = "https://github.com/xMistt/fortnitepy-bot/archive/"
time = datetime.datetime.now().strftime('%H:%M:%S')
print('\033[1m' + f'[FORTNITEPY] [{time}] fortnitepy-bot made by xMistt and Alexa. credit to Terbau for creating the library.')
class Constants:
    def __init__(self):
        self.sittingout = False
        self.owner = data["owner"]
        self.isfirstjoin = True
        self.memberclone = None
        self.spamint = 1
constants = Constants()
warnings.filterwarnings("ignore", category=DeprecationWarning) 
def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

async def getEmoticon(search):
    url = f"http://benbotfn.tk:8080/api/cosmetics/search/multiple?displayName={search}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            benResponse = await r.json()
            for cosmetic in benResponse:
                if cosmetic['type'] == 'Emoticon':
                    return cosmetic  

print(f'[FORTNITEPY] [{time}] Config loaded.')
    
if data['debug'] == 'True':
    print(f'[FORTNITEPY] [{time}] Debug logging is on, prepare for a shitstorm.')
    debugOn()
else:
    print(f'[FORTNITEPY] [{time}] Debug logging is off.')
try:
    client = fortnitepy.Client(
        email=data['email'],
        password=data['password'],
        status=data['status'],
        platform=fortnitepy.Platform(data['platform'])
    )
except ValueError:
    print(f"[FORTNITEPY] [{time}] Found issue with initial settings, resetting status and platform")
    plat = fortnitepy.Platform.WINDOWS
    status = None
    client = fortnitepy.Client(
        email=data['email'],
        password=data['password'],
        status=status,
        platform=plat
    )

@client.event
async def event_ready():
    print(Fore.GREEN + '[FORTNITEPY] [' + time + '] Client ready as {0.user.display_name}. '.format(client))
    first = "Do"
    output = ""
    for friend in client.friends.values():
        if friend.is_online == True:
            if first == "Do":
                output += Fore.GREEN + f"[FORTNITEPY] [{time}] Client's friends online: {friend.display_name}, "
                first = "No"
            else:
                output += Fore.GREEN + f"{friend.display_name} "
    print(str(output))
    async with aiohttp.ClientSession() as s:
        resp = await s.get(GITHUB_BASE + "__version__.json")
        _response = await resp.text()
        response = json.loads(_response)
        with open("__version__.json", "r") as v:
            version = json.load(v)
        if response["version"] != version["version"]:
            print(f"[FORTNITEPY] [{time}] The client is outdated! Version:{response['version']} | Current:{version['version']}")
            async with aiohttp.ClientSession() as session:
                url = MASTER_ZIP + version["branch"] + ".zip"
                print(url)
                TMP = Path(__file__).parent / 'tmp'
                TMP.mkdir(exist_ok=True)
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open('tmp/master.zip', mode='wb+')
                        await f.write(await resp.read())
                        await f.close()
                with zipopen('tmp/master.zip', 'r') as f:
                    f.extractall()
        elif response["version"] == version["version"]:
            print(Fore.GREEN + f"[FORTNITEPY] [{time}] The client is up to date! Version:{version['version']}")


    
async def setVTID(VTID):
    url = f'http://benbotfn.tk:8080/api/assetProperties?file=FortniteGame/Content/Athena/Items/CosmeticVariantTokens/{VTID}.uasset'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            fileLocation = await r.json()

            SkinCID = fileLocation['export_properties'][0]['cosmetic_item']
            VariantChanelTag = fileLocation['export_properties'][0]['VariantChanelTag']['TagName']
            VariantNameTag = fileLocation['export_properties'][0]['VariantNameTag']['TagName']

            VariantType = VariantChanelTag.split('Cosmetics.Variant.Channel.')[1].split('.')[0]

            VariantInt = int("".join(filter(lambda x: x.isnumeric(), VariantNameTag)))

            if VariantType == 'ClothingColor':
                return SkinCID, 'clothing_color', VariantInt
            else:
                return SkinCID, VariantType, VariantInt
@client.event
async def event_party_invite(invite):
    await invite.accept()
    print(f'[FORTNITEPY] [{time}] Accepted party invite.')

@client.event
async def event_friend_request(request):
    print(f'[FORTNITEPY] [{time}] Declined friend request.')
    ownerid = constants.owner
    member = await client.fetch_profile_by_display_name(ownerid)
    f = await client.get_friend(member.id)
    await f.send(f"Would you like to accept {request.display_name}")
    res = await client.wait_for('friend_message')
    content = res.content.lower()
    yes = ('y', 'yes', 'si señor', 'sure', 'si', 'of course' )
    no = ('no', 'none', 'of course not', 'nope', 'nothing')
    if content in yes:
        await request.accept()
        await res.reply(f"Accepted friend request from {request.display_name}")
    elif content in no:
        await request.decline()
        await res.reply(f"Declined friend request from {request.display_name}")
@client.event
async def event_party_member_join(member):
    variants = client.user.party.me.create_variants(**{data['variants-type']: data['variants']})
    if member.id == client.user.id:
        try:
            skin = await BenBotAsync.getSkin(data["cid"])
            if constants.isfirstjoin == True:
                print(f"[FORTNITEPY] [{time}] Selected default {skin['type']} as {skin['displayName']} | {skin['description']}")
        except KeyError:
            skin = None
        try:
            emote = await BenBotAsync.getEmote(data["eid"])
            if constants.isfirstjoin == True:
                print(f"[FORTNITEPY] [{time}] Selected default {emote['type']} as {emote['displayName']} | {emote['description']}")
        except KeyError:
            emote = None
        try:
            backbling = await BenBotAsync.getBackpack(data["bid"])
            if constants.isfirstjoin == True:
                print(f"[FORTNITEPY] [{time}] Selected default {backbling['type']} as {backbling['displayName']} | {backbling['description']}")
        except KeyError:
            backbling = None
        try:
           pickaxe = await BenBotAsync.getPickaxe(data["pid"])
           if constants.isfirstjoin == True:
                print(f"[FORTNITEPY] [{time}] Selected default {pickaxe['type']} as {pickaxe['displayName']} | {pickaxe['description']}")
                constants.isfirstjoin == False
        except KeyError:
            pickaxe = None
        await asyncio.sleep(0.1)
        if skin != None:
            await client.user.party.me.set_outfit(asset=skin["id"], variants=variants)
            await asyncio.sleep(0.1)
        if backbling != None:
            await client.user.party.me.set_backpack(asset=backbling["id"])
            await asyncio.sleep(0.1)
        if pickaxe != None:
            await client.user.party.me.set_pickaxe(asset=pickaxe["id"])
            await asyncio.sleep(0.1)
        await client.user.party.me.set_banner(data['banner'], data['banner_colour'], data['level'])
        await asyncio.sleep(0.5)
        if emote != None:
            await client.user.party.me.set_emote(asset=emote["id"])
        await asyncio.sleep(0.1)
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
    
    if client.user.display_name != member.display_name:
        print(f"[FORTNITEPY] [{time}] {member.display_name} has joined the lobby.")

@client.event
async def event_friend_message(message):
    ownerid = constants.owner
    member = await client.fetch_profile_by_display_name(ownerid)
    if member.id == message.author.id:
        contetaaa = message.content
        args = message.content.split()
        content = contetaaa.replace(args[0] + " ", "")
        print('[FORTNITEPY] [' + time + '] {0.author.display_name}: {0.content}'.format(message))

        if "!skin" in args[0].lower():
            id = await BenBotAsync.getSkinId(content)
            if id == None:
                await message.reply(f"Couldn't find a skin with the name: {content}")
            else:
                await client.user.party.me.set_outfit(asset=id)
                await message.reply('Skin set to ' + id)
                print(f"[FORTNITEPY] [{time}] Set Skin to: " + id)
            
        if "!backpack" in args[0].lower():
            id = await BenBotAsync.getBackpackId(content)
            if id == None:
                await message.reply(f"Couldn't find a backpack with the name: {content}")
            else:
                await client.user.party.me.set_backpack(asset=id)
                await message.reply('Backpack set to ' + id)
                print(f"[FORTNITEPY] [{time}] Set Backpack to: " + id)

        if "!emote" in args[0].lower():
            await client.user.party.me.clear_emote()
            id = await BenBotAsync.getEmoteId(content)
            if id == None:
                await message.reply(f"Couldn't find a skin with the name: {content}")
            else:
                await client.user.party.me.set_emote(asset=id)
                await message.reply('Skin set to ' + id)
                print(f"[FORTNITEPY] [{time}] Set Skin to: " + id)

        if "!pickaxe" in args[0].lower():
            id = await BenBotAsync.getPickaxeId(content)
            if id == None:
                await message.reply(f"Couldn't find a pickaxe with the name: {content}")
            else:
                await client.user.party.me.set_pickaxe(asset=id)
                await message.reply('Pickaxe set to ' + id)
                print(f"[FORTNITEPY] [{time}] Set Pickaxe to: " + id)

        if "!pet" in args[0].lower():
            id = await BenBotAsync.getPetId(content)
            await client.user.party.me.set_backpack(
                    asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + id + "." + id
            )

            await message.reply('Pet set to ' + id)
            print(f"[FORTNITEPY] [{time}] Client's PetCarrier set to: " + id)

        if "!emoji" in args[0].lower():
            e = await getEmoticon(content)
            id = e["id"]
            await client.user.party.me.clear_emote()
            if id is not None:
                await client.user.party.me.set_emote(
                        asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + id + "." + id
                )

            await message.reply('Emoji set to ' + id)
            print(f"[FORTNITEPY] [{time}] Client's Emoji set to " + id)
        if "!searchvariants" in args[0].lower():
            aab = args[2:]
            aaa = ''.join(aab)
            if args[1].lower() == "skin":
                iid = await BenBotAsync.getSkinId(aaa)
            elif args[1].lower() == "backbling":
                iid = await BenBotAsync.getBackpackId(aaa)
            elif args[1].lower() == "pickaxe":
                iid = await BenBotAsync.getPickaxeId(aaa)
            else:
                await message.reply("Variants not recognized!, please stick to the format |!searchvariants|<skin, pickaxe or backbling>|<skin name, pickaxe name or backbling name>")
            headers={"type": args[1],
            "query":iid}
            async with aiohttp.ClientSession(headers=headers) as session:
                try:
                    async with session.get("https://fnapi.terax235.com/api/v1.2/cosmetics/search") as r:
                        json_body = await r.json()
                except TypeError:
                    await message.reply(f"Cosmetic {aaa} not found!")
            data = json_body["data"]
            variants = data["variants"]
            output = "\n"
            lengh = len(variants)
            for index, lists in enumerate(variants):
                if index == 0:
                    output += f"Channels found for {args[2]}:{lists['channel']}"
                else:
                    output += f", {lists['channel']}"
            output += "\n"
            for lists in variants:
                output += f"Styles found for channel: {lists['channel']}:\n"
                lengh = len(lists["tags"])
                for index, info in enumerate(lists["tags"]):
                    output += f"    {info['name']['en']}"
                    output += f":{info['tag']}"
                    if lengh == lengh:
                        output += "\n"
            await message.reply(output)

        if "!purpleskull" in args[0].lower():
            variants = client.user.party.me.create_variants(
                clothing_color=1
            )

            await client.user.party.me.set_outfit(
                asset='CID_030_Athena_Commando_M_Halloween',
                variants=variants
            )

            await message.reply('Skin set to Purple Skull Trooper!')

        if "!pinkghoul" in args[0].lower():
            variants = client.user.party.me.create_variants(
                material=3
            )

            await client.user.party.me.set_outfit(
                asset='CID_029_Athena_Commando_F_Halloween',
                variants=variants
            )

            await message.reply('Skin set to Pink Ghoul Trooper!')

        if "!brainiacghoul" in args[0].lower():
            variants = client.user.party.me.create_variants(
                material=2
            )

            await client.user.party.me.set_outfit(
                asset='CID_029_Athena_Commando_F_Halloween',
                variants=variants
            )

            await message.reply('Skin set to Brainiac Ghoul Trooper!')

        if "!purpleportal" in args[0].lower():
            variants = client.user.party.me.create_variants(
                item='AthenaBackpack',
                particle_config='Particle',
                particle=1
            )

            await client.user.party.me.set_backpack(
                asset='BID_105_GhostPortal',
                variants=variants
            )

            await message.reply('Backpack set to Purple Ghost Portal!')

        if "!banner" in args[0].lower():
            if len(args) == 1:
                await message.reply('You need to specify which banner, color & level you want to set the banner as.')
            if len(args) == 2:
                await client.user.party.me.set_banner(icon=args[1], color=data['banner_colour'], season_level=data['level'])
            if len(args) == 3:
                await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=data['level'])
            if len(args) == 4:
                await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

            await message.reply(f'Banner set to; {args[1]} {args[2]} {args[3]}')
            print(f"[FORTNITEPY] [{time}] Banner set to; {args[1]} {args[2]} {args[3]}")

        if "CID_" in args[0]:
            await client.user.party.me.set_outfit(
                asset=args[0]
            )

            await message.reply(f'Skin set to {args[0]}')
            await print(f'[FORTNITEPY] [{time}] Skin set to ' + args[0])

        if "VTID_" in args[0]:
            VTID = await setVTID(args[0])
            if VTID[1] == 'Particle':
                variants = client.user.party.me.create_variants(particle_config='Particle', particle=1)
            else:
                variants = client.user.party.me.create_variants(**{VTID[1].lower(): int(VTID[2])})

            await client.user.party.me.set_outfit(asset=VTID[0], variants=variants)
            await message.reply(f'Variants set to {args[0]}.\n(Warning: This feature is not supported, please use !variants)')
        if "!clone" in args[0]:
            mid = await client.fetch_profile_by_display_name(args[1])
            if mid != None:
                constants.memberclone = mid.id
        if "!variants" in args[0]:
            currentskin = await BenBotAsync.getCosmeticFromId(client.user.party.me.outfit)
            currentback = await BenBotAsync.getCosmeticFromId(client.user.party.me.backpack)
            currentpick = await BenBotAsync.getCosmeticFromId(client.user.party.me.pickaxe)
            
            meme = filter(str.isdigit, args[3])
            a = "".join(meme)
            args3 = int(a)
            cid = client.user.party.me.outfit
            bid = client.user.party.me.backpack
            pid = client.user.party.me.pickaxe

            if 'skin' in args[1]:
                variants = client.user.party.me.create_variants(**{args[2]: args3})
                variants.extend(client.user.party.me.outfit_variants)
                currentcosmetic = currentskin["displayName"]
                await client.user.party.me.set_outfit(
                    asset=cid,
                    variants=variants
                )
            elif 'backbling' in args[1]:
                variants = client.user.party.me.create_variants(item='AthenaBackpack', **{args[2]: args3})
                variants.extend(client.user.party.me.backbling)
                currentcosmetic = currentback["displayName"]
                await client.user.party.me.set_backpack(
                    asset=bid,
                    variants=variants
                )
            elif 'pickaxe' in args[1]:
                variants = client.user.party.me.create_variants(item='AthenaPickaxe', **{args[2]: args3})
                variants.extend(client.user.party.me.pickaxe_variants)
                currentcosmetic = currentpick["displayName"]
                await client.user.party.me.set_pickaxe(
                    asset=pid,
                    variants=variants
                )

            await message.reply(f'Set variants of {currentcosmetic} to {args[2]} {args[3]}.')
            print(f'[FORTNITEPY] [{time}] Set variants of {args[1]} to {args[2]} {args[3]}.')

        if "!checkeredrenegade" in args[0].lower():
            variants = client.user.party.me.create_variants(
                material=2
            )

            await client.user.party.me.set_outfit(
                asset='CID_028_Athena_Commando_F',
                variants=variants
            )

            await message.reply('Skin set to Checkered Renegade!')

        if "EID_" in args[0]:
            await client.user.party.me.clear_emote()
            await client.user.party.me.set_emote(
                asset=args[0]
            )
            await message.reply('Emote set to ' + args[0] + '!')
            
        if "!stop" in args[0].lower():
            await client.user.party.me.clear_emote()
            await message.reply('Stopped emoting.')

        if "BID_" in args[0]:
            await client.user.party.me.set_backpack(
                asset=args[0]
            )

            await message.reply('Backbling set to ' + message.content + '!')

        if "!help" in args[0].lower():
            await message.reply('For a list of commands, goto; https://github.com/xMistt/fortnitepy-bot')

        if "PICKAXE_ID_" in args[0].lower():
            await client.user.party.me.set_pickaxe(
                    asset=args[0]
            )

            await message.reply('Pickaxe set to ' + args[0] + '!')

        if "PetCarrier_" in args[0]:
            await client.user.party.me.set_backpack(
                    asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + args[0] + "." + args[0]
            )

        if "Emoji_" in args[0]:
            await client.user.party.me.set_emote(asset='EID_ClearEmote')
            await client.user.party.me.set_emote(
                    asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + args[0] + "." + args[0]
            )

        if "!legacypickaxe" in args[0].lower():
            await client.user.party.me.set_pickaxe(
                    asset=args[1]
            )

            await message.reply('Pickaxe set to ' + args[1] + '!')

        if "!ready" in args[0].lower():
            await client.user.party.me.set_ready(True)
            await message.reply('Ready!')

        if ("!unready" in args[0].lower()) or ("!sitin" in args[0].lower()):
            await client.user.party.me.set_ready(False)
            await message.reply('Unready!')

        if "!sitout" in args[0].lower():
            await client.user.party.me.set_ready(None)
            await message.reply('Sitting Out!')

        if "!bp" in args[0].lower():
            await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp='0', friend_boost_xp='0')

        if "!level" in args[0].lower():
            await client.user.party.me.set_banner(icon=client.user.party.me.banner[0], color=client.user.party.me.banner[1], season_level=args[1])

        if "!echo" in args[0].lower():
            await client.user.party.send(content)

        if "!status" in args[0].lower():
            await client.set_status(content)

            await message.reply(f'Status set to {content}')
            print(f'[FORTNITEPY] [{time}] Status set to {content}.')

        if "!leave" in args[0].lower():
            await client.user.party.me.set_emote('EID_Wave')
            await asyncio.sleep(2)
            await client.user.party.me.leave()
            await message.reply('Bye!')
            print(f'[FORTNITEPY] [{time}] Left the party as requested by {message.author.display_name}.')

        if "!kick" in args[0].lower():
            user = await client.fetch_profile(content)
            member = client.user.party.members.get(user.id)
            if member is None:
                await message.reply("Couldn't find that user, are you sure they're in the party?")
            else:
                try:
                    await member.kick()
                    await message.reply(f"Kicked user: {member.display_name}.")
                    print(f"[FORTNITEPY] [{time}] Kicked user: {member.display_name}")
                except fortnitepy.Forbidden:
                    await message.reply(f"Couldn't kick {member.display_name}, as I'm not party leader.")
                    print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to kick member as I don't have the required permissions." + Fore.WHITE)

        if "!promote" in args[0].lower():
            if len(args) != 1:
                user = await client.fetch_profile(content)
                member = client.user.party.members.get(user.id)
            if len(args) == 1:
                user = await client.fetch_profile(message.author.display_name)
                user = await client.user.party.members.get(user.id)

            if member is None:
                await message.reply("Couldn't find that user, are you sure they're in the party?")
            else:
                try:
                    await member.promote()
                    await message.reply(f"Promoted user: {member.display_name}.")
                    print(f"[FORTNITEPY] [{time}] Promoted user: {member.display_name}")
                except fortnitepy.Forbidden:
                    await message.reply(f"Couldn't promote {member.display_name}, as I'm not party leader.")
                    print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to promote member as I don't have the required permissions." + Fore.WHITE)

        if "Playlist_" in args[0]:
            try:
                await client.user.party.set_playlist(playlist=args[0])
            except fortnitepy.Forbidden:
                    await message.reply(f"Couldn't set gamemode to {args[1]}, as I'm not party leader.")
                    print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to set gamemode as I don't have the required permissions." + Fore.WHITE)

        if "!platform" in args[0]:
            await message.reply('Setting platform to ' + args[1] + '.')
            party_id = client.user.party.id
            await client.user.party.me.leave()
            client.platform = fortnitepy.Platform(args[1])
            await message.reply('Platform set to ' + str(client.platform) + '.')
            try:
                await client.join_to_party(party_id, check_private=True)
            except fortnitepy.Forbidden:
                await message.reply('Failed to join back as party is set to private.')
        if "!members" in args[0]:
            outputcontent = ""
            for member in client.user.party.members:
                outputcontent += member
            await message.reply(outputcontent)
        if "!join" in args[0]:
            try:
                _friend = await client.fetch_profile_by_display_name(content)
                fid = _friend.id
                friend = client.get_friend(fid)
                if friend != None:
                    await friend.join_party()
                await message.reply(f"Joining {friend.display_name}'s party...")
            except Exception as e:
                await message.reply(f"""Failed to join to {friend.display_name}'s party \n 
                error code: {e}""")
        if "!crash" in args[0].lower():
            await asyncio.sleep(2)
            await client.user.party.me.set_outfit('/Game/Athena/Items/Cosmetics/Characters//./')
        if args[0] == "!id":
            user = await client.fetch_profile(content, cache=False, raw=False)
            try:
                await message.reply(f"{content}'s Epic ID is: {user.id}")
            except AttributeError:
                await message.reply(f"I couldn't find an Epic account with the name: {content}.")
    else:
        constants.spamint += 1
class CosmeticLoadout:
    """Defines a cosmetic loadout in fortnite"""
    def __init__(self):
        self.EID = None
        self.CID = "CID_029_Athena_Commando_F_Halloween"
        self.BID = None
cloadout = CosmeticLoadout()
@client.event
async def event_party_member_update(member):
    if constants.memberclone != None:
        if constants.memberclone == member.id:
            
            clientmember = client.user.party.me
            cloadout.EID = member.emote
            cloadout.CID = member.outfit
            cloadout.BID = member.backpack
            if clientmember.outfit != cloadout.CID:
                await asyncio.sleep(0.1)
                await clientmember.set_outfit(cloadout.CID)
                print(f"[FORTNITEPY][{time}] Cloned loadout from {member.display_name}")
            if clientmember.backpack != cloadout.BID:
                await asyncio.sleep(0.1)
                await clientmember.set_backpack(cloadout.BID)
            await asyncio.sleep(0.1)
            if cloadout.EID is not None:
                if cloadout.EID != clientmember.emote:
                    await asyncio.sleep(0.1)
                    await clientmember.set_emote(cloadout.EID)
if __name__ == "__main__":
    if data["isconfigured"] == False:
        print(Fore.GREEN + f"[FORTNITEPY] [{time}] Settings are not loaded, please configure them in the json file")
        total = 1000
        i = 0
        while i < total:
            functions.progress(i, total, status='Loading settings...')
            sleep.sleep(0.01)
            i += 1
            if i == 999:
                i += 1
                functions.progress(i, total, status="Done           ")#Don't remove the whitespace at the end
        print("\n")
        exit(1)
    else:
        data["platform"] = data["platform"].upper()
        print(Fore.GREEN + f"[FORTNITEPY] [{time}] Settings are loaded.")
        total = 1000
        i = 0
        while i < total:
            functions.progress(i, total, status= Fore.GREEN + f"[FORTNITEPY] [{time}] Loading main bot..")
            sleep.sleep(0.01)
            i += 1
            if i == 999:
                i += 1
                functions.progress(i, total, status=Fore.GREEN + f"[FORTNITEPY] [{time}] Done              ")#Don't remove the whitespace at the end
        try:
            client.run()
        except fortnitepy.AuthException:
            print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Invalid account credentials.")
            data["email"] = input("What is your account email?")
            data["password"] = input("What is the account password?")
            exit(0)
