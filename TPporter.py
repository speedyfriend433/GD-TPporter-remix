import re
import plistlib
import os
import sys
import argparse
from math import floor, ceil
from os.path import isfile, join


def divideLowFloor(value):
    return "{" + str(floor(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[0]) / 4)) + "," + str(floor(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[1]) / 4)) + "}"


def divideMediumFloor(value):
    return "{" + str(floor(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[0]) / 2)) + "," + str(floor(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[1]) / 2)) + "}"


def divideLowCeil(value):
    return "{" + str(ceil(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[0]) / 4)) + "," + str(ceil(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[1]) / 4)) + "}"


def divideMediumCeil(value):
    return "{" + str(ceil(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[0]) / 2)) + "," + str(ceil(int(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[1]) / 2)) + "}"


def divideFloatLow(value):
    return "{" + str(float(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[0]) / 4) + "," + str(float(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[1]) / 4) + "}"


def divideFloatMedium(value):
    return "{" + str(float(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[0]) / 2) + "," + str(float(re.search("(?<={)(.*)(?=})", value).group(1).split(',')[1]) / 2) + "}"


parser = argparse.ArgumentParser(description='A Texture Pack porter made by ItalianApkDownloader, forked by Weebify')
parser.add_argument('-l', '--low', help='Optional argument. Use if you want to port your tp to low graphics', action='store_true')
args = parser.parse_args()

directory = os.path.dirname(os.path.realpath(__file__))
fileI = [f for f in os.listdir(directory) if isfile(join(directory, f))]

removal = []
for w in range(len(fileI)):
    filenameInput, file_extensionInput = os.path.splitext(fileI[w])

    if (file_extensionInput != ".plist" and file_extensionInput != ".png" and file_extensionInput != ".fnt") or \
            filenameInput[-4:] == "Desc" or \
            filenameInput[-6:] == "DescMD" or \
            filenameInput[-6:] == "Effect" or \
            filenameInput[-6:] == "effect" or \
            filenameInput[-7:] == "Effect2" or \
            filenameInput[-4:] == "Open" or \
            filenameInput[-6:] == "Opened" or \
            filenameInput == "circle" or \
            filenameInput[-12:] == "EffectPortal" or \
            filenameInput[-10:] == "EffectGrav" or \
            filenameInput[-12:] == "EffectVortex" or \
            filenameInput == "firework" or \
            filenameInput[-5:] == "Desc2" or \
            filenameInput[-9:] == "Destroy01" or \
            filenameInput[-10:] == "EffectIcon" or \
            filenameInput[-3:] == "001" or \
            filenameInput[-10:] == "Complete01" or \
            filenameInput[:9] == "LevelData" or \
            filenameInput == "LoadData" or \
            filenameInput[-11:] == "Definitions" or \
            filenameInput[:7] == "portalE" or \
            filenameInput[:5] == "Skull" or \
            filenameInput[:6] == "speedE" or \
            filenameInput[-8:] == "Effect01" or \
            filenameInput == "starFall" or \
            filenameInput == "stoneHit" or \
            filenameInput[:6] == "streak" or \
            filenameInput == "sun":
        removal.append(w)

removal.reverse()

for w in removal:
    fileI.pop(w)

print("\nCreating a folder for the ported tp(s)...")
try:
    os.mkdir('Ported')
except FileExistsError:
    print("Folder already created, skipping...\n")

directory = directory + r"/Ported"

print("Files input: %s (not including invalid files)" % str(len(fileI)))
if args.low:
    print("Porting mode: All elements to low graphics.")
else:
    print("Porting mode: All elements to one graphics level lower.")

print("Getting there...")

if len(fileI) == 0:
    print("\nUhhh, do you mind if you check the texture pack if there is actually any valid file?\n")

