import os

def submit(year):
    if year=='2017':
        b = './cfg2017/'
        file_name='dataset_2017_nano_v4.py'
    elif year=='2018':
        b = './cfg2018/'
        file_name='dataset_2018_nano_v4.py'
    elif year=='2016':
        b = './cfg2016/'
        file_name='dataset_2016_nano_v4.py'

    handle=open(file_name,"r")
    exec(handle)
    _Samples = Samples

    for iSample in _Samples :
        file=iSample+'_cfg.py'
        os.system('crab submit -c '+b+file)
        #print('crab submit -c '+b+file)

if __name__ == '__main__':
    submit('2016')
    #submit('2017')
    #submit('2018')
