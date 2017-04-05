import gramfuzz
from rtf_windbg import CDBFuzzer

debuggerPath = "C:\\Program Files (x86)\\Debugging Tools for Windows (x86)\\cdb.exe"
crashDirectory = "M:\\Fuzzing\\RTF\\crash\\"
programPath = "C:\\Program Files (x86)\\Microsoft Office\\Office14\\WINWORD.EXE"

fuzzer = gramfuzz.GramFuzzer()
fuzzer.load_grammar("rtf_grammar.py")
list_rtf = fuzzer.gen(cat = "rtf", num = 100)

index = 0
for rtf in list_rtf:
    fileName = "C:\\Users\\khoanx.VISC\\Desktop\\" + str(index) + ".rtf"
    print fileName
    open(fileName, "wt").write(rtf)
    dbg = CDBFuzzer(programPath, crashDirectory, debuggerPath)
    dbg.startFuzz(fileName, 320)
    dbg.stopFuzz(str(index))

    dbg.wasCrash()
    dbg.dumpCrash()
    index = index + 1
    exit(0)
