import mechanize
from bs4 import BeautifulSoup
from time import sleep


import kivy
kivy.require("2.0.0")

from kivy.app import App
from kivy.uix.label import Label


def get_lessons(username, password):

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.open("https://portal.headstartphuket.com/Login.aspx")

    browser.select_form(name = "aspnetForm")
    browser.form['ctl00$PageContent$loginControl$txtUN'] = username
    browser.form['ctl00$PageContent$loginControl$txtPwd'] = password
    browser.submit()

    browser.open("https://portal.headstartphuket.com/vle/default.aspx")

    soup = BeautifulSoup(browser.response().read(), features="html5lib")
    result = soup.find_all("span", {"class" : "ttLessonText"})

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    day_int = 0

    for i in result:

        period = i.find_all("strong")
    
        if "Homeroom" in i.text:

            print(days[day_int])
            
            if day_int == 4:
                day_int = 0 
            else:
                day_int += 1

        else:
            print(i.get_text(separator="\n"))

        print("\n")


class MyApp(App):

    def build(self):

        return Label(text="Timetable fetcher")

if __name__ == '__main__':

    MyApp().run()