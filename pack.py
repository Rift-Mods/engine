import sys
import os
import urllib.request
import subprocess
import zipfile
from loguru import logger
from sys import platform
import json
import time
import shutil
from zipfile import ZipFile
from diff_match_patch import diff_match_patch
RIFT_SOURCE = './source'
RIFT_SOURCE = os.path.abspath(RIFT_SOURCE)
def cleanup(data):
    output = []
    for line in data:
            line = line.split("//")[0]
            line = line.strip()
            if len(line) > 0 and not line.startswith("//"):
                output.append(f"{line}\n")
    return ''.join(output)
if len(sys.argv) > 1:
    mod = sys.argv[1]

    manifest_path = os.path.join(mod,'manifest.json')
    if os.path.exists(os.path.join(mod,'manifest.json')):

        with open(manifest_path, 'rt') as f:
            manifest = json.loads(f.read())
            output_changes = []
            with ZipFile(f'{manifest["name"]}.zip', 'w') as myzip:
                for change in manifest['changes']:
                    if os.path.exists(os.path.join(mod,change['org'])) and os.path.exists(os.path.join(RIFT_SOURCE,change['dest'])):
                        with open(os.path.join(mod,change['org']), 'rt') as f1:
                            with open(os.path.join(RIFT_SOURCE,change['dest']), 'rt') as f2:
                                f1_clean = cleanup(f1.readlines())
                                f2_clean = cleanup(f2.readlines())
                                dmp = diff_match_patch()
                                patches = dmp.patch_make(f2_clean,f1_clean)

                                myzip.writestr(f"{os.path.splitext(change['org'])[0]}.diff",dmp.patch_toText(patches))
                                output_changes.append({'org': f"{os.path.splitext(change['org'])[0]}.diff", 'dest': change['dest']})
                    else:
                        logger.critical(f"Cant find source files")
                        exit(1)
                manifest['changes'] = output_changes
                myzip.writestr('manifest.json', json.dumps(manifest,indent=2))

    else:
        logger.critical(f"No manifest file in {manifest_path}")
        exit(1)
else:
    logger.critical("No arguments given")
    exit(1)
