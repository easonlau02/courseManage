#-*- coding:utf-8 -*-
import pandas as pd
import os, time

from PIL import ImageDraw, Image, ImageFont

FILLING = 500
COLOR = 120,0,0
ROOT_FOLDER = os.getcwd()
IMAGE_PATH_BOY = ROOT_FOLDER + "/template/template_boy.jpeg"
IMAGE_PATH_GIRL = ROOT_FOLDER + "/template/template_girl.jpeg"
# FONT_STYLE="/System/Library/Fonts/Monaco.dfont"
FONT_STYLE = "/System/Library/Fonts/PingFang.ttc"
GENERATED_ROOT = ROOT_FOLDER+'/generated/'
V_OFFSET = 140
H_OFFSET = 500

FONT_SIZE=95
GLOBAL_D_WIDTH, GLOBAL_D_HEIGHT = 230,145

# excel
EXCEL_PATH = ROOT_FOLDER+"/course_record.xlsx"
# excel sheet to load by sheet name
SHEET_NAME = 'sheet2'
# generate student by phase
PHASE=2


class CourseManage:
    def __init__(self,excel_path,sheet_name,phase):
        self.phase = phase
        self.sheet_name = sheet_name
        self.excel_path = excel_path
        #read course_record
        self.df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    # geta printable dataset with params @phase
    def getDataSet(self):
        if self.df.empty:
            return None
        if self.phase is not None:
            dataSet = self.df[self.df['Phase']==self.phase]
            return dataSet
        else:
            return self.df

    # get default header from xlsx
    def getHeader(self):
        if self.df.empty == False:
            return self.df.columns
        else:
            return []

    def getFolderWithDate(self):
        currentDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        folderName = currentDate
        index = 1
        while currentDate and os.path.exists(GENERATED_ROOT+folderName):
            folderName = currentDate + '_'+str(index)
            index += 1
        
        fullPath = GENERATED_ROOT+folderName + '/'
        os.mkdir(fullPath)
        return fullPath

    def process(self):
        print('===========Start to generate image with student information=========')
        fullPath = self.getFolderWithDate()
        font = ImageFont.truetype(FONT_STYLE,FONT_SIZE)
        dataSet = self.getDataSet()
        if hasattr(dataSet,'empty') and dataSet.empty == False:
            size,_ = dataSet.shape
            print('Total students at Phase \''+str(self.phase)+'\' : '+str(size))
            # open Image
            image_template = IMAGE_PATH_BOY

            for _, rowData in dataSet.iterrows():
                d_width, d_height = GLOBAL_D_WIDTH,GLOBAL_D_HEIGHT
                sex = rowData['Sex']
                if sex is not None:
                    if sex == 1:
                        image_template = IMAGE_PATH_BOY
                    else:
                        image_template = IMAGE_PATH_GIRL
                img = Image.open(image_template)
                draw = ImageDraw.Draw(img)

                for k,v in rowData.items():
                    if type(k) != int:
                        k = k.encode('utf-8')
                    if type(v) != int:
                        v = v.encode('utf-8')
                    if k == 'Phase' or k == 'Sex':
                        continue
                    c_width = d_width
                    # inset Key
                    draw.text((c_width,d_height),  k.decode('utf-8') if type(k) != int else str(k), COLOR, font=font)
                    # inset value
                    c_width += H_OFFSET
                    draw.text((c_width, d_height), v.decode('utf-8') if type(v) != int else str(v)  , COLOR, font=font)
                    d_height += V_OFFSET

                # img.show()
                _, extension = os.path.splitext(image_template)
                new_filename = rowData[rowData.keys()[2]]
                img.save(fullPath+new_filename+extension)
            print('Please check ouput results in Path : \''+fullPath+'\'')
        else:
            print('Total students at Phase '+str(self.phase)+' : '+str(0))
            print('No result ouput.')
        print('===========End to generate image with student information=========')
                

imgp=CourseManage(EXCEL_PATH,sheet_name=SHEET_NAME,phase=PHASE)
imgp.process()