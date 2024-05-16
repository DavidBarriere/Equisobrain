import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'gkg', 'python' ) )

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from CopyFileDirectoryRm import *
from MWF_Preprocessing import *
from VBM_Preprocessing import *
from NODDI_Preprocessing import *
from func_Preprocessing import *

def runPipeline( Dir,
                 subjectJsonFileName,
                 taskJsonFileName,
                 verbose ):

  ##############################################################################
  # reading subject information
  ##############################################################################

    subjects = dict()
    with open( subjectJsonFileName, 'r' ) as f:
        subjects = json.load( f )

  ##############################################################################
  # reading task information
  ##############################################################################

    taskDescription = dict()
    with open( taskJsonFileName, 'r' ) as f:
        taskDescription = json.load( f )

  ##############################################################################
  # first loop over groups and individuals to perform individual processing
  ##############################################################################

    for subject in subjects.keys():

        ########################################################################
        # running MWF Data Preprocessing
        ########################################################################

        if ( taskDescription[ "MWF_Preprocessing" ] == 1 ):

            if ( verbose == True ):
                print( "=====================================================" )
                print( subject + ' ' + "Myelin Water Fraction Preprocessing" )
                print( "=====================================================" )

            template = os.path.join( Dir,
                                     'Turone_Equine_Social_Brain_Dataset',
                                     'Turone_Equine_Brain_Atlas_and_Templates',
                                     'relaxo',
                                     'template.nii.gz' )

            mask = os.path.join( Dir,
                                 'Turone_Equine_Social_Brain_Dataset',
                                 'Turone_Equine_Brain_Atlas_and_Templates',
                                 'relaxo',
                                 'mask.nii.gz')
                                 
            LinearTransformation_02 = os.path.join( Dir,
																		             		'Turone_Equine_Social_Brain_Dataset',
																		             		'Turone_Equine_Brain_Atlas_and_Templates',
																		             		'relaxo',
																		             		'data-to-template_Affine.mat')

            DiffeoTransformation_01 = os.path.join( Dir,
																		             		'Turone_Equine_Social_Brain_Dataset',
																		             		'transformations',
																		             		'relaxo',
																		             		subject + '_vfa-to-msme_Warped_1Warp.nii.gz')

            LinearTransformation_01 = os.path.join( Dir,
																		             		'Turone_Equine_Social_Brain_Dataset',
																		             		'transformations',
																		             		'relaxo',
																		             		subject + '_vfa-to-msme_Warped_0GenericAffine.mat')

            fileNameFAValues = os.path.join( Dir,
																		         'FA.txt')

            fileNameTEValues = os.path.join( Dir,
																		         'TE.txt')

            fileNameTRValues = os.path.join( Dir,
																		         'TR.txt')

            group = subjects[subject].get('Group')


            sex = subjects[subject].get('SEX')
            
            runMyelinWaterFraction( Dir,
                                    subject,
                                    template,
                                    mask,
                                    LinearTransformation_02,
                                    DiffeoTransformation_01,
                                    LinearTransformation_01,
                                    fileNameFAValues,
                                    fileNameTEValues,
                                    fileNameTRValues,
                                    group,
                                    sex,
                                    1 )

        ########################################################################
        # running Voxel-Based Morphometry Data Preprocessing 
        ########################################################################

        if ( taskDescription[ "VBM_Preprocessing" ] == 1 ):

            template = os.path.join( Dir,
                                     'Turone_Equine_Social_Brain_Dataset',
                                     'Turone_Equine_Brain_Atlas_and_Templates',
                                     'anat',
                                     'template_new.nii' )

            group = subjects[subject].get('Group')

            sex = subjects[subject].get('SEX')

            if ( verbose == True ):
                print( "=====================================================" )
                print( subject + ' ' + "Voxel-Based Morphometry Preprocessing" )
                print( "=====================================================" )

            runVoxelBasedMorphomertry( Dir,
                                       subject,
                                       template,
                                       group,
                                       sex,
                                       1 )

        ########################################################################
        # running Diffusion Data Preprocessing 
        ########################################################################

        if ( taskDescription[ "NODDI_Preprocessing" ] == 1 ):

            template = os.path.join( Dir,
                                     'Turone_Equine_Social_Brain_Dataset',
                                     'Turone_Equine_Brain_Atlas_and_Templates',
                                     'diff',
                                     'diffusionSpace_Templates',
                                     'template.nii.gz' )

            mask = os.path.join( Dir,
                                 'Turone_Equine_Social_Brain_Dataset',
                                 'Turone_Equine_Brain_Atlas_and_Templates',
                                 'diff',
                                 'diffusionSpace_Templates',
                                 'mask.nii.gz' )

            diff_to_anat_affine = os.path.join( Dir,
                                     						'Turone_Equine_Social_Brain_Dataset',
                                     						'Turone_Equine_Brain_Atlas_and_Templates',
                                     						'anat',
                                     						'GisFormat',
                                     						'diff-to-anat.trm')

            diff_to_anat_direct = os.path.join( Dir,
                                     						'Turone_Equine_Social_Brain_Dataset',
                                     						'Turone_Equine_Brain_Atlas_and_Templates',
                                     						'anat',
                                     						'GisFormat',
                                     						'diff-to-anat.ima')

            diff_to_anat_inverse = os.path.join( Dir,
                                     						'Turone_Equine_Social_Brain_Dataset',
                                     						'Turone_Equine_Brain_Atlas_and_Templates',
                                     						'anat',
                                     						'GisFormat',
                                     						'anat-to-diff.ima')

            rot_tracto = os.path.join( Dir,
                                     	 'Turone_Equine_Social_Brain_Dataset',
                                     	 'Turone_Equine_Brain_Atlas_and_Templates',
                                     	 'anat',
                                     	 'GisFormat',
                                     	 'rotation_tractograms.trm')

            group = subjects[subject].get('Group')

            sex = subjects[subject].get('SEX')

            if ( verbose == True ):
                print( "=====================================================" )
                print( subject + ' ' + "Diffusion Data Preprocessing " )
                print( "=====================================================" )

            runNoddiProcessing( Dir,
                                subject,
                                template,
                                mask,
                                diff_to_anat_affine,
                                diff_to_anat_direct,
                                diff_to_anat_inverse,
                                rot_tracto,
                                group,
                                sex,
                                1 )

        ########################################################################
        # running Functional Data Preprocessing
        ########################################################################

        if ( taskDescription[ "func_Preprocessing" ] == 1 ):

            if ( verbose == True ):
                print( "=====================================================" )
                print( subject + ' ' + "functional Data Preprocessing" )
                print( "=====================================================" )

            Encoding_Direction = subjects[subject].get('Encoding_Direction')
            
            TopUp_Protocol = subjects[subject].get('TopUp_Protocol')

            template = os.path.join( Dir,
                                     'Turone_Equine_Social_Brain_Dataset',
                                     'Turone_Equine_Brain_Atlas_and_Templates',
                                     'relaxo',
                                     'template.nii.gz' )

            mask = os.path.join( Dir,
                                 'Turone_Equine_Social_Brain_Dataset',
                                 'Turone_Equine_Brain_Atlas_and_Templates',
                                 'relaxo',
                                 'mask.nii.gz')

            inverted_mask = os.path.join( Dir,
                                 					'Turone_Equine_Social_Brain_Dataset',
                                 					'Turone_Equine_Brain_Atlas_and_Templates',
                                 					'relaxo',
                                 					'inverted_mask.nii.gz')

            LinearTransformation_01 = os.path.join( Dir,
																		             		'Turone_Equine_Social_Brain_Dataset',
																		             		'transformations',
																		             		'func',
																		             		subject + '_fc_average_1Warp.nii.gz')

            DiffeoTransformation_01 = os.path.join( Dir,
																		             		'Turone_Equine_Social_Brain_Dataset',
																		             		'transformations',
																		             		'func',
																		             		subject + '_fc_average_0GenericAffine.mat')

            LinearTransformation_02 = os.path.join( Dir,
																		             		'Turone_Equine_Social_Brain_Dataset',
																		             		'Turone_Equine_Brain_Atlas_and_Templates',
																		             		'func',
																		             		'func-to-relaxo_1Warp.nii.gz')


            DiffeoTransformation_02 = os.path.join( Dir,
																		             		'Turone_Equine_Social_Brain_Dataset',
																		             		'Turone_Equine_Brain_Atlas_and_Templates',
																		             		'func',
																		             		'func-to-relaxo_0GenericAffine.mat')

            seg = os.path.join( Dir,
                                'Turone_Equine_Social_Brain_Dataset',
                                'Turone_Equine_Brain_Atlas_and_Templates',
                                'relaxo',
                                'seg.nii.gz')
            
            group = subjects[subject].get('Group')


            sex = subjects[subject].get('SEX')

            runFuncPreproccessing( Dir,
                              		 subject,
                              		 template,
                              		 mask,
                              		 inverted_mask,
                              		 Encoding_Direction,
                              		 TopUp_Protocol,
                              		 LinearTransformation_01,
                              		 DiffeoTransformation_01,
                              		 LinearTransformation_02,
                              		 DiffeoTransformation_02,
                              		 seg,
                              		 group,
                              		 sex,
                              		 1 )

