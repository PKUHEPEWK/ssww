import os

def submit(year):
    if year=='2017':
        file_name='crab_collection2017.py'
    elif year=='2018':
        file_name='crab_collection2018.py'
    elif year=='2016':
        file_name='crab_collection2016.py'
    handle=open(file_name,"r")
    exec(handle)
    _Success = Success

    for iSample in _Success :
        hadd_all = 'haddnano.py '+iSample+'.root '
        for iiSample in _Success[iSample]:
            tmp_str=_Success[iSample][iiSample]   # dataset
            # print iSample,'   ',iiSample,'    ',tmp_str
            # tmp_str=(re.findall(r"/(.+?)/", tmp_str))[0]
            hadd_all += tmp_str+'*.root '
        os.system(hadd_all)
        # print hadd_all
        print 'successfully hadd ', iSample

if __name__ == '__main__':
    submit('2016')
    submit('2017')
    submit('2018')
