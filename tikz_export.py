"""
Automically generate the pdf/eps/svg files from the tikz diagram

basic usage:
    >>> # to generate the pdf files from all the tikzpicture
    >>> tikz_export.py -i basic.tex -f pdf
    >>> # to generate the eps files from all the tikzpicture
    >>> tikz_export.py -i basic.tex -f eps
    >>> # to change the output filename, the output filename will be
    >>> # myfile0.eps myfile1.eps, ...
    >>> tikz_export.py -i basic.tex -f eps -o myfile
    >>> # only keep the 5th image
    >>> tikz_export.py -i basic.tex -f eps -n 5

Note: you can also define the filename for each tizkpicture by adding the
following line (start with '$$$ ') before the tikzpicture. For example,

%%% mypicture
\begin{tikzpicture}
..
\end{tikzpicture}
Then the exported file will have name "mypicture.pdf/svg/eps"
"""

import sys, getopt, os, traceback
import glob
tex2pdf_external = (
    '\\usetikzlibrary{external}\n'
    '\\tikzset{external/system call={pdflatex \\tikzexternalcheckshellescape'
    '-halt-on-error -interaction=batchmode -jobname "\\image" "\\texsource"'
    '}}\n'
    '\\tikzexternalize[shell escape=-enable-write18]\n\n')

pdf_export_cmd = {}
pdf_export_cmd['.eps'] = "pdftops -eps"
pdf_export_cmd['.svg'] = "pdf2svg"

tikz_export_tip = """
tikz_export.py -i <tex file> -o <eps file> -f [pdf|eps|svg] -d <destination folder> [-n N]
   -i: input tex file
   -o: default output file prefix
   -d: the destination folder
   -f [pdf|svg|eps]: default file format
   -n N: keep the Nth figure only"""

def tizk_export(argv):
    tip = tikz_export_tip
    inputfile = ''
    outputfile = ''
    fmt = ".pdf"
    dest = '.'
    fig = []
    try:
        opts, _ = getopt.getopt(argv[1:], "hi:o:f:n:d:")
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
            if pdf_export_cmd.get(f, None) is None:
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
                os.system(r"%s %s %s"%(pdf_export_cmd[fe], f, fout))
            else:
                os.system("del %s"%(fout))
                os.rename(f, fout)

        os.system("del temp*.*")

if __name__ == "__main__":
    tizk_export(sys.argv)

