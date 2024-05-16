import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'gkg', 'python' ) )

from CopyFileDirectoryRm import *

def runDwImportAndQspace( Dir,
                          subject,
                          verbose ):
                      
  
  if ( verbose == True ):

#-----------------------------------------------------------------------------
# Make Directories and Inputs
#-----------------------------------------------------------------------------

    makedir( os.path.join( Dir,
                           subject,
                           '02-Diffusion',
                           '03-DWIAndQSpace' ) )
    
    dw_Shell1 = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '01-TopUp',
                              'dw_01_eddy_corrected_data')

    dw_Shell2 = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '01-TopUp',
                              'dw_02_eddy_corrected_data')

    dw_Shell3 = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '01-TopUp',
                              'dw_03_eddy_corrected_data')

    txt_Shell1 = os.path.join( Dir,
                               subject,
                               '02-Diffusion',
                               '00-Dicom-to-Gis',
                               'dw_01')

    txt_Shell2 = os.path.join( Dir,
                               subject,
                               '02-Diffusion',
                               '00-Dicom-to-Gis',
                               'dw_02')

    txt_Shell3 = os.path.join( Dir,
                               subject,
                               '02-Diffusion',
                               '00-Dicom-to-Gis',
                               'dw_03')
#-----------------------------------------------------------------------------
# DWIAndQSpace
#-----------------------------------------------------------------------------

    parameterValues = {
      '_algorithmName' : 'DWI-Data-Import-And-QSpace-Sampling',
      '_subjectName' : '',
      'acqpFileNames' : '',
      'applyVisuCoreTransformation' : 1,
      'bValFileNames' : '',
      'bValueStdDev' : 10.0,
      'bValueThreshold' : 10.0,
      'bVecFileNames' : '',
      'fileNameDwi' : '',
      'gradientCharacteristicsFileNames' : '',
      'invertXAxis' : 0,
      'invertYAxis' : 0,
      'invertZAxis' : 0,
      'manufacturer' : 3,
      'methodFileNames' : '',
      'outputWorkDirectory' : '',
      'phaseAxis' : 1,
      'qSpaceSamplingType' : 2,
      'sliceAxis' : 0,
      'visuParsFileNames' : ''
    }
    
    dwiFile = dw_Shell1 + '.ima' + ';' + \
              dw_Shell2 + '.ima' + ';' + \
              dw_Shell3 + '.ima'
    
    bvalFile = txt_Shell1 + '.bval' + ';' + \
               txt_Shell2 + '.bval' + ';' + \
               txt_Shell3 + '.bval'

    bvecFile = dw_Shell1 + '.eddy_rotated_bvecs' + ';' + \
               dw_Shell2 + '.eddy_rotated_bvecs' + ';' + \
               dw_Shell3 + '.eddy_rotated_bvecs'

    outputFolder = os.path.join( Dir,
                                 subject,
                                 '02-Diffusion',
                                 '03-DWIAndQSpace' )

    parameterValues[ 'fileNameDwi' ] = dwiFile
    parameterValues[ 'bValFileNames' ] = bvalFile
    parameterValues[ 'bVecFileNames' ] = bvecFile

    runGinkgo( parameterValues, outputFolder )
    print( 'Done' )