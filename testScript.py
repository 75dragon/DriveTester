from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

with open('gDriveInfo.json') as data_file:
    data = json.load(data_file)

#global variables
filePath = data["fileToUploadPath"]
fileName = data["fileToUploadName"]
presentationName = data["presentationName"]
spreadsheetName = data["spreadsheetName"]
documentName = data["documentName"]
switchDelay = data["switchDelay"]
timeDelay = data["timeDelay"]
user = data["testemail"]
password = data["testpassword"]
emailToShareTo = data["shareemail"]
driver = webdriver.Chrome(data["chromeDriverPath"])
url = data["url"]


#code. Takes ~45s to exectute everything
driver.get(url)
#wait for the page to load. There is probably a better way, by checking if the element appears.
#logging in
#finds the html element with the ID for input of username/password
emailLoginElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//input[@type="email"]')))
emailLoginElem.send_keys(user)
nextElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="identifierNext"]')))
nextElem.click()
passLoginElem =  WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//input[@type="password"]')))
passLoginElem.send_keys(password)
nextElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="passwordNext"]')))
nextElem.click()
#uploading file
#click the My Drive button
myDriveElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drive_main_page"]/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div[1]/div/div')))
myDriveElem.click()
#click the upload file method - tricks javascript to open the file input location
uploadFileElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="h-w a-w h-w a-w-Xi a-w-Mr"]/div[@class="a-w-x"]/div[3]')))
uploadFileElem.click()
#and now, suddenly the upload file method appears. Cheers!
fileInputElem = driver.find_element(By.XPATH, '/html/body/input[2]')
#set this to the path of the file your uploading
fileInputElem.send_keys(filePath)

#downloading and deleting
googleDriveElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label=' + "\"" + fileName + "\"" + ']')))
#download
actionChains = ActionChains(driver)
#right click, arrow up x2, then enter. Ta~da, were done!
actionChains.context_click(googleDriveElem).send_keys(u'\ue013').send_keys(u'\ue013').send_keys(u'\ue006').perform()
#delete
actionChains = ActionChains(driver)
#right click, arrow up x1, then enter. Ta~da, were done!
actionChains.context_click(googleDriveElem).send_keys(u'\ue013').send_keys(u'\ue006').perform()

#making a document, slides, then speadsheet
#click the My Drive button
myDriveElem.click()
#click the make document method
makeDocumentElem = driver.find_element(By.XPATH, '//div[@class="h-w a-w h-w a-w-Xi a-w-Mr"]/div[@class="a-w-x"]/div[6]')
makeDocumentElem.click();
#move to the second window
time.sleep(switchDelay)
driver.switch_to_window(driver.window_handles[1])
#enter a presentationName
renameElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="docs-title-widget"]/input')))
renameElem.clear()
renameElem.send_keys("")
renameElem.send_keys(documentName)
renameElem.send_keys(u'\ue006')
time.sleep(switchDelay)
#share with a friend
shareElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="docs-titlebar-share-client-button"]/div')))
actionChains = ActionChains(driver)
actionChains.click(shareElem).send_keys().send_keys(emailToShareTo).send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue006').perform()
time.sleep(switchDelay)
#unshare the friend. Messy hardcode due to a lot of popups.
actionChains = ActionChains(driver)
actionChains.click(shareElem).send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue006').send_keys(
    u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(
    u'\ue004').send_keys(u'\ue004').send_keys(u'\ue006').perform()
time.sleep(switchDelay)
actionChains = ActionChains(driver)
actionChains.send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue006').perform()
time.sleep(switchDelay)
actionChains = ActionChains(driver)
actionChains.send_keys(u'\ue006').perform()
time.sleep(switchDelay)
driver.close()
driver.switch_to_window(driver.window_handles[0])
#delete doc
documentElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label=' + "\"" + documentName +"\"" + ']')))
actionChains = ActionChains(driver)
#right click, arrow up x2, then enter. Ta~da, were done!
actionChains.context_click(documentElem).send_keys(u'\ue013').send_keys(u'\ue006').perform()

#use action path to make a presentation
actionChains = ActionChains(driver)
actionChains.context_click(myDriveElem).send_keys(u'\ue013').send_keys(u'\ue013').send_keys(u'\ue013').send_keys(u'\ue006').perform()
time.sleep(switchDelay)
driver.switch_to_window(driver.window_handles[1])
renameElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="docs-title-widget"]/input')))
renameElem.clear()
renameElem.send_keys("")
renameElem.send_keys(presentationName)
renameElem.send_keys(u'\ue006')
time.sleep(switchDelay)
driver.close()
driver.switch_to_window(driver.window_handles[0])
#delete present
presentationElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label=' + "\"" + presentationName +"\"" + ']')))
actionChains = ActionChains(driver)
#right click, arrow up x2, then enter. Ta~da, were done!
actionChains.context_click(presentationElem).send_keys(u'\ue013').send_keys(u'\ue006').perform()


#use action path to make a speadsheet
actionChains = ActionChains(driver)
actionChains.context_click(myDriveElem).send_keys(u'\ue013').send_keys(u'\ue013').send_keys(u'\ue013').send_keys(u'\ue013').send_keys(u'\ue006').perform()
time.sleep(switchDelay)
driver.switch_to_window(driver.window_handles[1])
renameElem = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="docs-title-widget"]/input')))
renameElem.clear()
renameElem.send_keys("")
renameElem.send_keys(spreadsheetName)
renameElem.send_keys(u'\ue006')
time.sleep(switchDelay)
driver.close()
driver.switch_to_window(driver.window_handles[0])
#delete speadsheet
spreadsheetName = WebDriverWait(driver, timeDelay).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label=' + "\"" + spreadsheetName +"\"" + ']')))
actionChains = ActionChains(driver)
#right click, arrow up x2, then enter. Ta~da, were done!
actionChains.context_click(spreadsheetName).send_keys(u'\ue013').send_keys(u'\ue006').perform()

#signout
myDriveName = driver.find_element(By.XPATH, '//a[@class="gb_b gb_db gb_R"]')
myDriveName.click()
time.sleep(switchDelay)
actionChains = ActionChains(driver)
actionChains.send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue004').send_keys(u'\ue006').perform()
