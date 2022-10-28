from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout

import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


try:

    file_check = open("info.txt", "r")

except FileNotFoundError:

    file_creation = open("info.txt", "w")
    file_creation.close()

try:

    import mechanize
    from bs4 import BeautifulSoup
    from os import stat

    import kivy
    kivy.require("2.0.0")

    max_col = 10
   
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.boxlayout import BoxLayout


    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    def get_lessons(username, password):

        class_list = []

        #set up the browser
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open("https://portal.headstartphuket.com/Login.aspx")

        #log in to the portal
        browser.select_form(name = "aspnetForm")
        browser.form['ctl00$PageContent$loginControl$txtUN'] = username
        browser.form['ctl00$PageContent$loginControl$txtPwd'] = password
        browser.submit()

        browser.open("https://portal.headstartphuket.com/vle/default.aspx")

        soup = BeautifulSoup(browser.response().read(), features="html5lib")
        result = soup.find_all(["span", "td"], {"class" : ["ttLessonText", "break"]})



        day_int = 0
        p_count = 0

        for i in result:

            #period = i.find_all("strong")

            if "Homeroom" in i.text:

                class_list.append(days[day_int])


                if day_int == 4:
                    day_int = 0 
                else:
                    day_int += 1

                

            else:
                class_list.append(i.get_text(separator="\n"))
                p_count += 1


            #print("\n")

        return class_list





    class MyApp(App):

        global username
        global password


        def build(self):


            def on_press_button(instance):

            
                #username.select_all()
                username_info = username.text


                #password.select_all()
                password_info = password.text

                if username.text != "" and password.text != "":

                    with open("info.txt", "w") as file:

                        file.write(username_info)
                        file.write('\n')
                        file.write(password_info)
                
                b.remove_widget(username)
                b.remove_widget(password)
                b.remove_widget(button)

                confirm = Label(text = "Credientials saved, please reopen the app for further usage.")
                b.add_widget(confirm)
                

            def reset(instance):

                open('info.txt', 'w').close()
                message = Label(text = "Credentials reset, please reopen the app to login again.")
                box.clear_widgets()
                box.add_widget(message)


        
            def get_class(instance):

                
                box.clear_widgets()
                

                wait = Label(text="Fetching your current timetable from the student portal...")
                wait.font_size = "100dp"
                box.add_widget(wait)

                classes = get_lessons(username, password)

                box.remove_widget(wait)

                final_list = []
                sub_list = []
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

                for i in classes:

                    if i in days:
                        
                        final_list.append(sub_list)
                        sub_list = []
                        sub_list.append(i)
                    else:
                        sub_list.append(i)

                del final_list[0]
                
                
            
                class_file = open("classes.txt", "w")
                for days in final_list:
                    sub_box = BoxLayout(orientation='horizontal')

                    for k in days:

                        widget = Label(text=k, size_hint=(1,1))
                        widget.font_size = '5dp' 
                        sub_box.add_widget(widget)
                        class_file.write(k)
                        class_file.write("<>")
                    box.add_widget(sub_box)
                    class_file.write("|")    
                class_file.close()
                box.add_widget(get_classes)
                box.add_widget(clear_info)
                    




            if stat("info.txt").st_size == 0:


                b = BoxLayout(orientation ='vertical')
            
                username = TextInput(font_size = 50,
                            size_hint_y = None,
                            height = 100)

                password = TextInput(font_size = 50,
                            size_hint_y = None,
                            height = 100, password=True)

                b.add_widget(username)
                b.add_widget(password)
        

                button = Button(text='Please login',
                                size_hint=(.2, .1),
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


                box = BoxLayout(orientation='vertical')

                try:
                    class_file = open("classes.txt", "r")
                except FileNotFoundError:
                    pass
                else:
                    final_list = []
                    classes = class_file.read()
                    classes = classes.split("|")
                    for i in classes:
                        final_list.append(i.split("<>"))
                    class_file.close()

                    for days in final_list:
                        sub_box = BoxLayout(orientation='horizontal')

                        for k in days:

                            widget = Label(text=k, size_hint=(1,1))
                            widget.font_size = '5dp' 
                            sub_box.add_widget(widget)
                        box.add_widget(sub_box)
                   



                get_classes = Button(text="Update classes", size_hint=(.2, .2), pos_hint={'center_x': .5, 'center_y': 0.9})
                get_classes.bind(on_press=get_class)

                clear_info = Button(text="Reset login credentials", size_hint=(.2, .2), pos_hint={'center_x': .5, 'center_y': 0.1})
                clear_info.bind(on_press=reset)

                box.add_widget(get_classes)
                box.add_widget(clear_info)

                scatter = ScatterLayout(do_rotation=False)
                scatter.add_widget(box)

                return scatter
        
    MyApp().run()

except ModuleNotFoundError as e:

    class ExceptionApp(App):

        def build(self):

            b = BoxLayout(orientation ='vertical')
            text = str(e)
            message = Label(text = text, size_hint = (0.1, 0.1), pos_hint = {'center_x': .5, 'center_y': 0.1})
            message.font_size = '20dp' 
            b.add_widget(message)

            return b

    app = ExceptionApp()
    app.run()


    

        
   