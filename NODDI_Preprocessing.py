import os, json, sys, shutil
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from time import time

# DIPY Local PCA Denoising
from dipy.denoise.localpca import mppca 
from dipy.core.gradients import gradient_table
from dipy.io.image import load_nifti
import dipy.reconst.dki as dki

sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'gkg', 'python' ) )

from CopyFileDirectoryRm import *

def runNoddiProcessing( Dir,
                        subject,
                        template,
                        mask,
                        diff_to_anat_affine,
                        diff_to_anat_direct,
                        diff_to_anat_inverse,
                        rot_tracto,
                        group,
                        sex,
                        verbose ):
                      
  
  if ( verbose == True ):

    #-----------------------------------------------------------------------------
    # Make Directories & Inputs
    #-----------------------------------------------------------------------------

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion',
                           '01-TopUpCorrection' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion',
                           '02-Dicom-to-Gis' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion',
                           '03-DWIAndQSpace' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion',
                           '04-LocalModelling_DTI ' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion',
                           '05-NODDI' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion',
                           '06-ProcessedData' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '03-Diffusion',
                           '07-Tractography_SRD_1seed' ) )

    rawDataDir =  os.path.join( Dir,
    														'Turone_Equine_Social_Brain_Dataset' )

    topUpParameters = os.path.join( rawDataDir,
                                    'topup_parameters_dw.txt' )

    epi_resolution = [2, 2, 2.4]

    epi_matrix = [128, 128, 56]

    trm = os.path.join( rawDataDir,
                        'ID_Matrix.trm' )

    template_tracto = os.path.join( rawDataDir,
                             				'Turone_Equine_Brain_Atlas_and_Templates',
                             				'diff',
                             				'tractogram',
                             				'template.ima' )

    mask_tracto = os.path.join( Dir,
                             		'Turone_Equine_Social_Brain_Dataset',
                             		'Turone_Equine_Brain_Atlas_and_Templates',
                             		'diff',
                             		'tractogram',
                             		'mask.ima' )

    #-------------------------------------------------------------------------
    # NODDI preprocessing
    #-------------------------------------------------------------------------
    	#-----------------------------------------------------------------------
    	# Data Collecting
    	#-----------------------------------------------------------------------
    print( 'Data Collecting ' + subject)

    directions = { '_acq-RL_dir-6_dwi':{ 'nbDir':'dw_01',
    																		 'index':'index_6',
																				 'nbVolumes':'7' },
    							 '_acq-RL_dir-30_dwi':{ 'nbDir':'dw_02',
    																		  'index':'index_30',
    																		  'nbVolumes':'31' },
    							 '_acq-RL_dir-64_dwi':{ 'nbDir':'dw_03',
    																		  'index':'index_64',
    																		  'nbVolumes':'65' } }

    for key in directions.keys():
    	"""
    	command = 'AimsSubVolume ' + \
	            	'-i ' + os.path.join( rawDataDir,
																			subject,
																			'dwi',
																			subject + str( key ) + '.nii.gz ' ) + \
	            	'-o ' + os.path.join( Dir,
																			subject,
																			'03-Diffusion',
																			'01-TopUpCorrection',
																			str( directions[ key ]['nbDir'] ) + '.nii.gz ' ) + \
	            	'-z 0 ' + \
	            	'-Z 55'
    	os.system( command )

    	command = 'cp -f ' + \
	            	os.path.join( rawDataDir,
	                            subject,
	                            'dwi',
	                            subject + str( key ) + '.bvec ' ) + \
	            	os.path.join( Dir,
	                            subject,
	                            '03-Diffusion',
	                            '01-TopUpCorrection',
	                            str( directions[ key ]['nbDir'] ) + '.bvec ' )
    	os.system( command )

    	command = 'cp -f ' + \
	            	os.path.join( rawDataDir,
	                            subject,
	                            'dwi',
	                            subject + str( key ) + '.bval ' ) + \
	            	os.path.join( Dir,
	                            subject,
	                            '03-Diffusion',
	                            '01-TopUpCorrection',
	                            str( directions[ key ]['nbDir'] ) + '.bval ' )
    	os.system( command )

    encoding = { '_acq-topupRL_dir-6_dwi':'dw_BlipUp',
    						 '_acq-topupLR_dir-6_dwi':'dw_BlipDown' }
    						 
    for key in encoding.keys():

    	command = 'AimsSubVolume ' + \
	            	'-i ' + os.path.join( rawDataDir,
																			subject,
																			'dwi',
																			subject + str( key ) + '.nii.gz ' ) + \
	            	'-o ' + os.path.join( Dir,
																			subject,
																			'03-Diffusion',
																			'01-TopUpCorrection',
																			str( encoding[ key ] ) + '.nii.gz ' ) + \
	            	'-z 0 ' + \
	            	'-Z 55'
    	os.system( command )
    print( 'Done' )

    	#-----------------------------------------------------------------------
    	# TopUp Correction
    	#-----------------------------------------------------------------------
    print( 'TopUp Correction ' + subject)

    command = 'fslmerge ' + \
							'-t ' + \
							os.path.join( Dir,
														subject,
														'03-Diffusion',
														'01-TopUpCorrection',
														'dw_TopUp.nii.gz ' ) + \
							os.path.join( Dir,
														subject,
														'03-Diffusion',
														'01-TopUpCorrection',
														'dw_BlipUp.nii.gz ' ) + \
							os.path.join( Dir,
														subject,
														'03-Diffusion',
														'01-TopUpCorrection',
														'dw_BlipDown.nii.gz ' )

    os.system( command )
    	"""
    for key in directions.keys():
        """
        command = 'topup ' + \
									'--imain=' + os.path.join( Dir,
																						 subject,
																						 '03-Diffusion',
																						 '01-TopUpCorrection',
																						 'dw_TopUp.nii.gz ' ) + \
									'--datain=' + topUpParameters + \
									' --fwhm=0 ' + \
									'--config=b02b0.cnf ' + \
									'--out=' + os.path.join( Dir,
																						 subject,
																						 '03-Diffusion',
																						 '01-TopUpCorrection',
																						 'TopUp_results' )
        print( command )
        os.system( command )

        print( 'TopUp Correction ' + str( directions[ key ]['nbDir'] ) + ' : Done! ' )

        command = 'antsApplyTransforms ' + \
        					'-d 3 ' + \
        					'-e 0 ' + \
        					'-i ' + mask + \
        					' -o ' + os.path.join( Dir,
																			   subject,
																			   '03-Diffusion',
																			   '01-TopUpCorrection',
																			   str( directions[ key ]['nbDir'] ) + '_mask.nii.gz ' ) + \
        					'-r ' + os.path.join( Dir,
																			  'Turone_Equine_Social_Brain_Dataset',
																			  'transformations',
																			  'diff',
																			  subject + '_' + str( directions[ key ]['nbDir'] ) + '.nii.gz ' ) + \
        					'-n Linear ' + \
        					'-t ' + os.path.join( Dir,
																			  'Turone_Equine_Social_Brain_Dataset',
																			  'transformations',
																			  'diff',
																			  subject + '_' + str( directions[ key ]['nbDir'] ) + "_1InverseWarp.nii.gz [" ) + \
													os.path.join( Dir,
																			  'Turone_Equine_Social_Brain_Dataset',
																			  'transformations',
																			  'diff',
																			  subject + '_' + str( directions[ key ]['nbDir'] ) + "_0GenericAffine.mat, 1]" )
        os.system( command )

        command = 'eddy' + \
          				' --imain=' + os.path.join( Dir,
																						  subject,
																						  '03-Diffusion',
																						  '01-TopUpCorrection',
																						  str( directions[ key ]['nbDir'] ) + '.nii.gz ' ) + \
          				' --mask=' + os.path.join( Dir,
																						 subject,
																						 '03-Diffusion',
																						 '01-TopUpCorrection',
																						 str( directions[ key ]['nbDir'] ) + '_mask.nii.gz ' ) + \
          				' --acqp=' + topUpParameters + \
          				' --index=' + os.path.join( rawDataDir,
																			        str( directions[ key ]['index'] ) + '.txt' ) + \
          				' --bvecs=' + os.path.join( Dir,
																			   			subject,
																			   			'03-Diffusion',
																			   			'01-TopUpCorrection',
																			   			str( directions[ key ]['nbDir'] ) + '.bvec ' ) + \
          				' --bvals=' + os.path.join( Dir,
																			   			subject,
																			   			'03-Diffusion',
																			   			'01-TopUpCorrection',
																			   			str( directions[ key ]['nbDir'] ) + '.bval ' ) + \
          				' --topup=' + os.path.join( Dir,
																						  subject,
																						  '03-Diffusion',
																						  '01-TopUpCorrection',
																						  'TopUp_results ' ) + \
          				' --niter=8 ' + \
          				' --fwhm=10,8,4,2,0,0,0,0 ' + \
          				' --repol ' + \
          				' --out=' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'01-TopUpCorrection',
																						str( directions[ key ]['nbDir'] ) + '_corrected' ) + \
          				' --verbose'
        print( command )
        os.system( command )

        command = 'N4BiasFieldCorrection ' + \
        					'-d 4 ' + \
        					'-i ' + os.path.join( Dir,
																			  subject,
																			  '03-Diffusion',
																			  '01-TopUpCorrection',
																			  str( directions[ key ]['nbDir'] ) + '_corrected.nii.gz ' ) + \
        					'-o ' + os.path.join( Dir,
																			  subject,
																			  '03-Diffusion',
																			  '01-TopUpCorrection',
																			  str( directions[ key ]['nbDir'] ) + '_corrected_N4.nii.gz' )
        os.system( command )

        data, affine = load_nifti(os.path.join( Dir,
																			  			  subject,
																			  			  '03-Diffusion',
																			  			  '01-TopUpCorrection',
																			  			  str( directions[ key ]['nbDir'] ) + '_corrected_N4.nii.gz' ))

        denoised = mppca( data,patch_radius=6)

        nib.save(nib.Nifti1Image( denoised,
        													affine), 
        													os.path.join( Dir,
																			  			  subject,
																			  			  '03-Diffusion',
																			  			  '01-TopUpCorrection',
																			  			  str( directions[ key ]['nbDir'] ) + '_corrected_N4_Denoised.nii.gz' ))

    	#-----------------------------------------------------------------------
    	# Nifti to Gis Conversion
    	#-----------------------------------------------------------------------

        print( 'Nifti to Gis Conversion ' + str( directions[ key ]['nbDir'] ) )
        command = 'AimsFileConvert ' + \
          				'-i ' + os.path.join( Dir,
																			  subject,
																			  '03-Diffusion',
																			  '01-TopUpCorrection',
																			  str( directions[ key ]['nbDir'] ) + '_corrected_N4_Denoised.nii.gz ' ) + \
          				'-o ' + os.path.join( Dir,
																				subject,
																				'03-Diffusion',
																				'02-Dicom-to-Gis',
																				str( directions[ key ]['nbDir'] ) + '.ima ' )
        os.system( command )

        my_file = open(os.path.join( Dir,
				                        		 subject,
				                        		 '03-Diffusion',
				                        		 '02-Dicom-to-Gis',
				                        		 str( directions[ key ]['nbDir'] ) + '.dim' ),
				                        		 "w")

        string_list = [str(epi_matrix[0]) + \
				               ' ' + \
				               str(epi_matrix[1]) + \
				               ' ' + \
				               str(epi_matrix[2]) + \
				               ' ' + str( directions[ key ]['nbVolumes'] ) + '\n' + \
				               '-type FLOAT\n' + \
				               '-dx ' + str(epi_resolution[0]) + \
				               ' ' + \
				               '-dy ' + str(epi_resolution[1]) + \
				               ' ' + \
				               '-dz ' + str(epi_resolution[2]) + \
				               ' -dt ' + str( directions[ key ]['nbVolumes'] ) + '\n' + \
				               '-bo DCBA\n' + \
				               '-om binar\n']

        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()

        command = 'AimsFileConvert ' + \
          				'-i ' + os.path.join( Dir,
																			   subject,
																			   '03-Diffusion',
																			   '01-TopUpCorrection',
																			   str( directions[ key ]['nbDir'] ) + '_mask.nii.gz ' ) + \
          				'-o ' + os.path.join( Dir,
																			   subject,
																			   '03-Diffusion',
																			   '02-Dicom-to-Gis',
																			   str( directions[ key ]['nbDir'] ) + '_mask.ima ' ) + \
          				'-t S16'
        os.system( command )

        my_file = open(os.path.join( Dir,
				                        		 subject,
				                        		 '03-Diffusion',
				                        		 '02-Dicom-to-Gis',
				                        		 str( directions[ key ]['nbDir'] ) + '_mask.dim' ),
				                        		 "w")

        string_list = [str(epi_matrix[0]) + \
				               ' ' + \
				               str(epi_matrix[1]) + \
				               ' ' + \
				               str(epi_matrix[2]) + \
				               ' 1\n' + \
				               '-type S16\n' + \
				               '-dx ' + str(epi_resolution[0]) + \
				               ' ' + \
				               '-dy ' + str(epi_resolution[1]) + \
				               ' ' + \
				               '-dz ' + str(epi_resolution[2]) + \
				               ' -dt 1\n' + \
				               '-bo DCBA\n' + \
				               '-om binar\n']

        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()

        command = 'cp -f ' + \
				          os.path.join( Dir,
																subject,
																'03-Diffusion',
																'01-TopUpCorrection',
																str( directions[ key ]['nbDir'] ) + '_corrected.eddy_rotated_bvecs ' ) + \
				          os.path.join( Dir,
																subject,
																'03-Diffusion',
				                        '02-Dicom-to-Gis',
																str( directions[ key ]['nbDir'] ) + '.bvec' )
        os.system( command )

        command = 'cp -f ' + \
				          os.path.join( Dir,
																subject,
																'03-Diffusion',
																'01-TopUpCorrection',
																str( directions[ key ]['nbDir'] ) + '.bval ' ) + \
				          os.path.join( Dir,
																subject,
																'03-Diffusion',
				                        '02-Dicom-to-Gis',
																str( directions[ key ]['nbDir'] ) + '.bval' )
        os.system( command )

        command = 'rm -rf ' + \
				          os.path.join( Dir,
																subject,
																'03-Diffusion',
				                        '02-Dicom-to-Gis',
																'*.minf' )
        os.system( command )

        print( 'Nifti to Gis Conversion ' + str( directions[ key ]['nbDir'] ) + ' : Done! ' )

    #-----------------------------------------------------------------------------
    # DWIAndQSpace
    #-----------------------------------------------------------------------------

    parameterValues = {
      '_algorithmName' : 'DWI-Data-Import-And-QSpace-Sampling',
      '_subjectName' : '',
      'acqpFileNames' : '',
      'applyVisuCoreTransformation' : 0,
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
      'phaseAxis' :0,
      'qSpaceSamplingType' : 3,
      'sliceAxis' : 0,
      'visuParsFileNames' : ''
    }
    
    dwiFile = os.path.join( Dir,
														subject,
														'03-Diffusion',
														'02-Dicom-to-Gis',
														'dw_01.ima;' ) + \
              os.path.join( Dir,
														subject,
														'03-Diffusion',
														'02-Dicom-to-Gis',
														'dw_02.ima;' ) + \
              os.path.join( Dir,
														subject,
														'03-Diffusion',
														'02-Dicom-to-Gis',
														'dw_03.ima' )
    
    bvalFile = os.path.join( Dir,
														 subject,
														 '03-Diffusion',
														 '02-Dicom-to-Gis',
														 'dw_01.bval;' ) + \
               os.path.join( Dir,
														 subject,
														 '03-Diffusion',
														 '02-Dicom-to-Gis',
														 'dw_02.bval;' ) + \
               os.path.join( Dir,
														 subject,
														 '03-Diffusion',
														 '02-Dicom-to-Gis',
														 'dw_03.bval' )

    bvecFile = os.path.join( Dir,
														 subject,
														 '03-Diffusion',
														 '02-Dicom-to-Gis',
														 'dw_01.bvec;' ) + \
               os.path.join( Dir,
														 subject,
														 '03-Diffusion',
														 '02-Dicom-to-Gis',
														 'dw_02.bvec;' ) + \
               os.path.join( Dir,
														 subject,
														 '03-Diffusion',
														 '02-Dicom-to-Gis',
														 'dw_03.bvec' )

    outputFolder = os.path.join( Dir,
                                 subject,
                                 '03-Diffusion',
                                 '03-DWIAndQSpace' )

    parameterValues[ 'fileNameDwi' ] = dwiFile
    parameterValues[ 'bValFileNames' ] = bvalFile
    parameterValues[ 'bVecFileNames' ] = bvecFile

    runGinkgo( parameterValues, outputFolder )

    print( 'QSpace Sampling ' + subject + ' : Done! ' )

    #-----------------------------------------------------------------------------
    # NODDI analysis
    #-----------------------------------------------------------------------------

    t2 = os.path.join( Dir,
                       subject,
                       '03-Diffusion',
                       '03-DWIAndQSpace',
                       't2.ima ' )

    data = os.path.join( Dir,
                         subject,
                         '03-Diffusion',
                         '03-DWIAndQSpace',
                         'dw.ima ' )

    mask = os.path.join( Dir,
												 subject,
												 '03-Diffusion',
												 '02-Dicom-to-Gis',
												 'dw_01_mask.ima ' )
    
    outputDir = os.path.join( Dir,
                              subject,
                              '03-Diffusion',
                              '05-NODDI' )

    command = 'GkgExecuteCommand DwiMicrostructureField ' + \
              '-t2 ' + t2 + \
              '-dw ' + data + \
              '-m '+ mask + \
              '-type noddi_microstructure_cartesian_field ' + \
              '-f gfa ' + \
              ' intracellular_fraction ' + \
              ' isotropic_fraction ' + \
              ' kappa ' + \
              ' orientation_dispersion ' + \
              ' rgb ' + \
              ' stationary_fraction ' + \
              ' -o ' + os.path.join( outputDir,
                                     subject + '_gfa.ima ' ) + \
                       os.path.join( outputDir,
                                     subject + '_intracellular_fraction.ima ' ) + \
                       os.path.join( outputDir,
                                     subject + '_isotropic_fraction.ima ' ) + \
                       os.path.join( outputDir,
                                     subject + '_kappa.ima ' ) + \
                       os.path.join( outputDir,
                                     subject + '_orientation_dispersion.ima ' ) + \
                       os.path.join( outputDir,
                                     subject + '_rgb.ima ' ) + \
                       os.path.join( outputDir,
                                     subject + '_stationary_fraction.ima ' ) + \
              ' -scalarParameters 0.0 0.5   0.0 1.7e-9 3.0e-9 0.0 ' + \
                                 '0.0 0.0   0.0 0.0,   0.0,   0.0 ' + \
                                 '1.0 1.0 100   3.0e-9 4.0e-9 1.0 ' + \
                                 '0.1 0.1   1.0 0.2e-9 0.2e-9 0.1 ' + \
                                 '0   0     0   1      1      1 0 ' + \
                                 '0.03 ' + \
                                 '1 5 ' + \
                                 '1 1000 0.001 ' + \
                                 '0 500 500 50 1000 ' + \
              ' -stringParameters watson '  + \
              ' -verbose true '
  
    os.system( command )

    print( 'NODDI Analysis ' + subject + ' : Done! ' )

    #-----------------------------------------------------------------------------
    # Normalize data
    #-----------------------------------------------------------------------------
    contrasts = [ 'gfa', 'intracellular_fraction',
									'isotropic_fraction', 'kappa',
									'orientation_dispersion', 'rgb',
									'stationary_fraction' ]

    command = 'GkgExecuteCommand Gis2NiftiConverter ' + \
							'-i ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'04-LocalModelling_DTI',
						                        'dti_diffusion_weighted_t2.ima ' ) + \
							'-o ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'06-ProcessedData',
						                         subject + '_t2.nii.gz ' )
    os.system( command )

    command = 'GkgExecuteCommand Flipper ' + \
							'-i ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'06-ProcessedData',
						                         subject + '_t2.nii.gz ' ) + \
							'-o ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'06-ProcessedData',
						                         subject + '_t2.nii.gz ' ) + \
							'-t yz '
    os.system( command )

    command = 'GkgExecuteCommand Flipper ' + \
							'-i ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'06-ProcessedData',
						                         subject + '_t2.nii.gz ' ) + \
							'-o ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'06-ProcessedData',
						                         subject + '_t2.nii.gz ' ) + \
							'-t z '
    os.system( command )

    for con in contrasts:
        print( 'conversion and normalization of ' + con + ' ' + subject )
        if con == 'rgb':
        	command = 'AimsSplitRgb ' + \
										'-i ' + os.path.join( Dir,
																					subject,
																					'03-Diffusion',
																					'05-NODDI',
							                             subject + '_' + str(con) + '.ima ' ) + \
										'-o ' + os.path.join( Dir,
																			subject,
																			'03-Diffusion',
																			'06-ProcessedData',
		                                   subject + '_' + str(con) )
        	os.system( command )

        	channels = ['r', 'g', 'b']
        	for cha in channels:
        	  command = 'GkgExecuteCommand Gis2NiftiConverter ' + \
											'-i ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '_' + cha + '.ima ' ) + \
											'-o ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '_' + cha + '.nii.gz ' )
        	  os.system( command )


        	  command = 'GkgExecuteCommand Flipper ' + \
											'-i ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '_' + cha + '.nii.gz ' ) + \
											'-o ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '_' + cha + '.nii.gz ' ) + \
											'-t yz '
        	  os.system( command )

        	  command = 'GkgExecuteCommand Flipper ' + \
											'-i ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '_' + cha + '.nii.gz ' ) + \
											'-o ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '_' + cha + '.nii.gz ' ) + \
											'-t z '
        	  os.system( command )

        else:
        	command = 'GkgExecuteCommand Gis2NiftiConverter ' + \
								    '-i ' + os.path.join( Dir,
																					subject,
																					'03-Diffusion',
																					'05-NODDI',
								                           subject + '_' + str(con) + '.ima ' ) + \
								    '-o ' + os.path.join( Dir,
																					subject,
																					'03-Diffusion',
																					'06-ProcessedData',
								                           subject + '_' + str(con) + '.nii.gz ' )

        	os.system( command )

        	command = 'GkgExecuteCommand Flipper ' + \
											'-i ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '.nii.gz ' ) + \
											'-o ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '.nii.gz ' ) + \
											'-t yz '
        	os.system( command )

        	command = 'GkgExecuteCommand Flipper ' + \
											'-i ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '.nii.gz ' ) + \
											'-o ' + os.path.join( Dir,
																						subject,
																						'03-Diffusion',
																						'06-ProcessedData',
										                         subject + '_' + str(con) + '.nii.gz ' ) + \
											'-t z '
        	os.system( command )

        command = 'rm -rf ' + \
									os.path.join( Dir,
																subject,
																'03-Diffusion',
																'06-ProcessedData',
										            '*.ima ' ) + \
									os.path.join( Dir,
																subject,
																'03-Diffusion',
																'06-ProcessedData',
										            '*.ima.minf ' ) + \
									os.path.join( Dir,
																subject,
																'03-Diffusion',
																'06-ProcessedData',
										            '*.dim ' )
        os.system( command )

    #-----------------------------------------------------------------------------
    # Local Modelling Make Directories and Inputs
    #-----------------------------------------------------------------------------

    parameterValues ={
      '_algorithmName' : 'DWI-Local-Modeling',
      '_subjectName' : '',
      'aqbiLaplaceBeltramiSharpeningFactor' : 0.0,
      'aqbiMaximumSHOrder' : 8,
      'aqbiRegularizationLcurveFactor' : 0.006,
      'computeOdfVolume' : 0,
      'dotEffectiveDiffusionTime' : 25.0,
      'dotMaximumSHOrder' : 8,
      'dotOdfComputation' : 2,
      'dotR0' : 12.0,
      'dsiFilteringDataBeforeFFT' : 2,
      'dsiMarginalOdf' : 2,
      'dsiMaximumR0' : 15.0,
      'dsiMinimumR0' : 1.0,
      'dtiEstimatorType' : 0,
      'fileNameDw' : '',
      'fileNameMask' : '',
      'fileNameT1' : '',
      'fileNameT2' : '',
      'fileNameTransformationDwToT1' : '',
      'odfType' : 7,
      'outputOrientationCount' : 500,
      'outputWorkDirectory' : '',
      'qbiEquatorPointCount' : 50,
      'qbiPhiFunctionAngle' : 0.0,
      'qbiPhiFunctionMaximumAngle' : 0.0,
      'qbiPhiFunctionType' : 0,
      'rgbScale' : 1.0,
      'saAqbiLaplaceBeltramiSharpeningFactor' : 0.0,
      'saAqbiMaximumSHOrder' : 8,
      'saAqbiRegularizationLcurveFactor' : 0.006,
      'sdFilterCoefficients' : '1 1 1 0.5 0.1 0.02 0.002 0.0005 0.0001 0.0001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001',
      'sdKernelLowerFAThreshold' : 0,
      'sdKernelType' : 0,
      'sdKernelUpperFAThreshold' : 1,
      'sdKernelVoxelCount' : 300,
      'sdMaximumSHOrder' : 8,
      'sdUseCSD' : 0,
      'sdtKernelLowerFAThreshold' : 0,
      'sdtKernelType' : 0,
      'sdtKernelUpperFAThreshold' : 1,
      'sdtKernelVoxelCount' : 300,
      'sdtMaximumSHOrder' : 8,
      'sdtRegularizationLcurveFactor' : 0.006,
      'sdtUseCSD' : 0,
      'viewType' : 5
    }

    mask = os.path.join( Dir,
												 subject,
												 '03-Diffusion',
												 '02-Dicom-to-Gis',
												 'dw_01_mask.ima' )

    t1 = os.path.join( Dir,
                       subject,
											 '03-Diffusion',
                       '03-DWIAndQSpace',
                       't2.ima ' )

    t2 = os.path.join( Dir,
                       subject,
											 '03-Diffusion',
                       '03-DWIAndQSpace',
                       't2.ima ' )

    data = os.path.join( Dir,
                         subject,
											   '03-Diffusion',
                         '03-DWIAndQSpace',
                         'dw.ima ' )

    outputFolder = os.path.join( Dir,
											   				 subject,
											   				 '03-Diffusion',
											   				 '04-LocalModelling_DTI' )

    parameterValues[ 'fileNameDw' ] = data
    parameterValues[ 'fileNameMask' ] = mask
    parameterValues[ 'fileNameT1' ] = t1
    parameterValues[ 'fileNameT2' ] = t2
    parameterValues[ 'fileNameTransformationDwToT1' ] = trm
    parameterValues[ 'outputWorkDirectory' ] = outputFolder

    runGinkgo( parameterValues, outputFolder )

    print( 'Local Modelling ' + subject + ' : Done! ' )

    #-----------------------------------------------------------------------------
    # Tractography SRD 1 Seeds Make Directories and Inputs
    #-----------------------------------------------------------------------------

    command = 'GkgExecuteCommand Binarizer ' + \
							'-i ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'05-NODDI',
																		subject +'_isotropic_fraction.ima ' ) + \
							'-o ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'07-Tractography_SRD_1seed',
																		'isotropic_fraction_bin.ima ' ) + \
							'-m ge ' + \
							'-t1 0.1'
    os.system( command )

    command = 'AimsReplaceLevel ' + \
							'-i ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'07-Tractography_SRD_1seed',
																		'isotropic_fraction_bin.ima ' ) + \
							'-o ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'07-Tractography_SRD_1seed',
																		'isotropic_fraction_bin.ima ' ) + \
							'-g 0 1 ' + \
							'-n 1 0'
    os.system( command )

    command = 'cartoLinearComb.py ' + \
							'-i ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'02-Dicom-to-Gis',
																		'dw_01_mask.ima ' ) + \
											os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'07-Tractography_SRD_1seed',
																		'isotropic_fraction_bin.ima ' ) + \
							'-o ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'07-Tractography_SRD_1seed',
																		'tractoMask.ima ' ) + \
							'-f I1*I2'
    os.system( command )

    command = 'AimsFileConvert ' + \
							'-i ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'07-Tractography_SRD_1seed',
																		'tractoMask.ima ' ) + \
							'-o ' + os.path.join( Dir,
																		subject,
																		'03-Diffusion',
																		'07-Tractography_SRD_1seed',
																		'tractoMask.ima ' ) + \
							'-t S16'
    os.system( command )

    command = 'GkgExecuteCommand DwiTractography' + \
            	' -s ' + os.path.join( Dir,
                               		 	 subject,
                               		 	 '03-Diffusion',
                               		 	 '04-LocalModelling_DTI',
                               		 	 'dti_odf_site_map.sitemap' ) + \
            	' -o ' + os.path.join( Dir,
                               		 	 subject,
                               		 	 '03-Diffusion',
                               		 	 '04-LocalModelling_DTI',
                               		 	 'dti_odf_texture_map.texturemap' ) + \
            	' -r ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																	   'tractoMask.ima ' ) + \
            	' -m ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																	   'tractoMask.ima ' ) + \
            	' -type streamline-regularized-deterministic ' + \
            	' -b ' + os.path.join( Dir,
                               		 	 subject,
                               		 	 '03-Diffusion',
                               		 	 '07-Tractography_SRD_1seed',
                               		 	 subject ) + \
            	' -scalarParameters 8 0.4 10 5 300.0 30.0 0.0 0.001 ' + \
            	' -outputOrientationCount 500 ' + \
            	' -stepCount 1 ' + \
            	' -bundleMapFormat aimsbundlemap ' + \
            	' -verbose '
    print( command )
    os.system( command )

    command = 'GkgAntsRegistration3d' + \
							' -r ' + template_tracto + \
							' -m ' + mask_tracto + \
							' -f ' + os.path.join( Dir,
                               		   subject,
                               		   '03-Diffusion',
                               		   '03-DWIAndQSpace',
                               		   't2.ima' ) + \
							' -M ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																		 'tractoMask.ima ' ) + \
							' -d ' + os.path.join( Dir,
                               		   subject,
                               		   '03-Diffusion',
                               		   '07-Tractography_SRD_1seed',
                               		   'direct') + \
							' -i ' + os.path.join( Dir,
                               		   subject,
                               		   '03-Diffusion',
                               		   '07-Tractography_SRD_1seed',
                               		   'inverse') + \
							' -t affine_and_diffeomorphic'
    os.system( command )

    command = 'GkgExecuteCommand DwiBundleOperator' + \
              ' -i ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																		 subject + '.bundles' ) + \
              ' -o ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																		 subject + '-to-template.bundles' ) + \
              ' -op transform3d' + \
              ' -stringParameters ' + os.path.join( Dir,
                               		   							 subject,
                               		   							 '03-Diffusion',
                               		   							 '07-Tractography_SRD_1seed',
                               		   							 'direct.trm ' ) + \
																		 os.path.join( Dir,
                               		   							 subject,
                               		   							 '03-Diffusion',
                               		   							 '07-Tractography_SRD_1seed',
                               		   							 'direct.ima ') + \
																		 os.path.join( Dir,
                               		   							 subject,
                               		   							 '03-Diffusion',
                               		   							 '07-Tractography_SRD_1seed',
                               		   							 'inverse.ima ')
    os.system( command )

    command = 'GkgExecuteCommand DwiBundleOperator' + \
              ' -i ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																		 subject + '-to-template.bundles' ) + \
              ' -o ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																		 subject + '-to-anat.bundles' ) + \
              ' -op transform3d' + \
              ' -stringParameters ' + diff_to_anat_affine + ' ' + \
																			diff_to_anat_direct + ' ' + \
																			diff_to_anat_inverse
    os.system( command )

    command = 'GkgExecuteCommand DwiBundleOperator' + \
              ' -i ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																		 subject + '-to-anat.bundles' ) + \
              ' -o ' + os.path.join( Dir,
																		 subject,
																		 '03-Diffusion',
																		 '07-Tractography_SRD_1seed',
																		 subject + '-to-anat.bundles' ) + \
              ' -op transform3d' + \
              ' -stringParameters ' + os.path.join( Dir,
																										'Turone_Equine_Social_Brain_Dataset',
																										'Turone_Equine_Brain_Atlas_and_Templates',
																										'anat',
																										'GisFormat',
																										'correction.trm' )
    os.system( command )
    """
    contrasts = [ 'gfa', 'rgb_b',
								 'intracellular_fraction', 'rgb_g',
								 'isotropic_fraction','rgb_r',
								 'kappa','stationary_fraction',
								 'orientation_dispersion']

    for con in contrasts:
        print( 'Spatial normalization of ' + con + ' ' + subject )

        if con == 'rgb_g' or 'rgb_b' or 'rgb_r':

        	command = 'antsApplyTransforms ' + \
										'-d 3 ' + \
										'-e 0 ' + \
										'-i ' + os.path.join( Dir,
																			 		subject,
																			 		'03-Diffusion',
																			 		'06-ProcessedData',
																			 		subject + '_' +  con + '.nii.gz ' ) + \
										'-o ' + os.path.join( Dir,
																			 		'03-NODDI_GroupAnalysis',
																			 		'00-data',
																			 		'NODDI',
																			 		subject + '_' + group + '_' + sex + '_' +  con + '.nii.gz ' ) + \
										'-n NearestNeighbor ' + \
										'-r ' + os.path.join( Dir,
																			 		'Turone_Equine_Social_Brain_Dataset',
																			 		'transformations',
																			 		'diff',
																			 		'tractography',
																			 		'template.nii.gz ' ) + \
										'-t ' + os.path.join( Dir,
																			 		'Turone_Equine_Social_Brain_Dataset',
																			 		'transformations',
																			 		'diff',
																			 		'tractography',
																			 		subject + '_t2_1Warp.nii.gz ' ) + \
														os.path.join( Dir,
																			 		'Turone_Equine_Social_Brain_Dataset',
																			 		'transformations',
																			 		'diff',
																			 		'tractography',
																			 		subject + '_t2_0GenericAffine.mat' )
        	os.system( command )

        	command = 'AimsFileConvert ' + \
										'-i ' + os.path.join( Dir,
																			 		'03-NODDI_GroupAnalysis',
																			 		'00-data',
																			 		'NODDI',
																			 		subject + '_' + group + '_' + sex + '_' +  con + '.nii.gz ' ) + \
										'-o ' + os.path.join( Dir,
																			 		'03-NODDI_GroupAnalysis',
																			 		'00-data',
																			 		'NODDI',
																			 		subject + '_' + group + '_' + sex + '_' +  con + '.nii.gz ' ) + \
										'-t U8 '
        	os.system( command )

        else:
        	command = 'antsApplyTransforms ' + \
										'-d 3 ' + \
										'-e 0 ' + \
										'-i ' + os.path.join( Dir,
																			 		subject,
																			 		'03-Diffusion',
																			 		'06-ProcessedData',
																			 		subject + '_' +  con + '.nii.gz ' ) + \
										'-o ' + os.path.join( Dir,
																			 		'03-NODDI_GroupAnalysis',
																			 		'00-data',
																			 		'NODDI',
																			 		subject + '_' + group + '_' + sex + '_' +  con + '.nii.gz ' ) + \
										'-n Linear ' + \
										'-r ' + os.path.join( Dir,
																			 		'Turone_Equine_Social_Brain_Dataset',
																			 		'transformations',
																			 		'diff',
																			 		'tractography',
																			 		'template.nii.gz ' ) + \
										'-t ' + os.path.join( Dir,
																			 		'Turone_Equine_Social_Brain_Dataset',
																			 		'transformations',
																			 		'diff',
																			 		'tractography',
																			 		subject + '_t2_1Warp.nii.gz ' ) + \
														os.path.join( Dir,
																			 		'Turone_Equine_Social_Brain_Dataset',
																			 		'transformations',
																			 		'diff',
																			 		'tractography',
																			 		subject + '_t2_0GenericAffine.mat' )

        	os.system( command )

    print( 'Tractography ' + subject + ' : Done! ' )

    print( 'Preprocessing of ' + subject + ' : Done! ' )
