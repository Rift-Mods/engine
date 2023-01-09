import sys
import os
import urllib.request
import subprocess
from sys import exit
import zipfile
from loguru import logger
from sys import platform
import time
import shutil
from zipfile import ZipFile
import json
from diff_match_patch import diff_match_patch
#ENV

RIFT_PATH = './test' # rift dir
RIFT_SOURCE = './source' # the dir to decompile to
BAD_SHIT = [
        'mscorlib.dll', # dont touch this it breaks everything
        'System.Core.dll', # dont touch this it breaks everything
        'Assembly-CSharp.dll' # dont touch this it breaks everything
] # dont touch this it breaks everything
#ENV


linux = False
BAD_SHIT = [x.lower() for x in BAD_SHIT]
RIFT_PATH = os.path.abspath(RIFT_PATH)
RIFT_SOURCE = os.path.abspath(RIFT_SOURCE)

if platform == "linux" or platform == "linux2":
    linux = True


def cleanup(data):
    output = []
    for line in data:
            line = line.split("//")[0]
            line = line.strip()
            if len(line) > 0 and not line.startswith("//"):
                output.append(f"{line}\n")
    return ''.join(output)

def check_ilspy():
        try:
                subprocess.run(['ilspycmd', '-v'], stdout=None,stderr=None)
        except FileNotFoundError:
                logger.critical("ilspycmd is not installed")
                exit(1)
        # if not os.path.exists('./dnSpy/dnSpy.Console.exe'):

        #         check_dnspy()
def decompile():
        if os.path.exists(RIFT_SOURCE):
                shutil.rmtree(RIFT_SOURCE)
                os.makedirs(RIFT_SOURCE)
        else:
                os.makedirs(RIFT_SOURCE)
        logger.info("Starting decompile in 1 second")
        time.sleep(1)
        args = ['ilspycmd','-p', f'-o {RIFT_SOURCE}' , os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"), '-lv CSharp1']
        logger.info(args)
        subprocess.run(args)
        logger.info("Decompiled")

def compile():

        cmd1 = ['dotnet','restore',RIFT_SOURCE]
        cmd2 = ['msbuild', RIFT_SOURCE]
        # if linux:
        #         cmd.append('mcs')
        # for file in os.listdir(os.path.join(RIFT_PATH,"RIFT_Data/Managed/")):
        #         if file.endswith(".dll") and not file.lower() in BAD_SHIT:
        #                 cmd.append(f"/r:{os.path.join(RIFT_PATH,'RIFT_Data/Managed/',file)}")
        # cmd.append(os.path.join(RIFT_SOURCE,"**.cs"))
        # cmd.append("/target:library")
        # cmd.append("/out:Assembly-CSharp.dll")

        logger.info("Starting compile in 1 second")
        time.sleep(1)
        subprocess.run(cmd1)
        logger.info("Project restored!")
        subprocess.run(cmd2)
        logger.info("Compiled!")

logger.info(f"platform: {platform}")
if linux:
    logger.info(f"using \'wine\' as windows runner")
logger.info(f"checking for ilSpy")
check_ilspy()

logger.info("START")

def restore():
        logger.info("Restoring vanilla")
        if os.path.exists(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll.bak")):
                logger.info("Backup found restoring")
                if os.path.exists(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll")): os.remove(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"))
                shutil.copy(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll.bak"), os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"))
        else:
                logger.critical("No bacups")
if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'add':
                restore()
                decompile()
                dmp = diff_match_patch()
                for mod in sys.argv[2:]:
                        if os.path.exists(mod):
                                with ZipFile(mod,'r') as f:
                                        logger.info("file loaded")
                                        logger.info("parsing mod")
                                        manifest_object = json.loads(f.read("manifest.json").decode('ascii'))
                                        logger.info(manifest_object)
                                        for change in manifest_object['changes']:
                                                patch_data = f.read(change['org']).decode('ascii')
                                                logger.info(patch_data)
                                                patches = dmp.patch_fromText(patch_data)
                                                with open(os.path.join(RIFT_SOURCE,change['dest']), 'rt') as ff:
                                                        unpatched_data = cleanup(ff.readlines())
                                                        patched_data = dmp.patch_apply(patches,unpatched_data)
                                                        # print(patched_data[1])
                                                        if all(patched_data[1]) == True:
                                                                with open(os.path.join(RIFT_SOURCE,change['dest']), 'wt') as fff:
                                                                        fff.write(patched_data[0])
                                                        else:
                                                                logger.warning(f"couldnt patch {change['dest']}")



                        else:
                                logger.critical("Failed to open file")
                                exit(1)
                compile()
                logger.info("Deleting Source")
                # shutil.rmtree(RIFT_SOURCE)
                logger.info("Moving file")
                if not os.path.exists(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll.bak")): os.rename(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"), os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll.bak"))
                shutil.move('Assembly-CSharp.dll', os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"))

        if command == 'restore':
                restore()
        if command == 'get_source':
                decompile()
        if command == 'clean':
                logger.info("Deleting Source")
                shutil.rmtree(RIFT_SOURCE)
else:
        logger.critical("No arguments given")
        exit(1)
