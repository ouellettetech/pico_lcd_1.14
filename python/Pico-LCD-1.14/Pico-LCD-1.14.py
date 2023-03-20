from machine import Pin,SPI,PWM
import framebuf
import time

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240 
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
  
if __name__=='__main__':
    currentMenuItem=0
    numMenuItems=4
    lastButton=-1

    def drawMenu():
        LCD.text("Main Menu",90,40,LCD.green)
        LCD.text("Select Profile",90,60,LCD.green)
        LCD.text("...",90,80,LCD.green)
        LCD.text("Start!",90,100,LCD.green)
    
    
        LCD.text("OK",210,15,LCD.white)
        LCD.text("BACK",195,110,LCD.white)

    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    #color BRG
    LCD.fill(LCD.black)
 
    LCD.show()
    drawMenu()
    
    
    
    
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)

    
    LCD.show()
    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)#UP
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)#CENTER
    key4 = Pin(16 ,Pin.IN,Pin.PULL_UP)#LEFT
    key5 = Pin(18 ,Pin.IN,Pin.PULL_UP)#DOWN
    key6 = Pin(20 ,Pin.IN,Pin.PULL_UP)#RIGHT
    
    while(1):
        if(keyA.value() == 0):
            if(lastButton != 0):
                LCD.rect(208,12,20,20,LCD.green)
                print("A")
                lastButton = 0
        else :
            if(lastButton == 0 ):
                lastButton = -1
            LCD.rect(208,12,20,20,LCD.white)
            
            
        if(keyB.value() == 0):
            if(lastButton != 1):
                LCD.rect(193,103,35,20,LCD.green)
                print("B")
                lastButton = 1
        else :
            if(lastButton == 1):
                lastButton = -1
            LCD.rect(193,103,35,20,LCD.white)
    
        if(key2.value() == 0):#上
            if(lastButton != 2):
                LCD.fill_rect(37,35,20,20,LCD.red)
                print("UP")
                currentMenuItem-=1
                currentMenuItem=currentMenuItem%numMenuItems
                print(currentMenuItem)
                lastButton = 2
        else :
            if(lastButton == 2):
                lastButton = -1
            LCD.fill_rect(37,35,20,20,LCD.white)
            LCD.rect(37,35,20,20,LCD.red)
            
            
        if(key3.value() == 0):#中
            if(lastButton != 3):
                LCD.fill_rect(37,60,20,20,LCD.red)
                print("CTRL")
                lastButton = 3
        else :
            if(lastButton == 3):
                lastButton = -1
            LCD.fill_rect(37,60,20,20,LCD.white)
            LCD.rect(37,60,20,20,LCD.red)
            
        

        if(key4.value() == 0):#左
            if(lastButton != 4):
                LCD.fill_rect(12,60,20,20,LCD.red)
                print("LEFT")
                lastButton = 4
        else :
            if(lastButton == 4):
                lastButton = -1
            LCD.fill_rect(12,60,20,20,LCD.white)
            LCD.rect(12,60,20,20,LCD.red)
            
            
        if(key5.value() == 0):#下
            if(lastButton != 5):
                LCD.fill_rect(37,85,20,20,LCD.red)
                print("DOWN")
                currentMenuItem+=1
                currentMenuItem=currentMenuItem%numMenuItems
                print(currentMenuItem)
                lastButton = 5
        else :
            if(lastButton == 5):
                lastButton = -1
            LCD.fill_rect(37,85,20,20,LCD.white)
            LCD.rect(37,85,20,20,LCD.red)
            
            
        if(key6.value() == 0):#右
            if(lastButton != 6):
                LCD.fill_rect(62,60,20,20,LCD.red)
                print("RIGHT")
                lastButton = 6
        else :
            if(lastButton == 6):
                lastButton = -1
            LCD.fill_rect(62,60,20,20,LCD.white)
            LCD.rect(62,60,20,20,LCD.red)

            
        LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)

