import os
import re

def submit(year):
    if year=='2017':
        file_name='dataset_2017_nano_v4.py'
    elif year=='2018':
        file_name='dataset_2018_nano_v4.py'
    elif year=='2016':
        file_name='dataset_2016_nano_v4.py'
    initial_path='/home/pku/xiaoj/nano'+year+'/'
    handle=open(file_name,"r")
    tmp=open('hadd_list_'+year+'.sh', "w")
    exec(handle)
    _Samples = Samples

    for iSample in _Samples :
        for iiSample in _Samples[iSample]:
            tmp_str=_Samples[iSample][iiSample]   # dataset
            tmp_str=(re.findall(r"/(.+?)/", tmp_str))[0]
            tmp_str='haddnano.py '+iSample+'.root '+initial_path+tmp_str+'/'+iSample+'/'+'19*/0000/*.root'
            print tmp_str
            tmp.write(tmp_str+'\n')

if __name__ == '__main__':
    submit('2016')
    #submit('2017')
    #submit('2018')
