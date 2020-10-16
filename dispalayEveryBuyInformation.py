from projectVariables import ProjectVariables
from PIL import Image, ImageTk
import PIL.Image

class DisplayEveryBuyInformation():
    def __init__(self,master,buyInfFromDatabase):
        self.master=master
        self.master.geometry('1100x900+20+10')
        
        self.image = Image.open("/home/pi/Downloads/images/ebrahim/rangi.jpg")
        self.img_copy= self.image.copy()
        self.image = self.img_copy.resize((790, 460))     ###(x,y)
        self.background_image = ImageTk.PhotoImage(self.image)
        
        self.canvas_root = Canvas(self.master)
        self.canvas_root.pack(anchor = NW,fill=BOTH, expand=YES)
        x=self.canvas_root.create_image(400, 200, image=self.background_image)

        self.text_canvas=[]
        j=0
        for j in range(len(buyInfFromDatabase)):
            self.text_canvas=[]
            for i in range(len(buyInfFromDatabase[j])):
                self.text_canvas.append(self.canvas_root.create_text(100+i*90,200+j*90,anchor=E))
                self.canvas_root.itemconfig(self.text_canvas[i],text=buyInfFromDatabase[j][i],font=(ProjectVariables.font_name,ProjectVariables.font_size-5))
            

