# courseManage

1. Install required py lib

```
pip install -r requirement_macos.txt
```

2. Modify record under file `course_record.xlsx`
![](https://github.com/easonlau02/courseManage/blob/master/temp/excel_template.png "excel_template.png")

3. for example, if you wanna generate above record, need to change below config in file `courceManage.py`
```
# generate student by phase
PHASE = 1
```

4. Run below command to generate image with student information

```
python courseManage.py
```

5. Below is the output
```
===========Start to generate image with student information=========
Total students at Phase '2' : 4
Please check ouput results in Path : '~/imageProcess/generated/2018-05-06/'
===========End to generate image with student information=========
```

6. Check file under `~/imageProcess/generated/2018-05-06/`
![Eason](https://github.com/easonlau02/courseManage/blob/master/temp/Eason.jpeg "Eason.jpeg")
![Jason](https://github.com/easonlau02/courseManage/blob/master/temp/Jason.jpeg "Jason.jpeg")
![Jim](https://github.com/easonlau02/courseManage/blob/master/temp/Jim.jpeg "Jim.jpeg")
![Kimmy](https://github.com/easonlau02/courseManage/blob/master/temp/Kimmy.jpeg "Kimmy.jpeg")
