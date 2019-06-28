import os
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-f','--fake', help='run fake configuration', dest='fakeable', type=bool, default=False)
args = parser.parse_args()


def submit(year):
    if args.fakeable:
        isfake='_fr_'
    else:
        isfake=''
    if year=='2017':
        b = './cfg%s2017/' %isfake
        file_name='dataset_2017_nano_v4_new.py'
    elif year=='2018':
        b = './cfg%s2018/' %isfake
        file_name='dataset_2018_nano_v4_new.py'
    elif year=='2016':
        b = './cfg%s2016/' %isfake
        file_name='dataset_2016_nano_v4_new.py'

    handle=open(file_name,"r")
    exec(handle)
    _Samples = Samples

    for iSample in _Samples :
        file=iSample+'_cfg.py'
        os.system('crab submit -c '+b+file)
        #print('crab submit -c '+b+file)

if __name__ == '__main__':
    submit('2016')
    submit('2017')
    submit('2018')
