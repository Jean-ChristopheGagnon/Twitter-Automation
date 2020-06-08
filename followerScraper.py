from selenium import webdriver
import time
import pickle
import autoLogin

def sanitizeHandle(input): #this removes all @ from the beginning of a potential twitter handle
    if input[:1] == "@":   # this is not used in the final version, although the code to do so is still there and commented
        return sanitizeHandle(input[1:])
    else:
        return input

def saveFollower(scrapedHandle, pickleFile):

    with open(pickleFile, "rb") as saveFile:   # Unpickling
        handleStatusList = pickle.load(saveFile)

    if handleStatusList.count([scrapedHandle, 0]) == 0 and handleStatusList.count([scrapedHandle, 1]) == 0: # add scraped twitter handle if not already in file
        handleStatusList.append([scrapedHandle, 0]) #status 0 means not yet followed

    with open(pickleFile, "wb") as saveFile: #save the new twitter handles
        pickle.dump(handleStatusList, saveFile)


def followerScraper(email, password, scrapingUrl, pickleFile):

    driver = autoLogin.autoLogin(email, password)

    driver.get(scrapingUrl)
    time.sleep(4)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:

        while True:
            try:
                for elem in driver.find_elements_by_class_name('css-16my406'):
                    if elem.text[:1] == "@": #is the text element UP TO FIRST CHARACTER a "@",this excludes empty string
                        #sanitizedHandle = sanitizeHandle(elem.text[1:])
                        #print(sanitizedHandle)
                        #saveFollower(sanitizedHandle, pickleFile)
                        print(elem.text[1:])
                        saveFollower(elem.text[1:], pickleFile) #this is to save only when there is a single @, this excludes some handle in user descriptions

                break  #si le text des elements est stale, le programme se rend pas au break et re-essaye
            except Exception as e:
                print(e)


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(300)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height

if __name__ == '__main__':
    followerScraper()
