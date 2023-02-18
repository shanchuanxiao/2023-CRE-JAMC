# 2023-CER-JAMC
This repository provides important support for a research paper submitted to Journal of Applied Meteorology and Climatology (JAMC) entitled “A Long-term experiment on the cooling effects of three high albedo materials in Nanjing, China”

## original_data
1、The original radiation four-component data is minute data, and one copy is stored in excel format for direct viewing and feather binary data for easy reading;  
2、Daily precipitation data of Nanjing Station from 2017 to 2020;  
3、However the original excel and feather exceed github upload file size, so cannot be uploaded;  

## after_processing
Data obtained after the original minute data processing, 30min average, including excel and feather format, convenient viewing and Python reading respectively.  

## excel_feather.py
Python code to convert raw excel data to feather format  
  1. Integrated the data of all time;  
  2. Each material is stored separately as a feather format data;  
  3. All four materials are stored in the same excel;  
  4. Delete the time when all four components of radiation are missing measurement;  

## time_processing.py
Re-sample the original data and calculate the 30min average (forward average)  
00:30 included (00:00, 00:30], 01:00 included (00:30,01:00), 01:00 Included (01:00, 02:00)
01 00:00:00 Includes (00 00:00:00, 01 00:00:00)  
02-01 00:00:00 Includes (01-01 00:00:00, 02-01 00:00:00)  
1. Before averaging, quality control should be carried out on the original data;  
  a. Set the shortwave radiation value less than 5 as 0, missing measurement;  
  b. Downward short-wave radiation will be emitted. DR And UR are set as nan at the moment of upward shortwave radiation UR, missing test.  


