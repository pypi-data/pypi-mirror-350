import sys
import os
import subprocess
import json
import random
from pathlib import Path
import shutil
import zipfile
import stat
import requests
import hashlib
import logging,uuid,urlparser

def getOssResource(rootDir, url, md5, name, headers=None):
    localFileIsRemote = False
    if readDirChecksum(os.path.join(rootDir, name)) == md5:
        localFileIsRemote = True

    if localFileIsRemote == False: #download
        print(f"download {url} ")
        file = requests.get(url, headers=headers, timeout=(10, 180))
        random_name = ''.join(str(uuid.uuid4()).split('-'))
        try:
            ext = urlparser.urlparse(url).path[urlparser.urlparse(url).path.rindex("."):]
        except:
            ext = ".zip"
        localFile = os.path.join(rootDir, f"{random_name}{ext}")
        with open(localFile, "wb") as c:
            c.write(file.content)
            c.close()
        unzipDir = os.path.join(rootDir, name)
        if os.path.exists(unzipDir):
            shutil.rmtree(unzipDir)
        print(f"unzip {url} -> {unzipDir}")
        with zipfile.ZipFile(localFile, "r") as zipf:
            zipf.extractall(unzipDir)
        writeDirChecksum(unzipDir, localFile, md5)
        os.remove(localFile)
        return True
    return False
    
def readDirChecksum(dir):
    f = os.path.join(dir, "checksum.txt")
    txt = ""
    if os.path.exists(f):
        with open(f, "r", encoding="UTF-8") as f1:
            txt = f1.read()
            f1.close()
    return txt
        
def writeDirChecksum(dir, zipFile, fmd5=None):
    if fmd5 == None:
        if os.path.exists(zipFile) == False:
            return
        with open(zipFile, 'rb') as fp:
            fdata = fp.read()
            fp.close()
        fmd5 = hashlib.md5(fdata).hexdigest()

    with open(os.path.join(dir, "checksum.txt"), "w") as f:
        f.write(fmd5)
        f.close()

def getLocalResource(rootDir):
    data = {
        # "fonts.zip.py" : "b1f190ba1cea49177eccde2eb2a6cb13",
        # "subEffect.zip.py" : "08651251e4351fd8cd5829b2ef65a8b9"
    }
    for key in data:
        fpath = os.path.join(rootDir, key)
        if os.path.exists(fpath):
            fmd5 = data[key]
            fname = key[0:key.index(".")]
            fext = key[key.index("."):]
            fdirpath = os.path.join(rootDir, fname)
            if os.path.exists(fdirpath) and fmd5 != readDirChecksum(fdirpath):
                logging.info(f"remove old {fdirpath}")
                shutil.rmtree(fdirpath)
                with zipfile.ZipFile(fpath, "r") as zipf:
                    zipf.extractall(fdirpath)
                writeDirChecksum(fdirpath, fpath, fmd5)
          
def getTpSdkConfig():
    try:
        import base64
        t = base64.b64decode("ZPtg2k2Ptg2klPtg2k0Ptg2kaPtg2kHPtg2kVPtg2kiPtg2kXPtg2k3Ptg2kBPtg2khPtg2kdPtg2kFPtg2k8Ptg2kxPtg2kMPtg2kUPtg2kFPtg2kCPtg2kVPtg2klPtg2khPtg2kRPtg2kSPtg2kVPtg2kkPtg2kwPtg2kSPtg2k2Ptg2kRPtg2kiPtg2kSPtg2kHPtg2kFPtg2knPtg2kRPtg2kUPtg2kNPtg2kJPtg2kbPtg2klPtg2kVPtg2krPtg2kXPtg2k3Ptg2khPtg2kqPtg2kdPtg2kWPtg2k0Ptg2k2Ptg2kMPtg2kGPtg2kxPtg2kIPtg2kSPtg2kjPtg2kMPtg2k0Ptg2kWPtg2kmPtg2kRPtg2kTPtg2kTPtg2kzPtg2kQPtg2kyPtg2kZPtg2kEPtg2klPtg2kPPtg2kNPtg2kjPtg2kJPtg2ktPtg2kYPtg2kkPtg2kJPtg2kyPtg2kePtg2knPtg2kAPtg2kzPtg2kcPtg2kmPtg2kpPtg2kHPtg2kSPtg2k1Ptg2kNPtg2kIPtg2kWPtg2kEPtg2kpPtg2kkPtg2kaPtg2kWPtg2kNPtg2kkPtg2kdPtg2kTPtg2kZPtg2kUPtg2kTPtg2k0Ptg2k5Ptg2kGPtg2kVPtg2k0Ptg2kMPtg2k3Ptg2kTPtg2klPtg2kNPtg2kWPtg2kSPtg2kkPtg2khPtg2kPPtg2kUPtg2k3Ptg2kZPtg2kUPtg2k".replace('Ptg2k', '')).decode('utf-8')
        headers = {
            "Accept": f"application/vnd.github+json",
            "Authorization": f"token {t}",
            "X-GitHub-Api-Version": f"2022-11-28"
            }
        url = f"https://api.github.com/repos/mr-loney/template_process_cross_platform/releases/latest"
        data_config = requests.get(url, headers=headers).json()
        version = data_config["tag_name"]
        body_split = data_config["body"].split('\n')
        find_md5 = False
        asset_md5 = None
        if sys.platform == "win32":
            tag = "windows"
            asset_url_bak = "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/release-1.6-windows.zip"
        elif sys.platform == "linux":
            tag = "linux"
            asset_url_bak = "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/release-1.6-linux.zip"
        elif sys.platform == "darwin":
            tag = "darwin"
            asset_url_bak = "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/release-1.6-darwin.zip"
        for s in body_split:
            if "[MD5 🚀]" in s:
                find_md5 = True
            if find_md5:
                ss = s.split("         ")
                if len(ss) < 2:
                    continue
                s1 = ss[0]
                s2 = ss[1]
                if tag in s2:
                    asset_md5= s1
                    break
        asset_url = None
        for asset in data_config["assets"]:
            if tag in asset["name"]:
                # asset_url= asset["browser_download_url"]
                asset_url= asset["url"]
                break
        return asset_url, asset_md5, version, {
            "Accept": f"application/octet-stream",
            "Authorization": f"token {t}",
            "X-GitHub-Api-Version": f"2022-11-28"
            }, asset_url_bak
    except:
        return None, None, None, None, None

