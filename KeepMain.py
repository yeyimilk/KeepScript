#! usr/bin/python
#coding=utf-8

'''

Author : Lip/yeyimilk
Date : 2017/03/22
Email : zqwang1993@gmail.com

Please feel free to contact me if you have any questions. :)
'''

import urllib
import urllib2
import json
import os

keepHost = "https://api.gotokeep.com"
homeSpotlight = "/v1.1/home/spotlight"
poeple = "/v2/people"
genderWanted = "f"


def httpGet(url):
    req = urllib2.Request(url)
    responseData = urllib2.urlopen(req)
    return responseData.read()

'''
    get user id from discovery tab view
'''
def getUserIds():
    homeSpotlightUrl = keepHost + homeSpotlight

    return []


'''
    to known this user's gender
'''
def isUserRightGender(userId, wantedGender):
    return False


'''
'''
def getUserPhotoUrlList(id):

    return []


def checkDocuments(path):
    if os.path.exists(path) == False:
        os.mkdir(path)


def getImageName(imageUrl) :
    iamgeName = os.path.basename(imageUrl)
    if '.jpg' in iamgeName:
        return iamgeName

    return 'error.jpg'


def downloadUserPictures(userId, urllist):
    path = 'picture'
    checkDocuments(path)
    path = path + '/' +userId
    checkDocuments(path)

    for imageUrl in urllist:
        content = urllib2.urlopen(imageUrl).read()
        with open(path + '/' + getImageName(imageUrl), 'wb') as code:
            code.write(content)
    return


def getWhatYouWant(userIds):
    for uid in userIds:
        urllist = getUserPhotoUrlList(uid)
        downloadUserPictures(uid, urllist)

    return

def extractRightUserIds(userIds):
    return []

def start():
    allUserIds = getUserIds()
    if allUserIds.count() == 0:
        print "------SO SAD, empty user id -----"
        return

    rightUserIds = extractRightUserIds(allUserIds)
    if rightUserIds.count() == 0:
        print "------SO SAD, empty right user id -----"

    getWhatYouWant(rightUserIds)

if __name__ == '__main__':

    print "-------- Let's go ----------------"
    #start()
    print "----All End! Enjoy your photos----"

