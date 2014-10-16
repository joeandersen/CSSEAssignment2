###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 33422619
#
#   Student Name: Joseph Andersen
#
###################################################################

#
# Do not change the following import
#

from assign2_support import *

####################################################################
#
# Insert your code below
#
####################################################################

class PVData:
    """Class to hold the PV data for a given date."""

    def format_data(self,date_string):
        """reads in and loads data. Manipulates data into required format"""
                

        data = load_data(date_string)
        self._times = []
        self._temperatures = []
        self._sunlights = []
        self._powers = dict()
        for array in ARRAYS:
            self._powers[array] = []
            
        for record in data:
            self._times.append(record[0])
            self._temperatures.append(record[1])
            self._sunlights.append(record[2])
            powers= record[3]
            for array,datum in enumerate(powers):
                self._powers[ARRAYS[array]].append(datum)
        return
                
          


    def __init__(self):
        """initializes the pv data with yesterday's data

        precondition: data exists for yesterday

        """
        date_string = yesterday()
        
        #data = load_data(date_string)
        #self._data = data
        self.format_data(date_string)
        self._date = date_string
        return

    def change_date(self, date):
        """change the data to be for the given date. Must not
        reextract data if same date is used"""

        # Check if date change is actually required

        if self.get_date == date:
            return
        else:
            self._date = date
            self.format_data(date)
            
            return       

    def get_date(self):
        """return the date for the stored data

        pvdata.get_date() -> str

        precondition pvdata object correctly configured
        
        """
        return self._date

    def get_time(self,time_index):
        """return the time for the given index of the time data

        pvdata.get_time(int) -> string
        
        precondition pvdata object correctly configured, int is a
        valid index for the data.
        """
        return self._times[time_index]
    
    def get_temperature(self):
        """return the list of temperature values for the current date

        pvdata.get_temperature() -> [float]

        """
        return self._temperatures
 
    def get_sunlight(self):
        """return the list of sunlight values for the current date

        pvdata.get_sunlight() -> [float]

        """
        return self._sunlights

    def get_power(self,array):
        """returns power output for the current date and the given array

        pvdata.get_power(str) -> [float]

        precondition: str is a valid array name

        """
        return self._powers[array]
        
    def get_cumulative_energy(self,array):
        """computes and returns the list of cumulative energies for the
        current date and the given array

        pvdata.get_cumulative_energy(str) -> [float]

        precondition: str is a valid array name

        """

        powers = self._powers[array]

        cumulative_powers = []
        
        for count,power in enumerate(powers):
            accumulated_power = power
            for j in range(0,count):
                accumulated_power += powers[j]
            cumulative_powers.append(accumulated_power)

        return cumulative_powers
        
    
        
 
    

#Testing code for the data class functionality
    
"""
pvd = PVData()
pvd.change_date('13-09-2014')
print pvd.get_date()
print pvd.get_time(300)
print pvd.get_temperature()[300:304]
print pvd.get_sunlight()[300:304]
print pvd.get_power('UQ Centre, St Lucia')[300:304]
print pvd.get_power('All Arrays Combined')[300:304]
print pvd.get_cumulative_energy('All Arrays Combined')[300:304]
print pvd.get_power('All Arrays Combined')[0:4]
print pvd.get_cumulative_energy('All Arrays Combined')[0:4]

#get_data_for_date('')
#get_data_for_date('20-10-2050')
#get_data_for_date('20_10_2014')
#pvd.change_date('')
#pvd.change_date('20-10-2050')
#pvd.change_date('20_10_2014')
"""

