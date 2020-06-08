import pickle
import time
from selenium import webdriver
import autoLogin


####################################################################
followBatch = 20       #qty follows avant de se reposer
followBreak = 30       #duree du repos de autoFollower

pageVisitBatch = 55
pageVisitBreak = 200
####################################################################

def autoFollower(email, password, followAmount, pickleFile):

    with open(pickleFile, "rb") as saveFile:   # Unpickling
        handleStatusList = pickle.load(saveFile)

    followCounter = 0
    followBreakCounter = 1

    pageVisitCounter = 0
    pageVisitBreakCounter = 1

    driver = autoLogin.autoLogin(email, password)

    for handleStatus in handleStatusList:
        print(handleStatus)


        if handleStatus[1] == 0:
            url = 'https://twitter.com/'+handleStatus[0]

            try:
                driver.get(url)
                pageVisitCounter += 1
                time.sleep(1)
            except:
                pass

            try:
                viewButton = driver.find_element_by_xpath('//span[text()="Yes, view profile"]')
                viewButton.click()
            except:
                pass

            try:
                driver.find_element_by_xpath('//span[text()="Sorry, that page doesn’t exist!"]') #essaye quand meme de trouver un follow, si lelement est dans la description
                handleStatus[1] = 1
            except:
                pass

            try:
                driver.find_element_by_xpath('//span[text()="This account doesn’t exist"]') #essayera pas de trouver un follow, puisque que il click ceux du cote
                handleStatus[1] = 1
            except:

                followingElements = driver.find_elements_by_xpath('//span[text()="Following"]')
                if len(followingElements) >= 2:
                    handleStatus[1] = 1
                else:

                    try:
                        driver.find_element_by_xpath('//span[text()="Pending"]')
                        handleStatus[1] = 1
                    except:

                        try:
                            followButton = driver.find_element_by_xpath('//span[text()="Follow"]')
                            followButton.click()

                            try:
                                for x in range(3): ## tries to refresh and follow if twitter asks for login information up to 3 times
                                    driver.find_element_by_xpath('//span[text()="Log in"]')  # verifies if login prompt appeared
                                    driver.find_element_by_xpath('//span[text()="Sign up"]') #
                                    driver.get(url)
                                    time.sleep(1)
                                    followButton = driver.find_element_by_xpath('//span[text()="Follow"]')
                                    followButton.click()
                            except:
                                pass

                            followCounter += 1
                            handleStatus[1] = 1
                        except:
                            print("Pas de follow pour: "+url)

            with open(pickleFile, "wb") as saveFile: #save the new twitter handles
                pickle.dump(handleStatusList, saveFile)

        if followCounter >= followAmount:
            break

        if pageVisitCounter/pageVisitBatch >= pageVisitBreakCounter:
            pageVisitBreakCounter += 1
            time.sleep(pageVisitBreak)

        if (followCounter/followBatch) >= followBreakCounter: #pour prendre une pause toutes les (followbatch) follows
            followBreakCounter += 1
            time.sleep(followBreak)


if __name__ == '__main__':
    autoFollower()
