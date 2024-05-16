import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'gkg', 'python' ) )

from CopyFileDirectoryRm import *

def runTopUpEddyCurrentsAndMotionsCorrections( Dir,
                                               subject,
                                               BrainTemplate,
                                               BrainMask,
                                               trm,
                                               trm_inv,
                                               verbose ):
                      
  
  if ( verbose == True ):

#-----------------------------------------------------------------------------
# Make Directories and Inputs
#-----------------------------------------------------------------------------

    makedir( os.path.join( Dir,
                           subject,
                           '02-Diffusion',
                           '01-TopUp' ) )


    dw_BlipUp = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '00-Dicom-to-Gis',
                              'dw_BlipUp')

    dw_BlipDown = os.path.join( Dir,
                                subject,
                                '02-Diffusion',
                                '00-Dicom-to-Gis',
                                'dw_BlipDown')

    t2_BlipUp = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '01-TopUp',
                              't2_BlipUp')

    t2_BlipDown = os.path.join( Dir,
                                subject,
                                '02-Diffusion',
                                '01-TopUp',
                                't2_BlipDown')

    t2_topUp = os.path.join( Dir,
                             subject,
                             '02-Diffusion',
                             '01-TopUp',
                             't2_topUp' )
    
    dw_Shell1 = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '00-Dicom-to-Gis',
                              'dw_01')

    dw_Shell2 = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '00-Dicom-to-Gis',
                              'dw_02')

    dw_Shell3 = os.path.join( Dir,
                              subject,
                              '02-Diffusion',
                              '00-Dicom-to-Gis',
                              'dw_03')
    
    topUpParameters = os.path.join( Dir,
                                    'topup_parameters.txt' )

    #---------------------------------------------------------------------------
    # Prepare Diffusion Data
    #---------------------------------------------------------------------------
    print( 'Prepare Diffusion Data...' )

    command = 'GkgExecuteCommand SubVolume' + \
              ' -i ' + dw_BlipUp + '.ima ' + \
              ' -o ' + dw_BlipUp + '.ima ' + \
              ' -z 0 ' + \
              ' -Z 55 ' + \
              ' -verbose'

    os.system( command )

    command = 'GkgExecuteCommand SubVolume' + \
              ' -i ' + dw_BlipDown + '.ima ' + \
              ' -o ' + dw_BlipDown + '.ima ' + \
              ' -z 0 ' + \
              ' -Z 55 ' + \
              ' -verbose'

    os.system( command )

    command = 'GkgExecuteCommand SubVolume' + \
              ' -i ' + dw_Shell1 + '.ima ' + \
              ' -o ' + dw_Shell1 + '.ima ' + \
              ' -z 0 ' + \
              ' -Z 55 ' + \
              ' -verbose'

    os.system( command )

    command = 'GkgExecuteCommand SubVolume' + \
              ' -i ' + dw_Shell2 + '.ima ' + \
              ' -o ' + dw_Shell2 + '.ima ' + \
              ' -z 0 ' + \
              ' -Z 55 ' + \
              ' -verbose'

    os.system( command )

    command = 'GkgExecuteCommand SubVolume' + \
              ' -i ' + dw_Shell3 + '.ima ' + \
              ' -o ' + dw_Shell3 + '.ima ' + \
              ' -z 0 ' + \
              ' -Z 55 ' + \
              ' -verbose'

    os.system( command )

    print( 'Done' )

    #---------------------------------------------------------------------------
    # Extract B0 Data
    #---------------------------------------------------------------------------

    print( 'Extract B0 Data...' )

    command = 'GkgExecuteCommand VolumeAverager' + \
              ' -i ' + dw_BlipUp + '.ima ' + \
              ' -o ' + t2_BlipUp + '.ima ' + \
              ' -verbose'
    
    os.system( command )

    command = 'GkgExecuteCommand VolumeAverager' + \
              ' -i ' + dw_BlipDown + '.ima ' + \
              ' -o ' + t2_BlipDown + '.ima ' + \
              ' -verbose'

    os.system( command )

    command = 'GkgExecuteCommand Cat' + \
              ' -i ' + t2_BlipUp + '.ima ' + \
                       t2_BlipDown + '.ima ' + \
              ' -o ' + t2_topUp + '.ima ' + \
              ' -t t ' + \
              ' -verbose'

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + t2_BlipUp + '.ima ' + \
              ' -o ' + t2_BlipUp + '.nii ' + \
              ' --verbose'

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + t2_BlipDown + '.ima ' + \
              ' -o ' + t2_BlipDown + '.nii ' + \
              ' --verbose'

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + t2_topUp + '.ima ' + \
              ' -o ' + t2_topUp + '.nii ' + \
              ' --verbose'

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + dw_Shell1 + '.ima ' + \
              ' -o ' + dw_Shell1 + '.nii ' + \
              ' --verbose'

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + dw_Shell2 + '.ima ' + \
              ' -o ' + dw_Shell2 + '.nii ' + \
              ' --verbose'

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + dw_Shell3 + '.ima ' + \
              ' -o ' + dw_Shell3 + '.nii ' + \
              ' --verbose'

    os.system( command )

    print( 'Done' )

    #---------------------------------------------------------------------------
    # TopUp Procedure
    #---------------------------------------------------------------------------

    print( 'TopUp Procedure...' )

    command = 'topup' + \
              ' --imain=' + t2_topUp + '.nii ' + \
              ' --datain=' + topUpParameters + \
              ' --config=b02b0.cnf ' + \
              ' --out=' + os.path.join( Dir,
                                        subject,
                                        '02-Diffusion',
                                        '01-TopUp',
                                        subject + '_topup_results' )

    os.system( command )

    print( 'Done' )

    #---------------------------------------------------------------------------
    # Apply TopUp Procedure
    #---------------------------------------------------------------------------

    print( 'Apply TopUp Procedure...' )

    command = 'applytopup' + \
              ' --imain=' + dw_Shell1 + '.nii ' + \
              ' --datain=' + topUpParameters + \
              ' --inindex=1 ' + \
              ' --topup=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '01-TopUp',
                                          subject + '_topup_results' ) + \
              ' --method=jac ' + \
              ' --interp=trilinear ' + \
              ' --out=' + os.path.join( Dir,
                                         subject,
                                         '02-Diffusion',
                                         '01-TopUp',
                                         'dw_01.nii' )

    os.system( command )

    command = 'applytopup' + \
              ' --imain=' + dw_Shell2 + '.nii ' + \
              ' --datain=' + topUpParameters + \
              ' --inindex=1 ' + \
              ' --topup=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '01-TopUp',
                                          subject + '_topup_results' ) + \
              ' --method=jac ' + \
              ' --interp=trilinear ' + \
              ' --out=' + os.path.join( Dir,
                                         subject,
                                         '02-Diffusion',
                                         '01-TopUp',
                                         'dw_02.nii' )

    os.system( command )

    command = 'applytopup' + \
              ' --imain=' + dw_Shell3 + '.nii ' + \
              ' --datain=' + topUpParameters + \
              ' --inindex=1 ' + \
              ' --topup=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '01-TopUp',
                                          subject + '_topup_results' ) + \
              ' --method=jac ' + \
              ' --interp=trilinear ' + \
              ' --out=' + os.path.join( Dir,
                                         subject,
                                         '02-Diffusion',
                                         '01-TopUp',
                                         'dw_03.nii' )

    os.system( command )

    command = 'applytopup' + \
              ' --imain=' + t2_BlipUp + '.nii ' + \
              ' --datain=' + topUpParameters + \
              ' --inindex=1 ' + \
              ' --topup=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '01-TopUp',
                                          subject + '_topup_results' ) + \
              ' --method=jac ' + \
              ' --interp=trilinear ' + \
              ' --out=' + t2_topUp + '_Corrected.nii '

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + t2_topUp + '_Corrected.nii.gz ' + \
              ' -o ' + t2_topUp + '_Corrected.ima ' + \
              ' -t S16 ' + \
              ' --verbose'

    os.system( command )

    print( 'Done' )

    #---------------------------------------------------------------------------
    # Create diffusion mask
    #---------------------------------------------------------------------------

    print( 'Create Diffusion Mask...' )

    command = 'GkgExecuteCommand Resampling3D ' + \
              ' -reference ' + t2_topUp + '_Corrected.nii.gz ' + \
              ' -size 128 56 128 ' + \
              ' -resolution 2 2.4 2 ' + \
              ' -transforms ' + trm + \
              ' -output ' + t2_topUp + '_Corrected_Flipped.ima ' + \
              ' -order 0 ' + \
              ' -verbose'

    os.system( command )

    command = 'GkgExecuteCommand Flipper ' + \
              ' -i ' + t2_topUp + '_Corrected_Flipped.ima ' + \
              ' -o ' + t2_topUp + '_Corrected_Flipped.ima ' + \
              ' -t z '

    os.system( command )

    command = 'AimsFileConvert' + \
              ' -i ' + t2_topUp + '_Corrected_Flipped.ima ' + \
              ' -o ' + t2_topUp + '_Corrected_Flipped.nii '

    os.system( command )
    
    command = 'antsRegistrationSyN.sh' + \
              ' -d 3' + \
              ' -f ' + BrainTemplate + \
              ' -m ' + t2_topUp + '_Corrected_Flipped.nii ' + \
              ' -o ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     subject + '-to-Template_rigid_' ) + \
              ' -t t '

    os.system( command )

    command = 'AimsMask' + \
              ' -i ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     subject + '-to-Template_rigid_Warped.nii.gz' ) + \
              ' -m ' + BrainMask + \
              ' -o ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     subject + '-to-Template_rigid_Warped.nii.gz' )

    os.system( command )

    command = 'antsRegistrationSyN.sh' + \
              ' -d 3' + \
              ' -f ' + BrainTemplate + \
              ' -m ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     subject + '-to-Template_rigid_Warped.nii.gz' ) + \
              ' -o ' + os.path.join(  Dir,
                                      subject,
                                      '02-Diffusion',
                                      '01-TopUp',
                                      subject + '-to-Template_diffeomorphic_' ) + \
              ' -t so '

    os.system( command )

    rigidAffineTransformations = os.path.join( Dir,
                                               subject,
                                               '02-Diffusion',
                                               '01-TopUp',
                                               subject + '-to-Template_rigid_0GenericAffine.mat' )

    diffeomorphicAffineTransformations = os.path.join( Dir,
                                                       subject,
                                                       '02-Diffusion',
                                                       '01-TopUp',
                                                       subject + '-to-Template_diffeomorphic_0GenericAffine.mat' )

    diffeomorphiWarpTransformations = os.path.join( Dir,
                                                    subject,
                                                    '02-Diffusion',
                                                    '01-TopUp',
                                                    subject + '-to-Template_diffeomorphic_1InverseWarp.nii.gz ' )

    command = 'antsApplyTransforms' + \
              ' -d 3' + \
              ' -i ' +  BrainMask + \
              ' -r ' + os.path.join( Dir,
                                      subject,
                                      '02-Diffusion',
                                      '01-TopUp',
                                      't2_topUp_Corrected_Flipped.nii ' ) + \
              ' -o ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'mask.nii.gz' ) + \
              ' -n NearestNeighbor ' + \
              ' -t ' + diffeomorphiWarpTransformations + ' [' + \
                       diffeomorphicAffineTransformations + ',1] [' + \
                       rigidAffineTransformations + ',1] '


    os.system( command )

    command = 'GkgExecuteCommand Resampling3D ' + \
          ' -reference ' + os.path.join( Dir,
                                         subject,
                                         '02-Diffusion',
                                         '01-TopUp',
                                         'mask.nii.gz' ) + \
          ' -size 128 128 56' + \
          ' -resolution 2 2 2.4 ' + \
          ' -transforms ' + trm_inv + \
          ' -output ' +  os.path.join( Dir,
                                       subject,
                                       '02-Diffusion',
                                       '01-TopUp',
                                       'mask.ima' ) + \
          ' -order 0 ' + \
          ' -verbose'

    os.system( command )

    command = 'GkgExecuteCommand Flipper ' + \
              ' -i ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'mask.ima' ) + \
              ' -o ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'mask.ima' ) + \
              ' -t y '

    os.system( command )

    command = 'AimsMorphoMath' + \
              ' -i '  + os.path.join( Dir,
                                      subject,
                                      '02-Diffusion',
                                      '01-TopUp',
                                      'mask.ima' ) + \
              ' -r 2 ' + \
              '-m dil ' + \
              '-o '  + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'mask.ima' )

    os.system( command )

    print( 'Done' )

    #---------------------------------------------------------------------------
    # Eddy Currents and Motions Corrections
    #---------------------------------------------------------------------------

    print( 'Eddy Currents and Motions Corrections...' )

    indexFile_Shell1 = os.path.join( Dir,
                                     'Templates',
                                     'index_6.txt ' )

    indexFile_Shell2 = os.path.join( Dir,
                                     'Templates',
                                     'index_30.txt ' )

    indexFile_Shell3 = os.path.join( Dir,
                                     'Templates',
                                     'index_64.txt ' )

    command = 'AimsFileConvert' + \
              ' -i '  + os.path.join( Dir,
                                      subject,
                                      '02-Diffusion',
                                      '01-TopUp',
                                      'mask.ima' ) + \
              ' -o '  + os.path.join( Dir,
                                      subject,
                                      '02-Diffusion',
                                      '01-TopUp',
                                      'mask.nii.gz' )

    os.system( command )

    print( 'Shell 1...' )

    command = 'eddy' + \
              ' --imain=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '00-Dicom-to-Gis',
                                          'dw_01.nii' ) + \
              ' --mask=' + os.path.join( Dir,
                                         subject,
                                         '02-Diffusion',
                                         '01-TopUp',
                                         'mask.nii.gz' ) + \
              ' --acqp=' + topUpParameters + \
              ' --index=' + indexFile_Shell1 + \
              ' --bvecs=' + dw_Shell1 + '.bvec ' + \
              ' --bvals=' + dw_Shell1 + '.bval ' + \
              ' --topup=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '01-TopUp',
                                          subject + '_topup_results' ) + \
              ' --niter=8 ' + \
              ' --fwhm=10,8,4,2,0,0,0,0 ' + \
              ' --repol ' + \
              ' --out=' + os.path.join( Dir,
                                        subject,
                                        '02-Diffusion',
                                        '01-TopUp',
                                        'dw_01_eddy_corrected_data ' ) + \
              ' --verbose'

    os.system( command )

    print( 'Done' )

    print( 'Shell 2...' )

    command = 'eddy' + \
              ' --imain=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '00-Dicom-to-Gis',
                                          'dw_02.nii' ) + \
              ' --mask=' + os.path.join( Dir,
                                         subject,
                                         '02-Diffusion',
                                         '01-TopUp',
                                         'mask.nii.gz' ) + \
              ' --acqp=' + topUpParameters + \
              ' --index=' + indexFile_Shell2 + \
              ' --bvecs=' + dw_Shell2 + '.bvec ' + \
              ' --bvals=' + dw_Shell2 + '.bval ' + \
              ' --topup=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '01-TopUp',
                                          subject + '_topup_results' ) + \
              ' --niter=8 ' + \
              ' --fwhm=10,8,4,2,0,0,0,0 ' + \
              ' --repol ' + \
              ' --out=' + os.path.join( Dir,
                                        subject,
                                        '02-Diffusion',
                                        '01-TopUp',
                                        'dw_02_eddy_corrected_data ' ) + \
              ' --verbose'

    os.system( command )

    print( 'Done' )

    print( 'Shell 3...' )

    command = 'eddy' + \
              ' --imain=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '00-Dicom-to-Gis',
                                          'dw_03.nii' ) + \
              ' --mask=' + os.path.join( Dir,
                                         subject,
                                         '02-Diffusion',
                                         '01-TopUp',
                                         'mask.nii.gz' ) + \
              ' --acqp=' + topUpParameters + \
              ' --index=' + indexFile_Shell3 + \
              ' --bvecs=' + dw_Shell3 + '.bvec ' + \
              ' --bvals=' + dw_Shell3 + '.bval ' + \
              ' --topup=' + os.path.join( Dir,
                                          subject,
                                          '02-Diffusion',
                                          '01-TopUp',
                                          subject + '_topup_results' ) + \
              ' --niter=8 ' + \
              ' --fwhm=10,8,4,2,0,0,0,0 ' + \
              ' --repol ' + \
              ' --out=' + os.path.join( Dir,
                                        subject,
                                        '02-Diffusion',
                                        '01-TopUp',
                                        'dw_03_eddy_corrected_data ' ) + \
              ' --verbose'

    os.system( command )

    print( 'Done' )

    #---------------------------------------------------------------------------
    # Convert corrected data to GIS format
    #---------------------------------------------------------------------------

    print( 'Convert Corrected Data to GIS format...' )
    print( 'Shell 1...' )

    command = 'AimsFileConvert' + \
              ' -i ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'dw_01_eddy_corrected_data.nii.gz ' ) + \
              ' -o ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'dw_01_eddy_corrected_data.ima ' )

    os.system( command )

    print( 'Done' )
    print( 'Shell 2...' )

    command = 'AimsFileConvert' + \
              ' -i ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'dw_02_eddy_corrected_data.nii.gz ' ) + \
              ' -o ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'dw_02_eddy_corrected_data.ima ' )

    os.system( command )

    print( 'Done' )
    print( 'Shell 3...' )

    command = 'AimsFileConvert' + \
              ' -i ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'dw_03_eddy_corrected_data.nii.gz ' ) + \
              ' -o ' + os.path.join( Dir,
                                     subject,
                                     '02-Diffusion',
                                     '01-TopUp',
                                     'dw_03_eddy_corrected_data.ima ' )

    os.system( command )
    print( 'Done' )