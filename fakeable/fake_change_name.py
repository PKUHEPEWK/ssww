import os
path=input('path:')

f=os.listdir(path)

n=0
for i in f:

    oldname=path+f[n]

    newname=path+'fake_'+f[n]

    os.rename(oldname,newname)
    print(oldname,'======>',newname)

    n+=1
