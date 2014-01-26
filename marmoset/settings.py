import textwrap


PROG = "marmoset"
VERSION = "0.1.1"
DESCRIPTION = textwrap.dedent("""\
   A command line tool for interacting with the Marmoset Submission Server.
   -------------------------------------------------------------------------
""")
USAGE = textwrap.dedent('''\
    [ [ -h | -v ] [ -f course problem ] [ -l course problem submission ]
             [ -s course problem filename ] [ -r course problem submission ] ]
''')
COMMAND_LINE_ARGUMENTS = (
    {
      'name': 'additional_files',
      'args': {
          'nargs': '*',
          'help': 'additional files to zip with and submit.'
      }
    },
    { 
      'short': "-s", 
      'long': "--submit", 
      'args': {
          'nargs': 3,
          'metavar': ("course", "problem", "filename"),
          'help': "submit a file/assignment to the marmoset server."
       }
    },
    { 
      'short': "-f",
      'long': "--fetch",
      'args': {
          'nargs': 2,
          'metavar': ("course", "problem"),
          'help': "fetch the last five(5) test results."
      }
    },
    {
      'short': "-r",
      'long': "--release",
      'args': {
          'nargs': 3,
          'metavar': ("course", "problem", "submission"),
          'help': "release test specified submission (0 - Most Recent, Max - Oldest)"
      }
    },
    {
      'short': "-l",
      'long': "--long",
      'args': {
          'nargs': 3,
          'metavar': ("course", "problem", "submission"),
          'help': "get the long test results for the specified submission."
      }
    },
    {
      'short': "-v",
      'long': "--version",
      'args': {
          'action': "store_true",
          'help': "print the version string."
      }
    },
)
BUG = """
           GG                                        
          0G0@             ,.                        
               @      .@@f@tCi                       
               :@    1i                              
                8    @   ,t8@@GCLLfffffLG8@L         
                C.  ,@@Ltfffftttttttttttttff0        
            i@0:C1f@CGftttttttttttttttttttft@        
          G:    @@fffCfttttttttttttttttttfff8        
              i@0ffffCfttttttttttttttttt08880t,      
       .:8C@@@fLCftffCfttttttttttttttttttft@    G@   
     @@   L8;0ffttttfftttttttttttttttttttt8      i0  
   :,   ;C@@@.1ffffCCtttttttttttttttttttt0i       f0 
        @8@;:C,CC1GL ifftttttttfffffttff@          CC
        G0018 1Lf@8.8 GttttttttffG@@88@@t.           
     i@@@    tf8i@;:G 8ttttttttttfff@    ,f@         
  ,@L,   .@8fft0 .i. ftLtfttttfftC@        1@        
 00         f@8f0;.t0tfff80fC8@@;           0f       
f.              ,;11111:,.  t@8              @       
                             ;@                      
                             :@                      
                              G8                     
                               @                     
"""
