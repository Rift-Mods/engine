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
import xml.etree.ElementTree as ET
#ENV

RIFT_PATH = r'./test' # rift dir
RIFT_SOURCE = r'./source' # the dir to decompile to
BAD_SHIT = [
        'Assembly-CSharp.dll', # dont touch this it breaks everything
        'System.Core.dll'
] # dont touch this it breaks everything
#ENV



linux = False
RIFT_PATH = os.path.abspath(RIFT_PATH)
RIFT_SOURCE = os.path.abspath(RIFT_SOURCE)

if platform == "linux" or platform == "linux2":
    linux = True
    BAD_SHIT.append('mscorlib.dll')
#     BAD_SHIT.append('System.Core.dll')

BAD_SHIT = [x.lower() for x in BAD_SHIT]
def cleanup(data):
    output = []
    for line in data:
            if not ("\"" in line or "\'" in line):
                line = line.split("//")[0]
            line = line.strip()
            if len(line) > 0 and not line.startswith("//"):
                output.append(f'{line}\n')
    return ''.join(output)

def check_ilspy():
        try:
                subprocess.run(['ilspycmd', '-v'], stdout=subprocess.DEVNULL)
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

        shutil.copytree(os.path.join(RIFT_PATH,"RIFT_Data/Managed"), os.path.join(RIFT_SOURCE,"Managed"))
        logger.info("Starting decompile in 1 second")
        args = ['ilspycmd','-p', f'-o {RIFT_SOURCE}' , os.path.join(RIFT_SOURCE,"Managed","Assembly-CSharp.dll"), '-lv CSharp9_0']
        logger.info(args)
        subprocess.run(args)
        logger.info("Decompiled")
        logger.info("Deleting random stuff ¯\_(ツ)_/¯")
        shutil.rmtree(os.path.join(RIFT_SOURCE, "Properties"))
        # files_out = []
        # for root, dirs, files in os.walk(RIFT_SOURCE, topdown=False):
        #         for name in files:
        #                 if name.endswith(".cs"):
        #                         with open(os.path.join(root,name), 'r') as f:
        #                                 data = f.read()
        #                                 with open(os.path.join(root,name), 'w') as ff:
        #                                         ff.write(data.replace("MathF", "Mathf"))




def compile():

        # cmd1 = ['dotnet','restore',RIFT_SOURCE]
        cmd2 = ['dotnet', 'build', '-c','release', RIFT_SOURCE]
        # cmd2 = []
        # if linux:
        #         cmd2.append('csc')
        # else:
        #         cmd2.append('dotnet')
        #         cmd2.append("C:\\Program Files\\dotnet\sdk\\7.0.100\Roslyn\\bincore\\csc.dll")

        # cmd2.append("/target:library")
        # cmd2.append("/out:Assembly-CSharp.dll")
        elm = ET.parse(os.path.join(RIFT_SOURCE,"Assembly-CSharp.csproj"))
        elm.getroot().remove(elm.findall("ItemGroup")[1])
        elm.find("PropertyGroup").find("TargetFramework").text = 'net48'
        # if linux:
        #         elm.find("PropertyGroup").find("TargetFramework").text = 'net40'
        e = ET.SubElement(elm.getroot(), "ItemGroup")
        with open(os.path.join(RIFT_PATH, "RIFT_Data", "ScriptingAssemblies.json")) as f:
                j  = json.loads(f.read())

                for file in os.listdir(os.path.join(RIFT_PATH,"RIFT_Data/Managed/")):
                        if file.endswith(".dll") and not (file.lower() in BAD_SHIT):
                                ee = ET.SubElement(e, "Reference", {"Include":os.path.splitext(file)[0]})
                                eee = ET.SubElement(ee, "HintPath")
                                eee.text = os.path.abspath(os.path.join(RIFT_SOURCE,'Managed/',file))
        # eee.set("123123123123","123131231")

        # elm.getroot().append(e)
        elm.write(os.path.join(RIFT_SOURCE,"Assembly-CSharp.csproj"))


        # for file in os.listdir(os.path.join(RIFT_PATH,"RIFT_Data/Managed/")):
        #         if file.endswith(".dll") and not file.lower() in BAD_SHIT:

                        # cmd2.append(f"/r:{os.path.join(RIFT_PATH,'RIFT_Data/Managed/',file)}")




        logger.info("Starting compile in 1 second")
        result = subprocess.run(cmd2, capture_output=True, text=True)
        if os.path.exists(os.path.join(RIFT_SOURCE, "bin/release/net48/Assembly-CSharp.dll")):
                # logger.error(result.stdout)
                logger.info("Compiled!")
        else:
                logger.error(result.stdout)
                logger.critical("No output files Compile failed!")
                exit(1)

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
if len(sys.argv) > 2:
        command = sys.argv[1]
        RIFT_PATH = sys.argv[2]
        if command == 'add':
                # restore() // dont restore easy way to fix --no-restore ¯\_(ツ)_/¯
                decompile()
                dmp = diff_match_patch()
                for mod in sys.argv[3:]:
                        if os.path.exists(mod):
                                with ZipFile(mod,'r') as f:
                                        logger.info("file loaded")
                                        logger.info("parsing mod")
                                        manifest_object = json.loads(f.read("manifest.json").decode('ascii'))
                                        logger.info(manifest_object)
                                        for change in manifest_object['changes']:
                                                patch_data = f.read(change['org']).decode('ascii')
                                                patches = dmp.patch_fromText(patch_data)
                                                with open(os.path.join(RIFT_SOURCE,change['dest']), 'rt') as ff:
                                                        unpatched_data = cleanup(ff.readlines())
                                                        patched_data = dmp.patch_apply(patches,unpatched_data)
                                                        if all(patched_data[1]) == True:
                                                                with open(os.path.join(RIFT_SOURCE,change['dest']), 'wt') as fff:
                                                                        fff.write(patched_data[0])
                                                        else:
                                                                logger.warning(f"couldnt patch {change['dest']}")



                        else:
                                logger.critical("Failed to open file")
                                exit(1)
                compile()
                logger.info("Moving file")
                if not os.path.exists(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll.bak")): os.rename(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"), os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll.bak"))
                if os.path.exists(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll")): os.remove(os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"))
                shutil.move(os.path.join(RIFT_SOURCE, "bin/release/net48/Assembly-CSharp.dll"), os.path.join(RIFT_PATH,"RIFT_Data/Managed/Assembly-CSharp.dll"))
                logger.info("Deleting Source")
                shutil.rmtree(RIFT_SOURCE)

        if command == 'restore':
                restore()
        if command == 'getsource':
                decompile()
        if command == 'compile':
                compile()
        if command == 'clean':
                logger.info("Deleting Source")
                shutil.rmtree(RIFT_SOURCE)
else:
        logger.critical("No arguments given")
        exit(1)
