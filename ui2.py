#!/usr/bin/env python
import npyscreen
import curses
#npyscreen.disableColor()


# SplitFormWithMenus


def myFunction(*args):
    App = TestApp()
    App.run()

class SplitForm(npyscreen.FormWithMenus):
    MOVE_LINE_ON_RESIZE = False
    """Just the same as the Title Form, but with a horizontal line"""
    def __init__(self, draw_line_at=None, *args, **keywords):
        super(SplitForm, self).__init__(*args, **keywords)
        if not hasattr(self, 'draw_line_at'):
            if draw_line_at != None:
                self.draw_line_at = draw_line_at
            else:
                self.draw_line_at = self.get_half_way()

        self.logs=[]
        self.keypress_timeout = 1

    def draw_form(self,):
        MAXY, MAXX = self.curses_pad.getmaxyx()
        super(SplitForm, self).draw_form()
        self.curses_pad.vline(1,self.draw_line_at, curses.ACS_VLINE, MAXY-2)

    def get_half_way(self):
        return self.curses_pad.getmaxyx()[1] // 2

    def resize(self):
        super(SplitForm, self).resize()
        if self.MOVE_LINE_ON_RESIZE:
            self.draw_line_at = self.get_half_way()

    def create(self, *args, **keywords):
        super(SplitForm, self).create(*args, **keywords)
        self.keypress_timeout = 5
        self.counter=0
        self.text=self.add(npyscreen.TitleText, name = "Text:",max_height=20,max_width=self.get_half_way()-2  )
        self.text2=self.add(npyscreen.Pager, name = "Text:",relx=self.get_half_way()+2,
            max_width=self.get_half_way()-5, rely=self.text.rely)#,editable=False )

    def while_waiting(self):
        self.counter+=1
        for i in range(5):
            self.logs.append(self.counter)
        self.text2.values=self.logs
        # self.text2.scroll_exit=True
        # self.text2.cursor_line=5
        # from IPython import embed
        # print ("DEBUG NOW uuu")
        # embed()
        # raise RuntimeError("stop debug here")

#big for,
class MainForm(npyscreen.FormWithMenus):
    def create(self, *args, **keywords):
        super(MainForm, self).create(*args, **keywords)
        self.keypress_timeout = 5
        self.counter=0
        self.text=self.add(npyscreen.TitleText, name = "Text:",relx=100,max_height=20 )
        # self.columns=2
        # self.h_exit_mouse
        # self.show_from_x(100)

    def while_waiting(self):
        self.counter+=1
        self.text.value=str(self.counter)

    def afterEditing(self):
        self.text.value="AAA"
        self.parentApp.setNextForm("MAIN2")

class MainForm2(npyscreen.FormWithMenus):
    def create(self, *args, **keywords):
        super(MainForm2, self).create(*args, **keywords)
        self.keypress_timeout = 1
        self.counter=10000
        self.text=self.add(npyscreen.TitleText, name = "Text2:",relx=100 )

    def while_waiting(self):
        self.counter+=1
        self.text.value=str(self.counter)

    def afterEditing(self):
        self.parentApp.setNextForm(None)

class TestApp(npyscreen.StandardApp):

    def onStart(self):
        self.form_main=MainForm()
        self.form_main.max_x=50
        self.form_main2=MainForm2()
        self.form_split=SplitForm()
        self.registerForm("MAIN", self.form_split)
        self.registerForm("MAIN2", self.form_main)
        self.registerForm("MAIN3", self.form_main2)
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)




    def while_waiting(self):

        pass

    # def main(self):
    #     # # These lines create the form and populate it with widgets.
    #     # # A fairly complex screen in only 8 or so lines of code - a line for each control.
    #     # self.keypress_timeout_default = 1
    #     # F = MainForm(parentApp=self, name = "Welcome to Npyscreen",)
    #     # F.t = F.add(npyscreen.TitleText, name = "Text:",relx=100 )
    #     # fn = F.add(npyscreen.TitleFilenameCombo, name = "Filename:")
    #     # dt = F.add(npyscreen.TitleDateCombo, name = "Date:")
    #     # s = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider", color='DANGER')
    #     # ml= F.add(npyscreen.MultiLineEdit,
    #     #     value = """try typing here!\nMutiline text, press ^R to reformat.\n""",
    #     #     max_height=5, rely=9)
    #     # ms= F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One",
    #     #         values = ["Option1","Option2","Option3"], scroll_exit=True)
    #     #
    #     # # This lets the user play with the Form.
    #     # F.edit()
    #     pass


if __name__ == "__main__":
    npyscreen.wrapper_basic(myFunction)