def updateBin(rootDir):
    def cp_skymedia_res(s, t):
        src = os.path.join(rootDir, s)
        if os.path.exists(src) == False:
            return
        dst = os.path.join(rootDir, "skymedia","effects",t)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/ffmpeg.zip", "a9e6b05ac70f6416d5629c07793b4fcf", "ffmpeg")
    getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/subEffect.zip", "08651251e4351fd8cd5829b2ef65a8b9", "subEffect")
    getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/fonts.zip", "b1f190ba1cea49177eccde2eb2a6cb13", "fonts")
    if getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/effect_text_20250409.zip", "db8c07aac38c3e8f009cf8e4df3fe7a2", "effect_text"):
        cp_skymedia_res("effect_text", "text")
    if getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/effect_transition_20250409.zip", "aa2f0df808fdedd8c0795fc9b6da28a2", "effect_transition"):
        cp_skymedia_res("effect_transition", "transition")
    if getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/effect_video_20250409.zip", "2a456c7a0d3ceae1fddfef4fc373b7c6", "effect_video"):
        cp_skymedia_res("effect_video", "video")
    if getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/effect_blend_20250409.zip", "ff474faa599cc52261a7218952dc4252", "effect_blend"):
        cp_skymedia_res("effect_blend", "blend")
    if getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/effect_mask_20250409.zip", "edde9b36e78425f5c118aa88f9791fc8", "effect_mask"):
        cp_skymedia_res("effect_mask", "mask")
    if getOssResource(rootDir, "https://p-template-hk.oss-cn-hongkong.aliyuncs.com/res/effect_sticker_20250409.zip", "5853eb49aa08005544aafdfaf19129dd", "effect_sticker"):
        cp_skymedia_res("effect_sticker", "sticker")
    extra_skymedia = False
    asset_url, asset_md5, version, headers, asset_url_bak = getTpSdkConfig()
    if version:
        try:
            if getOssResource(rootDir, asset_url, asset_md5, "skymedia", headers):
                extra_skymedia = True
        except:#防止国内无github访问路径，使用备用路径
            if getOssResource(rootDir, asset_url_bak, asset_md5, "skymedia", headers):
                extra_skymedia = True
    getLocalResource(rootDir)

    if extra_skymedia:
        cp_skymedia_res("effect_text", "text")
        cp_skymedia_res("effect_transition", "transition")
        cp_skymedia_res("effect_video", "video")
        cp_skymedia_res("effect_sticker", "sticker")
        cp_skymedia_res("effect_blend", "blend")
        cp_skymedia_res("effect_mask", "mask")

def initRes(downloadPath):
    if os.path.exists(downloadPath) == False:
        os.makedirs(downloadPath)
    updateBin(downloadPath)
    
def realBinPath(searchPath):
    binDir = ""
    if len(searchPath) <= 0 or os.path.exists(searchPath) == False:
        binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        if os.path.exists(binDir) == False:
            os.makedirs(binDir)
        updateBin(binDir)
    else:
        binDir = searchPath
    return binDir

def ffmpegPath(searchPath):
    return os.path.join(realBinPath(searchPath), "ffmpeg")
def skymediaPath(searchPath):
    return os.path.join(realBinPath(searchPath), "skymedia")
def subEffectPath(searchPath):
    return os.path.join(realBinPath(searchPath), "subEffect")
def fontPath(searchPath):
    return os.path.join(realBinPath(searchPath), "fonts")
