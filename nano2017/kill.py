import os
import commands

def submit(year):
    if year=='2017':
        file_name='dataset_2017_nano_v4.py'
    elif year=='2018':
        file_name='dataset_2018_nano_v4.py'
    elif year=='2016':
        file_name='dataset_2016_nano_v4_new.py'


    handle=open(file_name,"r")
    exec(handle)
    _Samples = Samples

    for iSample in _Samples :
        file='crab_'+iSample+'_'+year
        #print(file)
        #a,b=commands.getstatusoutput('crab status -d '+file)
        os.system('crab kill -d '+file)
        #print('crab kill -d '+file)
        #print a
        #print b

if __name__ == '__main__':
    submit('2016')
    #submit('2017')
    #submit('2018')