class Plotter(Canvas):
    """class responsible for doing the plotting"""

    def __init__(self,parent,pvd,options_frame,plot_app,width,height):

        self._width = width
        self._height = height
        
        self._plot_app = plot_app
        self._parent = parent
        
        self._canvas = Canvas(parent, bg="white", width=self._width,
                              height=self._height)
        self._canvas.pack(side=TOP, expand=True, fill=BOTH)
        self._coord_trans=CoordinateTranslator(self._width,
                                               self._height,
                                               len(pvd.get_temperature()))

        self._options_frame = options_frame
        self._pvd = pvd
        self.draw_plot()

       
        return

    def draw_plot(self):
        """calls the functions to produce plots of the data.
        Will draw the correct figures based upon the selections
        in the options_frame

        precondition: options_frame object correctly set up.


        """

        
        if self._options_frame._power_v.get() ==2:
            self.draw_power(self._pvd,self._options_frame._array_variable.get())
        
        elif self._options_frame._power_v.get() ==3:
            self.draw_cumulative_energy(self._pvd,
                                        self._options_frame._array_variable.get())


        if self._options_frame._plot_sun.get():
            self.draw_sunlight(self._pvd)
        if self._options_frame._plot_temp.get():
            self.draw_temperature(self._pvd)
        
        return
    
    def draw_power(self,pvd,array):
        """Draws the polygon of the power. Only called if correct buttons are
        selected.

        precondition: objects correctly configured

        """
       
        powers = pvd.get_power(array)
    
    
        point_list = [(self._coord_trans.power_coords(0,0,array))]
        for count,power in enumerate(powers):

            point_list.append(self._coord_trans.power_coords(count,power,array))
            
        self._canvas.create_polygon(point_list,
                                    outline=POWER_COLOUR,fill=POWER_COLOUR)

    def draw_cumulative_energy(self,pvd,array):
        """Draws the polygon of the cumulative energy. Only
        called if correct buttons are selected.

        precondition: objects correctly configured

        """

       
        accum_energies = pvd.get_cumulative_energy(array)
 
    

        point_list = []
        for count,accum_energy in enumerate(accum_energies):
            point_list.append(self._coord_trans.power_coords(count,
                                                accum_energy/450,array))

        point_list.append(self._coord_trans.power_coords(count,
                                                             0,array))

        

        self._canvas.create_polygon(point_list,
                                    outline=POWER_COLOUR,fill=POWER_COLOUR)



    def draw_temperature(self,pvd):
        """Draws the line of the temperature. Only
        called if correct buttons are selected.

        precondition: objects correctly configured

        """
        temperatures = pvd.get_temperature()
        point_list = []
        for count,temp in enumerate(temperatures):
            point_list.append(self._coord_trans.temperature_coords(count,temp))
        self._canvas.create_line(point_list, fill='red')
    
    def draw_sunlight(self,pvd):
        """Draws the line of the sunlight. Only
        called if correct buttons are selected.

        precondition: objects correctly configured

        """
        sunlights = pvd.get_sunlight()
        point_list = []
        for count,sunlight in enumerate(sunlights):
            point_list.append(self._coord_trans.sunlight_coords(count,sunlight))
        self._canvas.create_line(point_list, fill='orange')


    def delete(self):
        """
        clears the canvas
        """
        self._canvas.delete(ALL)

    def resize(self,event):
        """Updates the coordinate transformations when the canvas is resized

        """
        self._width = event.width
        self._height = event.height
        self._coord_trans=CoordinateTranslator(self._width,
                                               self._height,
                                               len(self._pvd.get_temperature()))
        

    def remove_vertical(self,event):
        """Removes the vertical line. Called when the button is released.

        """
        self.delete()
        self.draw_plot()
        
        index = self._coord_trans.get_index(event.x)
        
 
        temperature = None
        sunlight = None
        power = None
        is_cumulative = False
                            

        label_string = pretty_print_data(self._pvd.get_date(),
                                         None,
                                         temperature,sunlight,power,
                                         is_cumulative)
        
        self._plot_app.update_label(label_string)



    def draw_vertical(self,event):
        """Draws the vertical line at the location of the mouse pointer
        when the mouse button is pressed.
        
        """
        self.delete()
        self.draw_plot()
        self._canvas.create_line([(event.x,0),(event.x,1000)])

        index = self._coord_trans.get_index(event.x)
        
        label_string = 'foo '+ str(index)+','+str(event.y)

        temperature = None
        sunlight = None
        power = None
        is_cumulative = False
        

        if self._options_frame._plot_temp.get():
            temperature = self._pvd.get_temperature()[index]
        if self._options_frame._plot_sun.get():
            sunlight = self._pvd.get_sunlight()[index]

        if self._options_frame._power_v.get() ==2:
            power = self._pvd.get_power(
                self._options_frame._array_variable.get())[index]
        
        elif self._options_frame._power_v.get() ==3:
            power =self._pvd.get_cumulative_energy(
                self._options_frame._array_variable.get())[index]
            is_cumulative = True

        
            

        label_string = pretty_print_data(self._pvd.get_date(),
                                         self._pvd.get_time(index),
                                         temperature,sunlight,power,
                                         is_cumulative)
        
        self._plot_app.update_label(label_string)

