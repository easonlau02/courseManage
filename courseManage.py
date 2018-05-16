#-*- coding:utf-8 -*-
import os
import time

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from math import isnan

FILLING = 500
COLOR = 120,0,0
ROOT_FOLDER = os.getcwd()
IMAGE_PATH_BOY = ROOT_FOLDER + "/template/template_boy.jpeg"
IMAGE_PATH_GIRL = ROOT_FOLDER + "/template/template_girl.jpeg"
# FONT_STYLE="/System/Library/Fonts/Monaco.dfont"
FONT_STYLE_MAC = "/System/Library/Fonts/PingFang.ttc"
FONT_STYLE_WIN = ''
FONT_STYLE_LINUX = ''
GENERATED_ROOT = ROOT_FOLDER+'/generated/'
V_OFFSET = 140
H_OFFSET = 500

FONT_SIZE=95
GLOBAL_D_WIDTH, GLOBAL_D_HEIGHT = 230,145

# excel
EXCEL_PATH = ROOT_FOLDER + "/course_record.xlsx"
# excel sheet to load by sheet name
SHEET_NAME = 'sheet2'
# generate student by phase
PHASE=2

class CourseManage:
    # initialize
    def __init__(self,excel_path,sheet_name,phase):
        self.phase = phase
        self.sheet_name = sheet_name
        self.excel_path = excel_path
        #read course_record
        self.df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    # get font
    def getFont(self):
        import platform as pf
        sysver = pf.system()

        if sysver is None:
            return FONT_STYLE_MAC
        if sysver.upper() == 'DARWIN':
            return FONT_STYLE_MAC
        elif sysver.upper() == 'LINUX':
            return FONT_STYLE_LINUX
        elif sysver.upper() == 'WINDOWS':
            return FONT_STYLE_WIN

    # geta printable dataset with params @phase
    def getDataSet(self):
        if self.df.empty:
            return None
        if self.phase is not None:
            dataSet = self.df[self.df['Phase']==self.phase]
            return dataSet
        else:
            return self.df

    # get default header from xlsxr
    def getHeader(self):
        if self.df.empty == False:
            return self.df.columns
        else:
            return []
    # get new folder for pic generating
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
    
    # get template
    def getImageTemplateBySex(self, sex):
        image_template = IMAGE_PATH_BOY
        if sex is not None:
            if sex == 1:
                image_template = IMAGE_PATH_BOY
            else:
                image_template = IMAGE_PATH_GIRL
        return image_template

    # process pic with student informaion based on excel EXCEL_PATH
    def process(self):
        print('===========Start to generate image with student information=========')
        fullPath = self.getFolderWithDate()
        print(self.getFont())
        font = ImageFont.truetype(self.getFont(),FONT_SIZE)
        dataSet = self.getDataSet()
        if hasattr(dataSet,'empty') and dataSet.empty == False:
            size,_ = dataSet.shape
            print('Total students at Phase \''+str(self.phase)+'\' : '+str(size))
            # open Image
            image_template = ''

            for _, rowData in dataSet.iterrows():
                d_width, d_height = GLOBAL_D_WIDTH,GLOBAL_D_HEIGHT
                
                # Get template
                image_template = self.getImageTemplateBySex(rowData['Sex'])
                
                img = Image.open(image_template)
                draw = ImageDraw.Draw(img)

                for k,v in rowData.items():
                    if type(v) == float and isnan(v):
                        v = ''
                        
                    if k == 'Phase' or k == 'Sex':
                        continue
                    if type(k) != int and type(v) != float:
                        k = k.encode('utf-8')
                    if type(v) != int and type(v) != float:
                        v = v.encode('utf-8')
                    
                    c_width = d_width
                    # inset Key
                    draw.text((c_width,d_height),  k.decode('utf-8') if k and type(k) != int and type(k) != float else str(k), COLOR, font=font)
                    # inset value
                    c_width += H_OFFSET
                    draw.text((c_width, d_height), v.decode('utf-8') if v and type(v) != int and type(v) != float else str(v)  , COLOR, font=font)
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
