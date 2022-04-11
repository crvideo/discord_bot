import os
import subprocess
import json
import re
import urllib.parse
from shutil import which
from pathlib import Path
from os.path import exists
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="config file for raincoat-prowlarr")
    parser.add_argument("--indexer", help="which indexer to search",default = "jackett,prowlarr")
    args = parser.parse_args()
    return args


################################################################################
################################################################################
###			Run shell cmd and capture stdoutput
################################################################################
################################################################################

def runShellCmd(cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE, shell = True)
    return output


################################################################################
################################################################################
### raincoat to search Jackett
### Because prowlarr has bugs with some private tracker, so use raincoat to query
### Jackett with private trackers. If prowlarr fixed the bugs, this can be ignored
### private tracker is safer so this is the top choice
################################################################################
################################################################################

def search_raincoat(args, keyword, indexer_manager):
    cfg_path = f"{str(Path.home())}/.config/raincoat_prowlarr.json"
    if args.config and exists(args.config):
        conf = args.config
    elif exists(cfg_path):
        conf = cfg_path
    else:
        print("No config file found")
        return ''
        
    if which("raincoat_prowlarr"):
        print(f"Use config file: {conf}")
        cmd = f"raincoat_prowlarr --indexer_manager {indexer_manager} -d 1 -c {conf} \""+ urllib.parse.quote(keyword) +'"'
        print(cmd)
        res = runShellCmd(cmd)
        for line in res.stdout.decode("utf8").splitlines():
            if re.search("Sending",line):
                return f"Downloading qBittorrent through {indexer_manager}: {keyword}"
            elif re.search("did not yield any result",line):
                return ''
    else:
        print("please install raincoat_prowlarr by: pip install raincoat-jackett")
        return ''
        
################################################################################
################################################################################
### Script based on Movie_Data_Capture: https://github.com/yoshiko2/Movie_Data_Capture
### Search JavDB, JavBus for a specific video
### These two sites has magnet Link and has chinese subtitle somethies
### As second choice
################################################################################
################################################################################
        
# def search_MovieInfo_number(number):
#     res = runShellCmd('python /mnt/mpathd/crvideo/myscript/python_project/Myproject/MovieInfo.py --number "' + number +'"')
#     if res.stdout :
#         json_data = json.loads(res.stdout)
#         print(json_data)
#         download_res = runShellCmd('python /mnt/mpathd/crvideo/myscript/python_project/Myproject/download.py --download "' + json_data["magnetlink"] +'"')
#         print(download_res.stdout)
#         if re.search("Torrent", download_res.stdout.decode("utf8")):
#             return "Downloading qBittorrent through MovieInfo"
#     return ''

    
################################################################################
################################################################################
###			main function for search
################################################################################
################################################################################

def search(number):
    args = parse_args()
    indexers = args.indexer.split(',')
    if indexers:
        for idx in indexers:
            result = search_raincoat(args,number,idx)
            if result:
                break
    if not result:
        result="not found"
    return result


if __name__ == '__main__':
    print(search("SSIS-358"))
    #print(search_prowlarr("SSIS-350"))
    #print(search_prowlarr("Uncensored LeakedTEK-072"))
    #print(search("FC2-2125351"))
    #print(search_MovieInfo_number("FC2-2125351"))
    