class OptionsFrame(Frame):
    """The widget used for choosing options"""

    

    def __init__(self,parent,plotting_app,pvd):



        self._plotting_app = plotting_app
        Frame.__init__(self,parent)


        

    
        rowA = Frame(self)
        row1 = Frame(rowA)
        #A row of three radiobuttons to choose between
        #No power, Instantaeous power and Cumulative power
        power_v = IntVar()
        power_v.set(2)
        Radiobutton(row1, text='No Power', variable=power_v,
                    value=1).pack(side=LEFT)
        Radiobutton(row1, text='Instantaneous Power', variable=power_v,
                    value=2).pack(side=LEFT)
        Radiobutton(row1, text='Cumulative Energy', variable=power_v,
                    value=3).pack(side=LEFT)
        self._power_v = power_v
 

        row2 = Frame(rowA)
        #A row of two checkbuttons so the user can choose
        #what data, other than power is displayed
        plot_temp = IntVar()
        plot_sun = IntVar()
        Checkbutton(row2, text='Temperature', variable=plot_temp).pack(side=LEFT)
        Checkbutton(row2, text='Sunlight', variable=plot_sun).pack(side=LEFT)
        self._plot_temp = plot_temp
        self._plot_sun = plot_sun
  

        row3 = Frame(self)
        row3a = Frame(row3)

        #an entry box where the user can enter a date
        Label(row3a,text = 'Choose Date:').pack(side=LEFT)
        self.entry = Entry(row3a, width=20)
        self.entry.insert(END,pvd.get_date())
        self.entry.pack(side=LEFT)
        #a button to apply the choice of date and array
        Button(row3a,text ='Apply',command=self.apply_choices).pack(side=LEFT)

       

        row3b = Frame(row3)
    
        #an OptionMenu allowing the user to choose which
        #which array to display. All combined is default
        array_variable = StringVar()
        array_variable.set(ARRAYS[-1])
        OptionMenu(row3b,array_variable,*ARRAYS).pack(side=RIGHT)

        self._array_variable = array_variable
        


        row3b.pack(side=RIGHT,anchor=SE, expand=True, fill=BOTH)
        row3a.pack(side=LEFT,anchor=SW, expand=True)
        
        row1.pack(side=TOP)
        row2.pack(side=TOP)
        row3.pack(side=TOP, fill=X, expand=1)
        rowA.pack()

        self._rowA = rowA
        self._row3 = row3
        
        self._pvd = pvd
        return


    def apply_choices(self):
        """Called when the apply button is depressed.
        Updates the date from the text box and redraws the plots

        """

        #print self._power_v.get()
        #print self._plot_temp.get()
        #print self._plot_sun.get()
        date_string = self.entry.get()
        self._date_string = date_string
        #print self._date_string
        #print self._array_variable.get()

        self._plotting_app.apply()
        return

    def update_plot(self):
        """Redraws the plots when the buttons are pressed/toggled with the
        new parameters

        """
        self._plotting_app.draw_plot()

    def update_plot_b(self,foo):
        """Redraws the plots when the buttons are pressed/toggled with the
        new parameters. This version is needed because the OptionMenu object
        acts annoyingly...

        """
        self._plotting_app.draw_plot()
        
    def fix_check_boxes(self):
        """Sets up the check boxes, radio buttons, etc to actually live update the
plot as they are selected. I cannot do this in the initialization because parts of
the Plotter class are needed, but I cannot initialize it first :/"""



        self._rowA.pack_forget()
        self._row3.pack_forget()

        pvd = self._pvd

        
        opframe = Frame(self)
        opframe.pack(side=BOTTOM, fill=X,expand=1)
        
        #rowA = Frame(self)
        #row1 = Frame(self._plotting_app._master)
        row1 = Frame(opframe)
        #A row of three radiobuttons to choose between
        #No power, Instantaeous power and Cumulative power
        power_v = IntVar()
        power_v.set(2)
        Radiobutton(row1, text='No Power', variable=power_v,
                    value=1, command=self.update_plot).pack(side=LEFT)
        Radiobutton(row1, text='Instantaneous Power', variable=power_v,
                    value=2, command=self.update_plot).pack(side=LEFT)
        Radiobutton(row1, text='Cumulative Energy', variable=power_v,
                    value=3, command=self.update_plot).pack(side=LEFT)
        self._power_v = power_v
 

        #row2 = Frame(self._plotting_app._master)
        row2 = Frame(opframe)
        
        #A row of two checkbuttons so the user can choose
        #what data, other than power is displayed
        plot_temp = IntVar()
        plot_sun = IntVar()
        Checkbutton(row2, text='Temperature', variable=plot_temp,
                    command=self.update_plot).pack(side=LEFT)
        Checkbutton(row2, text='Sunlight', variable=plot_sun,
                    command=self.update_plot).pack(side=LEFT)
        self._plot_temp = plot_temp
        self._plot_sun = plot_sun

        row1.pack(side=TOP)
        row2.pack(side=TOP)
        #rowA.pack()

        #row3 = Frame(self)
        row3 = Frame(opframe)
        row3.pack(side=TOP, fill=X,expand=1)

        #an entry box where the user can enter a date
        Label(row3,text = 'Choose Date:').pack(side=LEFT)
        self.entry = Entry(row3, width=20)
        self.entry.insert(END,pvd.get_date())
        self.entry.pack(side=LEFT)
        #a button to apply the choice of date and array
        Button(row3,text ='Apply',command=self.apply_choices).pack(side=LEFT)

        #row3a.pack(side=LEFT)

        #row3b = Frame(self)
    
        #an OptionMenu allowing the user to choose which
        #which array to display. All combined is default
        array_variable = StringVar()
        array_variable.set(ARRAYS[-1])
        OptionMenu(row3,array_variable,*ARRAYS,
                   command=self.update_plot_b).pack(side=RIGHT)

        self._array_variable = array_variable

  
        
        

        self._row1 = row1
        self._row3 = row3
    
      

