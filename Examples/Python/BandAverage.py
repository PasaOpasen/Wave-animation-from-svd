'''
Created on November 18, 2019
Using Python 3.6.5
Before running, please make sure that Polytec File Access is installed
@author: Kilian Shambaugh
'''
__version__ = '0.1' 
__author__ = 'Kilian_Shambaugh'

import win32com.client
import numpy as np
from tkinter import *
from tkinter import filedialog
import os

#Calculates the element-wise mimimum between all defined bands
def statmin(Data):
    MIN = []
    for i in range(0,len(Data[0])):
        current_compare = []
        for j in range(0,len(Data)):
            current_compare.append(Data[j][i])
        MIN.append(np.min(current_compare))
    return MIN
    
#Calculates the element-wise maximum between all defined bands
def statmax(Data):
    MAX = []
    for i in range(0,len(Data[0])):
        current_compare = []
        for j in range(0,len(Data)):
            current_compare.append(Data[j][i])
        MAX.append(np.max(current_compare))
    return MAX
    
#Calculates the element-wise mean over all defined bands
def statmean(Data):
    MEAN = []
    for i in range(0,len(Data[0])):
        current_compare = []
        for j in range(0,len(Data)):
            current_compare.append(Data[j][i])
        MEAN.append(np.mean(current_compare))
    return MEAN

#Calculates the element-wise geometric mean over all defined bands
def statgeomean(Data):
    logData = []
    for i in range(0,len(Data)):
        logdata = []
        for j in range(0,len(Data[i])):
            logdata.append(np.log(Data[i][j]))
        logData.append(logdata)
    GEO_MEAN = []
    for i in range(0,len(logData[0])):
        current_compare = []
        for j in range(0,len(logData)):
            current_compare.append(logData[j][i])
        GEO_MEAN.append(np.exp(np.mean(current_compare)))
    return GEO_MEAN

#Accepts a set of all defined bands and returns statistical calculations
def CalcBandAverage(Data):
    BandsMin = statmin(Data)
    BandsMax = statmax(Data)
    BandsMean = statmean(Data)
    BandsGeoMean = statgeomean(Data)
    return BandsMin, BandsMax, BandsMean, BandsGeoMean

#Create the main window and read in the file
root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.withdraw()

file_path = filedialog.askopenfilename(filetypes = [("Scan Files","*.svd")])

if file_path == "":
    file_selected = False
    final_text = "No file was selected. Quitting macro."
else:
    file_selected = True


