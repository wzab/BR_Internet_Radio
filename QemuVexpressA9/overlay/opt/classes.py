from xser import *

class xradio(Xser):
  serid="xradio"

  def __init__(self,rname=None,url=None):
    self.rname=rname
    self.url=url
xclasses['xradio']=xradio


