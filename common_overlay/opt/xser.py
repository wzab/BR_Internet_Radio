def escape_xml( istr ):
    istr = istr.replace("&", "&amp;")
    istr = istr.replace("<", "&lt;")
    istr = istr.replace(">", "&gt;")
    istr = istr.replace("\"", "&quot;")
    return istr

def encode_basic(val,name,level):
   #print(val,type(val))
   if (type(val)==str):
     ntype="str"
     out=escape_xml(val)
   elif type(val)==bool:
     ntype="bool"
     out=str(val)
   #In python 2 empty string is returned as None?
   elif val==None:
     ntype="str"
     out=""
   else:
     print(val)
     print(type(val))
     raise Exception("wrong type:")
   res=(level*"  ")+"<"+ntype
   if name != "":
      res+=" name=\""+name+"\">"
   else:
      res+=">"
   res+=out+"</"+ntype+">\n"
   return res

def encode_node(val,name,level):
   res=""
   if(isinstance(val,Xser)):
      res+=val.encode(name,level+1)
   elif type(val)==list:
      res+=encode_list(val,name,level+1)
   else:
      res+=encode_basic(val,name,level+1)
   return res

def encode_list(val,name,level):
   res=(level*"  ") + "<list" 
   if name != "":
      res+=" name=\""+name+"\">\n"
   else:
      res+=">\n"
   for el in val:
      res+=encode_node(el,"",level+1)
   res+=(level*"  ") + "</list>\n"
   return res


class Xser:
   serid="xser"
   def __init__(self):
     pass

   def encode(self,name,level):
     res=(level*"  ") + "<" + self.serid
     if name != "":
        res+=" name=\"" + name + "\""
     res+=">\n"
     for k in self.__dict__:
         res+=encode_node(self.__dict__[k],k,level)
     res+=(level*"  ") + "</" + self.serid + ">\n" 
     return res
   def decode(self):
     pass

class ctempl(Xser):
   serid="ctempl"
   def __init__(self):
     pass

xclasses={ 
  "ctempl":ctempl,
  "list":list,
  "bool":bool,
  "str":str,
}

import xml.etree.ElementTree as et
def build_node(el):
  res=xclasses[el.tag]()
  if type(res)==list:
    for cl in el.getchildren():
      res.append(build_node(cl))
  elif type(res)==bool:
    return bool(el.text=="True")
  elif type(res)==str:
    return el.text
  elif isinstance(res,Xser):
    for cl in el.getchildren():
      n=cl.attrib.get('name')
      if n:
        res.__dict__[n]=build_node(cl)
  else:
    raise Exception("wrong type:" + str(res))
  return res

def decode_xml(sxml):
  tr=et.ElementTree(et.fromstring(sxml))
  er=tr.getroot()
  cfg=build_node(er)
  return cfg


