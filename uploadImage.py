from selenium import webdriver
import pickle
import time
import os
import pathlib
import autoLogin
import pyautogui

def saveImageAsUploaded(image, imagePickle):

    with open(imagePickle, "rb") as saveFile:   # Unpickling
        uploadedImageList = pickle.load(saveFile)

    if image not in uploadedImageList:
        uploadedImageList.append(image)

    with open(imagePickle, "wb") as saveFile: #save the new twitter handles
        pickle.dump(uploadedImageList, saveFile)


def uploadImage(email, password, imageFolder, imagePickle):

    with open(imagePickle, "rb") as saveFile:   # Unpickling
        uploadedImageList = pickle.load(saveFile)


    imageFolderPath = str(pathlib.Path(__file__).parent.absolute()) + imageFolder
    availableImageList = os.listdir(imageFolderPath)

    newImageList = []
    for img in availableImageList:
        if img not in uploadedImageList:
            newImageList.append(img)

    if len(newImageList) >= 1:
        driver = autoLogin.autoLogin(email, password)

        for newImage in newImageList:

            imagePath = imageFolderPath + "/" + newImage
            print(imagePath)

            try:
                driver.get("https://twitter.com/compose/tweet")
                elements = driver.find_elements_by_class_name("r-1awozwy")
                elements[5].click()
                pyautogui.write(imagePath)
                pyautogui.press('enter')
                time.sleep(6)
                tweetButton = driver.find_element_by_xpath('//span[text()="Tweet"]')
                tweetButton.click()
                print("bouton tweet est clique")
                saveImageAsUploaded(newImage, imagePickle)
                time.sleep(10800)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    uploadImage()
