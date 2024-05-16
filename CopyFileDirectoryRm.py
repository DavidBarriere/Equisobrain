import numpy as np
import sys, os, string, inspect, types, glob, fnmatch, re, copy, shutil
import signal, time, errno, socket, platform, tempfile, traceback, stat
import distutils.spawn, operator, tarfile
from optparse import OptionParser
import math
import json
import random

#-----------------------------------------------------------------------------
# makedir()
#-----------------------------------------------------------------------------

def makedir( path ):
    if ( not os.path.exists( path ) ):
        os.makedirs( path )
        
    else:
        if ( not os.path.isdir( path ) ):
            rm( path )
            os.makedirs( path )

#-----------------------------------------------------------------------------
# copyFile()
#-----------------------------------------------------------------------------

def copyFile( source,
              dest,
              symlinks=False, 
              copyAsSymlinks=False ):
    if not os.path.exists( source ):
        print ( source,
                'does not exist' )
        return
    if os.path.islink( dest ):
        os.remove( dest )
        
    elif os.path.exists( dest ):
        os.chmod( dest,
                  stat.S_IWRITE | stat.S_IREAD )
        os.remove( dest )
        
    else:
        destDir = os.path.dirname( dest )
        if not os.path.isdir( destDir ):
              os.makedirs( destDir )

    if symlinks or copyAsSymlinks:
        if os.path.islink( source ) and not os.path.isabs( os.readlink( source ) ):
              os.symlink( os.readlink( source ),
                          dest )
                
        elif copyAsSymlinks and systemname != 'windows':
              os.symlink( source,
                          dest )
        else:
            shutil.copy2( source,
                          dest )
    else:
        shutil.copy2( source,
                      dest )

#-----------------------------------------------------------------------------
# copyDirectory()
#-----------------------------------------------------------------------------

def copyDirectory( sourceDir, destinationDir, 
                   symlinks = False, 
                   copyAsSymlinks = False,
                   include = None,
                   exclude = None,
                   copyCallback = None,
                   keepExistingDirs = True ):
    if not os.path.exists( sourceDir ):
        return
    
    stack = os.listdir( sourceDir )
    while stack:
        relSource = stack.pop()
        source = os.path.join( sourceDir,
                               relSource )
        dest = os.path.join( destinationDir,
                             relSource )
        if os.path.islink( source ) or not os.path.isdir( source ):
            if ( include is not None and not include.match( relSource ) ) or \
               ( exclude is not None and exclude.match( relSource ) ):
                continue
            if copyCallback is None or copyCallback( source,
                                                     dest ):
                copyFile( source,
                          dest,
                          symlinks=symlinks,
                          copyAsSymlinks=copyAsSymlinks )
                
        elif os.path.isdir( source ):
            if os.path.islink( dest ):
                os.unlink( dest )
                
            elif os.path.exists( dest ):
                if not keepExistingDirs:
                    rm( dest )
            else:
                os.makedirs( dest )
                stack += [os.path.join( relSource,
                                        f ) for f in os.listdir( source )]
        else:
            stack += [os.path.join( relSource,
                                    f ) for f in os.listdir( source )]

#-----------------------------------------------------------------------------
# rm()
#-----------------------------------------------------------------------------

def rm( *args ):
    sources = []
    for pattern in args:
        sources += glob.glob( pattern )
        sys.stdout.flush()
        
    for path in sources:
        if not os.path.islink( path ):
            os.chmod( path,
                      '0777' )
            
        if os.path.isdir( path ) and not os.path.islink( path ):
            rm( os.path.join( path,
                              '*' ) )
            os.rmdir( path )
    else:
        os.remove( path )

#-----------------------------------------------------------------------------
# runGinkgo()
#-----------------------------------------------------------------------------

def runGinkgo( parameterValues, outputWorkDirectory ):
    parameterValues[ 'outputWorkDirectory' ] = outputWorkDirectory
    makedir( outputWorkDirectory )
    algorithmName = parameterValues[ '_algorithmName' ]
    parameterFileName = os.path.join( outputWorkDirectory + os.sep + algorithmName + '.py' )
    
    with open( parameterFileName,
               'w' ) as f:
        json.dump( parameterValues,
                   f,
                   sort_keys=True,
                   indent=2,
                   separators=( ',',
                               ' : ' ) )

    command = 'ginkgo ' + \
              ' --batch ' + \
              ' -p ' + parameterFileName + \
              ' -d single-threading'
 
    print( command )
    os.system( command )

#-----------------------------------------------------------------------------
# Directory FastScan Function
#-----------------------------------------------------------------------------

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders
