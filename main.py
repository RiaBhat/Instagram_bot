from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time

class instaBot:
    def __init__(self,username, pw):
        self.driver = webdriver.Chrome()
        self.username= username
        self.driver.get("https://instagram.com")
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        time.sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        time.sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        count=0
        # for x in not_following_back:
        #     print(x)
        #     count=count+1
        # print(count)
        return not_following_back

    def get_num_of_followers(self):
        flw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
        sflw=b(flw.get_attribute('innerHTML'), 'html.parser')
        followers = sflw.findAll('span', {'class':'g47SY'})
        f = followers[1].getText().replace(',', '')
        if 'k' in f:
            f=float(f[:-1]) * 10**3
            return float(f)
        elif 'm' in f:
            f=float(f[:-1])*10**6
            return float(f)
        else:
            return float(f)

    def search(self):
        unfollowers=self.get_unfollowers()
        for x in unfollowers:
            self.driver.get("https://instagram.com" + "/" + x + "/")
            time.sleep(2)
            no_of_followers = self.get_num_of_followers()
            # print(no_of_followers)
            if no_of_followers < 1000.0:
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]")\
                    .click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")\
                    .click()
                time.sleep(2)


    def _get_names(self):
        time.sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        
        return names
    
# pass username and password in this object
my_bot = instaBot('','')
# my_bot.get_unfollowers()
my_bot.search()

