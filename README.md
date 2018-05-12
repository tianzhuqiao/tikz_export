**tikz_export** is a tool to generate the pdf/eps/svg files from the latex tikz diagrams.
### install
1. download/clone the scripts into a folder, then run
    ```
    $ sudo pip install -e .
    ```
### basic usage:
1.  to generate the **pdf** files from all the tikzpictures
    ```
    $ tikz_export basic.tex -f pdf
    ```
2. to generate the **eps** files with **-f** option
    ```
    $ tikz_export basic.tex -f eps
    ```
 3. change the output filename with **-o** option
    ```
    $ tikz_export basic.tex -f eps -o myfile
    ```
    - then the output filenames will be **myfile0.eps**, **myfile1.eps**, etc.
 4. only process the **nth** image with **-n** option. For example, to keep the first tikzpicture only
    ```
    $ tikz_export basic.tex -f eps -n 0
    ```
 5. only keep the tikzpictures with specific output filenames
    1. set the output filename in **latex** file. To define the filename, add a line before **\begin{tikzpicture}**, which starts with "%%% ", e.g.,
        ```
        %%% mypicture
        \begin{tikzpicture}
        ..
        \end{tikzpicture}
        ```
       
     2. then you can choose to generate that picture only,
        ```
        $ tikz_export basic.tex -f eps --fig mypicture
        ```
     3. it also supports wildcard character
        ```
        $ tikz_export basic.tex -f eps --fig *my*
        ```
        - it will process all the pictures with **my** in theirs output filenames.
