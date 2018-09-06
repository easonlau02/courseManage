from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random

class SecurityCode:
    def __init__(self, path):
        self.path = path

    def getBlur(self):
        img = Image.open(self.path)
        img2 = img.filter(ImageFilter.BLUR)

        img2.show()
    
    def rndColor(self):
        return (random.randint(64,255), random.randint(64,255), random.randint(64,255))

    def rndChar(self):
        return chr(random.randint(65, 90))

    def rndFontColor(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def getSecurityCode(self):
        width, height = 60*4, 60
        img = Image.new('RGB', (width, height), (255,255,255))

        font = ImageFont.truetype('arial.ttf', 36)

        draw = ImageDraw.Draw(img)

        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=self.rndColor())

        for t in range(4):
            draw.text((60 * t + 10, 10), self.rndChar(), font=font, fill=self.rndFontColor())

        img.filter(ImageFilter.BLUR).show()

sc = SecurityCode(path='./template/template_boy.jpeg')
sc.getSecurityCode()