for w in range(len(fileI)):
    try:
        filenameInput, file_extensionInput = os.path.splitext(fileI[w])

        if file_extensionInput == ".plist":
            try:
                with open(fileI[w], 'rb') as f:
                    plist_data = plistlib.load(f)
            except IndexError:
                plist_file = '<stdin>'
                plist_data = plistlib.loads(sys.stdin.buffer.read())
                exit()

            dictionary = plist_data.get("frames").items()

            if filenameInput[-3:] == "-hd":
                for key in dictionary:
                    try:
                        value = key[1]["textureRect"]
                        key[1]["textureRect"] = "{{" + str(ceil(int(re.search("(?<={{)(.*)(?=},)", value).group(1).split(',')[0]) / 2)) + "," + str(ceil(int(re.search("(?<={{)(.*)(?=},)", value).group(1).split(',')[1]) / 2)) + "},{" + str(floor(int(re.search("(?<=,{)(.*)(?=}})", value).group(1).split(',')[0]) / 2)) + "," + str(floor(int(re.search("(?<=,{)(.*)(?=}})", value).group(1).split(',')[1]) / 2)) + "}}"
                        if key[1]["spriteOffset"] != '':
                            key[1]["spriteOffset"] = divideFloatMedium(key[1]["spriteOffset"])
                        if key[1]["spriteSize"] != '':
                            key[1]["spriteSize"] = divideMediumFloor(key[1]["spriteSize"])
                        if key[1]["spriteSourceSize"] != '':
                            key[1]["spriteSourceSize"] = divideMediumFloor(key[1]["spriteSourceSize"])
                    except Exception as e:
                        print(e)
                        print(key)

                plist_data["metadata"]["size"] = divideMediumCeil(plist_data["metadata"]["size"])
                plist_data["metadata"]["realTextureFileName"] = plist_data["metadata"]["realTextureFileName"].replace("-hd", "")
                plist_data["metadata"]["textureFileName"] = plist_data["metadata"]["textureFileName"].replace("-hd", "")

                with open(os.path.join(directory, plist_data["metadata"]["textureFileName"].replace(".png", ".plist")), 'wb') as f:
                    plistlib.dump(plist_data, f)
                print("Done! (" + str((w + 1)) + "/" + str(len(fileI)) + ")")
                if (w + 1) == len(fileI):
                    print("Porting finished.")

            elif filenameInput[-3:] == "uhd" and args.low:
                for key in dictionary:
                    try:
                        value = key[1]["textureRect"]
                        key[1]["textureRect"] = "{{" + str(ceil(int(re.search("(?<={{)(.*)(?=},)", value).group(1).split(',')[0]) / 4)) + "," + str(ceil(int(re.search("(?<={{)(.*)(?=},)", value).group(1).split(',')[1]) / 4)) + "},{" + str(floor(int(re.search("(?<=,{)(.*)(?=}})", value).group(1).split(',')[0]) / 4)) + "," + str(floor(int(re.search("(?<=,{)(.*)(?=}})", value).group(1).split(',')[1]) / 4)) + "}}"
                        if key[1]["spriteOffset"] != '':
                            key[1]["spriteOffset"] = divideFloatLow(key[1]["spriteOffset"])
                        if key[1]["spriteSize"] != '':
                            key[1]["spriteSize"] = divideLowFloor(key[1]["spriteSize"])
                        if key[1]["spriteSourceSize"] != '':
                            key[1]["spriteSourceSize"] = divideLowFloor(key[1]["spriteSourceSize"])
                    except Exception as e:
                        print(e)
                        print(key)

                plist_data["metadata"]["size"] = divideLowCeil(plist_data["metadata"]["size"])
                plist_data["metadata"]["realTextureFileName"] = plist_data["metadata"]["realTextureFileName"].replace("uhd", "")
                plist_data["metadata"]["textureFileName"] = plist_data["metadata"]["textureFileName"].replace("uhd", "")

                with open(os.path.join(directory, plist_data["metadata"]["textureFileName"].replace(".png", ".plist")), 'wb') as f:
                    plistlib.dump(plist_data, f)
                print("Done! (" + str((w + 1)) + "/" + str(len(fileI)) + ")")
                if (w + 1) == len(fileI):
                    print("Porting finished.")

        else:
            if filenameInput[-3:] == "-hd":
                os.rename(fileI[w], os.path.join(directory, filenameInput[:-3] + file_extensionInput))
                print("Done! (" + str((w + 1)) + "/" + str(len(fileI)) + ")")
                if (w + 1) == len(fileI):
                    print("Porting finished.")
            elif filenameInput[-3:] == "uhd" and args.low:
                os.rename(fileI[w], os.path.join(directory, filenameInput[:-4] + file_extensionInput))
                print("Done! (" + str((w + 1)) + "/" + str(len(fileI)) + ")")
                if (w + 1) == len(fileI):
                    print("Porting finished.")
    except Exception as e:
        print(e)
        print("Encountered an issue with %s. Skipping." % fileI[w])
