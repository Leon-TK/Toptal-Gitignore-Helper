import requests
import os

FOLDERPATH = "E:\\Source\\testfolder"
TAGS = ["C++", "VisualStudio"]

def GetFolderPath():
    return FOLDERPATH

def GetGeneratorTags():

    # all to lowercase because api expect
    newTags = []

    for tag in TAGS:
        newTags.append(tag.lower())

    return newTags

def areElementsIn(elements, container):
    bools = []

    for element in elements:
        if element in container:
            bools.append(True)
        else:
            bools.append(False)

    if False in bools:
        return False
    else:
        return True

def GetApiTags():
    resp = requests.get("https://www.toptal.com/developers/gitignore/api/list")
    return resp.text

def areTagsCorrect():
    if areElementsIn(GetGeneratorTags(), GetApiTags()): return True
    else: return False

def SendGenerateRequest():
    apiTags = GetGeneratorTags()
    tagsString = ''
    tagCouter = 0
    for tag in apiTags:
        # last tag must be without ','
        if tagCouter == (len(apiTags) - 1):
            tagsString = tagsString + tag
        else:
            tagsString = tagsString + tag + ','
        tagCouter += 1

    print (f"Tags: {tagsString}")
    
    return requests.get(f"https://www.toptal.com/developers/gitignore/api/{tagsString}")


def GenerateGitIgnore():
    if areTagsCorrect() == False:
        print(f"Your tags are incorrect! Api tags are:\n{GetApiTags()}")
    else:
        resp = SendGenerateRequest()
        file = CreateFile(GetFolderPath(), ".gitignore")
        SaveGitIgnore(file, resp.text)
        AddIgnores(file)
        file.close()

def CreateFile(path, name):
    return open(path + "/" + name, 'w')

def SaveGitIgnore(file, apiText: str):
    file.write(apiText)
    file.flush()

def CreateFolders():
    folders = ["Logs", "TestContent"]
    for folder in folders:
        path = os.path.join(GetFolderPath(), folder)
        try: 
            os.mkdir(path) 
        except OSError as error: 
            print(error) 

def InsertToGitIgnore(file, text): 
    file.write(text + '\n')
    pass

def AddIgnores(file):
    InsertToGitIgnore(file, "# logs folder\n[Ll]ogs/")
    InsertToGitIgnore(file, "# folder contains content for test\n[Tt]estContent/")

GenerateGitIgnore()
CreateFolders()