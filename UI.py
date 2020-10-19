import json
import threading
import time
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import ttk, scrolledtext
from ttkthemes import themed_tk as tk
import TrafficData
from tkinter import filedialog

class AppUI:
    # Constructor which creates the UI
    def __init__(self):
        self.__root=tk.ThemedTk()
        self.__root.get_themes()
        self.__root.set_theme("radiance")
        self.__root.configure(background='black')
        self.__root.state('zoomed')
        self.__root.title("Network Traffic Data Fetcher")

        # This frame contains the widgets on the left side of the window
        self.__leftframe=self.__create_frame(self.__root,'black',LEFT,0)
        #This frame conatins the widgets on the right side of the window
        self.__rightframe=self.__create_frame(self.__root,'black',RIGHT,20)

        self.__headinglabel = self.__create_label(self.__leftframe,'WELCOME TO NETWORK TRAFFIC FETCHER','black','white', '16',TOP)

        # This frame contains the input fields and buttons to open and capture data
        self.__entryAndBtnframe=self.__create_frame(self.__leftframe,'black',TOP,0)

        # This frame contains the input field
        self.__inputframe=self.__create_frame(self.__entryAndBtnframe,'black',TOP,0)
        self.__inputlabel=self.__create_label(self.__inputframe,"Enter an URL",'black','white','12',LEFT)
        # This entry field takes the url input
        self.__entryfield=tkinter.Entry(self.__inputframe,width=55)
        self.__entryfield.pack(pady=10)

        # This frame contains the submit and capture button
        self.__btnframe=self.__create_frame(self.__entryAndBtnframe,'black',TOP,10)
        # This button opens the web page
        self.__submitbtn=ttk.Button(self.__btnframe,text="Submit",command=self.__open_page)
        self.__submitbtn.pack()
        # This button  captures the data
        self.__capturebtn=ttk.Button(self.__btnframe,text="Capture Traffic Data",state='disabled',command=self.__get_data)
        self.__capturebtn.pack(pady=10)

        # This frame contains a list box which shows the captured details and other widgets
        self.dataListFrame=self.__create_frame(self.__leftframe,'black',TOP,0)
        self.__add_widgets()

        label=self.__create_label(self.__rightframe,"REQUEST DETAILS",'black','white','12',TOP)

        # This frame contains the request method type, url and httpversion widgets
        reqlabelFrame=self.__create_frame(self.__rightframe,'white',TOP,10)
        self.reqMethod=self.__create_label(reqlabelFrame,"METHOD",'black','white','10',LEFT)
        self.reqURL=Text(reqlabelFrame,state='normal', width=80, height=1)
        self.reqURL.insert('end', 'URL')
        self.reqURL.configure(state='disabled')
        self.reqURL.pack(side=LEFT)
        self.reqHttpVersion=self.__create_label(reqlabelFrame,"HTTP VERSION",'black','white','10',RIGHT)

        # Declares the tabs which shows the request details
        tabControl=ttk.Notebook(self.__rightframe)
        tab1 = ttk.Frame(tabControl) # Headers tab
        tab3=ttk.Frame(tabControl) # Params tab
        tab4=ttk.Frame(tabControl) # Body tab

        tabControl.add(tab1, text ='Headers')
        # Creates a canvas in the tab
        headersArea=Canvas(tab1,width=800, height=200,background='white')
        headersArea.pack(side=LEFT)
        # Creates a window to add the header details and widgets to see the details
        self.headerFrame=self.__create_window(headersArea,tab1)

        tabControl.add(tab3,text='Params')
        # Creates a canvas in the params tab
        paramArea=Canvas(tab3,width=800, height=200,background='white')
        paramArea.pack(side=LEFT)
        # Creates a window to add the params details and widgets to see the details
        self.paramFrame=self.__create_window(paramArea,tab3)

        tabControl.add(tab4,text='Body')
        # Creates a canvas in the body tab
        bodyArea=Canvas(tab4,width=800, height=200,background='white')
        bodyArea.pack(side=LEFT)
        # Creates a window to add the body details and widgets to see the details
        self.bodyFrame=self.__create_window(bodyArea,tab4)

        tabControl.pack(expand = 0, fill ="both",side=TOP)

        label=self.__create_label(self.__rightframe,"RESPONSE DETAILS",'black','white','12',TOP)

        # Declares the tabs which shows the response details
        tabControl=ttk.Notebook(self.__rightframe)
        tab1 = ttk.Frame(tabControl) # headers
        tab3=ttk.Frame(tabControl) # Content
        tab4=ttk.Frame(tabControl) # Status

        tabControl.add(tab4,text='Status')
        # Creates a canvas in the status tab
        statusArea=Canvas(tab4,width=800, height=150,background='white')
        statusArea.pack(side=LEFT)
        # Creates a window to add the status details and widgets to see the details
        self.responseStatusFrame=self.__create_window(statusArea,tab4)

        tabControl.add(tab1, text ='Headers')
        # Creates a canvas in the headers tab
        headersArea=Canvas(tab1,width=800, height=150,background='white')
        headersArea.pack(side=LEFT)
        # Creates a window to add the headers details and widgets to see the details
        self.responseHeaderFrame=self.__create_window(headersArea,tab1)

        tabControl.add(tab3,text='Content')
        # Creates a canvas in the content tab
        contentArea=Canvas(tab3,width=800, height=150,background='white')
        contentArea.pack(side=LEFT)
        # Creates a window to add the content details and widgets to see the details
        self.responseContentFrame=self.__create_window(contentArea,tab3)

        tabControl.pack(expand = 0, fill ="both",side=TOP)

        self.__create_label(self.__rightframe,"Download List",'white','black','8',TOP)

        scb = tkinter.Scrollbar(self.__rightframe, orient='vertical') # Vertical scrollbar
        # Listbox for list of requests that are to be downloaded
        self.downloadlistbox = tkinter.Listbox(self.__rightframe, width=81, height=8, yscrollcommand=scb.set, bg='white')
        scb.config(command=self.downloadlistbox.yview)
        self.downloadlistbox.pack(side=LEFT)
        scb.pack(side=LEFT,fill='y')

        # This frames contains the button to add to list, remove from list and download requests
        downloadwidgetframe=self.__create_frame(self.__rightframe,'white',LEFT,0)
        self.__addToDListbtn=ttk.Button(downloadwidgetframe,text="Add",state='disabled',command=self.__addToDList)
        self.__addToDListbtn.pack()
        self.__removeFromDListbtn=ttk.Button(downloadwidgetframe,text="Remove",command=self.__removeFromDList)
        self.__removeFromDListbtn.pack()
        self.__downloadbtn=ttk.Button(downloadwidgetframe,text="Download",state='disabled',command=self.__download_data)
        self.__downloadbtn.pack()

        # Declares an empty list which stores the request-response pairs to be downloaded
        self.__downloadList=[]
        # Declares a variable for index of download listbox and sets it to -1
        self.__DListboxIndex=-1

        self.__root.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__root.mainloop()

    def __on_closing(self):
        try:
            self.__traffic.close()
        except:
            pass
        self.__root.destroy()

    # Creates a frame in the passed canvas(headersArea) and adds the widgets , add scrollbar to tab frame(rframe)
    def __create_window(self,headersArea,rframe):
        headersArea.grid(row = 0, column = 0, sticky = 'nsew')
        frame=tkinter.Frame(headersArea)
        # Scrollbar with canvas don't work thats why this window is created on the above frame
        headersArea.create_window( 0, 0, window = frame, anchor=NW )

        vbar = Scrollbar(rframe, orient = 'vertical', command= headersArea.yview)
        vbar.grid(row = 0, column = 1, sticky = 'ns')

        hbar= Scrollbar(rframe,orient='horizontal',command=headersArea.xview)
        hbar.grid(row = 1, column = 0, sticky = 'sw')

        headersArea.config(yscrollcommand = vbar.set)
        headersArea.config(xscrollcommand=hbar.set)

        frame.bind('<Configure>', lambda e: self.__on_config(e,headersArea))

        # Returns the frame which will conatin the textboxes to show the data
        return frame

    # Configures the scroll region
    def __on_config(self,e,headersarea):
        headersarea.configure(scrollregion=(0, 0, e.width, e.height))

    # Adds different widgets in the dataListFrame
    def __add_widgets(self):
        tabControl=ttk.Notebook(self.dataListFrame)
        tab1 = ttk.Frame(tabControl) # All Data tab
        tab2 = ttk.Frame(tabControl) # Search tab
        tabControl.add(tab1, text ='All Data')
        tabControl.add(tab2, text ='Search')
        tabControl.pack(expand = 1, fill ="both",side=TOP)

        # listboxmain shows all data and filtersmain stores the filter variables (IntVar())
        self.listboxmain,self.filtersmain=self.__getListbox(tab1,False)
        # listbox2 shows searched data and filters2 stores the search filter variables (IntVar())
        self.listbox2,self.filters2=self.__getListbox(tab2,True)

        # Binds a function for mouse double click on the listboxmain
        self.listboxmain.bind('<Double-1>',lambda x:self.__populateData(x,self.listboxmain))
        # Binds a function for mouse double click on the listbox2
        self.listbox2.bind('<Double-1>',lambda x:self.__populateData(x,self.listbox2))

        # This frame contains the widgets used for generating scripts
        genScriptFrame=Frame(self.dataListFrame)
        genScriptFrame.pack(side=TOP,pady=20)

        # Gives the chosen language from the language dropdown combo box
        self.chosenLang=StringVar()
        language=ttk.Combobox(genScriptFrame,width = 15,  textvariable = self.chosenLang)
        language['values']=['Java','Python','Node JS']
        language.pack(side=LEFT)
        language.current(0)
        language.configure(state='readonly')

        # Gives the chosen library from the library dropdown combo box
        self.chosenLib=StringVar()
        self.__library=ttk.Combobox(genScriptFrame,width = 15,  textvariable = self.chosenLib)
        self.__library['values']=['RestAssured','UniRest']
        self.__library.pack(side=LEFT)
        self.__library.current(0)
        self.__library.configure(state='readonly')

        # This thread changes the values of library dropdown depending on the chosen language and changes the state of buttons
        self.t=threading.Thread(target=self.__change_libraries,daemon=True)
        self.t.start()

        # This button invokes the generate script function
        genScript=ttk.Button(genScriptFrame,text="Generate Script",command=self.__generate_script)
        genScript.pack(side=RIGHT)

    # Changes the values of library dropdown and states of some buttons
    def __change_libraries(self):
        while(1):
            if(self.chosenLang.get()=='Java'):
                self.__library['values']=['RestAssured','UniRest']
            elif(self.chosenLang.get()=='Python'):
                self.__library['values']=['Requests']
            else:
                self.__library['values']=['LIB 1']

            # If the download list box is empty the the remove and download buttons are disabled else enabled
            if(self.__DListboxIndex<0):
                self.__removeFromDListbtn['state']='disabled'
                self.__downloadbtn['state']='disabled'
            else:
                self.__removeFromDListbtn['state']='enabled'
                self.__downloadbtn['state']='enabled'


    # Creates a frame
    def __create_frame(self,container,color,position,pady):
        frame=tkinter.Frame(container,background=color)
        frame.pack(side=position,fill=BOTH,pady=pady)
        return frame

    # Creates a label
    def __create_label(self,container,text,background,foreground,fontSize,position):
        label=ttk.Label(container,text=text,background=background,foreground=foreground,font="Times "+fontSize+" bold")
        label.pack(side=position,padx=10)
        return label

    # Opens the web page
    def __open_page(self):
        url=self.__entryfield.get()
        if(len(url)==0):
            tkinter.messagebox.showerror('Invalid URL!!', 'The entered URL is invalid')
            return
        try:
            # Creates a object of Traffic class
            self.__traffic=TrafficData.Traffic()
            # Calls the Traffic.open_page(url) function
            flag,message=self.__traffic.open_page(url)
            if(not flag):
                tkinter.messagebox.showerror('Exception!!',message)
                return
            self.__capturebtn['state']='enabled'
        except:
            tkinter.messagebox.showerror('Invalid URL!!', 'The entered URL is invalid')

    # Captures all the data and fetches
    def __get_data(self):
        # Class the Traffic.get_data() function
        flag,data=self.__traffic.get_data()
        if(not flag):
            tkinter.messagebox.showerror('Exception!!',data)
            return
        # Stores all the captured request urls
        self.__urldata =[]
        # Stores the entries as values and url as key
        self.__data={}

        # Removes everything from the list box of all data tab
        self.listboxmain.delete(0,'end')

        # Adds all the captured request urls in the list box of all data tab
        index=0
        for entry in data:
            url=entry['request']['url']
            if(url not in self.__urldata):
                self.__urldata.append(url)
                self.__data[url]=entry
                self.listboxmain.insert(index,url)
                index+=1

        self.__capturebtn['state']='disabled'

    # Dowloads all the request-response pairs from the download list box
    def __download_data(self):
        filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if('.json' not in filename):
            filename+='.json'
        out=open(filename,'w')
        data=[]
        for url in self.__downloadList:
            data.append(self.__data[url[:-1]])

        data={'entries':data}
        json.dump(data,out,indent=6)

    # Applies the filters on the list box of the all data tab
    def __apply_filter(self):
        if(self.listboxmain.size()==0):
            return
        flag=True
        # Checking whether any filter flag is true or not
        for i in self.filtersmain:
            if(i.get()):
                flag=False
                break

        # Clears all the entries from the list box
        self.listboxmain.delete(0,'end')
        index=0
        dic={'GET':0,'POST':1,'PUT':2,'OPTIONS':3,'DELETE':4}
        for entry in self.__data.values():
            method=entry['request']['method']
            # Checks the IntVar() of the corresponding request method whether that is true or no filter is set
            if(self.filtersmain[dic[method]].get() or flag):
                self.listboxmain.insert(index,entry['request']['url'])
                index+=1

    # Returns a list box object on specified tab in the parameters , serachField is true if the tab is search tab
    def __getListbox(self,tab,searcFeild):
        # This conatins the filters as dropdown check_button
        frame1=tkinter.Frame(tab)
        frame1.pack(side=TOP)

        # This conatins the listbox and the vertical scrollbar
        frame2=tkinter.Frame(tab)
        frame2.pack(side=TOP)

        # Add filter menubutton
        mb=Menubutton(frame1,text="Add Filter", relief=RAISED)
        mb.pack(side=LEFT)
        mb.menu  =  Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu

        # IntVar() for the filters
        post = IntVar()
        get = IntVar()
        put = IntVar()
        options=IntVar()
        delete= IntVar()
        javascript = IntVar()

        # Adds the check buttons
        mb.menu.add_checkbutton ( label="POST", variable=post)
        mb.menu.add_checkbutton ( label="GET", variable=get)
        mb.menu.add_checkbutton ( label="DELETE", variable=delete)
        mb.menu.add_checkbutton ( label="PUT", variable=put)
        mb.menu.add_checkbutton ( label="OPTIONS", variable=options)


        # If searchField is true then a search button is created otherwise apply button is created
        if(searcFeild):
            self.__searchentryfield=tkinter.Entry(frame1,width=55)
            self.__searchentryfield.pack(side=LEFT)
            # Invokes apply_search function
            applybtn=ttk.Button(frame1,text="Search",command=self.__apply_search)
            applybtn.pack(side=LEFT)
        else:
            # Invokes apply_filter function
            applybtn=ttk.Button(frame1,text="Apply",command=self.__apply_filter)
            applybtn.pack(side=LEFT)


        scb = tkinter.Scrollbar(frame2, orient='vertical')
        listbox = tkinter.Listbox(frame2, width=65, height=17, yscrollcommand=scb.set, bg='white')
        scb.config(command=listbox.yview)
        listbox.pack(side=LEFT)
        scb.pack(side=LEFT)

        # Returns the listbox object and the filter IntVar
        return  listbox,(get,post,put,options,delete,javascript)

    # Searches all the data and adds the required data in the list box of search tab
    def __apply_search(self):
        url=self.__searchentryfield.get()
        if(len(url)==0):
            tkinter.messagebox.showerror('Invalid URL!!', 'The entered URL is invalid')
            return
        # Removes all the entries from the list box of search tab
        self.listbox2.delete(0,'end')
        flag=True
        # Checking whether any filter flag is true or not
        for i in self.filters2:
            if(i.get()):
                flag=False
                break
        dic={'GET':0,'POST':1,'PUT':2,'OPTIONS':3,'DELETE':4}
        index=0
        for URL in self.__urldata:
            # Checks if the entered url is a substring of the url the request
            if(bool(re.search(url,URL))):
                method=self.__data[URL]['request']['method']
                # Checks the IntVar() of the corresponding request method whether that is true or no filter is set
                if(self.filters2[dic[method]].get() or flag):
                    self.listbox2.insert(index,URL)
                    index+=1

    # Populates the request details and response details tabs
    def __populateData(self,e, listbox):
        if(len(listbox.curselection())==0):
            return

        # Gets the selected url
        url=listbox.get(listbox.curselection())

        # If the url is not in downloadlist then the addToList button is enabled
        if(url not in self.__downloadList):
            self.__addToDListbtn['state']='enabled'
        # Gets the request details of the selected url
        request=self.__data[url]['request']
        # Gets the method of the request
        method=request['method']
        # Httpversion of the request
        httpVersion=request['httpVersion']
        # Inserts the details in the corresponding widgets
        self.reqMethod['text']=method
        self.reqURL.configure(state='normal')
        self.reqURL.delete('1.0','end')
        self.reqURL.insert('end',url)
        self.reqURL.configure(state='disabled')
        self.reqHttpVersion['text']=httpVersion

        # Gets the headers of the request
        headers=request['headers']
        # Stores the parameters if there is any
        params={}
        try:
            params=request['queryString']
        except:
            pass
        # Stores the body as field if there is any
        self.body={}
        try:
            self.body=request['postData']
        except:
            pass

        # Adds the headers in the header tab, stores the headers as field
        self.headers=self.__add_data(headers,self.headerFrame)
        # Adds the parameters in the params tab, stores the params as field
        self.params=self.__add_data(params,self.paramFrame)
        # Adds the body in the body tab
        self.__add_body_data(self.body,self.bodyFrame)

        # Stores the response of the selected url
        response=self.__data[url]['response']
        # Stores the response headers
        responseHeaders=response['headers']
        # Stores the response content
        responseContent=response['content']
        # Stores the response content
        responseStatus={'status':response['status'],'statusText':response['statusText'],'httpVersion':response['httpVersion']}
        # Adds the headers in header tab
        self.__add_data(responseHeaders,self.responseHeaderFrame)
        # Adds the content in content tab
        self.__add_body_data(responseContent,self.responseContentFrame)
        # Adds the status in the status tab
        self.__add_body_data(responseStatus,self.responseStatusFrame)

    # Adds the specified data in the specified frame
    def __add_data(self, data, frame):
        # Removes all the pre existing widgtes
        for widget in frame.winfo_children():
            widget.destroy()

        row=0
        # Converts the value of key 'name' as key and value of key 'value' as value and stores in this dictionary
        n_data={}
        # Adds the name and value of each entry in col 0 and col 1 of each row
        for each in data:
            name=each['name']
            value=each['value']

            n_data[name]=value

            nameText=Text(frame,state='normal',width=25, height=1)
            nameText.insert('end',name)
            nameText.configure(state='disabled')
            nameText.grid(row=row,column=0)

            valText=Text(frame,state='normal',width=1000, height=1)
            valText.insert('end',value)
            valText.configure(state='disabled')
            valText.grid(row=row,column=2)

            row+=1
        return n_data

    # Adds the specified data in the specified frame
    def __add_body_data(self, data, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        row=0
        # Adds the key and value of each entry in col 0 and col 1 of each row
        for key in data.keys():
            value=data[key]

            keyText=Text(frame,state='normal',width=25, height=1)
            keyText.insert('end',key)
            keyText.configure(state='disabled')
            keyText.grid(row=row,column=0)

            valText=Text(frame,state='normal',width=1000, height=1)
            valText.insert('end',value)
            valText.configure(state='disabled')
            valText.grid(row=row,column=2)

            row+=1

    # Generates a script in the chosen language and library to test the selected request
    def __generate_script(self):
        script=''
        if(self.chosenLang.get()=="Java" and self.chosenLib.get()=="RestAssured"):
            scriptGen=JavaRestAssuredScriptGenerator(self.headers,self.params,self.body,self.reqURL.get('1.0','end')[:-1])
            script=scriptGen.generate_script(self.reqMethod['text'])
        elif(self.chosenLang.get()=="Java" and self.chosenLib.get()=="UniRest"):
            scriptGen=JavaUniRestScriptGenerator(self.headers,self.params,self.body,self.reqURL.get('1.0','end')[:-1])
            script=scriptGen.generate_script(self.reqMethod['text'])
        elif(self.chosenLang.get()=="Python" and self.chosenLib.get()=="Requests"):
            scriptGen=PythonRequestsScriptGenerator(self.headers,self.params,self.body,self.reqURL.get('1.0','end')[:-1])
            script=scriptGen.generate_script(self.reqMethod['text'])
        else:
            return

        # Creates a popup window to show the genearted script

        self.__popupmessagewindow(script)

    # Adds the selected url in the download list box
    def __addToDList(self):
        url=self.reqURL.get('1.0','end')
        if(url not in self.__downloadList):
            self.__downloadList.append(url)
            self.__DListboxIndex+=1 # Inserts in the list
            self.downloadlistbox.insert(self.__DListboxIndex,url) # Inserts in the list box
        self.__addToDListbtn['state']='disabled'

    # Removes the selected url from the download list box
    def __removeFromDList(self):

        target_url=self.downloadlistbox.get(self.downloadlistbox.curselection())
        url=self.reqURL.get('1.0','end')
        # If the selected url from download list box and the url of the request loaded in the tabs is same then add button is enabled
        if(url==target_url):
            self.__addToDListbtn['state']='enabled'
        index=int(self.downloadlistbox.curselection()[0])
        self.downloadlistbox.delete(index) # Removes from download list box
        self.__DListboxIndex-=1
        self.__downloadList.remove(target_url) # Removes from download list

    # Creates a popup window
    def __popupmessagewindow(self,script):
        popup=tkinter.Tk()
        popup.wm_title('Script')
        popup.resizable(0,0)
        frame=tkinter.Frame(popup)
        frame.pack(side=TOP)
        text=Text(frame,state='normal',width=60, height=20,wrap=tkinter.NONE)
        text.insert('end',script)
        text.configure(state='disabled')
        text.pack(side=LEFT)
        vbar = Scrollbar(frame, orient = 'vertical', command= text.yview)
        vbar.pack(side=LEFT,fill='y')

        hbar = Scrollbar(popup,orient='horizontal',command=text.xview)
        hbar.pack(side=TOP,fill='x')
        text.configure(state='disabled',yscrollcommand=vbar.set)
        text.configure(xscrollcommand=hbar.set)

        btn=ttk.Button(popup,text='Save',command=lambda:self.__save_script(script,popup))
        btn.pack(side=TOP)

        popup.mainloop()

    # Saves the script
    def __save_script(self,script,popup):
        filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        if('.txt' not in filename):
            filename+='.txt'
        out=open(filename,'w')
        out.write(script)
        out.close()
        popup.destroy()


class ScriptGenerator:
    # Constructor which takes the headers,params ,body and the url as argument
    def __init__(self,headers,params,body,url):
        self.headers=headers
        self.params=params
        self.body=body
        self.url=url.split('?')[0] # The query parameters from the url are removed

    # Abstract method to generate the string for adding the body in script
    def create_body(self):
        pass
    # Abstract method to generate the string for adding the header in script
    def create_header(self):
        pass
    # Abstract method to generate the string for adding the params in script
    def create_params(self):
        pass
    # Abstarct method, returns the script string for get method
    def script_get(self):
        pass
    # Abstarct method, returns the script string for post method
    def script_post(self):
        pass
    # Abstarct method, returns the script string for put method
    def script_put(self):
        pass
    # Abstarct method, returns the script string for options method
    def script_options(self):
        pass
    # Abstarct method, returns the script string for delete method
    def script_delete(self):
        pass
    # Generates the script, takes method as argument
    def generate_script(self,method):
        self.create_body()
        self.create_header()
        self.create_params()
        script=None
        if(method=='GET'):
            script=self.script_get()
        elif(method=='POST'):
            script=self.script_post()
        elif(method=='PUT'):
            script=self.script_put()
        elif(method=='OPTIONS'):
            script=self.script_options()
        elif(method=='DELETE'):
            script=self.script_delete()
        return script

#Inherits from ScriptGenerator class, defines some methods for genertaing java script
class JavaScriptGenerator(ScriptGenerator):
    def __init__(self,headers,params,body,url):
        super().__init__(headers,params,body,url)
        self.script_body=None # Stores string for adding body to the script
        self.script_headers=None # Stores string for adding headers to the script
        self.script_params=None # Stores string for adding params to the script

    # Creates the string for adding body to the script
    def  create_body(self):
        if(len(self.body)==0):
            return
        self.script_body="Map<String, Object>  jsonAsMap = new HashMap<>();\n"
        for key in self.body.keys():
            string="jsonAsMap.put(\""+key+"\",\""+self.body[key]+"\")\n"
            self.script_body+=string
    # Creates the string for adding headers to the script
    def create_header(self):
        self.script_headers=""
        for key in self.headers.keys():
            string="                 .header(\""+key+"\",\""+self.headers[key]+"\")\n"
            self.script_headers+=string
    # Creates the string for params to the script
    def create_params(self):
        if(len(self.params)==0):
            return
        self.script_params=""
        for key in self.params.keys():
            string="                 .queryParam(\""+key+"\",\""+self.params[key]+"\")\n"
            self.script_params+=string

#Inherits from ScriptGenerator class, defines some methods for genertaing python script
class PythonScriptGenerator(ScriptGenerator):
    def __init__(self,headers,params,body,url):
        super().__init__(headers,params,body,url)
        self.script_body=None
        self.script_headers=None
        self.script_params=None
    def  create_body(self):
        if(len(self.body)==0):
            return
        self.script_body="payload = "+json.dumps(self.body,skipkeys = True,allow_nan = True,indent = 6)+"\n\n"
    def create_header(self):
        self.script_headers="headers = "+json.dumps(self.headers,skipkeys = True,allow_nan = True,indent = 6)+"\n\n"
    def create_params(self):
        if(len(self.params)==0):
            return
        self.script_params="params = "+json.dumps(self.params,skipkeys = True,allow_nan = True,indent = 6)+"\n\n"

#Inherits from JavaScriptGenerator class, defines the abstract methods for genertaing java rest assured script
class JavaRestAssuredScriptGenerator(JavaScriptGenerator):
    def __init__(self,headers,params,body,url):
        super().__init__(headers,params,body,url)

    def script_get(self):
        script="Response response=given()\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params

        script+="                 .when()\n" \
                "                 .get("+self.url+");"
        return script
    def script_post(self):
        script=""
        if(self.script_body):
            script=self.script_body+"\n"
        script+="Response response=given()\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+="                 .body(jsonAsMap)\n"
        script+="                 .when()\n" \
                "                 .post("+self.url+");"
        return script
    def script_put(self):
        script=""
        if(self.script_body):
            script=self.script_body+"\n"
        script+="Response response=given()\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+="                 .body(jsonAsMap)\n"

        script+="                 .when()\n" \
                "                 .put("+self.url+");"
        return script
    def script_options(self):
        script=""
        if(self.script_body):
            script=self.script_body+"\n"
        script+="Response response=given()\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+="                 .body(jsonAsMap)\n"

        script+="                 .when()\n" \
                "                 .options("+self.url+");"
        return script
    def script_delete(self):
        script=""
        if(self.script_body):
            script=self.script_body+"\n"
        script+="Response response=given()\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+="                 .body(jsonAsMap)\n"

        script+="                 .when()\n" \
                "                 .delete("+self.url+");"
        return script

#Inherits from JavaScriptGenerator class, defines the abstract methods for genertaing java Uni rest script
class JavaUniRestScriptGenerator(JavaScriptGenerator):
    def __init__(self,headers,params,body,url):
        super().__init__(headers,params,body,url)

    # Overrides the create_params method
    def create_params(self):
        if(len(self.params)==0):
            return
        self.script_params=""
        for key in self.params.keys():
            string="                 .query(\""+key+"\",\""+self.params[key]+"\")\n"
            self.script_params+=string
    # Overrides the create_body method
    def create_body(self):
        if(len(self.body)==0):
            return
        self.script_body=""
        for key in self.body.keys():
            string="                 .field(\""+key+"\",\""+self.body[key]+"\")\n"
            self.script_body+=string

    def script_get(self):
        script="HttpResponse<String> response=Unirest.get("+self.url+")\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params

        script+="                 .asString();"
        return script
    def script_post(self):
        script="HttpResponse<String> response=Unirest.post("+self.url+")\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+=self.script_body
        script+="                 .asString();"
        return script
    def script_put(self):
        script="HttpResponse<String> response=Unirest.put("+self.url+")\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+=self.script_body

        script+="                 .asString();"
        return script
    def script_options(self):
        script="HttpResponse<String> response=Unirest.options("+self.url+")\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+=self.script_body

        script+="                 .asString();"
        return script
    def script_delete(self):
        script="HttpResponse<String> response=Unirest.delete("+self.url+")\n" \
                ""+self.script_headers
        if(self.script_params):
            script+=self.script_params
        if(self.script_body):
            script+=self.script_body

        script+="                 .asString();"
        return script

#Inherits from PythonScriptGenerator class, defines the abstract methods for genertaing python requests script
class PythonRequestsScriptGenerator(PythonScriptGenerator):
    def __init__(self,headers,params,body,url):
        super().__init__(headers,params,body,url)

    def script_get(self):
        script="url = \""+self.url+"\"\n\n"+self.script_headers
        if(self.script_params):
            script+=self.script_params
        script+="response = requests.request(\"GET\",url,"
        if(self.script_params):
            script+="params=params,"
        script+="headers=headers)\n"
        return script
    def script_post(self):
        script="url = \""+self.url+"\"\n\n"+self.script_headers+self.script_body
        if(self.script_params):
            script+=self.script_params
        script+="response = requests.request(\"POST\",url,"
        if(self.script_params):
            script+="params=params,"
        script+="headers=headers,"
        if(self.script_body):
            script+="data=payload"
        script+=")\n"
        return script
    def script_put(self):
        script="url = \""+self.url+"\"\n\n"+self.script_headers+self.script_body
        if(self.script_params):
            script+=self.script_params
        script+="response = requests.request(\"PUT\",url,"
        if(self.script_params):
            script+="params=params,"
        script+="headers=headers,"
        if(self.script_body):
            script+="data=payload"
        script+=")\n"
        return script
    def script_options(self):
        script="url = \""+self.url+"\"\n\n"+self.script_headers+self.script_body
        if(self.script_params):
            script+=self.script_params
        script+="response = requests.request(\"OPTIONS\",url,"
        if(self.script_params):
            script+="params=params,"
        script+="headers=headers,"
        if(self.script_body):
            script+="data=payload"
        script+=")\n"
        return script
    def script_delete(self):
        script="url = \""+self.url+"\"\n\n"+self.script_headers+self.script_body
        if(self.script_params):
            script+=self.script_params
        script+="response = requests.request(\"DELETE\",url,"
        if(self.script_params):
            script+="params=params,"
        script+="headers=headers,"
        if(self.script_body):
            script+="data=payload"
        script+=")\n"
        return script

if __name__=='__main__':
    ui=AppUI()


