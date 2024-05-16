import os, json

from CommandList import *

Dir = '/home/dbarriere/Recherche/Equine_Project'
subjectJsonFileName = os.path.join( Dir,
                                    'subjects.json' )
taskJsonFileName = os.path.join( Dir,
                                 'TaskJsonFileName.json' )
verbose = 1
runPipeline( Dir,
             subjectJsonFileName,
             taskJsonFileName,
             verbose )
