from distutils.core import setup

setup(name='tikz_export',
        version='0.0.3',
        description='Generate pdf/svg/eps file from tikzpicture',
        author='Tianzhu Qiao',
        author_email='tq@feiyilin.com',
        license="MIT",
        platforms=["any"],
        py_module=['tikz_export'],
        install_requires=[
            'Click',
        ],
        entry_points='''
        [console_scripts]
        tikz_export=tikz_export:cli
        ''',
     )
