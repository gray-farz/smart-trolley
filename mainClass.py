from projectVariables import ProjectVariables
from dispalayEveryBuyInformation import DisplayEveryBuyInformation
from sshGroupConnection import SSHGroupConnection
from PIL import Image, ImageTk
import PIL.Image


class MainClass(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        global notbook,frame1,frame2,frame3,canvasMainClass,DoneBuysList,rootWaitForTransfer;
        
        self.master=master
        self.master.title('class manage')
        
        self.designStyle()
        self.creatTabs()
		self.creatButtons();
        self.defineCompletedBuysList()

        #################### THREADS
        self.master.after(100, self.checkNewDoneBuys)
        self.master.after(2000, self.checkStock)
		
	def creatButtons():
        imageButtons=[]
        imageButtonsCopy=[]
        imageButtonsArray=[]
        imageOnCanvasArray=[]
        for i in range(2):
            adad='a'+str(i)+'.png'
            imageButtons.append(Image.open('/home/pi/Downloads/images/modir-images/buttons/icons/'+adad))
            imageButtonsCopy.append(imageButtons[i].copy())
            imageButtonsArray.append(ImageTk.PhotoImage(imageButtons[i]))
            imageOnCanvasArray.append(self.canvas_tables.create_image(400+(i*150),600,image=imageButtonsArray[i],tags=i))
            canvasMainClass.tag_bind(imageOnCanvasArray[i],'<ButtonPress-1>',self.ButtonsActions)
			
	def ButtonsActions(self,event):
        sign=event.widget.find_closest(event.x, event.y)
        tags = canvasMainClass.itemcget(sign, "tags")    
        button_id=tags[0]
        if(button_id=='1'):
            self.raiseWaitWindow()
			_thread.start_new(self.transferDatabasesToAllNetworkDevices,())	
			
	def transferDatabasesToAllNetworkDevices(self):	
        
		##### SEND STOCK DATABASE FROM MANAGER DEVICE TO ALL DEVICES(TERROLIES)
		SSHGroupConnection.putToMultipleDevice(ProjectVariables.USERIPs,ProjectVariables.PathStockInSource,ProjectVariables.PathStockInDestination,ProjectVariables.StockFileNameInDestination)
        
		##### GET CUSTOMERS THAT HAVE BEEN REGISTERED RECENTLY IN TERROLIES
		SSHGroupConnection.getFromMultipleDevice(ProjectVariables.USERIPs,ProjectVariables.PathCustomorDatabaseInTerroliesDevice,ProjectVariables.PathCustomorDatabaseInManagerDevice,ProjectVariables.FileNameCustomorDatabaseInManagerDevice)
         
        ##### ADD NEW CUSTOMORS TO LAST CSTOMORS TABLE IN MANAGER DEVICE
		self.addNewCustomorsToDatabaseFromTerroliesDatabase()
						
		######	SEND UPDATED CUSTOMORS TO ALL DEVICES(TERROLIES)			
		SSHGroupConnection.putToMultipleDevice(ProjectVariables.USERIPs,ProjectVariables.FileCustomorDatabaseInManagerDevice,ProjectVariables.PathCustomorDatabaseInTerroliesDevice,ProjectVariables.FileNameCustomorDatabaseInManagerDevice)
  
        rootWaitForTransfer.destroy()

	def addNewCustomorsToDatabaseFromTerroliesDatabase():
	    projectVariables.ConnCustomorsDatabaseCursor.execute('SELECT * FROM customors')        
        rowsCustomorManager = projectVariables.ConnCustomorsDatabaseCursor.fetchall()
            
        for i in range(len(host_user)):
            customorTableNameInTerroliDevice=ProjectVariables.PathCustomorDatabaseInManagerDevice+'customors'+str(i+1)+'.db'
			connCustomorTerroli = sqlite3.connect(customorTableNameInTerroliDevice,check_same_thread=False)
            connCustomorTerroliCursor = conncustomorTerroli.cursor()
            connCustomorTerroliCursor.execute('SELECT * FROM customors')        
            rowsCustomorTerroli= connCustomorTerroliCursor.fetchall()
			
			for i in range(len(rowsCustomorTerroli)):
				for j in range(len(rowsCustomorManager)):
				
					####### ignore new customor if nationalcode or natinalcard barcode is repetitive(it has already been registered)
					if(rowsCustomorManager[i][2]==rowsCustomorTerroli[j][2] or rowsCustomorManager[i][3]==rowsCustomorTerroli[j][3])
						break
						
					else:
                        projectVariables.ConnCustomorsDatabaseCursor.execute("INSERT INTO customors(name, phone,codemeli,barcode_eng,barcode_farsi ) VALUES (?,?,?,?,?)",(rowsCustomorTerroli[j][0], rowsCustomorTerroli[j][1],rowsCustomorTerroli[j][2],rowsCustomorTerroli[j][3],rowsCustomorTerroli[j][4]))
                        projectVariables.ConnCustomorsDatabaseCursor.commit()
	
		
	def raiseWaitWindow():
        rootWaitForTransfer=Toplevel(self.master)
        rootWaitForTransfer.geometry('900x500+80+320')
        wait = AnimatedGIF(rootWaitForTransfer,"/home/pi/Downloads/images/modir-images/tenor3.gif")
        wait.pack(side='top')	

    def checkNewDoneBuys(self):
        content_folder=os.listdir(ProjectVariables.pathDoneBuysNames)
        for i in range(len(content_folder)):
            NewBuyFile=dest+'/'+content_folder[i]
            inputt = open(NewBuyFile)
            words=[]
            for line in inputt:
                for spacee in line.split():
                   words.append(spacee)
            if(len(words)==2):
                DoneBuysList.insert(END,str(words[1])+'buy number ')
  
            inputt.close()
            os.remove(NewBuyFile)
        self.master.after(100, self.checkNewDoneBuys)
        

    def checkStock(self):
	
            content_folder=os.listdir(ProjectVariables.pathAllUsersDatabase)            
            if(content_folder!=[]):
                for i in range(len(content_folder)):
                    
                    pathOneUserDatabase=ProjectVariables.pathAllUsersDatabase+'/'+content_folder[i]
                    
					allBuysTablesInOneUserDatabase = self.searchallBuysTablesInOneUserDatabase(pathOneUserDatabase)
                    for i in range(len(allBuysTablesInOneUserDatabase)):
                        name_table=allBuysTablesInOneUserDatabase[i][0]
                        if(name_table!='variabless'): 
							cursorOneUserDatabase.execute('SELECT * FROM {}'.format(name_table))        
							contentOneBuy= cursorOneUserDatabase.fetchall()
							self.subtractFromStock(contentOneBuy)            
                    os.remove(pathOneUserDatabase)           
            
            self.master.after(2000, self.checkStock) 

	def subtractFromStock(self,buy):
		for i in range(len(buy)):
			ProjectVariables.connStockDatabase.execute("SELECT remainAmount FROM food where kalaname='" + buy[i][3] + "' UNION SELECT remainAmount FROM dress where kalaname='" + buy[i][3] + "' UNION SELECT remainAmount FROM makeup where kalaname='" + buy[i][3] + "' UNION SELECT remainAmount FROM plastic where kalaname='" + buy[i][3] + "'")
			remainAmountOfOneProduct=ProjectVariables.connStockDatabase.fetchall()
			FinalremainAmountOfOneProduct=int(remainAmountOfOneProduct[0][0])-int(buy[i][2])
			
			c.execute("UPDATE food SET remainAmount='" + str(FinalremainAmountOfOneProduct) + "' WHERE kalaname='" + buy[i][3] + "'")
			c.execute("UPDATE dress SET remainAmount='" + str(FinalremainAmountOfOneProduct) + "' WHERE kalaname='" + buy[i][3] + "'")
			c.execute("UPDATE makeup SET remainAmount='" + str(FinalremainAmountOfOneProduct) + "' WHERE kalaname='" + buy[i][3] + "'")
			c.execute("UPDATE plastic SET remainAmount='" + str(FinalremainAmountOfOneProduct) + "' WHERE kalaname='" + buy[i][3] + "'")
			ProjectVariables.connStockDatabase.commit()	

    def searchallBuysTablesInOneUserDatabase(self,path):
		connOneUserDatabase = sqlite3.connect(path,check_same_thread=False)
		cursorOneUserDatabase = connOneUserDatabase.cursor()
		cursorOneUserDatabase.execute("SELECT name FROM sqlite_master WHERE type='table';")
		fetch=cursorOneUserDatabase.fetchall()
		return fetch
	
	def defineCompletedBuysList(self):

        fram_lis=Frame(self.master,bg=ProjectVariables.bgcolor)
        canvasMainClass.create_window(863, 443, window=fram_lis,anchor=CENTER)
 
        scrollbar = Scrollbar(fram_lis)
        scrollbar.pack(side=RIGHT, fill=Y)

        DoneBuysList = Listbox(fram_lis,width=25,height=28)
        DoneBuysList.pack()

        # attach listbox to scrollbar
        DoneBuysList.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=DoneBuysList.yview)

        DoneBuysList.bind('<<ListboxSelect>>', self.bindOnDoneBuysList)

    def bindOnDoneBuysList(self):
        index = modifiedItemsList.index(modifiedItemsList.curselection())
        value = modifiedItemsList.get(index)
        self.show_information(value)

    def show_information(self,value):
        number=value.split(' ')
        self.table_name='buy'+str(number[0])
        content_folder=os.listdir(ProjectVariables.pathDoneBuysTables)
        if(content_folder!=[]):
            for i in range(len(content_folder)):
                check_file=ProjectVariables.pathDoneBuysTables+'/'+content_folder[i]
                connBuysTables = sqlite3.connect(check_file,check_same_thread=False)
                cursorBuysTables = connBuysTables.cursor()
                try:
                    cursorBuysTables.execute('SELECT * FROM {}'.format(self.table_name))        
                    boughtItemsList = c3.fetchall()

                except:
                    pass
        root_information=Toplevel(self.master)
        gui_inform=DisplayEveryBuyInformation(root_information,boughtItemsList)
        root_information.after(2500, lambda: root_information.destroy()) # Destroy the widget after 30 seconds


    def designStyle(self):
        
        styleManage = ttk.Style()
        styleManage.configure('mayor.TNotebook',background=ProjectVariables.bgcolor)
        styleManage.configure('mayor.TNotebook.Tab', background ='#0081ce',font=('Helvetica', 16,'bold'))

    def creatTabs(self):
        backgroundTabs = ttk.Notebook(self.master,style='mayor.TNotebook', width=1200, height=750)
        backgroundTabs.pack()

        frame1 = Frame(backgroundTabs,background=ProjectVariables.bgcolor)   
        frame2 = Frame(backgroundTabs,background=ProjectVariables.bgcolor)   
        frame3 = Frame(backgroundTabs,background=ProjectVariables.bgcolor)

        frame1.pack()
        frame2.pack()
        frame3.pack()

        self.image_tabs=[]
        self.img_copy_tabs=[]
        self.back_image_tabs=[]
        for i in range(3):
            adad='a'+str(i)+'.png'
            image_tabs.append(Image.open(ProjectVariables.pathImageBackgroundTabs+adad))
            img_copy_tabs.append(image_tabs[i].copy())
            back_image_tabs.append(ImageTk.PhotoImage(image_tabs[i]))

        backgroundTabs.add(frame1, text='main menu',image=back_image_tabs[0])
        backgroundTabs.add(frame2, text='basic inf',image=back_image_tabs[1])
        backgroundTabs.add(frame3, text='terrolies',image=back_image_tabs[2])

