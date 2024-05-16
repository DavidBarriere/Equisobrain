import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'gkg', 'python' ) )
import os, json, sys, shutil
import nilearn
from nilearn import image
import numpy as np
import nibabel as nib
import pandas as pd

from CopyFileDirectoryRm import *

def runFuncPreproccessing( Dir,
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
                           verbose ):
                      
  
  if ( verbose == True ):

    #-----------------------------------------------------------------------------
    # Make Directories & Inputs
    #-----------------------------------------------------------------------------

    makedir( os.path.join( Dir,
                           subject,
                           '04-Functional' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '04-Functional',
                           '01-SliceTimingCorrection' ) )


    makedir( os.path.join( Dir,
                           subject,
                           '04-Functional',
                           '02-TopUpCorrection' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '04-Functional',
                           '03-MotionCorrection' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '04-Functional',
                           '04-SpatialNormalization' ) )

    makedir( os.path.join( Dir,
                           subject,
                           '04-Functional',
                           '05-SignalRegression' ) )

    makedir( os.path.join( Dir,
                           '04-fMRI_GroupAnalysis' ) )

    makedir( os.path.join( Dir,
                           '04-fMRI_GroupAnalysis',
                           '00-data' ) )

    makedir( os.path.join( Dir,
                           '04-fMRI_GroupAnalysis',
                           '01-ALFF' ) )                          
                           
    ST_data = os.path.join( Dir,
                            subject,
                            '04-Functional',
                            '01-SliceTimingCorrection' )

    TopUp_data = os.path.join( Dir,
                               subject,
                               '04-Functional',
                               '02-TopUpCorrection' )

    MoCorr_data = os.path.join( Dir,
                                subject,
                                '04-Functional',
                                '03-MotionCorrection' )

    SpatNorm_data = os.path.join( Dir,
                               		subject,
                               		'04-Functional',
                               		'04-SpatialNormalization' )

    CompCorr_data = os.path.join( Dir,
                               		subject,
                               		'04-Functional',
                               		'05-SignalRegression' )

    Turone_Data = os.path.join( Dir,
    														'Turone_Equine_Social_Brain_Dataset',
    														subject,
    														'func')
    Topup_parameters_RL = os.path.join( Dir,
																			  'Turone_Equine_Social_Brain_Dataset',
																			  'topup_parameters_RL.txt')

    TopUp_Params_AP = os.path.join( Dir,
    														 		'Turone_Equine_Social_Brain_Dataset',
    														 		'topup_parameters_AP.txt')

    fMRI_GroupAnalysis_Folder = os.path.join( Dir,
																		         '04-fMRI_GroupAnalysis',
																		         '00-data' ) 

    ALFF_Data = os.path.join( Dir,
															'04-fMRI_GroupAnalysis',
															'01-ALFF' )
    #-------------------------------------------------------------------------
    # Functional Data Preprocessing
    #-------------------------------------------------------------------------

    print( 'Run Slice Timing Correction...' )

    if Encoding_Direction == 1 :
        command = 'slicetimer ' + \
				          '-i ' + os.path.join( Turone_Data,
				          											subject + '_task-restingstate_acq-*.nii.gz ' ) + \
				          '-o ' + os.path.join( ST_data,
				          											'fc.nii.gz ' ) + \
				          '-d 1 ' + \
				          '-r 3.97 ' + \
				          '--odd '

        os.system( command )

    else:
        command = 'slicetimer ' + \
				          '-i ' + os.path.join( Turone_Data,
				          											subject + '_task-restingstate_acq-*.nii.gz ' ) + \
				          '-o ' + os.path.join( ST_data,
				          											'fc.nii.gz ' ) + \
				          '-d 2 ' + \
				          '-r 3.97 ' + \
				          '--odd '

        os.system( command )
    
    print( 'Done' )

    print( 'Run TopUp Correction...' )

    if TopUp_Protocol == 1:
        command = 'fslmerge ' + \
									'-t ' + \
									os.path.join( TopUp_data,
																'fc_TopUp.nii.gz ' ) + \
									os.path.join( Turone_Data,
																subject + '_task-topup_acq-LR_bold.nii.gz ' ) + \
									os.path.join( Turone_Data,
																subject + '_task-topup_acq-RL_bold.nii.gz ' )

        os.system( command )

        command = 'topup ' + \
									'--imain=' + os.path.join( TopUp_data,
																						 'fc_TopUp.nii.gz ' ) + \
									'--datain=' + Topup_parameters_RL + \
									' --fwhm=0 ' + \
									'--config=b02b0.cnf ' + \
									'--out=' + os.path.join( TopUp_data,
																					 'TopUp_results' )
        os.system( command )

        command = 'applytopup ' + \
									'--imain=' + os.path.join( ST_data,
																						 'fc.nii.gz ' ) + \
									'--datain=' + Topup_parameters_RL + \
									' --inindex=1 ' + \
									'--topup=' + os.path.join( TopUp_data,
																						 'TopUp_results ' ) + \
									'--method=jac ' + \
									'--interp=spline ' + \
									'--out=' + os.path.join( TopUp_data,
																					 'fc.nii.gz ' )
        os.system( command )

        command = 'AimsSubVolume ' + \
									'-i ' + os.path.join( TopUp_data,
																				'fc.nii.gz ' ) + \
									'-o ' + os.path.join( TopUp_data,
																				subject +	'_rs.nii.gz ' ) + \
									'-x 10 ' + \
									'-X 101 ' + \
									'-y 35 ' + \
									'-Y 110'
        os.system( command )

        command = 'ImageMath 4 ' + \
				           os.path.join( TopUp_data,
									    					 subject +	'_rs_Normalized.nii.gz ' ) + \
				          'RescaleImage ' + \
				           os.path.join( TopUp_data,
									    					 subject +	'_rs.nii.gz ' ) + \
				          '0 ' + \
				          '1000 '

        os.system( command )

        command = 'antsMotionCorr ' + \
				          '-d 3 ' + \
				          '-a ' + os.path.join( TopUp_data,
									    					 				subject +	'_rs_Normalized.nii.gz ' ) + \
				          '-o ' + os.path.join( TopUp_data,
				          										  subject +	'_rs_avg.nii.gz ' )

        os.system( command )

    if TopUp_Protocol == 2:

        command = 'fslmerge ' + \
									'-t ' + \
									os.path.join( TopUp_data,
				          							'fc_TopUp.nii.gz ' ) + \
									os.path.join( Turone_Data,
				          							subject + '_task-topup_acq-RL_bold.nii.gz ' ) + \
									os.path.join( Turone_Data,
				          							subject + '_task-topup_acq-LR_bold.nii.gz ' )

        os.system( command )

        command = 'topup ' + \
									'--imain=' + os.path.join( TopUp_data,
				          											     'fc_TopUp.nii.gz ' ) + \
									'--datain=' + Topup_parameters_RL + \
									' --fwhm=0 ' + \
									'--config=b02b0.cnf ' + \
									'--out=' + os.path.join( TopUp_data,
				          											   'TopUp_results' )
        os.system( command )
		  
        command = 'applytopup ' + \
									'--imain=' + os.path.join( ST_data,
				          										  		 'fc.nii.gz ' ) + \
									'--datain=' + Topup_parameters_RL + \
									' --inindex=1 ' + \
									'--topup=' + os.path.join( TopUp_data,
				          											     'TopUp_results ' ) + \
									'--method=jac ' + \
									'--interp=spline ' + \
									'--out=' + os.path.join( TopUp_data,
				          											   'fc.nii.gz ' )
        os.system( command )

        command = 'AimsSubVolume ' + \
									'-i ' + os.path.join( TopUp_data,
				          											'fc.nii.gz ' ) + \
				          '-o ' + os.path.join( TopUp_data,
				          										  subject +	'_rs.nii.gz ' ) + \
				          '-x 10 ' + \
				          '-X 101 ' + \
				          '-y 35 ' + \
				          '-Y 110'
		            
        os.system( command )

        command = 'ImageMath 4 ' + \
				           os.path.join( TopUp_data,
									    					 subject +	'_rs_Normalized.nii.gz ' ) + \
				          'RescaleImage ' + \
				           os.path.join( TopUp_data,
									    					 subject +	'_rs.nii.gz ' ) + \
				          '0 ' + \
				          '1000 '

        os.system( command )

        command = 'antsMotionCorr ' + \
				          '-d 3 ' + \
				          '-a ' + os.path.join( TopUp_data,
									    					 				subject +	'_rs_Normalized.nii.gz ' ) + \
				          '-o ' + os.path.join( TopUp_data,
				          										  subject +	'_rs_avg.nii.gz ' )

        os.system( command )

    if TopUp_Protocol == 3:

        command = 'fslmerge ' + \
									'-t ' + \
									os.path.join( TopUp_data,
				          							'fc_TopUp.nii.gz ' ) + \
									os.path.join( Turone_Data,
				          							subject + '_task-topup_acq-AP_bold.nii.gz ' ) + \
									os.path.join( Turone_Data,
				          							subject + '_task-topup_acq-PA_bold.nii.gz ' )

        os.system( command )

        command = 'topup ' + \
									'--imain=' + os.path.join( TopUp_data,
				          											     'fc_TopUp.nii.gz ' ) + \
									'--datain=' + TopUp_Params_AP + \
									' --fwhm=0 ' + \
									'--config=b02b0.cnf ' + \
									'--out=' + os.path.join( TopUp_data,
				          											   'TopUp_results' )
        os.system( command )
		  
        command = 'applytopup ' + \
									'--imain=' + os.path.join( ST_data,
				          										  		 'fc.nii.gz ' ) + \
									'--datain=' + TopUp_Params_AP + \
									' --inindex=1 ' + \
									'--topup=' + os.path.join( TopUp_data,
				          											     'TopUp_results ' ) + \
									'--method=jac ' + \
									'--interp=spline ' + \
									'--out=' + os.path.join( TopUp_data,
				          											   'fc.nii.gz ' )
        os.system( command )

        command = 'AimsSubVolume ' + \
									'-i ' + os.path.join( TopUp_data,
					        											'fc.nii.gz ' ) + \
					        '-o ' + os.path.join( TopUp_data,
					        										  subject +	'_rs.nii.gz ' ) + \
					        '-x 10 ' + \
					        '-X 101 ' + \
					        '-y 35 ' + \
					        '-Y 110'
        os.system( command )

        command = 'ImageMath 4 ' + \
				           os.path.join( TopUp_data,
									    					 subject +	'_rs_Normalized.nii.gz ' ) + \
				          'RescaleImage ' + \
				           os.path.join( TopUp_data,
									    					 subject +	'_rs.nii.gz ' ) + \
				          '0 ' + \
				          '1000 '

        os.system( command )

        command = 'antsMotionCorr ' + \
				          '-d 3 ' + \
				          '-a ' + os.path.join( TopUp_data,
									    					 				subject +	'_rs_Normalized.nii.gz ' ) + \
				          '-o ' + os.path.join( TopUp_data,
				          										  subject +	'_rs_avg.nii.gz ' )

        os.system( command )

    print( 'Done' )

    print( 'Run Motion Correction...' )
    command = 'AimsFlip ' + \
              '-i ' + os.path.join( TopUp_data,
									    					 		subject +	'_rs_Normalized.nii.gz ' ) + \
              '-o ' + os.path.join( MoCorr_data,
              											'fc.nii.gz ' ) + \
              '-m YZ'
    os.system( command )

    command = 'AimsFlip ' + \
              '-i ' + os.path.join( MoCorr_data,
              											'fc.nii.gz ' ) + \
              '-o ' + os.path.join( MoCorr_data,
              											'fc.nii.gz ' ) + \
              '-m ZZ'
    os.system( command )

    command = 'AimsFlip ' + \
              '-i ' + os.path.join( TopUp_data,
									    					 		subject +	'_rs_avg.nii.gz ' ) + \
              '-o ' + os.path.join( MoCorr_data,
              											'fc_avg.nii.gz ' ) + \
              '-m YZ'
    os.system( command )

    command = 'AimsFlip ' + \
              '-i ' + os.path.join( MoCorr_data,
              											'fc_avg.nii.gz ' ) + \
              '-o ' + os.path.join( MoCorr_data,
              											'fc_avg.nii.gz ' ) + \
              '-m ZZ'
    os.system( command )

    command = 'antsMotionCorr ' + \
              '-d 3 ' + \
              "-m GC[" + os.path.join( MoCorr_data,
              												 'fc_avg.nii.gz, ' ) + \
              os.path.join( MoCorr_data,
              							"fc.nii.gz,1,1,Random,0.05] " ) + \
              "-t Affine[ 0.005 ] " + \
              "-o [" + os.path.join( MoCorr_data,
              											 subject + '_fc_,' ) + \
              				 os.path.join( MoCorr_data,
              											 subject + '_fc.nii.gz,' ) + \
              				 os.path.join( MoCorr_data,
              											 subject + "_fc_average.nii.gz] " ) + \
              '-i 20 ' + \
              '-u 1 ' + \
              '-e 1 ' + \
              '-s 0 ' + \
              '-f 1 ' + \
              '-n 3 ' + \
              '-w 1 '

    os.system( command )
    
    command = 'ImageMath 3 ' + \
							os.path.join( MoCorr_data,
              							subject + '_fixed.nii.gz ' ) + \
              'ReplicateImage ' + \
							os.path.join( MoCorr_data,
              							'fc_avg.nii.gz ' ) + \
              '250 ' + \
              '3.97 ' + \
              '0'

    os.system( command )

    command = 'antsRegistration ' + \
    					'-d 4 ' + \
    					'-r ' + os.path.join( MoCorr_data,
              							        subject + '_fc_Warp.nii.gz ' ) + \
    					"-o [" + os.path.join( MoCorr_data,
              											 subject + "_fc_mocor_," ) + \
              				 os.path.join( MoCorr_data,
              											 subject + "_fc_mocor_Warped.nii.gz ] " ) + \
    					'--interpolation Linear ' + \
    					'--use-histogram-matching 1 ' + \
    					"--winsorize-image-intensities [0.005,0.995] " + \
    					"--transform SyN[0.1,3,0.0] " + \
    					"--metric meansquares[" + os.path.join( MoCorr_data,
              							                          subject + "_fixed.nii.gz," ) + \
              													os.path.join( MoCorr_data,
					        										                "fc.nii.gz] " ) + \
    					"--convergence [15x2,1e-6,4] " + \
    					'--shrink-factors 2x1 ' + \
    					'--smoothing-sigmas 1x0vox ' + \
    					'--restrict-deformation 1x1x1x0'

    os.system( command )
    
    command = 'antsMotionCorr ' + \
              '-d 3 ' + \
              '-a ' + os.path.join( MoCorr_data,
              											subject + '_fc_mocor_Warped.nii.gz ' ) + \
              '-o ' + os.path.join( MoCorr_data,
              											subject + '_fc_mocor_avg.nii.gz ' )

    os.system( command )

    print( 'Done' )

    print( 'Run Template Normalization...' )

    command = 'antsApplyTransforms ' + \
    					'-d 3 ' +  \
    					"-o [" + os.path.join( SpatNorm_data,
              										   subject + "_CollapsedWarp.nii.gz,1] " ) + \
    					'-t ' + DiffeoTransformation_02 + \
    					' -t ' + LinearTransformation_02 + \
    					' -t ' + DiffeoTransformation_01 + \
    					' -t ' + LinearTransformation_01 + \
    					' -r ' + template

    os.system( command )

    command = 'ImageMath 3 ' + \
    					os.path.join( SpatNorm_data,
              							subject + '_4DCollapsedWarp.nii.gz ' ) + \
              'ReplicateDisplacement ' + \
    					os.path.join( SpatNorm_data,
              							subject + '_CollapsedWarp.nii.gz ' ) + \
              '250 ' + \
              '3.97 ' + \
              '0'

    os.system( command )
    
    command = 'ImageMath 3 ' + \
							os.path.join( SpatNorm_data,
				      							'template_replicated.nii.gz ' ) + \
				      'ReplicateDisplacement ' + \
							template + \
				      ' 250 ' + \
				      '3.97 ' + \
				      '0'

    os.system( command )

    command = 'antsApplyTransforms ' + \
    					'-d 4 ' +  \
    					'-o ' + os.path.join( SpatNorm_data,
              										  'fc.nii.gz ' ) + \
    					'-t ' + os.path.join( MoCorr_data,
              											subject + '_fc_mocor_1Warp.nii.gz ' ) + \
    					'-t ' + os.path.join( MoCorr_data,
              											subject + '_fc_mocor_0Warp.nii.gz ' ) + \
    					'-t ' + os.path.join( SpatNorm_data,
              							        subject + '_4DCollapsedWarp.nii.gz ' ) + \
    					'-r ' + os.path.join( SpatNorm_data,
				      											'template_replicated.nii.gz ' ) + \
    					' -i ' + os.path.join( MoCorr_data,
					        									 'fc.nii.gz ' )

    os.system( command )

    print( 'Done' )

    print( 'Run Spatial Smoothing and Signal Regression...' )

    command = 'ImageMath ' + \
    					'4 ' + \
    					os.path.join( CompCorr_data,
              							'fc_CSF_WM.nii.gz ' ) + \
    					'ThreeTissueConfounds ' + \
    					os.path.join( SpatNorm_data,
              							'fc.nii.gz ' ) + \
    					seg + \
    					' 1 3'
    print ( command )
    os.system( command )

    command = 'ImageMath ' + \
    					'4 ' + \
    					os.path.join( CompCorr_data,
              							'fc_CompCorrAuto.nii.gz' ) + \
    					' CompCorrAuto ' + \
    					os.path.join( SpatNorm_data,
              							'fc.nii.gz ' ) + \
    					inverted_mask + \
    					' 6'
    print ( command )
    os.system( command )

    smoothed = nilearn.image.smooth_img( os.path.join( SpatNorm_data,
              																				 'fc.nii.gz' ),
																				 fwhm=None)

    nib.save(smoothed,os.path.join( CompCorr_data,
              											'fc.nii.gz' ))

    confound_01 = os.path.join( MoCorr_data,
              									subject + '_fc_MOCOparams.csv' )

    confound_02 = os.path.join( CompCorr_data,
              									'fc_CSF_WM_compcorr.csv' )

    confound_03 = os.path.join( CompCorr_data,
              									'fc_CompCorrAuto_compcorr.csv' )

    confounds=pd.concat([ pd.read_csv(confound_01),
                     			pd.read_csv(confound_02),
                     			pd.read_csv(confound_03)],
                     			axis= 1,
                     			ignore_index=False )	 

    confounds.to_csv( os.path.join( CompCorr_data,
						                  			'confounds.csv' )) 

    df = pd.read_csv( os.path.join( CompCorr_data,
						                			  'confounds.csv' ),
						         header=0,
						         delimiter=',')
	
    df = df.drop( df.columns[[0,1, 2,18]],
    							axis=1)

    df.to_csv( os.path.join( CompCorr_data,
						                 'confounds_cleaned.csv' )) 
						                  			
    x = nilearn.image.clean_img( imgs=os.path.join( CompCorr_data,
              																			'fc.nii.gz' ),
						                     runs=None,
						                     detrend=True,
						                     standardize=True,
						                     confounds=df,
						                     low_pass=0.1,
						                     high_pass=0.008,
						                     t_r=3.97,
						                     ensure_finite=False,
						                     mask_img=mask )
		                   
    nib.save(x, os.path.join( CompCorr_data,
						                  'fc_corrected.nii.gz' ))       

    command = 'mv -f ' + \
    					os.path.join( CompCorr_data,
						                'fc_corrected.nii.gz ' ) + \
    					os.path.join( fMRI_GroupAnalysis_Folder,
						                subject + '_fc.nii.gz')

    os.system( command )

    print( 'Done' )						  
    print( 'Preprocessing of ' + subject + ' Done ! ' )
    print( 'Preprocessed Data Are Available here : ' + fMRI_GroupAnalysis_Folder  )


    print( 'Running ALFF analysis' )						      
    print( 'Processing of ' + subject )
    print( 'Cleaning of ' + subject )

    command = 'fslroi ' + \
              os.path.join( fMRI_GroupAnalysis_Folder,
						                subject + '_fc.nii.gz ') + \
              os.path.join( ALFF_Data,
						                subject + '_fc_cleaned.nii.gz ') + \
              '15 ' + \
              '-1'

    os.system( command )

    print( 'Done' )						  
    print( "ALFF' Calculation for " + subject )
    command = 'chmod +x ' + os.path.join( Dir,
    																		  'createALFF.sh ' )
    os.system( command )

    command = './createALFF.sh ' + \
    					os.path.join( ALFF_Data,
						                subject + '_' + group + '_' + sex + '.nii.gz ') + \
						  os.path.join( ALFF_Data,
						                subject + '_fc_cleaned.nii.gz ' ) + \
							mask + \
							' 3.97 ' + \
							"0.01,0.08 "

    os.system( command )
    print( "Classical ALFF analysis (0.01,0.08 Hz) : Done" )						  

    command = './createALFF.sh ' + \
    					os.path.join( ALFF_Data,
						                subject + '_' + group + '_' + sex + '_slow-4.nii.gz ') + \
						  os.path.join( ALFF_Data,
						                subject + '_fc_cleaned.nii.gz ' ) + \
							mask + \
							' 3.97 ' + \
							"0.027,0.073 "

    os.system( command )
    print( "Slow-4 frequency analysis (0.027,0.073 Hz) : Done" )						  

    command = './createALFF.sh ' + \
    					os.path.join( ALFF_Data,
						                subject + '_' + group + '_' + sex + '_slow-5.nii.gz ') + \
						  os.path.join( ALFF_Data,
						                subject + '_fc_cleaned.nii.gz ' ) + \
							mask + \
							' 3.97 ' + \
							"0.01,0.027 "

    os.system( command )
    print( "Slow-5 frequency analysis (0.01,0.027 Hz) : Done" )						  

