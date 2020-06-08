from selenium import webdriver
import time
import autoLogin

####################################################################
unfollowBatch = 20       #qty follows avant de se reposer
unfollowBreak = 30       #duree du repos de autoFollower
####################################################################

def autoUnfollower(email, password, unfollowAmount, unfollowUrl):

    driver = autoLogin.autoLogin(email, password)

    driver.get(unfollowUrl)
    time.sleep(4)

    unfollowCounter = 0
    unfollowBreakCounter = 1

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:

        while True:
            try:
                elements = driver.find_elements_by_xpath('//span[text()="Following"]')
                for i in range(2, len(elements)): ##############quel est le bon range??? (debut surtout)
                    driver.execute_script("arguments[0].click();", elements[i])
                    time.sleep(0.5)

                    try:
                        unfollowButton = driver.find_element_by_xpath('//span[text()="Unfollow"]')
                        unfollowButton.click()
                        unfollowCounter += 1
                        time.sleep(0.5)
                    except:
                        pass

                    if unfollowCounter >= unfollowAmount:
                        break

                    if unfollowCounter/unfollowBatch >= unfollowBreakCounter:
                        unfollowBreakCounter += 1
                        time.sleep(unfollowBreak)


                break  #si le text des elements est stale, le programme se rend pas au break et re-essaye
            except Exception as e:
                print(e)

        if unfollowCounter >= unfollowAmount:
            break

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
    autoUnfollower()
