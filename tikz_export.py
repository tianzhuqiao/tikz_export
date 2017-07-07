"""
automically generate the eps file from the tikz diagram
"""
import sys, getopt, os
import glob
tex2pdf_external = ('\\usetikzlibrary{external}\n'
    '\\tikzset{external/system call={pdflatex \\tikzexternalcheckshellescape'
    '-halt-on-error -interaction=batchmode -jobname "\\image" "\\texsource"'
    '}}\n'
    '\\tikzexternalize[shell escape=-enable-write18]\n\n')

pdf2 = {}
pdf2['.eps'] = "pdftops -eps"
pdf2['.svg'] = "pdf2svg"

tikz_export_tip = """
%s -i <tex file> -o <eps file> -f [pdf|eps|svg] -d <destination folder> [-f N]
   -i: input tex file
   -o: default output file prefix
   -d: the destination folder
   -f [pdf|svg|eps]: default file format
   -n N: keep the Nth figure only"""

def tizk_export(argv):
    tip = tikz_export_tip%argv[0]
    inputfile = ''
    outputfile = ''
    fmt = ".pdf"
    dest = '.'
    fig = []
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:f:n:d:")
    except getopt.GetoptError:
        traceback.print_exc()
        print(tip)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(tip)
            return
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg
        elif opt == '-f':
            f = '.'+arg.strip()
            if pdf2.get(f, None) is None:
                print("unknown argument -f %s"%f)
                print(tip)
                sys.exit(2)
            fmt = f
        elif opt == '-n':
            fig.append(int(arg))
        elif opt == '-d':
            dest = arg.strip()

    if not os.path.isfile(inputfile):
        print(tip)
        return

    with open(inputfile) as fin:
        content = fin.readlines()
        ftemp = open('temp.tex', 'w')
        outputEnable = True
        fig_idx = 0
        fnames = []
        fname = ''
        for c in content:
            if "\\begin{document}" in c:
                ftemp.write((tex2pdf_external))
                ftemp.write("%s"%c)
                outputEnable = False
            elif "\\begin{tikzpicture" in c:
                outputEnable = (not fig) or (fig_idx in fig)
                fig_idx += 1
                if outputEnable:
                    fnames.append(fname)
                fname = ''
            elif "\\end{document}" in c:
                ftemp.write("%s"%c)
                break
            elif c.startswith("%%% "):
                fname = c[4:].strip()
            if outputEnable:
                ftemp.write("%s"%c)
            if "\\end{tikzpicture}" in c:
                outputEnable = False
        ftemp.close()
        # get the default output filename
        base = os.path.basename(inputfile)
        base = os.path.splitext(base)[0]
        if not outputfile:
            outputfile = base+'-figure'

        os.system(r"pdflatex --shell-escape temp.tex")
        for f in glob.glob('temp-figure*.pdf'):
            idx = int(f[11:-4])
            fout = ''
            if fnames[idx]:
                fn, fe = os.path.splitext(fnames[idx])
                if not fe:
                    fe = fmt
            else:
                fn, fe = "%s%d"%(outputfile, idx), fmt
            fout = dest+'\\'+fn+fe
            if fe != ".pdf":
                os.system(r"%s %s %s"%(pdf2[fe], f, fout))
            else:
                os.system("del %s"%(fout))
                os.rename(f, fout)

        os.system("del temp*.*")

if __name__ == "__main__":
    tex2eps(sys.argv)


