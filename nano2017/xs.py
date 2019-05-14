import os
import re

def submit(year):
    if year=='2017':
        file_name='dataset_2017_nano_v4.py'
    elif year=='2018':
        file_name='dataset_2018_nano_v4.py'
    elif year=='2016':
        file_name='xs_2016_nano_v4.py'
    initial_path='/home/pku/xiaoj/nano'+year+'/'
    handle=open(file_name,"r")
    tmp=open('xs_list_'+year+'.txt', "w")
    exec(handle)
    _Samples = Samples

    for iSample in _Samples :
        tmp_str=_Samples[iSample]['xs']   # dataset
        #print tmp_str
        tmp.write(iSample+'.root '+tmp_str+'\n')

if __name__ == '__main__':
    submit('2016')
    #submit('2017')
    #submit('2018')