if file_selected:
    try:
        #Open the file
        file = win32com.client.Dispatch('PolyFile.PolyFile') 
            
        #Make sure that you can write to the file
        file.ReadOnly = False
        
        file.Open(file_path)
        
        #Only run the macro if the file is closed and can be written to
        if file.IsOpen:
            
            # Check if the file is the correct type for band definitions
            band_error = False
            try :
                BandDomains = file.GetBandDomains(592703)
            except:
                band_error = True
                final_text = "In files of this type there are no band domains."
            else:
                #If the file is the correct type, check to see whether bands have been defined in the file
                if not BandDomains.Exists(3):
                    final_text = "Please define bands in the file\n   before running this macro!"
                    band_error = True
            
            #Only perform the macro if there were bands defined in the file
            if not band_error:
                DomainBand = BandDomains.Type(3)
                #Check if the file is 1D or 3D
                Is1D = DomainBand.Channels.Exists("Vib")
                Is3D = DomainBand.Channels.Exists("Vib X") and DomainBand.Channels.Exists("Vib Y") and DomainBand.Channels.Exists("Vib Z")
                
                #Assign channels for the file and check if there is velocity data present
                if Is1D:
                    Channel_01 = DomainBand.Channels("Vib")
                    VelocityExists = Channel_01.Signals.Exists("Velocity")
                elif Is3D:
                    Channel_01 = DomainBand.Channels("Vib X")
                    Channel_02 = DomainBand.Channels("Vib Y")
                    Channel_03 = DomainBand.Channels("Vib Z")
                    VelocityExists = Channel_01.Signals.Exists("Velocity")
                else:
                    VelocityExists = False
                
                #Return a list of data sets containing the band data for either a 1D or a 3D file - for 3D data, the resulting magnitude must additionally be calculated
                if VelocityExists and Is3D:
                    SignalBand_01 = Channel_01.Signals("Velocity")
                    SignalBand_02 = Channel_02.Signals("Velocity")
                    SignalBand_03 = Channel_03.Signals("Velocity")
                    DisplayBand_01 = SignalBand_01.Displays.Type(1)
                    DisplayBand_02 = SignalBand_02.Displays.Type(1)
                    DisplayBand_03 = SignalBand_03.Displays.Type(1)
                
                    Data = []
                    for DataBand in DomainBand.GetDataBands(DisplayBand_01.Signal):
                        data_01 = DataBand.GetData(DisplayBand_01, 0)
                        data_02 = DataBand.GetData(DisplayBand_02, 0)
                        data_03 = DataBand.GetData(DisplayBand_03, 0)
                        
                        data = []
                        for i in range(0,len(data_01)):
                            #Calculate the magnitude for 3D data
                            data.append(np.sqrt(data_01[i]**2 + data_02[i]**2 + data_03[i]**2))
                        data = np.asarray(data)
                        Data.append(data)
                        
                elif VelocityExists and Is1D:
                    SignalBand_01 = Channel_01.Signals("Velocity")
                    DisplayBand_01 = SignalBand_01.Displays.Type(1)
                    
                    Data = []
                    for DataBand in DomainBand.GetDataBands(DisplayBand_01.Signal):
                        data = DataBand.GetData(DisplayBand_01, 0)
                        Data.append(data)  
                else:
                    pass 
                        
                #Only run the macro if the file contains velocity data
                if VelocityExists:
                    
                    #Create a pop-up window
                    def popup_continue():
                        win1 = Toplevel()
                        
                        #Button commands
                        def confirm():
                            global continue_macro
                            continue_macro = True
                            win1.quit()
                            win1.destroy()
                        def deny():
                            global continue_macro
                            global final_text
                            continue_macro = False
                            final_text  = "Quitting macro. File has not been modified."
                            win1.quit()
                            win1.destroy()
                        
                        win1.protocol("WM_DELETE_WINDOW", deny)
                        #Resize the canvas to fill the pop-up window
                        class ResizingCanvas(Canvas):
                            def __init__(self,parent,**kwargs):
                                Canvas.__init__(self,parent,**kwargs)
                                self.bind("<Configure>", self.on_resize)
                                self.height = self.winfo_reqheight()
                                self.width = self.winfo_reqwidth()
                            def on_resize(self,event):
                                # determine the ratio of old width/height to new width/height
                                wscale = float(event.width)/self.width
                                hscale = float(event.height)/self.height
                                self.width = event.width
                                self.height = event.height
                                # resize the canvas 
                                self.config(width=self.width, height=self.height)
                                self.scale("all",0,0,wscale,hscale)
                        # Disable the pop-up window from being resizable
                        win1.resizable(0,0)
                        window_w = int(screen_width/3)
                        window_h = int(screen_height/3)
                        window_x = int(screen_width/3)
                        window_y = int(screen_height/3)
                        
                        #Font size dependent on screen resolution
                        fontsize = int(1.5*screen_width*screen_height/100000)
                        #Window size dependent on screen resolution
                        win1.geometry("{0}x{1}+{2}+{3}".format(window_w, window_h, window_x, window_y))
                        
                        frame = Frame(win1)
                        frame.pack(fill=BOTH, expand=YES)
                        
                        canvas = ResizingCanvas(frame,width=screen_width, height=screen_height, bg="grey70", highlightthickness=0)
            
                        canvas.grid(row=0, column=0,sticky=NW,padx=0,pady=0,columnspan=100,rowspan=100)
                        
                        file_name = os.path.basename(file_path)
                        
                        popup_text1 = "This macro will modify the file:"
                        popup_text2 = "'" + file_name + "'"
                        popup_text3 = "We strongly recommend working with a backup copy"
                        popup_text4 = "of the original data only."
                        popup_text5 = "Do you want to continue?"
                        
                        canvas.create_text(window_w/2,window_h/18,anchor=N, text=popup_text1, font=('Arial bold', int(fontsize/1.6)), fill="black")
                        canvas.create_text(window_w/2,2*window_h/18,anchor=N, text=popup_text2, font=('Arial bold', int(fontsize/1.6)), fill="black")
                        canvas.create_text(window_w/2,4*window_h/18,anchor=N, text=popup_text3, font=('Arial bold', int(fontsize/1.6)), fill="black")
                        canvas.create_text(window_w/2,5*window_h/18,anchor=N, text=popup_text4, font=('Arial bold', int(fontsize/1.6)), fill="black")
                        canvas.create_text(window_w/2,7*window_h/18,anchor=N, text=popup_text5, font=('Arial bold', int(fontsize)), fill="black")
                        
                        win1.title("Continue?")
                        
                        #Create the buttons to continue or quit
                        def deny_button_init():
                            def update_button_down(event):
                                canvas.delete(deny_b_2)
                                canvas.delete(deny_t_2)
                                deny()
                            def update_button_up(event):
                                button_text = "Cancel"
                                button_x = window_w/9
                                button_y = 5*window_h/9
                                button_width = window_w/3
                                button_height = window_h/3
                                global deny_b_2
                                global deny_t_2
                                deny_b_2 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="grey40", outline="grey60")
                                deny_t_2 = canvas.create_text(int((2*button_x+button_width)/2), int((2*button_y+button_height)/2), text=button_text)
                            button_text = "Cancel"
                            button_x = window_w/9
                            button_y = 5*window_h/9
                            button_width = window_w/3
                            button_height = window_h/3
                            global deny_b_1
                            global deny_t_1
                            deny_b_1 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="white", outline="grey60")
                            deny_t_1 = canvas.create_text((int((2*button_x+button_width)/2), int((2*button_y+button_height)/2)), text=button_text)
                            canvas.tag_bind(deny_b_1, "<Button-1>", update_button_up) ## when the square is clicked runs function "clicked".
                            canvas.tag_bind(deny_t_1, "<Button-1>", update_button_up) ## same, but for the text.
                            canvas.tag_bind(deny_b_1, "<ButtonRelease-1>", update_button_down) ## when the square is clicked runs function "clicked".
                            canvas.tag_bind(deny_t_1, "<ButtonRelease-1>", update_button_down) ## same, but for the text.
                        def export_button_hide():
                            canvas.delete(deny_b_1)
                            canvas.delete(deny_t_1)
                        deny_button_init()
                        
                        def confirm_button_init():
                            def update_button_down(event):
                                canvas.delete(confirm_b_2)
                                canvas.delete(confirm_t_2)
                                confirm()
                            def update_button_up(event):
                                button_text = "Continue"
                                button_x = 5*window_w/9
                                button_y = 5*window_h/9
                                button_width = window_w/3
                                button_height = window_h/3
                                global confirm_b_2
                                global confirm_t_2
                                confirm_b_2 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="grey40", outline="grey60")
                                confirm_t_2 = canvas.create_text(int((2*button_x+button_width)/2), int((2*button_y+button_height)/2), text=button_text)
                            button_text = "Continue"
                            button_x = 5*window_w/9
                            button_y = 5*window_h/9
                            button_width = window_w/3
                            button_height = window_h/3
                            global confirm_b_1
                            global confirm_t_1
                            confirm_b_1 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="white", outline="grey60")
                            confirm_t_1 = canvas.create_text((int((2*button_x+button_width)/2), int((2*button_y+button_height)/2)), text=button_text)
                            canvas.tag_bind(confirm_b_1, "<Button-1>", update_button_up) ## when the square is clicked runs function "clicked".
                            canvas.tag_bind(confirm_t_1, "<Button-1>", update_button_up) ## same, but for the text.
                            canvas.tag_bind(confirm_b_1, "<ButtonRelease-1>", update_button_down) ## when the square is clicked runs function "clicked".
                            canvas.tag_bind(confirm_t_1, "<ButtonRelease-1>", update_button_down) ## same, but for the text.
                        def confirm_button_hide():
                            canvas.delete(confirm_b_1)
                            canvas.delete(confirm_t_1)
                        confirm_button_init()
            
                        win1.mainloop()
                    #Open the pop-up window
                    popup_continue()
                    
                    if continue_macro:
                        
                        #Calculate the statistical data sets
                        BandsMin, BandsMax, BandsAvg, BandsGeoAvg = CalcBandAverage(Data)
                        
                        AverageDomains = file.GetPointAverageDomains(722751)
                        DomainAverage = AverageDomains.Type(3)
                        ChannelAverage = DomainAverage.Channels(1)
                        SignalAverage = ChannelAverage.Signals("Velocity")
                        YAxis = DomainAverage.GetYAxes(SignalAverage.Displays.Type(1)).Item(1)
                        
                        #Create a signal description for the new data
                        UsrSigDesc = SignalAverage.Description.Clone()
                        UsrSigDesc.DataType = 2
                        UsrSigDesc.DomainType = 3
                        UsrSigDesc.Name = "Magnitude Average over all Bands. Frame 1 is Min, Frame 2 is Geometric Average, Frame 3 is Average, Frame 4 is Max"
                        UsrSigDesc.Complex = False
                        UsrSigDesc.PowerSignal = False
                        UsrSigDesc.XAxis.MaxCount = len(BandsMin)
                        UsrSigDesc.XAxis.Min = 1
                        UsrSigDesc.XAxis.Max = len(BandsMin)
                        UsrSigDesc.XAxis.Name = "Measurement Point"
                        UsrSigDesc.XAxis.Unit = "Index"
                        UsrSigDesc.YAxis.Name = YAxis.Name
                        UsrSigDesc.YAxis.Min = YAxis.Min
                        UsrSigDesc.YAxis.Max = YAxis.Max
                        UsrSigDesc.YAxis.Unit = YAxis.Unit
                        UsrSigDesc.ResponseDOFs.Assign(0, 3, "Usr", YAxis.Name, YAxis.Unit)
                        
                        UsrSignal = AverageDomains.FindSignal(UsrSigDesc, True)
                        #Check if the signal already exists in the file
                        global new_file
                        global write_data
                        
                        new_file = False
                        write_data = False
                        #Check whether the signal already exists in the file. If not, write the data to the file. Otherwise, prompt the user whether or not to overwrite the existing adata
                        if UsrSignal == None:
                            write_data = True
                            new_file = True
                        else:
                            #Create a pop-up window
                            def popup():
                                win1 = Toplevel()
                                #Button commands
                                def confirm():
                                    global write_data
                                    write_data = True
                                    win1.quit()
                                    win1.destroy()
                                def deny():
                                    win1.quit()
                                    win1.destroy()
                                win1.protocol("WM_DELETE_WINDOW", deny)
                                #Resize the canvas to fill the pop-up window
                                class ResizingCanvas(Canvas):
                                    def __init__(self,parent,**kwargs):
                                        Canvas.__init__(self,parent,**kwargs)
                                        self.bind("<Configure>", self.on_resize)
                                        self.height = self.winfo_reqheight()
                                        self.width = self.winfo_reqwidth()
                                    def on_resize(self,event):
                                        # determine the ratio of old width/height to new width/height
                                        wscale = float(event.width)/self.width
                                        hscale = float(event.height)/self.height
                                        self.width = event.width
                                        self.height = event.height
                                        # resize the canvas 
                                        self.config(width=self.width, height=self.height)
                                        self.scale("all",0,0,wscale,hscale)
                                # Disable the pop-up window from being resizable
                                win1.resizable(0,0)
                                window_w = int(screen_width/3)
                                window_h = int(screen_height/3)
                                window_x = int(screen_width/3)
                                window_y = int(screen_height/3)
                                
                                #Font size dependent on screen resolution
                                fontsize = int(1.5*screen_width*screen_height/100000)
                                #Window size dependent on screen resolution
                                win1.geometry("{0}x{1}+{2}+{3}".format(window_w, window_h, window_x, window_y))
                                
                                frame = Frame(win1)
                                frame.pack(fill=BOTH, expand=YES)
                                
                                canvas = ResizingCanvas(frame,width=screen_width, height=screen_height, bg="grey70", highlightthickness=0)
                
                                canvas.grid(row=0, column=0,sticky=NW,padx=0,pady=0,columnspan=100,rowspan=100)
                                canvas.create_text(window_w/2,window_h/3,anchor=N, text="Overwite data?", font=('Arial bold', fontsize), fill="black")
                                canvas.create_text(window_w/2,1.5*window_h/9,anchor=N, text="A user defined signal with this name already exists.", font=('Arial bold', int(fontsize/1.5)), fill="black")
                                
                                win1.title("Continue?")
                                
                                #Create the buttons to continue or quit
                                def deny_button_init():
                                    def update_button_down(event):
                                        canvas.delete(deny_b_2)
                                        canvas.delete(deny_t_2)
                                        deny()
                                    def update_button_up(event):
                                        button_text = "Cancel"
                                        button_x = window_w/9
                                        button_y = 5*window_h/9
                                        button_width = window_w/3
                                        button_height = window_h/3
                                        global deny_b_2
                                        global deny_t_2
                                        deny_b_2 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="grey40", outline="grey60")
                                        deny_t_2 = canvas.create_text(int((2*button_x+button_width)/2), int((2*button_y+button_height)/2), text=button_text)
                                    button_text = "Cancel"
                                    button_x = window_w/9
                                    button_y = 5*window_h/9
                                    button_width = window_w/3
                                    button_height = window_h/3
                                    global deny_b_1
                                    global deny_t_1
                                    deny_b_1 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="white", outline="grey60")
                                    deny_t_1 = canvas.create_text((int((2*button_x+button_width)/2), int((2*button_y+button_height)/2)), text=button_text)
                                    canvas.tag_bind(deny_b_1, "<Button-1>", update_button_up) ## when the square is clicked runs function "clicked".
                                    canvas.tag_bind(deny_t_1, "<Button-1>", update_button_up) ## same, but for the text.
                                    canvas.tag_bind(deny_b_1, "<ButtonRelease-1>", update_button_down) ## when the square is clicked runs function "clicked".
                                    canvas.tag_bind(deny_t_1, "<ButtonRelease-1>", update_button_down) ## same, but for the text.
                                def export_button_hide():
                                    canvas.delete(deny_b_1)
                                    canvas.delete(deny_t_1)
                                deny_button_init()
                                
                                def confirm_button_init():
                                    def update_button_down(event):
                                        canvas.delete(confirm_b_2)
                                        canvas.delete(confirm_t_2)
                                        confirm()
                                    def update_button_up(event):
                                        button_text = "Continue"
                                        button_x = 5*window_w/9
                                        button_y = 5*window_h/9
                                        button_width = window_w/3
                                        button_height = window_h/3
                                        global confirm_b_2
                                        global confirm_t_2
                                        confirm_b_2 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="grey40", outline="grey60")
                                        confirm_t_2 = canvas.create_text(int((2*button_x+button_width)/2), int((2*button_y+button_height)/2), text=button_text)
                                    button_text = "Continue"
                                    button_x = 5*window_w/9
                                    button_y = 5*window_h/9
                                    button_width = window_w/3
                                    button_height = window_h/3
                                    global confirm_b_1
                                    global confirm_t_1
                                    confirm_b_1 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="white", outline="grey60")
                                    confirm_t_1 = canvas.create_text((int((2*button_x+button_width)/2), int((2*button_y+button_height)/2)), text=button_text)
                                    canvas.tag_bind(confirm_b_1, "<Button-1>", update_button_up) ## when the square is clicked runs function "clicked".
                                    canvas.tag_bind(confirm_t_1, "<Button-1>", update_button_up) ## same, but for the text.
                                    canvas.tag_bind(confirm_b_1, "<ButtonRelease-1>", update_button_down) ## when the square is clicked runs function "clicked".
                                    canvas.tag_bind(confirm_t_1, "<ButtonRelease-1>", update_button_down) ## same, but for the text.
                                def confirm_button_hide():
                                    canvas.delete(confirm_b_1)
                                    canvas.delete(confirm_t_1)
                                confirm_button_init()
                
                                win1.mainloop()
                            #Open the pop-up window
                            popup()
            
                        #Write the data to the file and save or quit the macro without writing to the file
                        if write_data:
                            if new_file:
                                #Add the signal description to the file
                                UsrSignal = AverageDomains.AddSignal(UsrSigDesc)
                            else:
                                #Update the file's signal description
                                UsrSignal.Channel.Signals.Update(UsrSignal.Name, UsrSigDesc)
                            DomainAverage.SetData(UsrSignal, 1, np.asarray(BandsMin))
                            DomainAverage.SetData(UsrSignal, 2, np.asarray(BandsGeoAvg))
                            DomainAverage.SetData(UsrSignal, 3, np.asarray(BandsAvg))
                            DomainAverage.SetData(UsrSignal, 4, np.asarray(BandsMax))
                            file.Save()
                            final_text = "Finished! Data written to file."
                        else:
                            final_text = "Quitting macro. File has not been modified."
        
                else:
                    final_text = "The file does not contain an appropriate velocity signal!\n     Quitting macro."

    finally:
        if file.IsOpen:
            #Close the open file
            file.Close()
            
