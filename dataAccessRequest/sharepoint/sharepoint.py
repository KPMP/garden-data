from distutils.command.config import config
from shareplum import Site, Office365
from shareplum.site import Version
import hashlib
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = ROOT_DIR + '/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['share_point']

USERNAME = config['user']
PASSWORD = config['password']
SHAREPOINT_URL = config['url']
SHAREPOINT_SITE = config['site']

class SharePoint:
    def auth(self):
        self.authcookie = Office365(
            SHAREPOINT_URL,
            username=USERNAME,
            password=PASSWORD,
        ).GetCookies()
        self.site = Site(
            SHAREPOINT_SITE,
            version=Version.v365,
            authcookie=self.authcookie,
        )
        return self.site
    
    def upload_folder(self):
        self.auth_site = self.auth()
        desiredDir = 'CKD_PAS'
        for root, dirs, files in os.walk("../data/"):
            for file in files:
                if file != '.DS_Store':
                    packageName = root.split('/')[-1]
                    if packageName == desiredDir:
                        packageName = ''
                    with open(root + '/' +file, mode='rb') as readfile:
                        fileContent = readfile.read()
                        self.auth_site.Folder('Shared Documents/'+desiredDir+'/')

                        if packageName != '':
                            folder = self.auth_site.Folder('Shared Documents/'+desiredDir+'/'+packageName +'/')
                            folder.upload_file(fileContent, file)
                            print('for file ' + root+'/'+file+ ', md5s:', hashlib.md5(fileContent).hexdigest(), hashlib.md5(folder.get_file(file)).hexdigest())
                        else:
                            folder = self.auth_site.Folder('Shared Documents/' + desiredDir + '/')
                            folder.upload_file(fileContent, file)
                            print('for file ' + root+'/'+file+ ', md5s:', hashlib.md5(fileContent).hexdigest(), hashlib.md5(folder.get_file(file)).hexdigest())


SharePoint().upload_folder()