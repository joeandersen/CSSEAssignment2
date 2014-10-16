# A simple example of a GUI focussing mostly on layout.

# Look carefully at the differences between one frame and the next frame.
# Also resize the window and see how the layout changes

# This example is not really in an OO style - if it was then I probably
# would have made the different components (i.e. each frame) inherit from
# Frame and contain the required buttons

from Tkinter import *

#A standard message box
from tkMessageBox import askokcancel


class DemoApp(object):
    """Layout demo."""

    def __init__(self, master=None):
        master.title("Layout Demo")
        self._master = master
        master.protocol("WM_DELETE_WINDOW", self.quit)
        # Create a frame and put some buttons in it
        frame1 = Frame(master,bg='black')
        frame1.pack()
        self.button1 = Button(frame1, text="Button 01",bg='green',
                              width=len("Button 01"))
        self.button1.pack(side=LEFT)
        self.button2 = Button(frame1, text="Button 02", bg='green')
        self.button2.pack(side=LEFT)
        self.button3 = Button(frame1, text="Button 03",bg='green')
        self.button3.pack(side=LEFT)
        # Create another frame and put some buttons in it
        frame2 = Frame(master, bg='black')
        frame2.pack(fill=X)
        self.button4 = Button(frame2, text="Button 04",bg='green')
        self.button4.pack(side=LEFT,expand=1)
        self.button5 = Button(frame2, text="Button 05",bg='green')
        self.button5.pack(side=LEFT,expand=1)
        self.button6 = Button(frame2, text="Button 06",bg='green')
        self.button6.pack(side=LEFT)
        # Yet another one
        frame3 = Frame(master,bg = 'blue')
        frame3.pack(fill=X, expand = 1)
        self.button7 = Button(frame3, text="Button 07",bg='green')
        self.button7.pack(side=LEFT)
        self.button8 = Button(frame3, text="Button 08",bg='green')
        self.button8.pack(side=LEFT)
        self.button9 = Button(frame3, text="Button 09",bg='green')
        self.button9.pack(side=LEFT)
        # Yet another one
        frame4 = Frame(master,bg='yellow')
        frame4.pack(fill=BOTH,expand=1,padx=20)
        self.button10 = Button(frame4, text="Button 10",bg='green')
        self.button10.pack(side=LEFT,ipadx=30)
        self.button11 = Button(frame4, text="Button 11",bg='green')
        self.button11.pack(side=LEFT, padx=40)
        self.button12 = Button(frame4, text="Button 12",bg='green')
        self.button12.pack(side=LEFT)
        
        # Yet another one
        frame5 = Frame(master)
        frame5.pack(fill=BOTH)
        self.quitbutton = Button(frame5, text="QUIT", command = self.quit)
        self.quitbutton.pack(side=LEFT,expand=1)
        dont = Button(frame5, text="DON'T PRESS ME", command = self.dontdoit)
        dont.pack(side=LEFT, expand=1)
        self.shout = 'I TOLD YOU NOT TO DO THAT'.split(' ')
        self.shoutbuttons = [(self.button1, 'Button 01'),
                             (self.button3, 'Button 03'),
                             (self.button4, 'Button 04'),
                             (self.button5, 'Button 05'),
                             (self.button9, 'Button 09'),
                             (self.button10, 'Button 10'),
                             (self.button11, 'Button 11')]
        self.shout_index = 0

    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans: self._master.destroy()


    def dontdoit(self):
        """An example using timer events - after 500 milliseconds this
        function is called.
        """

        i = self.shout_index
        if i == 7:
            # got to the end - reset the last button and index
            button,text = self.shoutbuttons[i-1]
            button.configure(bg='green',fg='black',text=text)
            self.shout_index = 0
        elif i == 0:
            # just started - change the first button
            button,text = self.shoutbuttons[i]
            button.configure(bg='red',fg='yellow',text=self.shout[i])
            self.shout_index += 1
            # after 500ms call self.dontdoit
            self._master.after(500, self.dontdoit)
        else:
            # reset the previous button and change the next button
            previousbutton,previoustext = self.shoutbuttons[i-1]
            previousbutton.configure(bg='green',fg='black',text=previoustext)
            button,text = self.shoutbuttons[i]
            button.configure(bg='red',fg='yellow',text=self.shout[i])
            self.shout_index += 1
            self._master.after(500, self.dontdoit)
        



root = Tk()
app = DemoApp(root)
root.mainloop()
