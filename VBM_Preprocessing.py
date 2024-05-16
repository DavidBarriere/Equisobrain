import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'gkg', 'python' ) )

from CopyFileDirectoryRm import *

def runVoxelBasedMorphomertry( Dir,
                               subject,
                               template,
                               group,
                               sex,
                               verbose ):
                      
  
  if ( verbose == True ):

    #-----------------------------------------------------------------------------
    # Make Directories & Inputs
    #-----------------------------------------------------------------------------

    makedir( os.path.join( Dir,
                           subject,
                           '02-VBM' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '02-VBM',
                           '01-BiasFieldCorrection' ) )


    makedir( os.path.join( Dir,
                           subject,
                           '02-VBM',
                           '02-Denoising' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '02-VBM',
                           '03-SpatialNormalization' ) )
                           
    rawDataDir =  os.path.join( Dir,
                                'Turone_Equine_Social_Brain_Dataset' )

    #-------------------------------------------------------------------------
    # Voxel Based Morphomertry preprocessing
    #-------------------------------------------------------------------------
    	#-----------------------------------------------------------------------
    	# Rotation of t1 Data
    	#-----------------------------------------------------------------------
    print( 'Flipping ' + subject )
    command = 'AimsFlip ' + \
            	'-i ' + os.path.join( rawDataDir,
	                                  subject,
	                                  'anat',
	                                  subject + '_T1w.nii.gz ' ) + \
            	'-o ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '01-BiasFieldCorrection',
	                                  't1.nii.gz ' ) + \
            	'-m YZ'
    os.system( command )

    command = 'AimsFlip ' + \
            	'-i ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '01-BiasFieldCorrection',
	                                  't1.nii.gz ' ) + \
            	'-o ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '01-BiasFieldCorrection',
	                                  't1.nii.gz ' ) + \
            	'-m ZZ'
    os.system( command )
    print( 'Done ' )

  	#-----------------------------------------------------------------------
  	# Bias Field Correction
  	#-----------------------------------------------------------------------
    print( 'Bias Field Correction ' + subject )

    command = 'N4BiasFieldCorrection ' + \
              '-d 3 ' + \
              '-i ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '01-BiasFieldCorrection',
	                                  't1.nii.gz ' ) + \
              ' -o ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '01-BiasFieldCorrection',
	                                  't1_N4.nii.gz ' )
    os.system( command )
    print( 'Done ' )

  	#-----------------------------------------------------------------------
  	# Denoising
  	#-----------------------------------------------------------------------
  	 
    print( 'Denoising ' + subject )
   	 	
    command = 'DenoiseImage ' + \
              '-d 3 ' + \
              '-i ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '01-BiasFieldCorrection',
	                                  't1_N4.nii.gz ' ) + \
              '-o ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '02-Denoising',
	                                  't1.nii.gz ' ) + \
              '-n Gaussian ' + \
              '-p 2x2x2 ' + \
              '-r 4x4x4'

    os.system( command )
    print( 'Done ' )

  	#-----------------------------------------------------------------------
  	# Spatial Normalization
  	#-----------------------------------------------------------------------

    print( 'Spatial Normalization of ' + subject )
   	 	
    command = 'antsRegistrationSyNQuick.sh ' + \
    					'-d 3 ' + \
    					'-f ' + template + \
    					' -m ' + os.path.join( Dir,
	                                   subject,
	                                   '02-VBM',
	                                   '02-Denoising',
	                                   't1.nii.gz ' ) + \
    					'-o ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '02-Denoising',
	                                  't1_ ' ) + \
    					'-t t'

    os.system( command )

    command = 'antsApplyTransforms ' + \
    					'-d 3 ' + \
    					'-e 0 ' + \
    					'-i ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '02-Denoising',
	                                  't1.nii.gz ' ) + \
    					'-o ' + os.path.join( Dir,
	                                  subject,
	                                  '02-VBM',
	                                  '03-SpatialNormalization',
	                                  subject + '_' + group + '_' + sex + '_t1.nii.gz ' ) + \
    					'-r ' + template + \
    					' -n Linear ' + \
    					'-t ' + os.path.join( Dir,
	                                   subject,
	                                   '02-VBM',
	                                   '02-Denoising',
	                                   't1_0GenericAffine.mat' )
    os.system( command )
    print( 'Done ' )
