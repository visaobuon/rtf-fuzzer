import gramfuzz 
from gramfuzz.fields import *
from gramfuzz.rand import *

class NRef(Ref):
    cat = "rtf_def"
class NDef(Def):
    cat = "rtf_def"

Def("rtf", And("{", NRef("header"), NRef("document")," }"), cat="rtf", sep=" ")

NDef("header", And("\\rtf1 ", Opt("\\fbidis "), NRef("character set"), Opt(NRef("from")), NRef("deffont"),
    NRef("deflang"), Opt(NRef("listtables"))))
NDef("document", "{fuzzer}")

NDef("character set", Or("\\ansi ", "\\mac ", "\\pc ", "\\pca "))
NDef("from", Or("\\fromtext ", "\\fromhtml "))
NDef("deffont", Or("\\deff1 ", "\\adeff1 "))
NDef("deflang", Or("\\deflang1 ", "\\adeflang1 "))
NDef("listtables", And("{\\*", "\\listtable ", Opt(NRef("listpicture")), STAR(NRef("list"), max=10), "}"))
NDef("listpicture", And("{\\*\\listpicture ", String(min=1, max=2), "}"))


NDef("list", And("\\list ", "\\listtemplateid ", Or("\\listsimple ", "\\listhybrid"),
    STAR(NRef("listlevel")), "\\listrestarthdn ", "\\listid" + str(randint(10)), "\\listname ", data(20, "\x80\x90khoanx?"), ";"))
NDef("listlevel", "\\listlevel ")

