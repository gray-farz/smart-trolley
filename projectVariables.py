class ProjectVariables(object):
    
	################################################	DATABASE FILE PATHS
    pathImageBackgroundTabs='/home/pi/myProjects/smartTerroli/tabs'
    pathDoneBuysTables = "/home/pi/myProjects/smartTerroli/databases/doneBuysTables"
    pathDoneBuysNames = "/home/pi/myProjects/smartTerroli/databases/DoneBuysNames"
    pathAllUsersDatabase="/home/pi/myProjects/smartTerroli/databases/allUsersDatabase"
	
	############### STOCK DATABASE PATH IN MANAGER AND TERROLIES DEVICES
	PathStockInSource ="/home/pi/myProjects/smartTerroli/stock/stockDatabase.db"
	PathStockInDestination = "/home/pi/myProjects/smartTerroli/stock/"
	StockFileNameInDestination ="stockDatabase.db"
	
	############### CUSTOMORS DATABASE PATH IN MANAGER AND TERROLIES DEVICES
	PathCustomorDatabaseInManagerDevice="/home/pi/myProjects/smartTerroli/customors/"
	PathCustomorDatabaseInTerroliesDevice="/home/pi/myProjects/smartTerroli/customors/customors.db"
	FileNameCustomorDatabaseInManagerDevice="customors.db"
	FileCustomorDatabaseInManagerDevice=PathCustomorDatabaseInManagerDevice+FileNameCustomorDatabaseInManagerDevice
	
	#################################################		SQLITE CONNECTION AND CURSOR
    connStockDatabase = sqlite3.connect(PathStockInSource,check_same_thread=False)
    cursorStockDatabase = connStockDatabase.cursor()
	
	ConnCustomorsDatabase = sqlite3.connect(FileCustomorDatabaseInManagerDevice,check_same_thread=False)
	ConnCustomorsDatabaseCursor = ConnCustomorsDatabase.cursor()
	ConnCustomorsDatabaseCursor.execute('''CREATE TABLE if not exists customors(name stringvar,phone stringvar,nationalCode stringvar,nationalCardBarcode stringvar)''')
	
	
	USERIPs = ["192.168.0.201","192.168.0.202","192.168.0.205"]
	
	bgcolor='white'
    font_name='Helvetica'
    font_size=22
	
	USERNAME = "pi"
	PASSWORD= "raspberry"
	PORT=22



        
