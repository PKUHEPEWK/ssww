import os
import re
import shutil
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--year', help='run over which year', dest='chosenyear', default = '2022')
parser.add_argument('--mode', help='original mode and simplified mode', dest='mode', default='simplified')
args = parser.parse_args()

path = '/pnfs/ihep.ac.cn/data/cms/store/user/jixiao/'
version = '_v0/'


def remove_text(a, year):
    with open('crab_collection' + year + '.py', 'r') as f:
        lines = []  # empty list
        for line in f.readlines():
            lines.append(line)
    with open('crab_collection' + year + '.py', 'w') as f:
        for line in lines:
            if not (a in line):
                f.write('%s' % line)


def status(year):
    if year == '2017':
        file_name = 'dataset_2017_nano_v4_new.py'
    elif year == '2018':
        file_name = 'dataset_2018_nano_v4_new.py'
    elif year == '2016':
        file_name = 'dataset_2016_nano_v4_new.py'

    handle = open(file_name, "r")
    exec (handle)
    _Samples = Samples

    if not os.path.exists('crab_collection' + year + '.py'):
        collect = open('crab_collection' + year + '.py', "a+")
        collect.write('Success = {} \n')
        collect.close()
    else:
        pass

    for iSample in _Samples:
        with open('crab_collection' + year + '.py', 'r') as collect:
            exec (collect)
            _Success = Success
        file = 'crab_' + iSample + '_' + year
        try:
            process = _Samples[iSample]['nanoAOD']
        except KeyError:
            process = _Samples[iSample]['nanoAODSIM']
        process = re.findall(r"/(.+?)/", process)
        if '_ext' in iSample:
            sample_name = iSample[:len(iSample) - 5]
        else:
            sample_name = iSample

        try:
            _Success[sample_name][iSample]
        except KeyError:
            pass
        except ValueError:
            pass
        else:
            continue
        if args.mode == 'simplified':
            p = os.popen('crab status -d ' + file)
            pp = p.read()
            # pp = 'COMPLETED'
            try:
                pp.index('COMPLETED')
            except ValueError:
                print 'NOT COMPLETED: ', file
                try:
                    pp.index('failed       \t\t')
                except ValueError:
                    pass
                else:
                    os.system('crab resubmit -d ' + file)
                    # pass
            else:
                print "COMPLETED: ", file
                shutil.rmtree(file)
                tmp = {}
                try:
                    tmp = _Success[sample_name]
                except KeyError:
                    tmp[iSample] = path + 'nano' + year + version + process[0] + '/' + iSample + '_' + year + '/' + pp[pp.index('Task name:\t\t\t') + 13:pp.index('Task name:\t\t\t') + 26] + '/0000/'
                    # tmp[iSample] = 'path'
                else:
                    try:
                        tmp[iSample]
                    except KeyError:
                        tmp[iSample] = path + 'nano' + year + version + process[0] + '/' + iSample + '_' + year + '/' + pp[pp.index('Task name:\t\t\t') + 13:pp.index('Task name:\t\t\t') + 26] + '/0000/'
                        # tmp[iSample] = 'path'
                    else:
                        pass
                try:
                    old = 'Success[\'' + sample_name + '\'] = '
                except KeyError:
                    pass
                else:
                    remove_text(old, year)
                new = 'Success[\'' + sample_name + '\'] = ' + str(tmp) + '\n'

                with open('crab_collection' + year + '.py', 'a+') as collect:
                    collect.write(new)
        elif args.mode == 'original':
            os.system('crab status -d ' + file)

        # print('crab status -d '+file)
        # print a
        # print b


if __name__ == '__main__':
    if args.chosenyear == '2022':
        status('2016')
        status('2017')
        status('2018')
    else:
        status(args.chosenyear)