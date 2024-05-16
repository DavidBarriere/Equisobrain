function  DataSegmentation( BASEdir )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Wrote by David André Barrière 09th September 2022
% This function permit to create and launch Normalization and Segmentation
% processing using SPM8 function.
% Usage : set BASEdir variable with your current working directory 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Variables

    % SPM Batch to load
T = load( 'processing_step01_MultiSubject.mat' ) ; 

    % Filtered Data Directory
DataDir = [ BASEdir,...
            '/00-data/' ] ;; 
        
    % Filtered Data List
NiiFiles = dir( fullfile(DataDir,...
                'sub*.nii' ) ) ; 
NiiFiles = { NiiFiles(:).name } ;

    % Prior image for Segmentation
Priors = { [ BASEdir,...
             '/Turone_Equine_Brain_Atlas_and_Templates',...
             '/gm.nii' ],...
           [ BASEdir,...
             '/Turone_Equine_Brain_Atlas_and_Templates',...
             '/wm.nii' ],...
           [ BASEdir,...
             '/Turone_Equine_Brain_Atlas_and_Templates',...
             '/csf.nii' ] } ;
                  
    % list of SPM function to run
TemplateJob = { [ BASEdir,...
                  '/processing_step01_Template.mat' ] } ;

    % Make output Directory
mkdir ( [ BASEdir,...
          '/02-LinearNormalisation' ]) ;
OutputDir = { [ BASEdir,...
                '/02-LinearNormalisation' ] } ;

    % Prior image for Coregistration
gm_prior = { [ BASEdir,...
               '/Turone_Equine_Brain_Atlas_and_Templates',...
               '/gm.nii,1' ] } ;
wm_prior = { [ BASEdir,...
               '/Turone_Equine_Brain_Atlas_and_Templates',...
               '/gm.nii,1' ] } ;
csf_prior = { [ BASEdir,...
                '/Turone_Equine_Brain_Atlas_and_Templates',...
                '/gm.nii,1' ] } ;
Template = { [ BASEdir,...
               '/Turone_Equine_Brain_Atlas_and_Templates',...
               '/template.nii' ] } ;

    % Create SPM Batch
m = 1 ;
for i = 1 : 1 : length( NiiFiles )
    
    NII = { [ DataDir, NiiFiles{i} ] } ;
    disp(NiiFiles{i}) ;
    
    T.matlabbatch{1}.cfg_basicio.runjobs.jobs = TemplateJob;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{1}.innifti = NII ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{2}.innifti = Priors ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{3}.innifti = NII ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{4}.innifti = gm_prior ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{5}.innifti = wm_prior ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{6}.innifti = csf_prior ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{7}.innifti = Template ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{8}.indir = OutputDir;
    m = m+1;
   
end

    % Run SPM Batch
matlabbatch = T.matlabbatch ;
save(  'processing_step01_MultiSubject_Loaded', 'matlabbatch'  ) ;
spm_jobman('run',matlabbatch);              
            