from urllib.parse import *

def transcode(srcFile):
    try:
        from pathlib import Path
        from PIL import Image
        file_name = Path(srcFile).name
        ext = file_name[file_name.index("."):].lower()
        if ext in [".jpg", ".png", ".jpeg", ".bmp"]:
            image = Image.open(srcFile, "r")
            format = image.format
            if format.lower() != "webp":
                fname = Path(srcFile).name
                newFile = srcFile.replace(fname[fname.index("."):], ".webp")
                image.save(newFile, "webp", quality=90)
                image.close()
                return True, newFile
    except Exception as e:
        pass
    return False, srcFile

def additionalUrl(srcFile, ossUrl):
    from pathlib import Path
    from PIL import Image
    try:
        file_name = Path(srcFile).name
        ext = file_name[file_name.index("."):].lower()
        params = {}
        if ext in [".jpg", ".png", ".jpeg", ".bmp", ".webp", ".gif"]:
            img = Image.open(srcFile)
            params["width"] = img.width
            params["height"] = img.height
        elif ext in [".mp4",".mov",".avi",".wmv",".mpg",".mpeg",".rm",".ram",".flv",".swf",".ts"]:
            params = {}
        elif ext in [".mp3",".aac",".wav",".wma",".cda",".flac",".m4a",".mid",".mka",".mp2",".mpa",".mpc",".ape",".ofr",".ogg",".ra",".wv",".tta",".ac3",".dts"]:
            params = {}
        else:
            params = {}
        parsed_url = urlparse(ossUrl)
        updated_query_string = urlencode(params, doseq=True)
        final_url = parsed_url._replace(query=updated_query_string).geturl()
        return final_url
    except:
        return ossUrl

def upload(src, taskUUID=None, needTranscode=True, keep_it_always=False):
    import os
    from pathlib import Path
    from ryry import taskUtils
    if os.path.exists(src) == False:
        raise Exception(f"upload file not found")
    if taskUUID == None or len(taskUUID) <= 0:
        taskUUID = taskUtils.taskInfoWithFirstTask()
    targetDomain = taskUtils.taskDomainWithUUID(taskUUID)

    if needTranscode:
        needDeleteSrc, newSrc = transcode(src)
    else:
        needDeleteSrc = False
        newSrc = src
    support_subdomain = getSubdomain(targetDomain)
    if support_subdomain:
        import uuid
        file_name = Path(newSrc).name
        ext = os.path.splitext(file_name)[-1][1:]
        new_file_name = ''.join(str(uuid.uuid4()).split('-'))
        ossurl = ftpUpload(newSrc, f"{new_file_name}.{ext}", support_subdomain)
    else:
        from ryry import ryry_webapi
        file_name = Path(newSrc).name
        ossurl = ryry_webapi.upload(newSrc, os.path.splitext(file_name)[-1][1:], keep_it_always)
        
    ossurl = additionalUrl(newSrc, ossurl)
    if needDeleteSrc:
        os.remove(newSrc)
    return ossurl

def deepFtpUpload(file, new_file_name, ftp, writepath, readpath):
    import ftplib, os
    try:
        safe_cwd(ftp, writepath)
    except ftplib.error_perm as e:
        if e.args[0].startswith('550'):
            safe_mkd(ftp, writepath)
            safe_cwd(ftp, writepath)
            
    with open(file, 'rb') as f:
        ftp.storbinary(f'STOR {new_file_name}', f)
    return f"{readpath}/{new_file_name}"

def ftpUpload(file, new_file_name, subdomain):
    ip = subdomain["host"]
    port = subdomain["port"]
    username = subdomain["username"]
    password = subdomain["password"]
    writepath = subdomain["writepath"]
    readpath = subdomain["readpath"]
    import ftplib
    ftp = ftplib.FTP()
    ftp.connect(ip, port, timeout=5)
    ftp.login(username, password)  

    s = deepFtpUpload(file, new_file_name, ftp, writepath, readpath)
    ftp.quit()
    return s
    
def _can_connect_ftp(ip, port, username, password, writepath):  
    import ftplib
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port, timeout=5)
        ftp.login(username, password)  
        try:
            safe_cwd(ftp, writepath)
        except ftplib.error_perm as e:
            if e.args[0].startswith('550'):
                # 如果远程目录不存在，则创建它
                safe_mkd(ftp, writepath)
                safe_cwd(ftp, writepath)
        ftp.quit()
        return True
    except Exception as e:  
        print(f"Failed to connect to FTP server {ip}:{writepath} {e}")  
        return False
