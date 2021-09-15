import sys
import utime
import urandom
import machine
from machine import Pin, Signal, PWM, ADC, I2C
import driver_i2clcd1602

# VARIABLE DEFINE
USERINPUT=""
RANDOMNUM=0
COMPUTERINPUT=""
# 1000 ~ 1800 : button01
# 1800 ~ 2500 : button02
# 2500 ~ 3400 : button03
# 3500 ~ 4095 : button04

# GPIO DEFINE
pin_buttonlist=ADC(Pin(36, Pin.IN))
pin_servo01=PWM(Pin(4, Pin.OUT), freq=50 )
pin_servo02=PWM(Pin(2, Pin.OUT), freq=50 )
pin_servo03=PWM(Pin(27, Pin.OUT), freq=50 )

# GPIO INIT
pin_buttonlist.atten(ADC.ATTN_11DB)
pin_buttonlist.width(ADC.WIDTH_12BIT)
i2c = I2C(1, sda=Pin(21), scl=Pin(22))

pin_servo01.duty(120)
pin_servo02.duty(120)
pin_servo03.duty(120)


# DRIVER INIT
addreesslist=i2c.scan() # list
I2C_ADDR = int(addreesslist[0]) #0x27
lcd = driver_i2clcd1602.I2CLCD1602(i2c, addr=I2C_ADDR)
lcd.on()

while True :
    # START
    lcd.clear()
    lcd.puts("GAME START",0,0)
    lcd.puts("R ! S ! P !",0,1)

    while True :
        if pin_buttonlist.read() >= 1000 and pin_buttonlist.read() <= 1800 :
            break
        utime.sleep(0.1)
        
    lcd.clear()
    lcd.puts("Your Choose",0,0)
    lcd.puts("R:2 / S:3 / S:4",0,1)

    # USER INPUT
    while True :
        if pin_buttonlist.read() >= 1800 and pin_buttonlist.read() <= 2500 :
            USERINPUT="ROCK"
            break
        elif pin_buttonlist.read() >= 2500 and pin_buttonlist.read() <= 3400 :
            USERINPUT="SCISSOR"
            break
        elif pin_buttonlist.read() >= 3500 and pin_buttonlist.read() <= 4095 :
            USERINPUT="PAPER"
            break
        utime.sleep(0.1)

    # COMPUTER INPUT
    RANDOMNUM=urandom.randrange(1,4)
    if RANDOMNUM == 1 :
        COMPUTERINPUT="ROCK"
    elif RANDOMNUM == 2 :
        COMPUTERINPUT="SCISSOR"
    elif RANDOMNUM == 3 :
        COMPUTERINPUT="PAPER"

    lcd.clear()
    lcd.puts("Computer Choosing",0,0)

    temp=0
    while temp < 2 :
        temp +=1
        lcd.puts("Wating Please"+str(temp),0,1)
        utime.sleep(1)
        
    if COMPUTERINPUT == "ROCK" :
        pin_servo01.duty(75)
    elif COMPUTERINPUT == "SCISSOR" :
        pin_servo02.duty(75)
    elif COMPUTERINPUT == "PAPER" :
        pin_servo03.duty(75)

    # RESULT
    utime.sleep(1)

    lcd.clear()
    if USERINPUT == COMPUTERINPUT :
        lcd.puts("RESULT : DROW",0,0)
    elif USERINPUT == "ROCK" and COMPUTERINPUT == "SCISSOR" :
        lcd.puts("RESULT : WIN",0,0)
    elif USERINPUT == "SCISSOR" and COMPUTERINPUT == "PAPER" :
        lcd.puts("RESULT : WIN",0,0)
    elif USERINPUT == "PAPER" and COMPUTERINPUT == "ROCK" :
        lcd.puts("RESULT : WIN",0,0)
    elif USERINPUT == "ROCK" and COMPUTERINPUT == "PAPER" :
        lcd.puts("RESULT : LOSE",0,0)
    elif USERINPUT == "SCISSOR" and COMPUTERINPUT == "ROCK" :
        lcd.puts("RESULT : LOSE",0,0)
    elif USERINPUT == "PAPER" and COMPUTERINPUT == "SCISSOR" :
        lcd.puts("RESULT : LOSE",0,0)  
    lcd.puts("U:"+USERINPUT+"/C:"+COMPUTERINPUT,0,1)    

    utime.sleep(3)
    pin_servo01.duty(120)
    pin_servo02.duty(120)
    pin_servo03.duty(120)
    continue

pin_servo01.deinit()
pin_servo02.deinit()
pin_servo03.deinit()

