import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from requests import session

from bs4 import BeautifulSoup,SoupStrainer

import time

baseurl = "http://id.bits-hyderabad.ac.in/moodle/"

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data, **properties):
        super().__init__(**properties)
        self.data=data
        self.add(data)

def login(uname,pwd,ses):
    authdata = {
        'action': 'login',
        'username': uname,
        'password': pwd
    }
    res = ses.post(baseurl + 'login/index.php', data=authdata, allow_redirects=False)
    res2 = ses.get(baseurl + 'my/index.php', allow_redirects=False)
    #print(res2.status_code)
    if res2.status_code==200:
        return True
    else:
        return False

class LoginWindow(Gtk.Window):


    def __init__(self):

        Gtk.Window.__init__(self, title="Login to Moodle")
        self.set_size_request(640, 360)
        self.set_border_width(10)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

        self.listbox=Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listbox, True, True, 0)

        self.unameentry = Gtk.Entry()
        self.unameentry.set_placeholder_text("Username")
        self.unameentry.set_text("student")
        #self.hbox1.pack_start(self.unameentry, True, True, 0)
        self.listbox.add(ListBoxRowWithData(self.unameentry))

        self.pwdentry = Gtk.Entry()
        self.pwdentry.set_placeholder_text("Password")
        self.pwdentry.set_text("moodle")
        self.pwdentry.props.visibility = False
        #self.hbox1.pack_start(self.pwdentry, True, True, 0)
        self.listbox.add(ListBoxRowWithData(self.pwdentry))


        self.loginbutton = Gtk.Button(label="Login")
        self.loginbutton.connect("clicked", self.login_button_clicked)
        #self.vbox.pack_start(self.loginbutton, True, True, 0)
        self.listbox.add(ListBoxRowWithData(self.loginbutton))


    def login_button_clicked(self, widget):
        print("Logging in")
        uname = self.unameentry.get_text()
        pwd = self.pwdentry.get_text()
        #print(uname + ' ' + pwd)
        with session() as ses:
            if login(uname,pwd,ses):
                HomePageWindow(ses)
                self.destroy()
            else:
                ses.close()

class CourseTitleListBoxRow(Gtk.ListBoxRow):
    def __init__(self,data):
        super(Gtk.ListBoxRow,self).__init__()
        self.data=data
        self.label=Gtk.Label(self.data[0])
        self.button=Gtk.Button()
        self.button.add(self.label)
        self.add(self.button)

class   (Gtk.Window):
    def __init__(self, ses):
        self.ses=ses
        super(Gtk.Window,self).__init__()

        self.set_size_request(640, 360)
        self.set_border_width(10)

        self.lb = Gtk.ListBox()
        self.lb.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(self.lb)

        res=ses.get(baseurl+'my/index.php?mynumber=-2')
        only_div = SoupStrainer("div")
        soup = BeautifulSoup(res.text, "html.parser", parse_only=only_div)

        for child in soup.find_all('div'):
            if child.get('class')!= None and child.get('class')[0] == 'course_title':

                print(child.h2.a.string)
                print(child.h2.a['href'])

                lbr = CourseTitleListBoxRow([child.h2.a.string, child.h2.a['href']])
                self.lb.add(lbr)

        self.show_all()
        self.connect("delete-event", Gtk.main_quit)


window = LoginWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