class PVPlotApp:
    """top level class for the GUI. responsible for
    creating and managing instances of the above classes"""

    def __init__(self, master):

        master.title('PV Plotter')
        self._pvd = PVData()
        #pvd.change_date('08-12-2013')
        width = 900
        height = 500
        
        self._options_frame = OptionsFrame(master,self,self._pvd)
        self._options_frame.pack(side=BOTTOM)

        self._text_line = Frame(master)
        self._label = Label(self._text_line,text=
                        pretty_print_data(self._pvd.get_date(),
                                          None,None,None,None))
        self._label.pack(side=LEFT)
        self._text_line.pack(side=TOP, anchor=W)
        self._master = master
        self._plotter = Plotter(master,self._pvd,self._options_frame,
                                self,width,height)#.pack(side=TOP)

        self._plotter._canvas.bind("<B1-Motion>", self._move_event)
        self._plotter._canvas.bind("<Button-1>", self._click_event)
        self._plotter._canvas.bind("<ButtonRelease-1>", self._release_event)
        self._plotter._canvas.bind("<Configure>", self._configure_event)
        self._options_frame.fix_check_boxes()

    def apply(self):
        """
        Loads new data if needed (when date is changed), produces error messages
        if appropriate, redraws figures when appropraite. Called from options
        frame class, when apply button pressed
        """
        self._old_date = self._pvd.get_date()
        try:
            
            self._pvd.change_date(self._options_frame._date_string)
            self._plotter.delete()
            self._label.pack_forget()
            self._label = Label(self._text_line,text=
                        pretty_print_data(self._pvd.get_date(),
                                          None,None,None,None))
            self._label.pack(side=LEFT)
            self._plotter.draw_plot()
        except Exception as e:

            tkMessageBox.showwarning(title="Date Error", message=e)
            self._pvd._date = self._old_date
            
    def draw_plot(self):
        """
        Redraws plot. Used when paramters are changed in options frame.
        Is probably superfluous...
        """

        
        self._plotter.delete()
        self._plotter.draw_plot()
        

    def update_label(self,label_text):
        """
        updates the text label. Called from Plotter object
        during mouse-button events to show data at point selected
        """
        self._label.pack_forget()
        self._label = Label(self._text_line,text=label_text)
        self._label.pack(side=LEFT)

        
    def _move_event(self,event):
        """
        Handler for mouse dragging events. Calls function in Plotter to
        actually do the work...
        """
        self._plotter.draw_vertical(event)

    def _click_event(self,event):
        """
        Handler for mouse click events. Calls function in Plotter to
        actually do the work...
        """
        self._plotter.draw_vertical(event)

    def _release_event(self,event):
        """
        Handler for mouse button release events. Calls function in Plotter to
        actually do the work...
        """
        self._plotter.remove_vertical(event)

    def _configure_event(self,event):
        """
        Handler for window resize events. Calls function in Plotter to
        actually do the work...
        """
        self._plotter.resize(event)
        self.draw_plot()
  

####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = PVPlotApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()






