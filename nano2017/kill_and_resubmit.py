import os
import re
import shutil
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-s','--sample', help='kill and resubmit which sample',nargs='*')

args = parser.parse_args()

if __name__ == '__main__':
    # print args.sample

    for i in range(0,len(args.sample)):
        os.system('crab kill -d ' + args.sample[i])
        shutil.rmtree(args.sample[i])
        if '2016' in args.sample[i]:
            os.system('crab submit -c ./cfg2016/'+args.sample[i][5:len(args.sample[i])-5]+'_cfg.py')
        elif '2017' in args.sample[i]:
            os.system('crab submit -c ./cfg2017/'+args.sample[i][5:len(args.sample[i])-5]+'_cfg.py')
        elif '2018' in args.sample[i]:
            os.system('crab submit -c ./cfg2018/'+args.sample[i][5:len(args.sample[i])-5]+'_cfg.py')
        else:
            pass

'''
crab_ZZTo2L2Q_2016
crab_TTWJetsToQQ_2016 
crab_TTZToLLNuNu_M-10_ext3_2016
crab_WZTo3LNu_3Jets_MLL-50_2016
crab_DYJetsToLL_Pt-650ToInf_2016
'''