ftp_192_168_50_12={
    "host" : "192.168.50.12",
    "port": 21,
    "username" : "mcn",
    "password" : "meco@2024+",
    "writepath" : "mnt/NAS/mcn/cache",
    "readpath" : "ftp://192.168.50.12/mnt/NAS/mcn/cache"
}
ftp_183_6_90_205={
    "host" : "183.6.90.205",
    "port": 2221,
    "username" : "mcn",
    "password" : "meco@2024+",
    "writepath" : "mnt/NAS/mcn/cache",
    "readpath" : "ftp://183.6.90.205/mnt/NAS/mcn/cache"
}
SUBDOMAIN = {
    "183.6.90.205": [
        ftp_192_168_50_12,
        ftp_183_6_90_205,
    ],
    "192.168.50.138": [
        ftp_192_168_50_12,
        ftp_183_6_90_205,
    ]
}

def getSubdomain(targetDomain):
    if len(targetDomain) <= 0:
        return None
    for ip in SUBDOMAIN.keys():
        for host_item in SUBDOMAIN[ip]:
            if targetDomain == host_item["readpath"]:
                if _can_connect_ftp(ip, host_item["port"], host_item["username"], host_item["password"], host_item["writepath"]):
                    return host_item
    return None

def getFirstSupportSubdomain():
    def get_network_hash():
        import socket
        from hashlib import md5
        try:
            local_ip = socket.gethostbyname('localhost')
        except socket.gaierror:
            local_ip = '127.0.0.1'  # 默认回退到 localhost 地址
        return md5(local_ip.encode('utf-8')).hexdigest()
    network_hash = get_network_hash()  
    def _getFirstSupportSubdomain():
        for ip in SUBDOMAIN.keys():
            for host_item in SUBDOMAIN[ip]:
                if _can_connect_ftp(ip, host_item["port"], host_item["username"], host_item["password"], host_item["writepath"]):
                    return host_item
        return None
    from ryry import store
    sp = store.Store()
    read_data = sp.read()
    firstSupportDomainConfig = read_data.get("firstSupportDomainConfig", {})
    if len(firstSupportDomainConfig.keys()) < 1:
        firstSupportDomainConfig = _getFirstSupportSubdomain()
        firstSupportDomainConfig["hash"] = network_hash
        read_data["firstSupportDomainConfig"] = firstSupportDomainConfig
        sp.write(read_data)
    else:
        last_network_hash = firstSupportDomainConfig["hash"]
        if last_network_hash != network_hash:
            firstSupportDomainConfig = _getFirstSupportSubdomain()
            firstSupportDomainConfig["hash"] = network_hash
            read_data["firstSupportDomainConfig"] = firstSupportDomainConfig
            sp.write(read_data)
    return firstSupportDomainConfig

def download(url, saveDir):
    import uuid, requests, os
    from urlparser import urlparser
    from fake_useragent import UserAgent
    if len(url) <= 0:
        return None
    try:
        name = ''.join(str(uuid.uuid4()).split('-'))
        
        if url.startswith("ftp"):
            import ftplib, random
            parsed_url = urlparse(url)  
            host = parsed_url.hostname
            if host in SUBDOMAIN:
                for host_item in SUBDOMAIN[host]:
                    try:
                        ip = host_item["host"]
                        port = host_item["port"]
                        username = host_item["username"]
                        password = host_item["password"]
                        writepath = host_item["writepath"]
                        readpath = host_item["readpath"]
                        replace_path = host_item.get("path_replace", [])
                        ftp = ftplib.FTP()
                        ftp.connect(ip, port, timeout=5)
                        ftp.login(username, password)
                    
                        if len(replace_path) > 0:
                            parsed_url = urlparse(url.replace(replace_path[0], replace_path[1]))
                        remote_filepath = parsed_url.path
                        if "." in urlparser.urlparse(url).path:
                            ext = urlparser.urlparse(url).path[urlparser.urlparse(url).path.index("."):]
                            savePath = os.path.join(saveDir, f"{name}{ext}")
                            with open(savePath, 'wb') as f:  
                                ftp.retrbinary(f'RETR {remote_filepath}', f.write)
                            return savePath
                        else:
                            safe_cwd(ftp, remote_filepath)
                            files = ftp.nlst()
                            if files:
                                random_file = random.choice(files)
                                savePath = os.path.join(saveDir, f"{name}_{random_file}")
                                with open(savePath, 'wb') as f:  
                                    ftp.retrbinary(f'RETR {random_file}', f.write)  
                                return savePath
                        ftp.quit()
                    except Exception as ex:
                        pass
            print(f"download fail: domain {host} not support")
        elif url.startswith("http"):
            ua = UserAgent()
            ext = urlparser.urlparse(url).path[urlparser.urlparse(url).path.index("."):]
            savePath = os.path.join(saveDir, f"{name}{ext}")
            if os.path.exists(savePath):
                os.remove(savePath)
            #first orginal url
            try:
                file = requests.get(url, verify=False, 
                                    headers={'User-Agent': ua.random}, timeout=30)
                with open(savePath, "wb") as c:
                    c.write(file.content)
                if os.path.exists(savePath) and os.stat(savePath).st_size > 100:
                    return savePath
            except:
                pass
            
            try:
                parsed_url = urlparser.urlparse(url)
                domain_parts = parsed_url.netloc.split('.')
                if len(domain_parts) >= 3:
                    subdomain = domain_parts[0]  # 例如：upload、r2、widget等
                else:
                    subdomain = domain_parts[0]  # 默认处理
                #second, bak url
                file = requests.get(f"https://aigc.zjtemplate.com/{subdomain}{parsed_url.path}", 
                                    verify=False, 
                                    headers={
                                        'User-Agent': ua.random,
                                    },
                                    timeout=30)
                with open(savePath, "wb") as c:
                    c.write(file.content)
                if os.path.exists(savePath) and os.stat(savePath).st_size > 100:
                    return savePath
            except Exception as ex:
                print(ex)
                pass
                
            print(f"download success but file not found")
        else:
            print(f"url {url} not support")
    except Exception as e:
        print(f"download fail: {e}")
    return None