#Create a pop-up window when macro is finished
def final_popup():
    win1 = Toplevel()
    #Button commands
    def OK():
        win1.quit()
        win1.destroy()
    win1.protocol("WM_DELETE_WINDOW", OK)
    #Resize the canvas to fill the pop-up window
    class ResizingCanvas(Canvas):
        def __init__(self,parent,**kwargs):
            Canvas.__init__(self,parent,**kwargs)
            self.bind("<Configure>", self.on_resize)
            self.height = self.winfo_reqheight()
            self.width = self.winfo_reqwidth()
        def on_resize(self,event):
            wscale = float(event.width)/self.width
            hscale = float(event.height)/self.height
            self.width = event.width
            self.height = event.height
            # resize the canvas 
            self.config(width=self.width, height=self.height)
            self.scale("all",0,0,wscale,hscale)
    # Disable the pop-up window from being resizable
    win1.resizable(0,0)
    window_w = int(screen_width/3)
    window_h = int(screen_height/3)
    window_x = int(screen_width/3)
    window_y = int(screen_height/3)
    
    #Font size dependent on screen resolution
    fontsize = int(1.5*screen_width*screen_height/100000)
    #Window size dependent on screen resolution
    win1.geometry("{0}x{1}+{2}+{3}".format(window_w, window_h, window_x, window_y))
    
    frame = Frame(win1)
    frame.pack(fill=BOTH, expand=YES)
    
    canvas = ResizingCanvas(frame,width=screen_width, height=screen_height, bg="grey70", highlightthickness=0)

    canvas.grid(row=0, column=0,sticky=NW,padx=0,pady=0,columnspan=100,rowspan=100)
    canvas.create_text(window_w/2,1.5*window_h/9,anchor=N, text=final_text, font=('Arial bold', int(fontsize/1.2)), fill="black")
    
    win1.title("Macro Finished")
    
    #Create the button to quit
    def OK_button_init():
        def update_button_down(event):
            canvas.delete(OK_b_2)
            canvas.delete(OK_t_2)
            OK()
        def update_button_up(event):
            button_text = "Quit"
            button_x = window_w*0.1
            button_y = 5*window_h/9
            button_width = window_w*0.8
            button_height = window_h/3
            global OK_b_2
            global OK_t_2
            OK_b_2 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="grey40", outline="grey60")
            OK_t_2 = canvas.create_text(int((2*button_x+button_width)/2), int((2*button_y+button_height)/2), text=button_text, font=('Arial bold', int(fontsize/1.2)), fill="black")
        button_text = "Quit"
        button_x = window_w*0.1
        button_y = 5*window_h/9
        button_width = window_w*0.8
        button_height = window_h/3
        global OK_b_1
        global OK_t_1
        OK_b_1 = canvas.create_rectangle(button_x, button_y, button_x + button_width, button_y + button_height, fill="white", outline="grey60")
        OK_t_1 = canvas.create_text((int((2*button_x+button_width)/2), int((2*button_y+button_height)/2)), text=button_text, font=('Arial bold', int(fontsize/1.2)), fill="black")
        canvas.tag_bind(OK_b_1, "<Button-1>", update_button_up) ## when the square is clicked runs function "clicked".
        canvas.tag_bind(OK_t_1, "<Button-1>", update_button_up) ## same, but for the text.
        canvas.tag_bind(OK_b_1, "<ButtonRelease-1>", update_button_down) ## when the square is clicked runs function "clicked".
        canvas.tag_bind(OK_t_1, "<ButtonRelease-1>", update_button_down) ## same, but for the text.
    def export_button_hide():
        canvas.delete(OK_b_1)
        canvas.delete(OK_t_1)
    OK_button_init()

    win1.mainloop()
#Open the pop-up window
final_popup()
