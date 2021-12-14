import json
from os import path
import os
from threading import Lock
base32_chrs="01234567890abcdefghijklmnopqrstuvwxyz'"


def ensure_dir(pth):
    if(not path.exists(path.dirname(pth))):
        os.makedirs(path.dirname(pth))
def load_json(pth):
    f=open(pth,'r')
    j=json.load(f)
    f.close()
    return j
def save_json(pth,j):
    ensure_dir(pth)
    f=open(pth,'w')
    json.dump(j,f)
    f.close()

def shashi(s,length=24):
    ret=0
    mask=(1<<length)-1
    for ch in s:
        i=ord(ch)
        ret=(ret<<7)^i
        ret=(ret&mask)^(ret>>length)
    return ret
def hashi(x,length=24):
    if(isinstance(x,str)):
        return shashi(x,length=24)
    else:
        raise TypeError()

def base32(x,length=8):

    blength=length*5
    mask=(1<<blength)-1
    if(not isinstance(x,int)):
        x=hashi(x,length=blength)
    
    while(x>>blength):
        x=(x&mask)^(x>>blength)
    
    mask=0b11111
    ret=[]
    for i in range(length):
        ret.append(base32_chrs[x&mask])
        x>>=5
    return ''.join(ret[::-1])

class db:
    def __init__(self,pth):
        self.d={}
        self.loaded=set()
        self.pth=pth
        self.lck=Lock()
    def lock_exec(self,func,*args,**kwargs):
        self.lck.acquire()
        try:
            ret = func(*args,**kwargs)
        except Exception as e:
            self.lck.release()
            raise e
        self.lck.release()
        return ret
    def _lazyload(self,key):
        short_key=base32(key,length=4)
        pth=path.join(self.pth,short_key+'.json')
        if(pth in self.loaded):
            return
        if(path.exists(pth)):
            self.d[short_key]=load_json(pth)
        else:
            self.d[short_key]={}
    def _getitem(self,key):
        short_key=base32(key,length=4)
        self._lazyload(key)
        dd=self.d.get(short_key,{})
        if(key in dd):
            return dd[key]
        else:
            raise KeyError(key)
    def __getitem__(self,key):
        return self.lock_exec(self._getitem,key)
    def _setitem(self,key,value):
        short_key=base32(key,length=4)
        pth=path.join(self.pth,short_key+'.json')
        self._lazyload(key)
        dd=self.d.get(short_key,{})
        dd[key]=value
        save_json(pth,dd)
        self.d[short_key]=dd
    def __setitem__(self,key,value):
        self.lock_exec(self._setitem,key,value)
    def _contains(self,key):
        short_key=base32(key,length=4)
        self._lazyload(key)
        dd=self.d.get(short_key,{})
        return (key in dd)
    def __contains__(self,key):
        return self.lock_exec(self._contains(key))
    def _get(self,key,*args):
        if(self._contains(key)):
            return self._getitem(key)
        elif(args):
            return args[0]
        else:
            raise KeyError(key)
    def get(self,key,*args):
        return self.lock_exec(self._get,key,*args)
if(__name__=='__main__'):
    d=db(path.join(path.dirname(__file__),'tempdb'))
    print(d['miao'])
    d['miao']='meow'
    d['mao']='cat'
    d['fu']='aaa'
    print(d['miao'])
    print(d.get('dne','v'))
    print(d['dne'])