import mechanize
from bs4 import BeautifulSoup
from time import sleep
from os import stat

import kivy
kivy.require("2.0.0")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


username = ""
password = ""

def get_lessons(username, password):

    class_list = []

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

            class_list.append(days[day_int])

            if day_int == 4:
                day_int = 0 
            else:
                day_int += 1

        else:
            class_list.append(i.get_text(separator="\n"))

        #print("\n")

    return class_list





class MyApp(App):

    global username
    global password


    def build(self):


        def on_press_button():
        
            #username.select_all()
            username_info = username.text


            #password.select_all()
            password_info = password.text

            with open("info.txt", "w") as file:

              file.write(username_info)
              file.write('\n')
              file.write(password_info)

    
        def get_class(instance):

            grid.remove_widget(get_classes)

            print(username)
            print(password)


            classes = get_lessons(username, password)
        
            for i in classes:

                print(i)

                grid.add_widget(Label(text=i))




        if stat("info.txt").st_size == 0:



            b = BoxLayout(orientation ='vertical')
        
            username = TextInput(font_size = 50,
                        size_hint_y = None,
                        height = 100)

            password = TextInput(font_size = 50,
                        size_hint_y = None,
                        height = 100)

            b.add_widget(username)
            b.add_widget(password)
    

            button = Button(text='Please login',
                            size_hint=(.2, .2),
                            pos_hint={'center_x': .5, 'center_y': 0.9})
            button.bind(on_press=on_press_button)

            b.add_widget(button)

            return b

        else:

            info = open("info.txt", "r")

            data = info.readlines()

            username = data[0]
            password = data[1]

            info.close()


            grid = GridLayout(cols = 5)


            get_classes = Button(text="Get classes", size_hint=(.2, .2), pos_hint={'center_x': .5, 'center_y': 0.9})
            get_classes.bind(on_press=get_class)

            grid.add_widget(get_classes)

            return grid

    


MyApp().run()
