#! usr/bin/python
#coding=utf-8

'''

Author : Lip/yeyimilk
Date : 2017/03/22
Email : zqwang1993@gmail.com

Please feel free to contact me if you have any questions. :)
'''


import json
import os
import time
import requests
import urllib2

keepHost = "https://api.gotokeep.com"
homeSpotlight = "/v1.1/home/spotlight"
people = "/v2/people"


def httpGet(url):

    headers = {
        'Content-Type':'application/json; charset=utf-8',
        'Server':'openresty'
    }
    responseData = requests.get(url)
    if responseData.status_code == 200:
        result =  responseData.text
        return result
    else:
        print "-----SO SAD, httpGet error, url = " + url
        return ''

'''
    get user id from discovery tab view
'''
def getEntriesIds():
    homeSpotlightUrl = keepHost + homeSpotlight
    content = httpGet(homeSpotlightUrl)
    if content == "":
        return []

    responseJson = json.loads(content)
    try:
        errorCode = responseJson['errorCode']
        if errorCode != 0:
            return []

        resultEntriesIds = []
        data = responseJson['data']
        for dataContent in data:
            if 'entries' in dataContent['schema']:
                resultEntriesIds.append(dataContent['_id'])

        return resultEntriesIds
    except Exception,e:
        print '-----SO SAD, getEntriesIds fail ----'
        print Exception, ":", e
        return []

    return []

'''
    to known this user's gender
'''
def getUserIdWithRightGender(entryId, wantedGender):
    entryUrl = keepHost + '/v1.1/entries/' + entryId + "?limit=20&reverse=true"
    content = httpGet(entryUrl)
    if content == "":
        return False

    responseJson = json.loads(content)
    try:
        errorCode = responseJson['errorCode']
        if errorCode != 0:
            return False

        author = responseJson['data']['author']
        if author:
            gender = author['gender']
            if gender.lower() == wantedGender:
                rid = author['_id']
                if rid:
                    return rid
                return ''

    except Exception,e:
        print '-----SO SAD, isUserRightGender error ----'
        print Exception, ':', e
        return ''

    return ''

'''
'''
def getUserPhotoUrlList(userId):
    timelineUrl = keepHost + people + '/' + userId + '/timeline?type=all%2Cphoto'
    content = httpGet(timelineUrl)
    if content == "":
        return []

    responseJson = json.loads(content)
    try:
        errorCode = responseJson['errorCode']
        if errorCode != 0:
            return []

        contentPhotolist = responseJson['data']['photo']

        if contentPhotolist.count == 0:
            return []

        photoUrlList = []
        for photoIndex in contentPhotolist:
            realUrl = photoIndex['photo']
            if realUrl:
                photoUrlList.append(realUrl)

        return photoUrlList

    except Exception, e:
        print '-----SO SAD, getUserPhotoUrlList error ----'
        print Exception, ':', e
        return []

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

        print '------ One of you loves has been downloaded to your picture----:)  ---'
    return


def getWhatYouWant(userIds):
    for uid in userIds:
        urllist = getUserPhotoUrlList(uid)
        downloadUserPictures(uid, urllist)

        # protect keep server, pls do not comment this line
        # protect keep server, pls do not comment this line
        # protect keep server, pls do not comment this line
        time.sleep(5)

    return

def extractRigthUserIds(entriesIds, genderWanted):
    resultUserIds = []
    for eId in entriesIds:
        rightId = getUserIdWithRightGender(eId, genderWanted)
        if rightId != '':
            resultUserIds.append(rightId)

    return resultUserIds

def start():
    allEntriesIds = getEntriesIds()
    if allEntriesIds.count == 0:
        print "------SO SAD, empty user id -----"
        return

    genderWanted = "f"
    rightUserIds = extractRigthUserIds(allEntriesIds, genderWanted)
    if rightUserIds.count == 0:
        print "------SO SAD, empty right user id -----"
        return

    getWhatYouWant(rightUserIds)

if __name__ == '__main__':

    print "-------- Let's go ----------------"
    start()
    getWhatYouWant(['55f0bbaa30ec054d2ae3fa47'])
    print "----All End! Enjoy your photos----"

