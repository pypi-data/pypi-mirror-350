import sys
import os
import urllib3
import shutil
import zipfile
import pathlib
import json
import getpass
import chardet
import base64

#this is meant to be used as a startup script
#all commands will be executed when python -m script -i is used


#generic function to load library from gitlab

def getSuitePath():
    installDir=os.path.join(os.path.expanduser('~'),'.labkey','software','src')
    if not os.path.isdir(installDir):
        os.makedirs(installDir)
    return installDir

def buildGITURL(server,project,path,branch='master'):
    if server.find('wiscigt')>-1:
        projectURL='%2f'.join(project)
        pathURL='%2f'.join(path)
        return server+'/api/v4/projects/'+projectURL+'/repository/files/'+pathURL+'?ref='+branch
    if server.find('fmf.uni-lj.si')>-1:
        projectURL='/'.join(project)#studen/nixSuite
        pathURL='/'.join(path)
        return '/'.join([server,projectURL,'raw',branch,pathURL])



def getResources():
    server='http://wiscigt.powertheword.com'
    project=['labkey','nixsuite']
    path=['remoteResources','resources.json']

    server='https://git0.fmf.uni-lj.si'
    project=['studen','nixSuite']
    
    remoteSourcesURL=buildGITURL(server,project,path)
    print('remoteSourcesURL {}'.format(remoteSourcesURL))
    http = urllib3.PoolManager()
    r = http.request('GET', remoteSourcesURL)
    #returns a JSON
    encoding=chardet.detect(r.data)['encoding']
    dataDecoded=r.data.decode(encoding)
    jsonData=json.loads(dataDecoded)
    print(jsonData)

    #since gogs drops raw data, we already did the hard part 
    if server.find('fmf.uni-lj.si')>-1:
        return jsonData

    #on gitlab a further decoding step is required
    #we are interested in content, do looped way of decoding it 
    b64_bytes=jsonData['content'].encode('ascii')
    m_bytes=base64.b64decode(b64_bytes)
    m=m_bytes.decode('ascii')
    return json.loads(m)

def loadModule(slicer,qt,name,moduleName):
    loadLibrary(name)
    modulePath=os.path.join(getSuitePath(),name,'slicerModules',moduleName+'.py')
    factoryManager = slicer.app.moduleManager().factoryManager()

    factoryManager.registerModule(qt.QFileInfo(modulePath))

    factoryManager.loadModules([moduleName,])
    slicer.util.selectModule(moduleName)


def loadLibrary(name,doReload=True):
    print('loadLibrary')
    installDir=getSuitePath()
    finalName=os.path.join(installDir,name)
    if os.path.isdir(finalName):
        if not doReload:
            #1 keep existing copy, return
            sys.path.append(finalName)
            return
        else:
            #1 remove existing copy
            shutil.rmtree(finalName)
    
    #load library from git, store it at a default location and 
    #add path to the python sys
    remoteSources=getResources()

    #two steps:
    #1 Download

    tempDir=os.path.join(os.path.expanduser('~'),'temp')
    if not os.path.isdir(tempDir):
        os.mkdir(tempDir)
    tempFile=os.path.join(tempDir,name+'.zip')
    
    http = urllib3.PoolManager()

    rsource=remoteSources[name]
    print(rsource)
    r = http.request('GET', rsource['url'], preload_content=False)
    chunk_size=65536 
    with open(tempFile, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)

    r.release_conn()
    print('File  {}: {}'.format(tempFile,os.path.isfile(tempFile)))
    #2 Unzip
    with zipfile.ZipFile(tempFile,'r') as zip_ref:
        zip_ref.extractall(installDir)
    
    #cleanup
    os.remove(tempFile)

    #rename
    #this is the best guess of the relation between zip directory and name
    try:
        zipName=name.lower()+'-'+rsource['branch']
        os.rename(os.path.join(installDir,zipName),finalName)
    except FileNotFoundError:
        try:
            zipName=name+'-'+rsource['branch']
            os.rename(os.path.join(installDir,zipName),finalName)
        except FileNotFoundError:
            #git0/gogs
            zipName=name.lower()
            os.rename(os.path.join(installDir,zipName),finalName)

    
    sys.path.append(finalName)
    updateSetup(name,finalName)
    return finalName

def updateSetup(name,path):

    #update setup.json
    #set paths[name]=finalName
    #for use in slicer, use .labkey/slicer/setup.json
    setupDir=os.path.join(os.path.expanduser('~'),'.labkey','slicer')
    if not os.path.isdir(setupDir):
        os.makedirs(setupDir)
    setupFile=os.path.join(setupDir,'setup.json')
    
    #if f is not there, create an empty json
    try:
        with open(setupFile,'r') as f:
            setup=json.load(f)
    except OSError:
        setup={}

    try:
        setup['paths'][name]=path
    except KeyError:
        setup['paths']={}
        setup['paths'][name]=path

    with open(setupFile,'w') as f:
        json.dump(setup,f)
    
