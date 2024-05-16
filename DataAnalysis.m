function  DataAnalysis( BASEdir )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Wrote by David André Barrière 09th September 2022
% This function permit to create and launch non linear normalization 
% (DARTEL), spatial smoothing and two sample Student' t-test comparison 
% using SPM8 function.
%
% Usage : set BASEdir variable with your current working directory 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BASEdir
    % SPM Batch to load
T = load( 'processing_step02_MultiSubject.mat' ) ;


    % list of SPM function to run
TemplateJob = { [ BASEdir,...
                  '/processing_step02_Template.mat' ] } ;

    % Segmented Data Directory
DataDir = [ BASEdir,...
            '/02-LinearNormalisation' ] ;
          
mkdir ( [ BASEdir,...
          '/03-DiffeoMorphicNormalisation' ] ) ;

mkdir ( [ BASEdir,...
          '/04-StatisticalAnalysis' ] ) ;
      
mkdir ( [ BASEdir,...
          '/04-StatisticalAnalysis',...
          '/Data' ] ) ;

mkdir ( [ BASEdir,...
          '/04-StatisticalAnalysis',...
          '/Two_Sample_t-test' ] ) ;

OutputDir_01 = [ BASEdir,...
                 '/03-DiffeoMorphicNormalisation' ] ;

OutputDir_02 = [ BASEdir,...
                 '/04-StatisticalAnalysis',...
                 '/Data' ] ;

OutputDir_03 = [ BASEdir,...
                 '/04-StatisticalAnalysis',...
                 '/Two_Sample_t-test' ] ;

    % Segmented Data 
        %Grey Matter Data
GmData = dir( fullfile( [ DataDir,...
                          '/rwc1sub*.nii' ] ) ) ;

for i = 1 : 1 : 23
    GmDataList{i} = [DataDir,'/' GmData(i).name] ;
end

        %White Matter Data
WmData = dir( fullfile( [ DataDir,...
                          '/rwc2sub*.nii' ] ) ) ;
for i = 1 : 1 : 23
    WmDataList{i} = [DataDir,'/' WmData(i).name] ;
end

    % Image for brain masking
mask = { [ BASEdir,...
           '/Turone_Equine_Brain_Atlas_and_Templates',...
           '/mask.nii' ] } ;
                
    % Data for paired two sample t-test comparison
UnweanedData = dir( fullfile( [ DataDir,...
                                '/rwc1sub*_Unweaned_*.nii' ] ) ) ;
                            
for i = 1 : 1 : 12
    UnweanedDataList{i} = [OutputDir_02,'/sw' UnweanedData(i).name] ;
end
    
    
WeanedData = dir( fullfile( [ DataDir,...
                                '/rwc1sub*_Weaned_*.nii' ] ) ) ;

for i = 1 : 1 : 11
    WeanedDataList{i} = [OutputDir_02,'/sw' WeanedData(i).name] ;
end




    % Create SPM Batch
T.matlabbatch{1}.cfg_basicio.runjobs.jobs = TemplateJob ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{1}.innifti = GmDataList ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{2}.innifti = WmDataList ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{3}.innifti = GmDataList ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{4}.indir = {OutputDir_01} ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{5}.indir = {OutputDir_02} ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{6}.indir = {OutputDir_03} ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{7}.innifti = UnweanedDataList ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{8}.innifti = WeanedDataList ;
T.matlabbatch{1}.cfg_basicio.runjobs.inputs{1}{9}.innifti = mask ;

    % Run SPM Batch
matlabbatch = T.matlabbatch ;
save(  'processing_step02_MultiSubject_Loaded', 'matlabbatch'  ) ;
spm_jobman('run',matlabbatch);