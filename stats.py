import time
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

oled_reset = digitalio.DigitalInOut(board.D4)

WIDTH = 128
HEIGHT = 64
BORDER = 5

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_re
set)

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('Movement.ttf', 10)

while True:

    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2
}'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell = True )

    draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((0, 16), str(CPU,'utf-8') + "%", font=font, fill=255)
    draw.text((80, 16), str(temp,'utf-8') , font=font, fill=255)
    draw.text((0, 32), str(MemUsage,'utf-8'), font=font, fill=255)
    draw.text((0, 48), str(Disk,'utf-8'), font=font, fill=255)

    oled.image(image)
    oled.show()
    time.sleep(.1)
