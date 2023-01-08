import sys
import os
import urllib.request
import subprocess
import zipfile
from loguru import logger
from sys import platform
import time
import shutil
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
    wine_cmd = 'wine'
    build_cmd = 'mcs'
    linux = True
else:
    wine_cmd = ''
    build_cmd = ''
def check_dnspy():
        if not os.path.exists('./dnSpy/dnSpy.Console.exe'):
                logger.warning("dnSpy not found downloading from https://github.com/dnSpy/dnSpy/releases/tag/v6.1.8")
                urllib.request.urlretrieve("https://github.com/dnSpy/dnSpy/releases/download/v6.1.8/dnSpy-net-win64.zip", "dnSpy.zip")
                logger.info("downloaded!")
                logger.info("extracting!")
                with zipfile.ZipFile("dnSpy.zip", 'r') as zip_ref:
                        zip_ref.extractall("./dnSpy/")
                logger.info("extracted!")
                os.remove('./dnSpy.zip')
                check_dnspy()
def decompile():
        logger.info("Starting decompile in 1 second")
        time.sleep(1)
        subprocess.run([wine_cmd, 'dnSpy/dnSpy.Console.exe', '-o', RIFT_SOURCE, os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll")])
        logger.info("Decompiled")

def compile():
        cmd = [build_cmd]
        for file in os.listdir(os.path.join(RIFT_PATH,"RIFT_Data/Managed/")):
                if file.endswith(".dll") and not file.lower() in BAD_SHIT:
                        logger.info(file)
                        logger.info(BAD_SHIT)
                        cmd.append(f"/r:{os.path.join(RIFT_PATH,'RIFT_Data/Managed/',file)}")
        cmd.append(os.path.join(RIFT_SOURCE,'Assembly-CSharp',"*.cs"))
        cmd.append("/target:library")
        cmd.append("/out:Assembly-CSharp.dll")
        logger.info(cmd)
        logger.info("Starting compile in 1 second")
        time.sleep(1)
        subprocess.run(cmd)
        logger.info("Compiled!")

logger.info(f"platform: {platform}")
if wine_cmd != '':
    logger.info(f"using \'{wine_cmd}\' as windows runner")
logger.info(f"checking for dnSpy")
check_dnspy()

logger.info("START")
if len(sys.argv) > 1:
        decompile()
        for mod in sys.argv[1:]:
                if os.path.exists(mod):
                        with open(mod) as f:
                                logger.info("file loaded")
                                logger.info("parsing mod")
                                logger.info("waiting 60 seconds before continuing")
                                time.sleep(60)



                else:
                        logger.critical("Failed to open file")
                        exit(1)
        compile()
        logger.info("Deleting Source")
        shutil.rmtree(RIFT_SOURCE)
        logger.info("Moving file")
        if os.path.exists(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll")): os.remove(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"))
        shutil.move('Assembly-CSharp.dll', os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"))
else:
        logger.critical("No arguments given")
        exit(1)