def safe_cwd(ftp, path):
    try:
        ftp.cwd(path)
        return
    except:
        pass
    
    if path[0:1] == "/":
        try:
            ftp.cwd(path.lstrip('/'))
            return
        except:
            pass
    else:
        try:
            ftp.cwd('/' + path)
            return
        except:
            pass
        
    if path[-1:] != "/":
        try:
            ftp.cwd(path + "/")
            return
        except:
            pass
    else:
        try:
            ftp.cwd(path.rstrip('/'))
            return
        except:
            pass
    raise Exception("cwd fail!")

def safe_mkd(ftp, path):
    try:
        ftp.mkd(path)
        return
    except:
        pass
    
    if path[0:1] == "/":
        try:
            ftp.mkd(path.lstrip('/'))
            return
        except:
            pass
    else:
        try:
            ftp.mkd('/' + path)
            return
        except:
            pass
        
    if path[-1:] != "/":
        try:
            ftp.mkd(path + "/")
            return
        except:
            pass
    else:
        try:
            ftp.mkd(path.rstrip('/'))
            return
        except:
            pass
    raise Exception("cwd fail!")

def downloadDir(url, saveDir, useCount=-1, autoDelete=False):
    import uuid, os
    if len(url) <= 0:
        return None
    try:
        name = ''.join(str(uuid.uuid4()).split('-'))
        
        if url.startswith("ftp"):
            import ftplib, random
            parsed_url = urlparse(url)  
            host = parsed_url.hostname
            if host in SUBDOMAIN:
                for host_item in SUBDOMAIN[host]:
                    try:
                        ip = host_item["host"]
                        port = host_item["port"]
                        username = host_item["username"]
                        password = host_item["password"]
                        replace_path = host_item.get("path_replace", [])
                        ftp = ftplib.FTP()
                        ftp.connect(ip, port, timeout=5)
                        ftp.login(username, password)   
                    
                        if len(replace_path) > 0:
                            parsed_url = urlparse(url.replace(replace_path[0], replace_path[1]))
                        remote_filepath = parsed_url.path
                        safe_cwd(ftp, remote_filepath)
                        files = ftp.nlst()
                        savePath = os.path.join(saveDir, f"{name}")
                        if os.path.exists(savePath) == False:
                            os.makedirs(savePath)
                        if useCount > 0 and useCount <= len(files):
                            files = random.sample(files, useCount)
                        for file in files:
                            with open(os.path.join(savePath, file), 'wb') as f:  
                                ftp.retrbinary(f'RETR {file}', f.write)
                            if autoDelete:
                                try:
                                    ftp.delete(file)
                                except Exception as e:
                                    print(f"Error deleting file {file}: {e}")
                        ftp.quit()
                        return savePath
                    except Exception as ex:
                        print(ex)
                        pass
            print(f"downloadDir fail: domain {host} not support")
        else:
            print(f"url {url} not support")
    except Exception as e:
        print(f"downloadDir fail: {e}")
    return None
