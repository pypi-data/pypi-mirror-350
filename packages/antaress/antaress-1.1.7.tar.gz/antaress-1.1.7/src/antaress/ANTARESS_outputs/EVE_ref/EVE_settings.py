# -*- coding: utf-8 -*-
import numpy as np
from math import pi
from antaress.ANTARESS_general.utils import stop

def EVE_settings(theo_data_set,dico_simu_set,dico_gen_plot_set,sp_settings_set,dico_ENA,dico_gen_anareg_set,dico_restore,dico_star_grid_set,dico_bodies_grid_set,obs_data_set,dico_collgrid,dico_elec,dico_SSgrids_set,plot_dic):
    r"""**EVE default settings.**
    
    Initializes EVE configuration settings with default values for specific sequences:
    Possible sequences are:

        - 'main_X' : performs simulation of opaque planetary disk with imported stellar disk emission in X-rays, to illustrate transits across inhomogeneous corona.
        - 'main_occ' : performs simulation of planetary disk with thermal emission to illustrate occultation and phase curve.
        - 'main_POLD' : performs simulation of opaque planetary disk to illustrate planet-occulted line distortions (POLDs) in transmission spectra
        - 'main_Na' : performs the same simulation as 'main_POLD', with an additional planetary atmosphere containing sodium.   
        - 'main_Fe' : performs simulation of a planet with iron front.
        - 'main_He' : performs simulation of a planet with extended thermosphere containing helium.
        - 'main_H' : performs simulation of a giant planet with escaping exosphere of hydrogen atoms.    
        - 'main_dust' : performs simulation of rocky planet with escaping exosphere of dust.       
        - 'main_comets' : performs simulation of solar system comets with escaping dust and gas.
        
    Args:
        TBD
    
    Returns:
        None
    
    """ 
    
    #################################################################################################################
    #%% Global settings
    #    - independent of the species, or common to several of them
    #################################################################################################################

    #%%% Grid run
    dico_simu_set['grid_run'] = False  


    #%%% Debug mode
    #    - activate to print useful values
    dico_simu_set['debug_mode'] = False  
    
    
    #%%% Output summary file
    #    - define properties to be output in 'output_content'
    dico_simu_set['output'] = True    
    dico_simu_set['output_content'] = {}
    
    
    #%%%% Elementary opacity
    if dico_simu_set['sequence'] in ['main_He','main_Na','main_Fe','main_H','main_dust']:         
        dico_simu_set['output_content']['dtau'] = True  
    else:
        dico_simu_set['output_content']['dtau'] = False  
    
    
    #################################################################################################################
    #%%% Simulation restoration
    #################################################################################################################
    
    #%%%% Save simulation state 
   	#    - default off: False
   	#    - indicate save frequency (in number of iterations)   
    dico_restore['save_state'] = False
    dico_restore['save_freq'] = 10    


    #%%%% Keep only one state in memory   
    dico_restore['mono_state'] = True    
    

    #%%%% Restore simulation state 
   	#    - set to False to start a new simulation 
   	#      otherwise indicate path to the unfinished simulation directory and retrieve manually the parameters 
   	# in the saved 'settings.py' file
   	#    - the simulation will start in the existing directory (must contain a 'restore' subdirectory; the more recent save will be used)    
    dico_restore['restore_path'] = ''
    

    
    #################################################################################################################
    #%%% Simulation main properties
    #################################################################################################################
    
    #-----------------------------------------------------------------
    #%%%% Numerical settings
    #-----------------------------------------------------------------
    
    #%%%%% Number of threads to be used
    #    - if nthreads>1 : parallel computing launched using multiprocessing module 
    #    - cores can have multiple threads: nthreads can be set higher than ncore
    dico_simu_set['nthreads'] = 12    
    
    
    #%%%%% Deactivate parallelization for specific modules
    #    - possibilities:
    # + stcell_surf_emission: when band spectra are very large
    # + part_opacity: when band spectra are very large
    dico_simu_set['no_para'] = []   


    #%%%% Plot settings
    
    #%%%%% Planetary orbit discretization
    #    - number of points discretizing the planetary orbits in plots
    dico_simu_set['npts_orbit'] = 10000


    #%%%%% Deactivate all plots
    #    - set to True
    dico_simu_set['noplot'] = False	


    #%%%%% Use non-interactive backend 
    #    - set to True to run matplotlib on servers such as DACE and EXOATMOS
    dico_simu_set['non_int_back'] = False	

    #%%%%% Save outputs for post-processing    
    #    - to save parameter values required to analyze the atmospheric properties with the ADAM module 
    #    - save_cloud is a list containing the species to be saved, or set to empty otherwise
    #    - the save is performed at the time steps following each required time (in h)
    # + possibilities: [t], [t1,t2,..],T0+(dt_simu/60.)*np.arange(T0,Tfinal,(dt_simu/60.)) 
    dico_simu_set['save_cloud']=[]
    dico_simu_set['time_savecloud']=[0.]   


    #-----------------------------------------------------------------
    #%%%% Physical properties
    #-----------------------------------------------------------------


    #%%%%% Star name
    if dico_simu_set['sequence']=='main_X':dico_simu_set['star_name'] = 'HD189733'    
    if dico_simu_set['sequence']=='main_occ':dico_simu_set['star_name'] = '55Cnc'  
    elif dico_simu_set['sequence'] in ['main_POLD','main_Na']:dico_simu_set['star_name'] = 'HD209458' 
    elif dico_simu_set['sequence']=='main_Fe':dico_simu_set['star_name'] = 'WASP76'
    elif dico_simu_set['sequence'] in ['main_He','main_H']:dico_simu_set['star_name'] = 'HAT_P_11'                                          
    elif dico_simu_set['sequence']=='main_dust':dico_simu_set['star_name'] = 'WD1145+017'
    elif dico_simu_set['sequence']=='main_comets':dico_simu_set['star_name'] = 'Sun'  


    #%%%%% Bodies name
    #    - we assume the main body ('body_0') to be the only one massive enough to affect the system barycenter 
    #    - the self-shielding grid is based and affected by the main body alone
    #    - see 'planet_data' file for possibilities
    if dico_simu_set['sequence']=='main_X':dico_simu_set['bodies_name'] = {'body_0':'HD189733b'}  
    elif dico_simu_set['sequence']=='main_occ':dico_simu_set['bodies_name'] = {'body_0':'55Cnc_e'}  
    elif dico_simu_set['sequence'] in ['main_POLD','main_Na']:dico_simu_set['bodies_name'] = {'body_0':'HD209458b'}
    elif dico_simu_set['sequence']=='main_Fe':dico_simu_set['bodies_name'] = {'body_0':'WASP76b'}
    elif dico_simu_set['sequence'] in ['main_He','main_H']:dico_simu_set['bodies_name'] = {'body_0':'HAT_P_11b'}                                      
    elif dico_simu_set['sequence']=='main_dust':dico_simu_set['bodies_name'] = {'body_0':'WD1145+017b'}
    elif dico_simu_set['sequence']=='main_comets':dico_simu_set['bodies_name'] = {'body_0':'comet0','body_1':'comet1'}

    
    #%%%%% Bodies sets
    #    - format : {prop_i : {bdy_j : val , ...} , ...}
    #    - offsets the value of 'prop_i' for 'bdy_j' by the requested value
    #      useful to create a set of bodies with properties varying around nominal values, such as a string of comets
    dico_simu_set['delta_prop'] = {}    


    #%%%%% Spectral reference frame
    #    - spectra are defined in 'vacuum' or 'air'
    #    - line transitions will be retrieved accordingly
    dico_simu_set['spectral_ref'] = 'vacuum'
    
    
    #%%%%% ISM extinction
    #    - set to None, or to the chosen dust extinction model that will be applied to the spectra at Earth
    if dico_simu_set['sequence']=='main_dust':dico_simu_set['extinct_mode'] = 'cardelli'     
    else:dico_simu_set['extinct_mode'] = None 


    #%%%%% Simulated species
    if dico_simu_set['sequence'] in ['main_X','main_occ','main_POLD']:dico_simu_set['sim_sp'] = []                               
    elif dico_simu_set['sequence']=='main_Na':dico_simu_set['sim_sp'] = ['Na_0+_g']
    elif dico_simu_set['sequence']=='main_Fe':dico_simu_set['sim_sp'] = ['Fe_0+_g']
    elif dico_simu_set['sequence']=='main_He':dico_simu_set['sim_sp'] = ['He_0+_g']                         
    elif dico_simu_set['sequence']=='main_H':dico_simu_set['sim_sp'] = ['H_0+_g']                 
    elif dico_simu_set['sequence']=='main_dust':dico_simu_set['sim_sp'] = ['pyrmg40']              
    elif dico_simu_set['sequence']=='main_comets':dico_simu_set['sim_sp'] = ['pyrmg40','Mg_0+_g']              
        

    #%%%%% Start/end times of the simulation (in hours)
    #    - t = 0 corresponds to the mid-transit time given for the main body in planet_data.py
    if dico_simu_set['sequence']=='main_X':
        dico_simu_set['T0_h'] = -1.1
        dico_simu_set['Tf_h'] =  1.1        
    elif dico_simu_set['sequence']=='main_occ':
        dico_simu_set['T0_h'] = -10.
        dico_simu_set['Tf_h'] =  10.  
    elif dico_simu_set['sequence'] in ['main_POLD','main_Na']:
        dico_simu_set['T0_h'] = -1.1
        dico_simu_set['Tf_h'] =  1.1
    elif dico_simu_set['sequence']=='main_Fe':
        dico_simu_set['T0_h'] = -2.
        dico_simu_set['Tf_h'] =  2.
    elif dico_simu_set['sequence']=='main_He':
        dico_simu_set['T0_h'] = -2.
        dico_simu_set['Tf_h'] =  2.
    elif dico_simu_set['sequence']=='main_H':
        dico_simu_set['T0_h'] = -6.
        dico_simu_set['Tf_h'] =  4.5                                        
    elif dico_simu_set['sequence']=='main_dust':
        dico_simu_set['T0_h'] = -0.016
        dico_simu_set['Tf_h'] =  0.016
    elif dico_simu_set['sequence']=='main_comets':
        dico_simu_set['T0_h'] = -10.
        dico_simu_set['Tf_h'] =  10.
    

    #%%%%% Time step (in mn) 
    #    - must be adapted to the planet orbital distance and gas dynamics (radiation pressure, thermal properties, etc)
    if dico_simu_set['sequence']=='main_X':dico_simu_set['dt_simu']=1.       
    elif dico_simu_set['sequence'] in ['main_POLD','main_Na']:dico_simu_set['dt_simu']=2.
    elif dico_simu_set['sequence']=='main_occ':dico_simu_set['dt_simu']=5.
    elif dico_simu_set['sequence']=='main_Fe':dico_simu_set['dt_simu']=5.
    elif dico_simu_set['sequence']=='main_He':dico_simu_set['dt_simu']=5.
    elif dico_simu_set['sequence']=='main_H':dico_simu_set['dt_simu']=1.                                      
    elif dico_simu_set['sequence']=='main_dust':dico_simu_set['dt_simu']=0.05
    elif dico_simu_set['sequence']=='main_comets':dico_simu_set['dt_simu']=10.


    #%%%%% Artificial particle deletion 
    #    - format is 'art_del':{'body_name':{'phi_behind': val, 'phi_forward': val, 'rad_low': val, 'rad_up': val}},
    #    - set in 'art_del' only bodies for which deletion should be performed 
    #    - we keep only particles within truncated half-cones:
    # + centered on the star with central axis the line toward a body
    # + between 0 and 'phi_behind' in the half-space extendind behind the main body, and between 0 and 'phi_forward' in front of the main body
    #   where phi is counted from the star/body axis, in deg
    # + between 'rad_low' and 'rad_up', counted from the star, in unit of body sma
    #    - check carefully that no particles are deleted that would contribute to absorption during all observations
    #    - be particularly cautious with multiple bodies, as secondary bodies will likely be at some time outside the deletion cone of the main body
    dico_simu_set['art_del'] = {}    
        

    #%%%%% Self-shielding from electronic transitions at restricted wavelengths
    #    - this option limits the calculation of self-shielding opacity from a given electronic transition to the wavelengths
    # at which particles (of any species) are sensitive to radiation pressure in the transition range (ie, if no particle is sensitive 
    # to radiation pressure at a wavelength that is shielded, self-shielding opacity is not calculated)
    #    - this option decreases significantly computing time, but assumes that the effect of shielding from electronic transitions 
    # on the local stellar spectrum can be neglected for processes over broad bands that include the transitions 
    dico_simu_set['limit_SS_electrans'] = True    


    #%%%%% Threshold on self-shielding absorption
    #    - stellar spectrum will be multiplied by shielding absorption table only at pixels with absorption coefficient below 1 - threshold
    dico_simu_set['thresh_SS_abs'] = 1e-3

    
    #################################################################################################################
    #%% Datasets
    #################################################################################################################        

    ################################################################################################## 
    #%%% Theoretical datasets
    #    - this dictionary contains spectra defined on independent wavelength bands, that represent the parts of the 
    # host star spectrum relevant to the simulation:
    # + if limb-darkening and/or the velocity field of the star is taken into account, the input spectra define the specific intensity along the LOS, so that at disk center:
    #   I0[l] = F_star_input[l][1au]*1au^2 / Sstar
    #   I0, and thus F_star_input, must be defined so that with the requested limb-darkening and velocity field, one retrieve in the end the expected disk-integrated stellar spectrum
    #   if the input at Earth distance is absorbed by the ISM, then the velocity field of the star cannot be modeled within EVE (each local spectrum would be absorbed differently because of its shift)
    #   in this case one can define a predefined stellar grid outside of the simulation
    # + spectra will be used to calculate radiation pressure, and to provide a reference stellar spectrum to be absorbed by the planets and their atmospheres
    # + the resolution and range of the spectra in a given band must be fine enough to trace the spectral variations of the radiation pressure
    # processes, and those of the cross-sections absorbers/emitters, that are relevant to this band 
    # + the bands must not overlap, and must be characterized by unique limb-darkening coefficients, but a given process may affect or require
    # several bands
    # + each band is read from a file, that contains the flux at 1au and Earth (erg s-1 cm-2 A-1) as a function of wavelength (A) in the stellar rest frame 
    #    - independently of observations, the stellar spectrum (with or without absorption/emission) may be used to calculate instrumental spectra
    # and light curves as observed with a given instrument (with response defined through the 'inst_set' field)
    # + a unique instrumental response must be used for a given band.
    # + bands must have a constant spectral resolution. Consider subdividing a band in smaller bands if one require a different resolution
    # + if theoretical spectra are to be compared with real observations, the instrumental response and required comparison range are defined in 
    # the 'obs_data' dictionary
    # + the 'inst_set' option can only be used for one instrument in a given band. Because the bands in 'theo_data_set' must be independent, it 
    # cannot be used to calculate spectra measured in a same band with two different instruments. Use the 'obs_data' dictionary.
    ################################################################################################## 
 

    #%%%% Activation
    #    - set to True if required
    theo_data_set['on'] = True

    
    #%%%% Time range
    #    - theoretical data will only be calculated within this range
    #    - relative to the transit center, in h
    #    - can be made of independent intervals
    #    - must include the time windows of all observations to be compared with the simulation results (accounting for an additional half timestep on each side of the observed exposure)
    if dico_simu_set['sequence']=='main_X':theo_data_set['trange'] =[[-1.5,1.5]]
    elif dico_simu_set['sequence'] in ['main_POLD','main_Na']:theo_data_set['trange'] =[[-1.,1.]]
    elif dico_simu_set['sequence']=='main_Fe':theo_data_set['trange'] =[[-1.5,1.5]]
    elif dico_simu_set['sequence']=='main_He':theo_data_set['trange'] =[[-1.5,1.5]]
    elif dico_simu_set['sequence']=='main_H':theo_data_set['trange'] =[[-4.,4.]]                                      
    elif dico_simu_set['sequence']=='main_dust':theo_data_set['trange'] =[[-0.01,0.01]]
    elif dico_simu_set['sequence']=='main_comets':theo_data_set['trange'] =[[-2.,2.]]

    
    #%%%% Band properties 
    #    - the call to 'theo_data_set' will calculate automatically the spectra over the bands defined here:
    # + at 1 au from the star 
    # + at Earth distance (with no instrument, at the resolution of the  input band spectrum)
    # 
    #    - format is 'bands' = { 'band_name' : { 
    #                               'mode' : val, 
    #                               'file' : val,
    #                               'limb_dark':{'mode':val,'coeffs':[..]},
    #                               'save_x' : [..],
    #                               'plotgrid' : [..],'trange_grid' :[t1,t2],
    #                               'indep_sp' : [...],
    #                                key : val }} 
    #      bands can be given any name 'band_name'
    # ++++++++++++
    #      'mode' defines the type of data to be calculated, and can be set to one of:
    # + 'raw_sp': only simulated spectra at the resolution of the theoretical reference spectrum are calculated (no instrumental response, defined at 1au from the star)
    # + 'inst_sp': simulated spectra are convolved by the chosen instrumental response and calculated at Earth
    # + 'inst_sp_lc': same as 'inst_sp', plus light curves are calculated at Earth from the instrumental spectra
    # ++++++++++++
    #      'file' is the path to the text file that contains the band spectra. The file must contain the following columns:
    # + wavelengths in the stellar reference frame (A), with constant resolution
    #               values correspond to bin centers  
    # + the stellar flux at 1au from the star (erg s-1 cm-2 A-1)
    # + the stellar flux at Earth distance (after ISM absorption; erg s-1 cm-2 A-1)  
    #      limit the range of the input spectrum to wavelengths effectively used in te simulation, to reduce computing time 
    #      if a predefined stellar grid is used as input (in 'dico_star_grid_set'), 'file' is unecessary 
    # ++++++++++++
    #     'limb_dark' controls broadband limb-darkening over the band, which scales the global flux level of the spectra tiling the stellar grid.
    # + 'mode' can be set to one of the laws implemented in the ANTARESS package
    # + 'coeffs' should be set according to the chosen law (unused if uniform law)    
    #      if a predefined stellar grid is used as input (in 'dico_star_grid_set'), 'limb_dark' is unecessary 
    # ++++++++++++
    #      'save_x' can be set to [] (no return) or to a combination of:
    # + 'file': save the spectra at all timesteps in 'trange'
    # + 'plot': plot the spectra at all timesteps in 'trange'    
    #       if relevant with the chosen mode, multiple 'save_x' can be defined, where 'x' is set to one of the 'mode' values
    #       add '_norm' as suffix of 'file' or 'plot' to return normalized spectra as well
    # ++++++++++++
    #       'plotgrid' can be set to [] (no return) or to a combination of:
    # + 'st_grid': stellar grid with emission in the band
    # + 'ross_stgrid': rotational broadening of stellar surface (if required, depends on LD and thus on the band)
    # + 'st_opa_grid_all': opacity/absorption from all regimes in the band, in the stellar grid
    # + 'st_opa_grid_ana': opacity/absorption from all analytical regimes in the band, in the stellar grid
    #                                       only if 'ana' in 'indep_sp'
    # + 'st_opa_grid_part': opacity/absorption from all particle regimes in the band, in the stellar grid
    #                       only if 'part' in 'indep_sp'
    # + 'st_scat_grid_part': scattered flux from all particle regimes in the band, in the sky grid
    #                        only if 'scat_part' in 'indep_sp'
    #       'trange_grid' defines the time range within which these plots should be done. Leave empty for the plots to be made at all timesteps.
    # ++++++++++++
    #       'indep_sp' controls the additional calculation of raw spectra accounting for individual contributors, and can be set to [] (no additional spectra are returned) or to a combination of:
    # + 'part': contributions from all absorbing particles regimes
    # + 'ana': contributions from all analytical regimes
    # + 'scat_part': contributions from all scattering particle regimes
    #        files and plots will include the selected contributions
    # ++++++++++++
    #    - for the 'inst_sp_lc' mode, define:
    # + 'wav_lc': spectral intervals over which calculate independent light curves (from instrumental spectra) 
    #             format: [[w1,w2],[w3,w4],..]
    #             to estimate the ranges use w_star = w_line*( 1+(rv_star[line]/c))        
    #
    #    - for the 'inst_sp_lc' mode define:
    # + 'trange_lc': time intervals over which calculate the light curves. They can be independent, but all within 'trange' 
    #
    #    - for any 'inst_x' mode, define:
    # + 'inst_set': one of the instrumental response defined in init_data.py
    #               the same instrumental properties will be used for all required intervals in a given band
    #      these are instrumental-like data calculated independently of any observed data
    if dico_simu_set['sequence']=='main_X':
        theo_data_set['bands']={
            'band_X':{
                  'mode':'raw_sp',
                  'file':'HD189733_X.d',
                  'limb_dark':{'mode':'uniform'},
                  'save_raw_sp':['file_norm','plot_norm']
                  }}  
    elif dico_simu_set['sequence']=='main_occ':
        theo_data_set['bands']={
            'band_occ':{
                'mode':'raw_sp',
                'file':'fitted_master_spitzer_4870K.txt',
                'save_raw_sp':['file','plot'],
                'inst_set':'JWST_TBD',
                'limb_dark':{'mode':'quadratic','coeffs':[0.2696, 0.2617, 0.,0.]},
                'plotgrid' :['pl_grid_emit'],
                'indep_sp':['emit_bdy']
            }}         
    elif dico_simu_set['sequence'] in ['main_POLD','main_Na']:
        theo_data_set['bands']={
            'band_NaI':{
                  'mode':'inst_sp','inst_set':'ESPRESSO_Na',
                  'file':'HD209458_NaI.d',
                  'limb_dark':{'mode':'LD_quad','coeffs':[0.,0.,0.,0.]},
                  'save_raw_sp':['file_norm','plot_norm'],'save_inst_sp':['file_norm','plot_norm'], 
                  }} 
    elif dico_simu_set['sequence']=='main_Fe':   
        theo_data_set['bands']={
            'band_FeI':{
                  'mode':'inst_sp','inst_set':'ESPRESSO_Fe',
                  'file':'WASP76_NaI.d',
                  'limb_dark':{'mode':'LD_quad','coeffs':[0.,0.,0.,0.]},
                  'save_raw_sp':['file_norm','plot_norm'],'save_inst_sp':['file_norm','plot_norm'], 
                  }}         
    elif dico_simu_set['sequence']=='main_He':                
        theo_data_set['bands']={
            'band_XUV':{'mode':'raw_sp','file':'HATP11_XUV.d','limb_dark':{'mode':'uniform'}},        
            'band_HeI':{
                  'mode':'inst_sp','inst_set':'NIRPS_He',
                  'file':'HATP11_HeI.d',
                  'limb_dark':{'mode':'LD_quad','coeffs':[0.26725386, 0.26492167, 0.,0.]},
                  'save_raw_sp':['file_norm','plot_norm'],'save_inst_sp':['file_norm','plot_norm'], 
                  }}           
    elif dico_simu_set['sequence']=='main_H':  
        theo_data_set['bands']={
            'band_XUV':{'mode':'raw_sp','file':'HATP11_XUV.d','limb_dark':{'mode':'uniform'}}, 
            'band_HI':{
                  'mode':'inst_sp','inst_set':'HST_STIS_G140M',
                  'file':'HATP11_HI.d',
                  'limb_dark':{'mode':'uniform'},
                  'save_raw_sp':['file_norm','plot_norm'],'save_inst_sp':['file_norm','plot_norm'], 
                  }}  
    elif dico_simu_set['sequence']=='main_dust':              
        theo_data_set['bands']={}
        for band_bd in [[1000.,2500.],[2500.,4000.],[4000.,5500.],[5500.,7000.],[7000.,8500.],[8500.,10000.],[10000.,20000.]]:
            theo_data_set['bands']['sy'+str(int(band_bd[0]))+'-'+str(int(band_bd[1]))]= {
                'mode':'inst_sp_lc','inst_set':'JWST_TBD','wav_lc':[band_bd],'trange_lc':[[-0.5*100./30,0.5*100./30]],
                'file':'sy'+str(int(band_bd[0]))+'-'+str(int(band_bd[1]))+'_t15900g80.spec',
                'limb_dark':{'mode':'uniform'},
                'save_raw_sp':['file_norm','plot_norm']} 
    elif dico_simu_set['sequence']=='main_comets':              
        theo_data_set['bands']={}
        for band_bd in [[1000.,2500.],[2500.,4000.],[4000.,5500.],[5500.,7000.],[7000.,8500.],[8500.,10000.],[10000.,20000.]]:
            theo_data_set['bands']['sy'+str(int(band_bd[0]))+'-'+str(int(band_bd[1]))]= {
                'mode':'inst_sp_lc','inst_set':'HST_STIS_E140M','wav_lc':[band_bd],'trange_lc':[[-0.5*100./30,0.5*100./30]],
                'file':'sy'+str(int(band_bd[0]))+'-'+str(int(band_bd[1]))+'_t15900g80.spec',
                'limb_dark':{'mode':'solar'},
                'save_raw_sp':['file_norm','plot_norm']} 
    
    

    #%%%% Photometry 
    #    - if filled, simulated spectra are multiplied by the chosen instrumental filter 
    #      no integration range needs to be defined since photometers retrieve photons over the full filter bandpass
    #      the reference stellar spectrum must cover (in a single or in multiple consecutive bands) the full filter bandpass 
    #    - define:
    # + 'inst_set': one of the instrumental response defined in init_data.py
    # + 'trange_lc': time intervals over which calculate the light curves. They can be independent, but all within 'trange' 
    #    - define the requested outputs via the list 'save_inst_lc', which can contain a combination of :
    # + 'file': save the spectra at all timesteps in 'trange'
    # + 'plot': plot the spectra at all timesteps in 'trange'    
    #      add '_norm' as suffix of 'file' or 'plot' to return normalized light curves as well    
    if dico_simu_set['sequence']=='main_X': 
        theo_data_set['inst_lc']={
            'inst_set':'XMM',
            'trange_lc':[[-0.5*100./30,0.5*100./30]],
            'save_inst_lc':['file','plot']
            }    
    elif dico_simu_set['sequence']=='main_dust': 
        theo_data_set['inst_lc']={
            'inst_set':'CHEOPS',
            'trange_lc':[[-0.5*100./30,0.5*100./30]],
            'save_inst_lc':['file','plot']
            }         
    else:theo_data_set['inst_lc']={}


    ##################################################################################################   
    #%%% Observational datasets
    #    - define a set of observed spectral bands and/or spectral/photometric light curves to be compared with the theoretical data of the simulation
    #    - to calculate spectra measured in a same band with two different instruments, define two fields with the same band but two different instrumental response.
    ################################################################################################## 
      
    #%%%% Activation
    #    - set to True if required
    obs_data_set['on'] = True
    

    #%%%% Dataset properties 
    #    - the call to 'obs_data_set' will process theoretical spectra calculated through 'obs_data_set' so that they are comparable with the chosen observational datasets
    #    - observational dataset should be specific to a given epoch
    #    - see routines in EVE_preproc to prepare observational data for EVE processing
    #
    #    - format is 'obs' = { 'obs_name' : {
    #                               'datatype': val,
    #                               'dir': val,  
    #                               'theoband': val,
    #                               'filelist':[file1,file2,...],
    #                               'file_norm': val,
    #                               'method': val,
    #                               'inst_set': val,
    #                               'chi2_range':[[val1,val2],[val3,val4],..],
    #                               'trange_sp' :[[t1,t2],[t3,t4],..],
    #                               'save_x' : [..],
    #                                }} 
    #      dataset can be given any name 'obs_name'    
    # ++++++++++++
    #      'datatype' indicates the type of the observed data, and can be set to one of:
    # + 'sp': spectral data
    # + 'photom': photometric data
    # ++++++++++++
    #      'dir' is the name of the subdirectory within Working_dir/Observed_data/star_name that contains the dataset files
    # ++++++++++++
    #      'filelist' lists the names of the dataset files
    # + for spectra:      one file per exposure, which contains in successive columns:
    #                       start wavelength of spectral bin, in the stellar rest frame
    #                       end wavelength of spectral bin, in the stellar rest frame    
    #                       flux density 
    #                       error on flux density 
    #                       start/end times of exposure (on the first two lines only, in BJD) 
    #                     all exposures will be used for chi2 comparison, within the requested spectral interval 'chi2_range' (to reduce computing time, limit this range to data useful for comparison)
    #                     spectral resolution can be variable, but bins must be consecutive and common to all exposures
    #                     exposures can overlap in time, and do not need to be ordered 
    #                     observed spectra are generally measured in the Solar system barycenter. Make sure that they are shifted to the star rest frame (taking into account the radial velocity of the center of mass of the planetary system, and the keplerian velocity of the star around the center of mass) before providing them as input
    # + for light curves: one file, that contains in successive columns:
    #                       start time of exposure, in BJD
    #                       end time of exposure, in BJD
    #                       flux 
    #                       error on flux 
    #                     exposures within the requested time range 'chi2_range' will be used for chi2 comparison            
    #      the simulation must start before the first observed exposure, and end after the last one
    #      absolute exposure times are automatically phased to the input ephemeris of the main body, and converted back to times relative to its T0     
    # ++++++++++++
    #      'file_norm' indicates the path to the file containing the observed reference spectrum
    # + relevant for 'method' that requires normalization of the observed data, or for normalized saves and plots
    # + file should contain four columns: start wavelength (A), end wavelength (A), flux, error 
    # ++++++++++++
    #      'theoband' indicates the theoretical band (among those defined in theo_data_set['bands']) used to compare with the observed dataset
    # + each observed dataset must be associated with a unique theoretical band
    # + a given theoretical band may however be associated with several observed datasets, as long as they do not overlap in wavelength  
    # ++++++++++++    
    #      'method' defines how theoretical spectra are processed for comparison with spectra:
    # + 'abso_spec': the comparison is performed over flux spectra directly (relevant when spectra have absolute flux levels and are well modelled by the simulation)
    # + 'trans_spec': the comparison is performed over transmission spectra calculated with the master-out-of transit spectrum as reference (provided as input for observations, calculated by EVE for simulated spectra)
    # + 'norm_cont': the comparison is performed over spectra normalized by their own continuum around the target absorption lines (relevant when no out-of-transit baseline is available)
    # + 'trans_spec_norm_cont': the comparison is performed over transmission spectra as with 'trans_spec', but their continuum is normalized (relevant in case the data is sensitive to uncertainties in the simulated continuum)
    #       or with photometry:
    # + 'abso_flux': the comparison is performed over flux directly (relevant when spectra or photometry measurements have absolute flux levels)
    # + 'trans_flux': the comparison is performed over relative flux, normalized by the master-out-of transit flux
    #      More details on each method can be found in spectrum.py > observational_data().
    #      Note that the instrumental response chosen through 'inst_set' must be consistent with the chosen 'method' 
    # ++++++++++++    
    #      'inst_set' defines the instrumental response applied to the simulated spectra:
    # + None: no response (it may then be more relevant to use 'theo_data_set' only)
    # + HST_WFC3_G102 : HST telescope, WFC3 spectrograph, G102 mode
    # + HST_STIS_G140M_rec_x : HST telescope, STIS spectrograph, G140M mode, specific to a given dataset x
    # + HST_STIS_G140M_1200_x : HST telescope, STIS spectrograph, G140M mode at 1200 A, tabulated for a given slit x = 52x01, 52x02, 52x05, 52x20
    # + HST_STIS_E230M_2400_slx_dwy : HST telescope, STIS spectrograph, E230M mode at 2400 A, tabulated for a given slit x = 01x003, 02x006, 02x02, 6x02
    #                                 specific the pixel width y in A
    # + HST_COS_G130M_x : HST telescope, COS spectrograph, G130M mode, tabulated at a given wavelength x every 1 A in between 1134 et 1431 A
    # + spectro_wbandW : spectrograph with LSF approximated by a Gaussian profile at constant resolving power
    #                    spectro can be any of 'HARPS','CARMENES_NIR','IRD','GIANO','ESPRESSO','SOPHIE_HE'
    #                    set W to the central wavelength (in A) of the simulated band (typically 5890 A for sodium, 10830 A for helium)
    #       additional responses can be defined in init_data.py > inst_prop()
    # ++++++++++++
    #      'chi2_range' : defines the spectral or temporal range (depending on the chosen 'method') over which observated and simulated spectra or photometry measurements are compared
    # + ranges can be defined as independent intervals, but must be within the spectral or temporal range covered by the observed data
    #   one merit value is returned per independent interval, but the comparison is performed on the cumulated merit value  
    # + to estimate the spectral range to be used to compare a given line you can use w_star = w_line*( 1.+(rv[M/star]/299792.458))    
    # ++++++++++++
    #      'trange_sp' (optional) defines the temporal windows within which theoretical spectra will be processed into observational data for saving/plotting 
    # + times can be defined as independent intervals
    # + times in h, relative to mid-transit
    # + times must be within theo_data_set['trange'] so that theoretical spectra are defined at the required timesteps
    #   the full duration of observed exposures must be covered by simulated exposures (ie, the start and end times of simulated time windows must cover at least [ tobs_start-0.5*dt_simu ; tobs_end+0.5*dt_simu ], for each observed exposure)
    # + observations can be compared with all simulated timesteps, independently of the value possibly set for 'trange_sp' 
    # ++++++++++++
    #    set 'save_lc', 'save_sp', or 'save_sp_lc' to [] (no return) or :
    # + 'save_sp': 'file' and/or 'plot' return the measured and equivalent theoretical spectra in the observed time windows  
    #              'file_all' returns the equivalent theoretical spectra at each timestep within 'trange_sp' ('plot_all' not enabled)  
    #              this option is only relevant if 'datatype' = 'sp'     
    # + 'save_lc': 'file' and/or 'plot' return the measured and equivalent theoretical flux, in the observed time windows         
    #              'file_all' and/or 'plot_all' to return the integrated flux for theoretical data as seen with the instrument but at each timestep within 'trange_sp' (similar to 'inst_lc' in theo_data)
    #              this option is only relevant if 'datatype' = 'photom' 
    # + 'save_sp_lc': 'file' and/or 'plot' return the flux from measured and equivalent theoretical spectra, integrated over the spectral 'wav_lc' ranges, in the observed time windows  
    #                 'file_all' and/or 'plot_all' return the flux from equivalent theoretical spectra, integrated over the spectral 'wav_lc' ranges, at each timestep within 'trange_sp' (similar to 'inst_sp_lc' in 'theo_data')
    #                 define via 'wav_lc' = [ [ [w_lcA_1,w_lcA_2] , [w_lcA_3,w_lcA_4] , .. ] , [ [w_lcB_1,w_lcB_2] , [w_lcB_3,w_lcB_4] , .. ] , .. ] the light curves to be calculated: each element is a list of non-overlapping ranges, over which a given light curve is calculated
    #                 this option is only relevant if 'datatype' = 'sp' 
    #       add '_norm' as suffix to return normalized spectra and light curves (requires 'file_norm' to be set)
    #    use the 'raw_sp' in 'theo_data' to return spectra/light-curves at 1au with no instrumental response and at all timesteps    
    if dico_simu_set['sequence']==['main_occ']:
        obs_data_set['obs']={
            'obs_CHEOPS':{'datatype':'photom',
                      'inst_set':'CHEOPS',
                      'file_norm':'TBD.txt',
                      'dir':'55Cnc_CHEOPS_dataset',
                      'filelist':'55Cnc_CHEOPS.txt',
                      'trange_sp':[[-10.,10.]],
                      # 'theoband':'band_NaI',
                      'method':'trans_flux',
                      'chi2_range':[[-10.,10.]],
                      'save_lc':['plot','plot_all'],                  
                      },
            'obs_Spitzer':{'datatype':'photom',
                      'inst_set':'Spitzer',
                      'file_norm':'TBD.txt',
                      'dir':'55Cnc_Spitzer_dataset',
                      'filelist':'55Cnc_Spitzer.txt',
                      'trange_sp':[[-10.,10.]],
                      # 'theoband':'band_NaI',
                      'method':'trans_flux',
                      'chi2_range':[[-10.,10.]],
                      'save_lc':['plot','plot_all'],                   
                      },            
            }   
    if dico_simu_set['sequence']==['main_POLD','main_Na']:
        obs_data_set['obs']={
            'obs_Na':{'datatype':'sp',
                      'inst_set':'ESPRESSO_Na',
                      'file_norm':'HD209458_NaI_Mout.txt',
                      'dir':'HD209458_NaI_dataset',
                      'filelist':['HD209458_NaI_'+str(i)+'.txt' for i in np.arange(10)],
                      'trange_sp':[[-1.,1.]],
                      'theoband':'band_NaI',
                      'method':'trans_spec',
                      'chi2_range':[[5882.22,5903.24]],
                      'save_sp':['file','plot'],
                      'save_sp_lc':['plot','plot_all'],'wav_lc':[[5887.,5899.]],                   
                      }}        
    elif dico_simu_set['sequence']=='main_He':
        obs_data_set['obs']={
            'obs_HeI':{'datatype':'sp',
                      'inst_set':'NIRPS_He',
                      'file_norm':'HATP11_HeI_Mout.txt',
                      'dir':'HATP11_HeI_dataset',
                      'filelist':['HATP11_HeI_'+str(i)+'.txt' for i in np.arange(10)],
                      'trange_sp':[[-0.5,0.5]],
                      'theoband':'band_HeI',
                      'method':'trans_spec',
                      'chi2_range':[[10827.,10837.]],
                      'save_sp':['file','plot'],
                      'save_sp_lc':['plot','plot_all'],'wav_lc':[[[10830.5,10833.5]],[[10823.,10830.]]],                     
                      }}                        
    elif dico_simu_set['sequence']=='main_H':
        obs_data_set['obs']={
            'obs_HI':{'datatype':'sp',
                      'inst_set':'HST_STIS_G140M',
                      'file_norm':'HATP11_HI_Mout.txt',
                      'dir':'HATP11_HI_dataset',
                      'filelist':['HATP11_HI_'+str(i)+'.txt' for i in np.arange(10)],
                      'trange_sp':[[-1.,5.]],
                      'theoband':'band_HI',
                      'method':'abso_spec',
                      'chi2_range':[[1214.45368821,  1216.88671179]],     #corresponds to -300 ; 300 km/s around the Ly-alpha transition  
                      'save_sp':['file','plot'],
                      'save_sp_lc':['plot','plot_all'],'wav_lc':[[[1215.18,1215.51]],[[1215.79,1216.48]]],    #= [[-120.,-40.],[30.,200.]] km/s around the Ly-alpha transition              
                      }}          
    elif dico_simu_set['sequence']=='main_dust':
        obs_data_set['obs']={
            'obs_HI':{'datatype':'photom',
                      'inst_set':'TESS',
                      'file_norm':'WD1145017_VIR_Mout.txt',
                      'dir':'WD1145017_VIR_dataset',
                      'filelist':'WD1145017_VIR.txt',
                      'trange_sp':[[-1.,5.]],
                      # 'theoband':'band_HI',    #TBD : how is this dealt with since several bands are defined ?
                      'method':'trans_flux',
                      'chi2_range':[[-5.,5.]],   
                      'save_lc':['plot','plot_all'],     
                      }}     


    #################################################################################################################
    #%% Sky-projected and stellar grids
    #    - the grid that contains the projected stellar disk is square and made of square cells, with the central cell at (0,0)
    #    - it can be defined in two ways:
    # + with a constant stellar spectrum (in shape) that can be modulated by limb-darkening and the velocity field of the star
    #   in this case the star is a disk
    # + with a predefined grid
    #   uncomment 'predefgrid' to select this option
    #   in this case the size and number of cells in the grid enclosing the star will be overwritten with the content of the input file
    #   the spatial distribution of the star surface is assumed to be the same for all bands used in the simulation, ie that all the bands set in 'theo_data' must be defined in the predefined grid, and that 
    # a cell will be flagged as being part of the star surface if it emits in at least one band.
    #   a disk-integrated spectrum is calculated in each band from the input grid, to be used for various processes in the simulation; this is a strong approximation, as the planet will see different stellar spectra 
    #   as it moves around the star if its emission is strongly inhomogeneous
    #   the input file must be placed in 'dir' defined in theo_data, and it must be a .npz with the following fields:
    #       st_grid_width : total width of the stellar grid, in au
    #       st_grid_hn: number of cells on the half-side of the stellar grid
    #       wav_tab: a dictionary with each field a band with value an array [nwav] that contains the spectral table of the band
    #                these tables follow the same rules as defined in theo_data
    #       flux_grid: a dictionary with each field a band with value an array [2*st_grid_hn+1,2*st_grid_hn+1,2,nwav])
    #                  each cell of the grid contains a local stellar spectrum for the band, defined at 1au and at Earth 
    #       flux_mean_1au: a dictionary with each field a band with value the 'average' stellar spectrum at 1au over all directions around the star
    #################################################################################################################

        
    #%%% Predefined grid
    #    - fill in the following fields to use a pre-defined stellar grid:
    # + 'name' = 'grid_name.npz', name of the file containing the grid, which must be put in the 'Working_dir/Reference_data/star_name/' directory
    # + 'theo_bands = { band_name : grid_band , ..}' associates a theoretical band in EVE (from 'theo_data_set') with one of the bands for which the grid is defined
    # + 'scaling_factors = { band_name : value , ..}' associates a theoretical band in EVE (from 'theo_data_set') with a scaling factor to avoid duplication of stellar grids
    if dico_simu_set['sequence'] in ['main_X']:
        dico_star_grid_set['predefgrid'] = {
            'name':'HD189733_Xray_grid.npz',
            'theo_bands':{'band_X':'Xray'}
            }         
    else:
        dico_star_grid_set['predefgrid'] = {} 


    #%%% Custom grid
    if len(dico_star_grid_set['predefgrid'])==0:
    
        #%%%% Size of sky-projected grid
        #    - total widths of a rectangular grid centered on the star (in au), over which is calculated radiative transfer along the LOS
        #      set to None, otherwise to [Wx,Wy] where Wx is the total width along the sky-projected equator and Wy along the sky-projected spin axis
        #    - in au
        #    - relevant if optical processes (eg scattering) occur beyond the stellar disk 
        #    - must be larger than the grid covering the star along at least one dimension
        if dico_simu_set['sequence'] in ['main_POLD','main_Na','main_Fe','main_He','main_H','main_comets']:
            dico_star_grid_set['sky_grid_width'] = None
        elif dico_simu_set['sky_grid_width']=='main_occ':
            dico_star_grid_set['sky_grid_width'] = [2*0.003631261,2.15*0.0321838670552953] 
        elif dico_simu_set['sequence'] in ['main_dust']:
            dico_star_grid_set['sky_grid_width'] = [3*0.005407364,0.000426],  #3 a_planet x 10 Rstar        
    
    
        #%%%% Resolution of sky-projected grid 
        #    - number of cells on a half-side of the sky-projected stellar grid, tiled with cells of constant size
        #      the stellar grid will be 2*st_grid_hn+1 cells wide, and if relevant the sky-projected grid will be tiled beyond this until reaching the 'sky_grid_width' boundaries
        #    - relevant with a custom grid, otherwise set by the pre-defined grid
        if dico_simu_set['sequence'] in ['main_occ','main_POLD','main_Na','main_Fe']:dico_star_grid_set['st_grid_hn'] = 40                                  
        elif dico_simu_set['sequence']=='main_He':dico_star_grid_set['st_grid_hn'] = 20                     
        elif dico_simu_set['sequence']=='main_H':dico_star_grid_set['st_grid_hn'] = 10                   
        elif dico_simu_set['sequence']=='main_dust':dico_star_grid_set['st_grid_hn'] = 5              
        elif dico_simu_set['sequence']=='main_comets':dico_star_grid_set['st_grid_hn'] = 50     
    

        #%%%% Oversampling of stellar grid 
        #    - number of subcells dividing the side of a stellar cell
        #    - use to oversample limb-darkening and velocity field values across the cells
        #    - set to value > 1 to activate
        if dico_simu_set['sequence'] in ['main_X','main_H','main_dust']:dico_star_grid_set['st_grid_nsub'] = 1            
        elif dico_simu_set['sequence'] in ['main_occ','main_POLD','main_Na','main_Fe','main_comets']:dico_star_grid_set['st_grid_nsub'] = 10                                  
        elif dico_simu_set['sequence'] in ['main_He']:dico_star_grid_set['st_grid_nsub'] = 2                     


        #%%%% Rossiter distortions
        #    - shifts the reference stellar spectrum for all bands in each cell of the stellar grid according to the stellar surface RV field
        #    - based on main body ('body_0') properties     
        if dico_simu_set['sequence'] in ['main_X','main_H','main_dust','main_comets']:dico_star_grid_set['rossiter'] = False           
        elif dico_simu_set['sequence'] in ['main_POLD','main_Na','main_Fe','main_He']:dico_star_grid_set['rossiter'] = True                                 


        #%%%% Spot properties
        print('SPOTS settings to be defined as in ANTARESS')
          
  
    #%%% Plot    
    #    - set to plot extension to plot discretized bodies disk in front of stellar disk (single plot at arbitrary position)
    dico_gen_plot_set['bodies_grid'] = ''


    #################################################################################################################
    #%% Body-related features
    #################################################################################################################

    #################################################################################################################
    #%%% Opaque bodies
    #    - define here the properties for all bodies set in 'bodies_name'
    #    - the body grid is defined as a sky-projected surface opaque at all simulated wavelengths
    #################################################################################################################
    if dico_simu_set['sequence'] in ['main_X','main_POLD','main_Na','main_Fe','main_He','main_H','main_dust']:
        dico_bodies_grid_set['body_0']={}
    elif dico_simu_set['sequence']=='main_comets':
        dico_bodies_grid_set['body_0']={}
        dico_bodies_grid_set['body_1']={}
    

    #%%%% Radii
    #    - radii of the opaque body surface projected on the sky, along the sky-projected equator (X) and sky-projected spin axis (Y)
    #    - the opaque body can be a disk (put Ry_st_sky_Rpl=Rx_st_sky_Rpl) or an ellipse (put Ry_st_sky_Rpl different from Rx_st_sky_Rpl)
    #    - in units of bulk planet radius (as defined in ANTARESS_systems.py)
    #    - DO NOT SET TO DIFFERENT VALUES IF THE ANALYTICAL REGIME IS ACCOUNTED FOR (it can only be spherical) 
    dico_bodies_grid_set['body_0']['Rx_st_sky_Rpl'] = 1.   
    dico_bodies_grid_set['body_0']['Ry_st_sky_Rpl'] = 1.
    if dico_simu_set['sequence']=='main_comets':
        dico_bodies_grid_set['body_1']['Rx_st_sky_Rpl'] = 1.   
        dico_bodies_grid_set['body_1']['Ry_st_sky_Rpl'] = 1.
    

    #%%%% Resolution
    #    - spatial resolution of the square cells subdividing the body grid 
    #    - for high-accuracy studies, 'dbox_pl' must be fine enough to avoid introducing numerical variations in the level of the continuum opacity 
    #    - in km
    if dico_simu_set['sequence']=='main_X':dico_bodies_grid_set['body_0']['dbox_pl'] = 100.  
    elif dico_simu_set['sequence']=='main_occ':dico_bodies_grid_set['body_0']['dbox_pl'] = 1000.  
    elif dico_simu_set['sequence'] in ['main_POLD','main_Na','main_Fe']:dico_bodies_grid_set['body_0']['dbox_pl'] = 200.  
    elif dico_simu_set['sequence'] in ['main_He','main_H']:dico_bodies_grid_set['body_0']['dbox_pl'] = 100.                                      
    elif dico_simu_set['sequence']=='main_dust':dico_bodies_grid_set['body_0']['dbox_pl'] = 10.  
    elif dico_simu_set['sequence']=='main_comets':
        dico_bodies_grid_set['body_0']['dbox_pl'] = 10.  
        dico_bodies_grid_set['body_1']['dbox_pl'] = 10.  

     
    #%%%% Occulted bands
    #    - define the stellar spectrum bands (as defined in 'theo_data_set') for which absorption along the LOS for the opaque body should be calculated
    #    - this absorption is independent of the species in the simulation, but can depend on the band if limb-darkening is accounted for
    #    - preventing the occultation from a body can be useful if it is negligible, or if its LOS absorption is no interest in a given band (eg if the band spectrum is used for ionization only) 
    #    - format is [band1, band2, ...]
    dico_bodies_grid_set['body_0']['bands_occ'] = [bands for bands in theo_data_set['bands']]


    #%%%% Enlightened bands
    #    - define the specral bands for which the planetary emission along the LOS is calculated
    if dico_simu_set['sequence']=='main_occ':dico_bodies_grid_set['body_0']['bands_emit']=['band_occ']
    else:dico_bodies_grid_set['body_0']['bands_emit']=[]

    

    
    
    
    #################################################################################################################
    #%%% Analytical regimes
    #    - properties defined here are independent of species
    #    - these properties describe all gas structures modelled as 3D grids (rather than particles) in the simulations
    #    - properties only need defining if at least one body requires an analytical regime
    #################################################################################################################

    ################################################################################################
    #%%%% Common properties
    ################################################################################################

    #%%%%% Spatial resolution
    #    - size of the cubic cells subdividing sky-projected cells and LOS columns
    #    - absorption from analytical regimes is calculated within this grid 
    #    - grid is defined with respect to the stellar grid and is common to all analytical regimes
    #    - in Rjup    
    if dico_simu_set['sequence'] in ['main_Na','main_Fe']:dico_gen_anareg_set['dbox_ana'] = 0.05
    elif dico_simu_set['sequence'] in ['main_He','main_H']:dico_gen_anareg_set['dbox_ana'] = 0.1                                   


    #%%%%% Subdivision of edge cells
    #    - number of sample points covering the sky-projected side of an analytical regime column
    #      used to find the barycenter and effective surface of columns at the edges of planetary bodies
    #    - adjust to get the required precision of the regime absorption (for atmosphere, this mainly impacts calculation of high-density layers contributing to opacity continuum) 
    #    - unused if set to 1    
    dico_gen_anareg_set['nsamp_edge'] = 1
    if dico_simu_set['sequence'] in ['main_X','main_POLD','main_Na','main_Fe']:dico_gen_anareg_set['nsamp_edge'] = 10


    #%%%%% Maximum absorption threshold
    #    - calculation will stop for a given absorber at all wavelengths where the opacity of an analytical regime column is larger than -ln(thresh_anabs_max)
    if dico_simu_set['sequence'] in ['main_Na','main_Fe','main_He','main_H']:dico_gen_anareg_set['thresh_anabs_max'] = 1e-6
    

    #%%%%% Minimum absorption threshold 
    #    - calculation will not be performed, for a given absorber, in all cells of an analytical regime column (sorted by increasing opacity) with cumulated maximum opacity lower than - ln( 1 - thresh_anabs_min )
    #    - beware that decreasing the grid resolution may require to lower this threshold (as the cumulation of removed cells over many columns may be enough to yield a significant opacity)    
    if dico_simu_set['sequence'] in ['main_Na','main_Fe','main_He','main_H']:dico_gen_anareg_set['thresh_anabs_min'] = 1e-6


    #%%%%% Voigt oversampling
    #    - set value higher or equal to 1 (default = 1; the higher, the finer the resolution) to oversample all Voigt cross-section profiles
    #    - resolution in the region (with delta_v the effective resolution set for the calculation of opacity profiles):
    # + from 100% to 50% of the profile maximum: min(delta_v,hwhm_voigt/4.)/upsamp_f   
    # + from 50% to 1% of the profile maximum: min(delta_v,hwhm_voigt/2.)/upsamp_f  
    # + from 1% to 0.1% of the profile maximum: min(delta_v,hwhm_voigt)/upsamp_f  
    # + from 0.1% to 0.01% of the profile maximum: delta_v/upsamp_f  
    # + below 0.01%: delta_v
    if dico_simu_set['sequence'] in ['main_Na']:dico_gen_anareg_set['upsamp_f'] = 2.
    else:dico_gen_anareg_set['upsamp_f'] = 1.

    
    ################################################################################################
    #%%%% Atmospheres
    #    - define properties specific to each body for which an analytical atmosphere is simulated, or from which particles are launched from the top of the atmosphere
    #    - not relevant if only the transit of the opaque body is simulated
    ################################################################################################
    if dico_simu_set['sequence'] in ['main_Na','main_Fe','main_He','main_H']:dico_gen_anareg_set['ana_atm'] = {'body_0':{}}


    #%%%%% Structure            
    #    - the atmospheric structure is defined by its density, temperature, velocity, and pressure profiles
    #      each structure is constrained by specific properties defined below
    #    - the atmospheric structure is used :
    # + to calculate species properties in the cells of the body analytical regime, if ana_therm=True
    # + to calculate the properties of escaping particles, if 'launch_mode'!='null'
    #    - set 'structure' to:
    # + 'imp': import a pre-calculated atmospheric structure defining all properties
    # + 'pwinds': calculate density, temperature, and vertical velocity structure using p-winds code
    # + isothermal structure : define a common density profile shared by all species (scaled by a species-specific value), with constant temperature
    #                          allow for a 'rad_sat' (in Rp) radius below which density is saturated to a constant value
    #                          allow for a 'rad_null' (in Rp) radius above which density is null
    #                          choose among :
    #   > 'const': constant density
    #   > 'hydrostat': vertical hydrostatic density (possibly by layers)
    #   > 'hydrostat_long': vertical hydrostatic density with longitudinal density variations (constant on one hemisphere - possibly offset from the dayside - and decreases exponentially into the other hemisphere with longitude)
    #   > 'parkwind': expanding vertical structure as a parker wind
    #    - additional models can be implemented                 
    if dico_simu_set['sequence']=='main_Na':dico_gen_anareg_set['ana_atm']['body_0']['structure'] = 'hydrostat'
    if dico_simu_set['sequence']=='main_Fe':dico_gen_anareg_set['ana_atm']['body_0']['structure'] = 'hydrostat_long'
    if dico_simu_set['sequence'] in ['main_He','main_H']:dico_gen_anareg_set['ana_atm']['body_0']['structure'] = 'pwinds'

    
    #-------------------------------------------------
    #%%%%%% Imported structure
    #    - the structure can be 1D, 2D, or 3D
    #    - imported profiles must be defined as a function of (r,th,phi), the coordinates in the 'star-planet' orbital plane referential centered on the planet,  
    # with Xsp the star-planet axis, Ysp its perpendicular within the orbital plane in the direction of the planet motion (different from the tangent to the
    # orbital plane if eccentric orbit), and Zsp the normal to the orbital plane:  
    # + altitude (r) counted from the planet center
    # + longitudinal angle (theta) counted from the star planet axis around the normal to the orbital plane
    # + latidudinal angle (phi) counted from the orbital plane to the (planet center-cell) axis 
    #    - each atmospheric property is imported independently:
    # + possible properties : 'press','temp','vert_vel','long_vel','lat_vel'   
    # + if velocity components are not defined, they are set to 0
    # + if pressure is not required, it needs not be imported
    # + each property can depend on different coordinates    
    # + density is specific to each species, and the path to the relevant file must be defined in the species dictionary within 'sp_settings_set'
    #    - the imported file should contain four columns: r, th, phi, val
    # + unused coordinate tables should be set to nan
    # + for now, the imported grids are regular. 
    #   in 1D, the coordinate table is unique
    #   in 2D, the coordinates tables are (x0,x0, .. x1,x1, ..) and (y0,y1,..,y0,y1,..)
    #   in 3D: TBD
    #    - format : 
    # { prop_name : { 'path' : file_path} }
    #-------------------------------------------------  
    if dico_gen_anareg_set['ana_atm']['body_0']['structure']=='imp':
        dico_gen_anareg_set['ana_atm']['body_0']['temp']={'path':'/Mock_system/Valinor_temp.txt'}            
        dico_gen_anareg_set['ana_atm']['body_0']['vert_vel']={'path':'/Mock_system/Valinor_vert_vel.txt'} 


    #-------------------------------------------------
    #%%%%%% P-winds structure
    #    - the structure is calculated using the p-winds code
    #    - required inputs:
    # + m_dot [g.s-1] : total mass loss rate
    # + T_0 [K] : temperature
    # + h_fraction [] : mixing ratio of number of particles (H number fraction)
    # + nr [Rp] : radial extension of the model
    # + XUV : high-energy stellar spectrum set as
    #         {'mod' : 'band' , 'band_id' : band_id } : uses the chosen band among theo_data_set['bands']; spectrum must be defined at 1AU from the star
    #         {'mod' : 'imp' , 'path' : path } : upload from chosen absolute path, pointing to 2-columns file with wavelength [A] and flux at  1AU from the star [erg.s-1.cm-2.A]
    elif dico_gen_anareg_set['ana_atm']['body_0']['structure'] == 'pwinds':
        if dico_simu_set['sequence']=='main_He':
            dico_gen_anareg_set['ana_atm']['body_0']['m_dot']=1e11 
            dico_gen_anareg_set['ana_atm']['body_0']['T_0']=7000 
            dico_gen_anareg_set['ana_atm']['body_0']['h_fraction']=0.80  
            dico_gen_anareg_set['ana_atm']['body_0']['nr']=150
            dico_gen_anareg_set['ana_atm']['body_0']['XUV']={'mod' : 'band' , 'band_id' : 'band_XUV' }
        elif dico_simu_set['sequence']=='main_H':
            dico_gen_anareg_set['ana_atm']['body_0']['m_dot']=1e11 
            dico_gen_anareg_set['ana_atm']['body_0']['T_0']=7000 
            dico_gen_anareg_set['ana_atm']['body_0']['h_fraction']=0.80  
            dico_gen_anareg_set['ana_atm']['body_0']['nr']=150
            dico_gen_anareg_set['ana_atm']['body_0']['XUV']={'mod' : 'band' , 'band_id' : 'band_XUV' }


    #-------------------------------------------------
    #%%%%%% Isothermal structures
    #    - the atmospheric structure is defined by a constant temperature, within a single or (if possible) successive layers, as
    # format : {'temp':{'funcname':'ana_prop_cst','constr':{'cst':T_val}}} 
    #      with T_val in [K]
    #    - a common density profile is computed, from which is derived the density profile for each species :
    # + with a density parameter at Rtrans specific to the species
    # + or via the species mass loss rate, defined at Rtrans
    #      both parameters are defined in the species dictionary, so that no density constraints need to be defined here (the single/multi-layers density model is set by the temperature field)
    #    - the pressure profile is derived from the temperature and total density profile, if required for the calculations
    #      total density is constant with these atmospheric structures, and is set by the species present in the atmosphere (see 'nonsim_sp')
    
    #%%%%%%% Hydrostatic density
    #    - the atmosphere can be defined in successive layers with independent, constant temperatures and continuous density profiles
    #    - temperature format:
    # + 2-layers : {'temp':{'funcname':'ana_prop_2templayers','constr':{'temp1':T1_val, 'rad1-2':R12_val, 'temp2':T2_val}}} 
    # + 3-layers : {'temp':{'funcname':'ana_prop_3templayers','constr':{'temp1':T1_val, 'rad1-2':R12_val, 'temp2':T2_val, 'rad2-3':R23_val, 'temp3':T3_val}}} 
    #   with Ti_val the layer 'i' temperature in [K], Rij_val the radius of the transition between the layers 'i' and 'j' in [Rp]
    elif (dico_gen_anareg_set['ana_atm']['body_0']['structure']=='hydrostat'):            
       if dico_simu_set['sequence']=='main_Na':
           dico_gen_anareg_set['ana_atm']['body_0']['temp'] = {'funcname':'ana_prop_2templayers','constr':{'temp1':1000.,'rad1-2':2.,'temp2':3000.}}


    #%%%%%%% Hydrostatic density with longitudinal variations
    #    - single-layer profile, hydrostatic vertically and with longitudinal variations to approximate condensation fronts on the nightside
    #      density is constant between th_off + th_condens_left and th_off + th_condens_right (th_off = 0 deg and th_condens = +-90 deg corresponds to the dayside hemisphere)
    #      density decreases exponentially from the condensation front toward th_off+-180deg, at a rate 'th_rate'
    #    - longitudinal density format :
    # {'dens':{'constr':{'th_off': val , 'th_condens_left': val , 'th_condens_right': val , 'th_rate': val }}
    #      with 'th_x' in [rad] and 'th_rate' in [/rad]      
    elif (dico_gen_anareg_set['ana_atm']['body_0']['structure']=='hydrostat_long'):            
       if dico_simu_set['sequence']=='main_Fe':
           dico_gen_anareg_set['ana_atm']['body_0']['temp'] = {'funcname':'ana_prop_cst','constr':{'cst':2000}}           
           dico_gen_anareg_set['ana_atm']['body_0']['dens'] = {'constr':{'th_off':50.*np.pi/180.,
                                                                         'th_condens_left':-40.*np.pi/180.,                              
                                                                         'th_condens_right':170.*np.pi/180.,    
                                                                         'th_rate':0.01*np.pi/180.}}
           
    #-------------------------------------------------
    #%%%%%%% Parker wind
    #    - defines the total density profile as well as a vertical velocity profile
    #    - format :
    # {'dens' : {'dr':dr_val,'r':R_ref}}
    #      where dr_val defines the radial resolution of the model grid at R_ref, in [Rp]
    elif (dico_gen_anareg_set['ana_atm']['body_0']['structure']=='parkwind'): 
        dico_gen_anareg_set['ana_atm']['body_0']['dens'] = {'dr':0.001,'r':1.}           

    
    #%%%%%% Additional velocity components 
    #    - velocity flows can be added (if not already part of the structure) along three dimensions
    if (dico_gen_anareg_set['ana_atm']['body_0']['structure']!='imp'):
    
        #%%%%%%% Longitudinal 
        #    - longitudinal velocity (perpendicular to the planet-cell axis, parallel to the planet equatorial plane)
        #    - possibilities:
        # + day-to-night side wind at both terminators, with constant velocity 'vel' in [km/s], and possibility to offset the symmetry axis of the wind by a longitudinal offset 'th_off' in [rad] (positive counterclockwise, counted from the antistellar point)
        #   format : { 'long_vel':{	 'funcname':'day2nightside_wind' , 'constr':{'vel': v_val, 'th_off': th_off}  }
        # + atmospheric rotation, with constant angular velocity 'om_atm' in [rad/s] (ie, velocity dependent on r and phi)  
        #   format : { 'long_vel':{	 'funcname':'atmrot' , 'constr':{'om_atm': val }  }
        #   set 'om_atm' to 2*pi/Porbital to model the effect of rotation from a tidally-locked planet      
        # + day-to-night side wind and atmospheric rotation (combination of the two)         
        #   format : { 'long_vel':{	 'funcname':'day2nightside_atmrot' , 'constr':{'om_atm': val , 'vel': v_val, 'th_off': th_off}  }        
        # + longitudinal jet
        #   format : { 'long_vel':{ 'funcname':'ana_prop_jet_longvel', 'constr':{'vel' : val} } }
        if dico_simu_set['sequence']=='main_Na':
            dico_gen_anareg_set['ana_atm']['body_0']['long_vel'] = { 'funcname':'atmrot' , 'constr':{'om_atm': 2.*np.pi/(3.52472*24.*3600.) } }            
        if dico_simu_set['sequence']=='main_Fe':
            dico_gen_anareg_set['ana_atm']['body_0']['long_vel'] = { 'funcname':'day2nightside_atmrot' , 'constr':{'om_atm': 2.*np.pi/(1.80988145*24.*3600.),'vel':8.,'th_off':-10.*np.pi/180. } }
            
    
        #%%%%%%% Latitudinal    
        #    - latitudinal velocity (perpendicular to the planet-cell axis, in the polar plane)    
        #    - possibilities:
        # + uniform speed in [km/s], from equator to poles 	
        #   format : { 'lat_vel':{	'funcname':'ana_prop_eqpoles_latvel', 'constr':{'vel':val} } }


        #%%%%%%% Vertical
        #    - upward velocity (along the planet-cell axis)
        #    - possibilities :
        # + uniform 
        #   format : { 'vert_vel' : { 'funcname':'ana_prop_cst','constr':{'cst' : v_val}} } with v_val in [km/s]
        # + expanding (from Koskinen et al. 2013)
        #   format : { 'vert_vel' : { 'funcname':'ana_prop_vertvelKosk','constr':{'vel' : v_val}} } with v_val in [km/s] set at the transition radius
        if (dico_gen_anareg_set['ana_atm']['body_0']['structure'] in ['const','hydrostat','hydrostat_long']):
            stop()
            

    #-----------------------------------------------------------------
    #%%%%%% Latitude/longitude plots
    #    - define properties to be plotted among:
    # + temperature: 'temp'
    # + longitudinal ('long_vel'), latitudinal ('lat_vel'), vertical ('vert_vel') velocity components
    # + radial velocity ('rv') in planet rest frame
    #    - set altitude from planet center (in Rp)
    #    - define time window for plotting (in h relative to main body mid-transit)
    #-----------------------------------------------------------------
    if dico_gen_anareg_set['ana_atm']['body_0']['structure']=='imp':
        dico_gen_anareg_set['ana_atm']['body_0']['plot']={
            'rad':1.2,
            'type':['long_vel','rv'],
            't_plot':[-2.,2.]}


    #-----------------------------------------------------------------
    #%%%%%% Composition properties
    #-----------------------------------------------------------------
    
    #%%%%%%% Additional species 
    #    - define species within the atmosphere, which contribute to its structure but are not simulated
    #    - format : 
    # {'nonsim_sp' : { sp_name : dens } }
    #      where sp_name is the name of the species (from constant_data.py), and dens its density at Rtrans (in atoms/cm3)
    #    - this affects:
    # + the total atmospheric density 
    # + pressure, which can be required for opacity calculations
    # + 'mean_mass', if not pre-defined
    dico_gen_anareg_set['ana_atm']['body_0']['nonsim_sp'] = {}                
                
                
    #%%%%%%% Mean mass 
    #    - in amu
    #    - mean_mass = sum(xi * mi) with xi number fraction of each species, and mi their mass in amu
    #      xi = Ni / Ntot where Ni is the number density of the species
    #      see constant_data.py for possible values of mi
    #      for a solar composition (90.965% H, 8.889% He): mean_mass = 1.2726
    #      for a dissociated H2O composition (66.66% H and 33.33% O): mean_mass = 6.    
    #    - required for structures: 'imp', 'pwinds'
    #      can be provided for structures: 'hydrostat','hydrostat_long','parkwind' (self-determined if set to None)    
    #    - self-determination uses the simulated species densities and additional species in 'nonsim_sp'
    # + this is mostly relevant for simulations of the lower atmosphere, with fixed density profiles
    # + for simulations of upper atmospheres with density profiles scaled by particle densities, it is better to fix the mean mass
    #   indeed we do not know how the density of non-simulated dominant species (H+, e-, ...) varies along with the density of the scaled species
    #   and we thus cannot fix or estimate their density to recalculate the mean mass after scaling
    #   we thus fix the mean mass and make the strong assumption that it is kept whatever the scaling of simulated species
    #   nonetheless if all dominant species are simulated and scaled together, the mean mass can be allowed to be calculated
    # + must not be used if pressure is required, as total density must be calculated 
    if dico_simu_set['sequence']=='main_Fe':dico_gen_anareg_set['ana_atm']['body_0']['mean_mass']  = 6.
    elif dico_simu_set['sequence'] in ['main_Na','main_He','main_H']:dico_gen_anareg_set['ana_atm']['body_0']['mean_mass']  = 1.2726

    
    #%%%%%%% Energy-based density scaling    
    #    - applies scaling as
    # val(d) = val(a_planet)*(a_planet/d)^2
    #      with input values defined at d = a_planet     
    # + for isothermal structures, val = density constraint and mass loss rate
    # + for p-wind structure, val = input XUV flux and mass loss rate
    # + not applicable to 'imp' structure
    #    - this is to approximate a denser mass loss because of irradiation varying over an eccentric orbit
    #    - the scaling is common to all species in the atmosphere, and thus does not change mean_mass
    dico_gen_anareg_set['ana_atm']['body_0']['NRJ_sc']  = True
    

    #-----------------------------------------------------------------
    #%%%%% Self-shielding 

    #%%%%%% Update of column density grid
    #    - set to False to calculate the column density grid of the body analytical regime used for self-shielding only once at 1st time step   
    #    - set to True to recalculate the grid at all time steps
    # + use if parameter profiles vary over time, or density profile cannot be scaled
    # + use only if at least one species requires one type of self-shielding 
    # + set automatically to True if eccentric orbit
    dico_gen_anareg_set['ana_atm']['body_0']['calc_SSgrid']  =  False


    #%%%%%% Grid angular resolution	
    #    - in degrees
    #    - to account for self-shielding by the analytical regime, we use a high resolution 3D grid of line-of-sights discretized along their lengths
    #    - the grid is spherical with LOS starting from the star center
    #    - the grid symmetry axis goes from the star center to the center of the body
    #    - we allow for different species to use different resolutions for the (Temperature,Velocity) grid
    # but the 3D cartesian grid discretizing the analytical regime line-of-sights is the same for all species 
    #    - we define the number of high resolution column density columns along the angular side of a self-shielding column   
    if dico_simu_set['sequence'] in ['main_H']:
        dico_gen_anareg_set['ana_atm']['body_0']['n_subphi_HRSS'] =  1.
        dico_gen_anareg_set['ana_atm']['body_0']['n_subth_HRSS']  =  1.  
        dico_gen_anareg_set['ana_atm']['body_0']['n_subr_HRSS']   =  1.


    #%%%%%% Grid temperature and velocity resolution
    #    - the column density grid is discretized in temperature (K) and velocity (km/s, along the grid line-of-sights)
    #    - used to calculate the spectral opacity of all lines of the species
    #    - if a reference species is used, the 'coldens_grid' settings of the reference species will be used
    if dico_simu_set['sequence'] in ['main_H']:
        dico_gen_anareg_set['ana_atm']['body_0']['coldens_grid']  = {'dtemp':100.,'dvel':1.}
    

    #-----------------------------------------------------------------    
    #%%%%% Transition analytical / particle regimes     
    
    #%%%%%% Radius 
    #    - defines the envelope of the analytical regime associated with the body, and if relevant the envelope from which particles are released
    #    - the envelope is constant for a given simulation and is the same for all species, but is specific to each body
    #    - set to one of:
    # + 'rad' (in Rp) to define a spherical envelope of radius `rad` (typically up to the Roche lobe)
    # + 'rad_Xorb','rad_Yorb','rad_Zorb','EP_Xorb' (in Rp) to define an ellipsoidal surface in the body's `orbital plane referential`. 
    #    the radius coordinates are the semi-major axes of the ellipsoidal along tangent to the orbit in the orbital plane (Xorb), the normal to the orbital plane (Yorb), and the normal to the orbit in the orbital plane (Zorb)
    #    the field `EP_Xorb` is the distance between the centers of the ellipsoidal and  ofthe planet along the Xorb axis (>0 to have the center shifted behind the planet motion)
    # + 'pot' to set the envelope to the 3D equipotential corresponding to the gravitational potential `pot`
    #    `pot` is defined in fraction between the minimum at Rp and the maximum ( = 0 ) at the Roche lobe, so that V(input) = V(Rp)*(1-pot) with pot in [0,1]                                        
    if dico_simu_set['sequence']=='main_Na':dico_gen_anareg_set['ana_atm']['body_0']['trans_cond']  = {'rad':2.} 
    elif dico_simu_set['sequence']=='main_Fe':dico_gen_anareg_set['ana_atm']['body_0']['trans_cond']  = {'rad':1.5} 
    elif dico_simu_set['sequence'] in ['main_He','main_H']:dico_gen_anareg_set['ana_atm']['body_0']['trans_cond']  = {'rad':3.} 
    

    #%%%%%% Species spatial launch distribution
    #    - define mode ('funcname') and corresponding angular constraints ('constr')
    # + 'funcname' = 'uniform' : Uniform launch distribution
    #    > random launch positions within theta and phi ranges
    #    > constraints = [th_low,th_high,phi_low,phi_high], angular boundaries in rad
    #      * full surface : [-pi , pi , -pi/2 , pi/2]
    #      * dayside : [-3.*pi/2 , -pi , -pi/2 , pi/2] 
    #        only valid with circular orbit
    #      * terminator : [pi/2 - half_th , pi/2 + half_th , -pi/2 , pi/2] or [-pi/2 - half_th , -pi/2 + half_th , -pi/2 , pi/2] where 'half_th' control the longitudinal width of the launch area
    #        only valid with circular orbit 
    #      * evening (westside) terminator : [-pi/2 - 5.*pi/180. , -pi/2 + 5.*pi/180. , -pi/2 , pi/2]
    #        only valid with circular orbit                
    # + 'funcname' = 'cosine' : Raised cosine launch distribution
    #    > approximates local escape from body surface (volcanos, plumes, ...)
    #      multiple launch sites can be defined
    #    > constraints = [ [th_mean,phi_mean,sig,weight] , [] , ...], with 'mean' and 'sig' the angles (in rad) defining the site central location and opening of the cosine, and 'weight' controlling the relative mass loss between multiple sites (must sum up to 1)
    #    - launch distributions are constrained through angles theta and phi, in rad
    #      they are defined in the planet referential tangential to the orbit:
    # Xtan is the normal to the orbital trajectory within the orbital plane (different from the star-planet axis in case of eccentric orbit), positive outward
    # Ytan is the tangent to the orbital plane, positive in the direction of the planet motion
    # Ztan is the normal to the orbital plane
    #      theta within the orbital plane (>0 counterclockwise, =0 at X+, in th_start+0:th_start+pi, where th_start is any value in 0:pi as an offset does not change the coordinates)
    #      phi within any plane perpendicular to the orbital plane at a given theta (>0 above, =0 at the orbital plane, in -pi/2:pi/2)
    #    - additional functions can be added in EVE_launch_coord.py  
    elif dico_simu_set['sequence'] in ['main_He','main_H']:
        dico_gen_anareg_set['ana_atm']['body_0']['launch_distrib']  = {     
            'funcname':'uniform',
            'constr':[-pi , pi , -pi/2 , pi/2]}                                    
    elif dico_simu_set['sequence']=='main_dust':
        dico_gen_anareg_set['ana_atm']['body_0']['launch_distrib']  = {     
            'funcname':'cosine',
            'constr':[ [0.,0.,30.,0.5] , [50.,45.,10.,0.3] , [-70.,-80.,2.,0.2]]}  
    elif dico_simu_set['sequence']=='main_comets':
        dico_gen_anareg_set['ana_atm']['body_0']['launch_distrib']  = {'funcname':'uniform','constr':[-pi , pi , -pi/2 , pi/2]}   
        dico_gen_anareg_set['ana_atm']['body_1']['launch_distrib']  = {'funcname':'uniform','constr':[-pi , pi , -pi/2 , pi/2]}     
    
    
    ################################################################################################
    #%%%% Bow-shocks
    #    - dependant on the stellar wind properties 
    #    - define for specific bodies, otherwise do not define
    #    - NOT FULLY IMPLEMENTED IN CODE
    ################################################################################################
    dico_gen_anareg_set['ana_bs'] = {}
    if 'body_0' in dico_gen_anareg_set['ana_bs']:

        #%%%%% Geometry 
        #    - set up the geometrical structure of the bow-shock:
        # + 'Rs' [Rp] : stand-off distance 
        # + 'Rt' [Rp]: obstacle width 
        # + 'dhi' [deg]: angular resolution of the 1st annulus at the nose shock 
        #                the shock is made of successive annuli with increasing dphi and constant volumes, so that particles can be randomly distributed spatially
        #                the number of particles depends on each annulus density, assumed to be constant: this requires 'dphi' not to be too large
        # + 'dr' [Rp]: width of the shock, perpendicularly to its surface (increase to increase the number of particles)       
        # + 'phi_max' [deg]: maximum angle from the shock nose until particles are launched (must be larger than the limit where density becomes negligible)     
        dico_gen_anareg_set['ana_bs']['body_0']['geom'] = {'Rs':4.,'Rt':4.,'dphi':1,'phi_max':90}

   

    
    
    
    
    #################################################################################################################
    #%%% Self-shielding grids
    #    - relevant only if self-shielding is activated for one of the simulated regimes
    #    - define grid properties for each body in the simulation that can be surrounded by particles 
    # + if no particles are launched from a body and particles are better processed by the grid of another body, no need to define a body grid for the first one
    # + particles in the shadow cone of all bodies in the simulation are shielded by default (no need to use self-shielding)
    # + after one body grid is processed, the shielded particles are removed before moving to the next grid. Indeed, because all grids are spherical and centered on the star, the remaining particles cannot be affected by the ones already processed.
    # + because of the spherical grid geometries, the shielding from the analytical regimes of other bodies cannot be accounted for when processing a given body grid. 
    #   to reduce this caveat, the grids are processed from the closest to the farthest body from the star, so that only the particles behind the regimes farther than the one already processed may not be properly shielded
    # + a warning is issued when analytical regimes overlap in projection
    #    - adjust the boundaries of each body grid so that they overlap to a minimum, with each covering the densest part of the particle cloud closest to it
    #    - beware that a higher spectral resolution of the reference stellar spectrum will significantly increase computing time for self-shielding
    #################################################################################################################
    if dico_simu_set['sequence'] in ['main_H']:
        dico_SSgrids_set['body_0'] = {}


    #%%%% Maximum boundaries
    #    - define the limits of the outermost grid in radius (units of Dplanet(t)) and phi (rad)
    #      note that 'Dplanet(t)' is the effective star-body distance, thus the radial boundary will vary for an eccentric orbit
    #    - radial velocity boundaries are similarly defined, but are specific to each species and absorption process (sp_settings_set[sp]['ss_proc'][proc]['v_range])
    #    - the goal of these boundaries is to prevent the grids automatically extending to isolated particles far from the bulk of the particle cloud
    #      boundaries must however be set with care to include all dense regions of the particle cloud
    # + mind the cases of low ionisation (long tails), ENA (high velocities), eccentric orbits 
    # + mind that dense regions can produce self-shielding over a large range of radial velocities (the velocity range should include velocities associated to those regions)
    # > mind with multiple bodies that particles can be found far from a given body. The 'phi' limits of all bodies should be adjusted to try preventing that their grids overlap, and to enclose the parts of the cloud closest to each body    

        
 __________   

    

    dico_SSgrids_set['body_0']['outbounds']={
        'rmin_set':0.3, 
        'rmax_set':5.,  
        'phimax_set':pi        
        }
        
    #%%%% Sub-grid resolutions
    #    - define the cell resolutions of the different grids in radius (units of Rplanet), phi (rad), theta (rad) 
    #    - to estimate the maximum values of r and phi to set the resolution, consider that dl(th)=r*sin(phi)*d_th , dl(phi)=r*d_phi
    #      largest cells are obtained for maximum 'r' and maximum 'phi'
    #      for all cells to be smaller than dr along the phi arc, take d_phi<dr/r_max
    #                                                    theta arc, take d_th<dr/(sin(phi_max)*r_max) 
    #    - check that modifying the resolution has no influence on the results

    #%%%%% Planet grid
    dico_SSgrids_set['body_0']['plgrid']={   
        'dr':0.15,      
        'dphi':0.04*pi/180.,    
        'dth':5.*pi/180   
        }
                
    #%%%%% Analytical regime grid      
    dico_SSgrids_set['body_0']['anagrid']={    
        'dr':0.15,                 
        'dphi':0.04*pi/180.,   
        'dth':5.*pi/180      
        }    
        
    #%%%%% Buffer grid
    #    - 'rad_add' (added to 'rad_trans') defines the outer limit of the mixed grid = inner limit of the exosphere grid 
    dico_SSgrids_set['body_0']['mixgrid']={  
        'rad_add':0.6,    
        'dr':0.15,     
        'dphi':0.03*pi/180.,     
        'dth':4.*pi/180.    
        }
            
    #%%%%% Exosphere grid
    dico_SSgrids_set['body_0']['exogrid']={   
        'dr':0.2,        
        'dphi':0.05*pi/180.,
        'dth':3.*pi/180.    
        }

    #%%%% Plots
    #    - absorption or opacity grids from self-shielding

    #%%%%% Absorption of stellar flux from analytical regime
    dico_gen_plot_set['opabs_SSanagrid_stflux'] = ''
    
    #%%%%% Absorption of stellar flux from everything
    dico_gen_plot_set['opabs_SSgrid_stflux'] = ''
    
    #%%%%% Absorption of stellar wind protons from analytical regime
    dico_gen_plot_set['opabs_SSanagrid_pr'] = ''
    
    #%%%%% Absorption of stellar wind protons from everything   
    dico_gen_plot_set['opabs_SSgrid_pr'] = ''


    

    
    #################################################################################################################
    #%%% Electron properties
    #    - defines the properties of electrons in the vicinity of each body
    #    - used to calculate electron ionization or recombination
    #################################################################################################################
    dico_elec = {}
    
    #%%%% Activation
   	#    - set to:
    # + None : no electrons are required
    # + 1: 3D grid or other way to take electron population into account self-consistently with ionization/recombination (TBD)
    # + 2: electrons profiles are imported
    dico_elec['calc_elecgrid'] = None
    
    
    #%%%% Properties    
    #    - specific to each body
    #    - settings determine how each electron property is calculated
    #    - set 'prop' to :
    # + 0 : profile is imported (set absolute 'path' to relevant file)
   	# + 1 : profile is constant (set 'val_limit' to the chosen value)      
   	# + 2 : profile is calculated with an analytical expression (set constraints with specific field for each property, if available)
    dico_elec['body_0'] = {
        
        #%%%%% Density 
        #    - in e-/cm3
        #    - prop = 2 sets a power law constrained by density 'val_limit' (e-/m3) at distance from the planet 'r_limit' (Rp)
        'dens':{
            'prop':2,
            'r_limit':2,
            'val_limit':1e8
        },	
             	
        #%%%%% Temperature 
        #    - temperature in K	
        #    - prop = 2 : TBD         
        'temp':{
            'prop':2,
        },

    }
    
    
    #################################################################################################################
    #%%% Collisions
    #    - define subdictionary for each body around which collisions are to be accounted for
    #      otherwise comment/do not define
    #################################################################################################################
    
    dico_collgrid.update({
    
    #    #Main body
    #    'body_0':{
    #    
    #        #Calculation of the collision grid 
    #        #    - possibilities:
    #        # 0: calculated until stationary regime 
    #        # 1: calculated each timestep (by default if eccentric orbit)      
    #        'calc_collgrid':1,
    #	
    #        #Grid properties
    #        #    - define the resolution of the fixed cubic cells: 
    #        # > should be large enough to allow adaptative mesh refinement until subcells have widths in the order of the mean free path)
    #        # > in Rp
    #        #    - define the size of each side of the grid:
    #        # > counted from the planet center in the orbital plane referential
    #        # > adjusted to the resolution
    #        # > in Rp
    #        'ds_grid':1.,      
    #        'x_min':15,   
    #        'x_max':15, 
    #        'y_min':15, 
    #        'y_max':15, 
    #        'z_min':15, 
    #        'z_max':15
    #
    #    }
    
    })
    
        

    
    #################################################################################################################
    #%% Stellar wind properties
    #    - defines the wind properties for Energetic Neutral Atoms formed through charge-exchange
    #    - properties are used if at least one species dictionary contains the field 'charge_ex'
    #################################################################################################################
    dico_ENA = {}
    
    #%%%% Time window
    #    - window during which ENA will be processed (in h)
    #    - leave empty to process the entire simulation
    #    - it corresponds to times when the stellar wind interacts with the planetary exosphere, not times when it was emitted by the star
    dico_ENA['ENA_window'] = []
    

    #%%%% Properties 
    #    - settings determine how each ENA property is calculated
    #    - set 'prop' to :
    # + 0 : profile is imported (set absolute 'path' to relevant file)
   	# + 1 : profile is constant (set 'val_limit' to the chosen value)      
   	# + 2 : profile is calculated with an analytical expression (set constraints with specific field for each property, if available)

    #%%%%% Density 
    #    - in protons/m3
    #    - prop = 2 sets a quadratic law constrained by density 'val_limit' (protons/m3) at distance from the star 'r_limit' (AU)
    dico_ENA['dens'] = {    
        'prop':2,
  		'r_limit':1.,   
  		'val_limit':1.,
    }


    #%%%%% Temperature 
    #    - in K
    #    - no analytical expression available
    dico_ENA['temp'] = {    
        'prop':1,
        'val_limit':200000.,	
    }
    
    
    #%%%%% Radial velocity 
    #    - in km/s
    #    - no analytical expression available
    dico_ENA['vel'] = {    
        'prop':1,
        'val_limit':100.,	
    }    
    
    
    
    #################################################################################################################    
    #%% Species properties 
    #    - defining their properties in the particle and analytical regimes
    #################################################################################################################
    
    #%%% Species
    sp_settings_set['H_0+_g']={}     #atomic example
    sp_settings_set['pyrmg40']={}    #dust grain example
    
    
    #################################################################################################################    
    #%%% Plots
    #    - set to a plot extension to activate
    #################################################################################################################
    
    #%%%% Escape rates
    #    - input and effective escape rates over time, for all species with launched particles
    dico_gen_plot_set['esc_tau'] = ''
    
    
    #################################################################################################################
    #%%% Particle regime
    #    - species can be atoms, molecules, or grains
    #    - the format of atomic species is `X_n+_Y` where `X` is the atomic symbol, `n` its ionization degree, and `Y` an identifier of its excitation level
    #    - implement new species properties in antaress.ANTARESS_general.constant_data.py
    #################################################################################################################    

    #%%%% Particles per metaparticle
    #    - a species is described by metaparticles that contain a fixed number of particles (atoms or dust grains), set by :
    # + gas: a constant Npermeta = 'npermeta' for all metaparticles
    # + dust: a power law Npermeta(s) = 'npermeta'*(s / 1 mic)^(-'npermeta_alpha')
    #         where 'npermeta' is the number of particles per metaparticles for grain sizes of 1 micron
    #         this is to avoid the simulation being dominated by small metagrains with very few large metagrains, as particles are directly launched as metaparticles and typical dust launch size distribution are power laws generating more small particles than large ones
    #         with 'npermeta_alpha' > 0, more small grains are grouped per metagrain of their size (ie, npermeta is larger) and fewer large grains are grouped per metagrain of their size (ie, npermeta is smaller) 
    #         an intermediate value must be found to sample adequately the metagrains in size, in between 0 (metagrain distribution is the same as grain, and small metagrains are over-represented) and the exponent of the grain launch size distribution 
    # sp_settings_set[sp]['siz_distrib']['exp'] (metagrain distribution is uniform, and small metagrains are under-represented)
    #    - 'npermeta' represents a discretization in density of the particle cloud
    #      furthermore a metaparticle absorbs the spectrum emitted by a stellar cell along the line-of-sight, and if requested the spectrum emitted by the point-source star along a radius of the self-shielding grid. 
    #      'npermeta' thus also represents a discretization in opacity of the particle cloud
    #      the number of particles per metaparticle must therefore be:
    # + small enough to sample the 3D structure of the particle cloud and ensure that a metaparticle absorption does not saturate
    # + large enough to allow the computation to run with a reasonable number of metaparticles    
    #      look at the relevant pre-processing tutorial to adjust 'npermeta' to maintain the maximum or mean opacity, over all processes, and over all spectral bands, below a given threshold 
    #      you can further check the metaparticle opacity for a given simulation in EVE Summary file
    #    - a smaller star with the same number of cells for the stellar grid will yield a larger opacity, for the same value of 'npermeta'         
    sp_settings_set['H_0+_g']['npermeta'] = 1e30
    
    sp_settings_set['pyrmg40']['npermeta'] = 1e22
    sp_settings_set['pyrmg40']['npermeta_alpha'] = 5./3.


    #################################################################################################################
    #%%% Radiative processes
    #    - these settings allow defining the opacity profiles to be calculated for radiative processes associated with the species 
    #    - processes can include:
    # + absorption (from particles and analytical regimes, along the line of sight)
    # + self-shielding (from particles and analytical regimes, along stellar radii)
    # + diffusion (from particles and analytical regimes)
    # + radiation pressure (upon particles)   
    #    - for each absorption/emission process, define if they should be accounted for particles and analytical regimes of all bodies that contain this species
    #    - processes are specific to a given species and be one of:
    # + electronic transitions: for atoms, defined analytically
    # + broadband processes: for atoms and molecules, defined analytically
    # + tabulated: for any type of species
    #      additional processes can be defined in EVE_mainproc > EVE_cross_sections.py
    #      each process is specific to a unique species, but a given species can be linked to multiple processes
    #    - beware that absorption can extend at high velocities because of damping wings/fast moving particles
    #    - the range of absorption/diffusion processes can overlap with several theoretical band spectra
    #    - remove field if no processes of a given type are required for the species
    #    - properties are common to all bodies harboring the species in the simulation  
    #    - each process is specific to a given species, as indicated in constant_data.py 
    #    - define the spectral range over which processes are calculated as :
    # + 'vrange' = [x1,x2] : in km/s, for electronic transitions
    # + 'wrange' = [x1,x2] : in A, for broadband processes  
    #    - for absorption, self-shielding, and diffusion processes, define the contributors to the process as sp > proc_type > proc_name > 'contributors' : [ x1, x2, .. ], where x can be:
    # + 'part': particles 
    # + 'ana_reg': analytical regimes  
    #    - specific plot can be requested for each process as 
    # sp > proc_type > proc_name > 'plot_proc' : [ plot1, plot2, etc ] 
    #      see list of plots available for each process in EVE_plots.py
    #      leave empty otherwise
    #################################################################################################################    
    
    #%%%% LOS absorption
    #    - those processes decrease the flux in the bands of the stellar spectrum defined in 'theo_data', as seen by the observer at 1au and at Earth distance
    #    - opacity profile from a given process should be calculated with a resolution fine enough to capture its variations, set up through 'sp_res' (in km/s for electronic transitions, in A for broadband processes)
    #      to do so, the corresponding cross-sections can either:
    # + be calculated at the resolution of the stellar spectrum, if it is close to the required resolution (set 'sp_res' = 0)         
    # + be calculated at a coarser resolution, defined with sp_res (in km/s for electronic transitions, in A for broadband processes)
    #   this approach should be used when the resolution of the stellar spectrum is much finer than the typical length of variation of the absorber opacity profile
    # + be imported as tabulated cross-section profiles, which are pre-interpolated over the stellar spectrum table (no need to define 'sp_res')
    sp_settings_set['H_0+_g']['abs_proc']={}    
    
    #----------------------------
    #%%%%% Electronic transition 
    sp_settings_set['H_0+_g']['abs_proc']['Lalpha'] = {
        
    
        #%%%%%% Contributors
        'contributors':['part','ana_reg'],   
    
    
        #%%%%%% Spectral range 
        #    - in km/s 
        'vrange':[-100.,100.],
    
    
        #%%%%%% Resolution
        #    - in km/s 
        'sp_res':0.,
    
    
        #%%%%%% Plots
        'plot_proc':[],
    
    }
    
    #------------------------  
    #%%%%% Broadband process
    sp_settings_set['H_0+_g']['abs_proc']['H0_XUV'] = {
    
    
        #%%%%%% Contributors
        'contributors':['part','ana_reg'],    
    
    
        #%%%%%% Spectral range
        #    - in A
        'wrange':[5.,912.],    
        
        #%%%%%% Resolution
        #    - in A
        'sp_res':0.,    
        
    
        #%%%%%% Plots
        'plot_proc':[],
    
    }
          
    #-----------------------------------------------------
    
    #%%%% Self-shielding
    #    - those processes decrease the flux in the bands of the stellar spectrum defined in 'theo_data', at the position of each particle subjected to radiative processes
    #    - opacity profiles will be calculated at the required resolution for each grid (using 'sp_res', unless tabulated), and interpolated 
    # over the stellar spectrum table (unless directly calculated over its spectral bins if 'sp_res' is set to 0)
    #    - opacity profile from a given process should be calculated with a resolution fine enough to capture its variations, either:
    # + at the resolution of the stellar spectrum, if it is close to the required resolution (set 0)
    # + at a coarser resolution (set in km/s for electronic transitions, in A for broadband processes)
    #      tabulated opacity profiles are pre-interpolated over the stellar spectrum table and needs no interpolation (no need to define 'sp_res')
    sp_settings_set['H_0+_g']['ss_proc']={}     

    #----------------------------
    #%%%%% Electronic transition 
    sp_settings_set['H_0+_g']['ss_proc']['Lalpha'] = {    
    
        #%%%%%% Contributors
        'contributors':['part','ana_reg'],     


        #%%%%%% Spectral range 
        #    - in km/s
        'vrange':[-100.,100.],
        
        
        #%%%%%% Resolution
        #    - spectral resolution of the opacity profiles in each self-shielding grid
        #    - in km/s  
        'sp_res':{'exogrid':10.,'mixgrid':5.,'anagrid':5.,'plgrid':5.},
 
    
        #%%%%%% Plots
        'plot_proc':[],    
 
    }
    
    #------------------------  
    #%%%%% Broadband process
    sp_settings_set['H_0+_g']['ss_proc']['H0_XUV'] = {
    
    
        #%%%%%% Contributors
        'contributors':['part','ana_reg'],    
    
    
        #%%%%%% Spectral range
        #    - in A
        'wrange':[5.,912.],    
        
        
        #%%%%%% Resolution
        #    - in A
        'sp_res':{'exogrid':10.,'mixgrid':10.,'anagrid':10.,'plgrid':10.}, 
        
    
        #%%%%%% Plots
        'plot_proc':[],
    
    }    

    #%%%%% Dynamical selection
    #    - particles with velocities outside of the range (in km/s) will not contribute to the self-shielding of any process
    #      this can be useful when a few particles have very large velocities, to prevent extending the self-shielding tables uselessly
    #    - beware that the range should include all velocities from regions of the atmosphere that contributes significantly to self-shielding, 
    # unless there are no particles that can be affected by self-shielding at these velocities
    #    - because projected Doppler velocities are lower than absolute velocities, particles with high absolute velocities may not be taken into account
    #      when stellar wind interactions are involved, and because they are linked to the absolute particle velocities, make sure the boundaries extend to the
    # maximum absolute velocities of particles of interest 
    sp_settings_set['H_0+_g']['ss_proc']['vrange_self'] = [-300.,100.]  

          
    #-----------------------------------------------------
    
    #%%%% Radiation pressure
    sp_settings_set['H_0+_g']['prad_proc']={}    

    #----------------------------
    #%%%%% Electronic transition 
    #    - radiation pressure-to-stellar gravity ratio is calculated from the disk-integrated stellar reference spectrum
    sp_settings_set['H_0+_g']['prad_proc']['Lalpha'] = {
    
    
        #%%%%%% Isotropic impulse
        #    - set to True to account for the isotropic contribution of the photons (from reemission) besides the radial contribution of the photons (from absorption)	
        'rad_iso':False,

    
        #%%%%%% Spectral range 
        #    - in km/s 
        'vrange':[-100.,100.],  


        #%%%%%% Self-shielding
        #    - set to True to use the stellar spectrum accounting for self-shielding processes
        'shielded_proc':False,        


        #%%%%%% Plots
        #    - options:
        # + 'prad_part': radiation pressure coefficients on each particle
        'plot_proc':[],        
        
    }
        
    #----------------------------
    #%%%%% Constant
    #    - assumes a constant radiation pressure-to-stellar gravity ratio, to mimick coupled dynamics between multiple species thus subjected to an 'average' radiation pressure
    #      for consistency set the same beta for those different species
    #    - set to a non-zero value to activate (only if no other radiative pressure process is defined)
    #    - not affected by self-shielding
    sp_settings_set['H_0+_g']['prad_proc']['constant_beta'] = {'beta' : 0}




    #################################################################################################################
    #%%% Change of state
    #    - possibilities: 
    # + 'photo_ion' : photo-ionization of gas species
    # + 'elec_ion' : electron-ionization of gas species
    # + 'elec_rec' : electron-recombination of gas species
    # + 'sublim' : sublimation of dust species
    # + 'charge_ex' : charge-exchange (between 'H_0+_g' and stellar wind protons for now)
    #    - leave the field undefined to disable
    ################################################################################################################# 

    #%%%% Photo-ionization
    #    - the input stellar spectrum must be defined up to the photoionization threshold of the species, except in ranges where the photoionization cross-section is low enough as to be neglected
    sp_settings_set['H_0+_g']['photo_ion'] = {
            
        
        #%%%%% Self-shielding
        #    - set to True to use the stellar spectrum accouting for self-shielding processes
        'shielded_proc':False,
        
        
        #%%%%% Release ionized species
        #    - set to True to simulate children species released by ionization of current species
        #    - the children species must be defined as an independent species in the current configuration file 
        'child_sp':False,               
    
    }  

    #%%%% Electron-ionization
    if 0==1:sp_settings_set['H_0+_g']['elec_ion'] = {}

    
    #%%%% Electron-recombination
    if 0==1:sp_settings_set['H_0+_g']['elec_rec'] = {}


    #%%%% Stellar wind interactions  
    if 0==1:sp_settings_set['H_0+_g']['charge_ex'] = {
      
        #%%%%% Self-shielding
        #    - if True, stellar wind protons are shielded by the species particles the analytical envelop of the main body
        'self_pr':False,
      
    }



    #################################################################################################################
    #%%% Analytical regime
    #################################################################################################################    



    
    if 0==1:
        sp_settings_set.update({


        'H_0+_g':{


            #################################################################################################################
            #Analytical regimes properties
            #    - can describe:
            # + atmospheres (spherical or ellipsoidal, as defined in 'dico_bodies_grid_set')
            # + launch conditions for particles 
            # + bow-shocks
            #    - the same bodies must be present in 'dico_gen_anareg_set'
            #################################################################################################################
            'dico_anareg':{
            
                #Main body
                'body_0':{
    
                    #Analytical atmosphere & transition properties 
                    #    - comment/remove if unused
                    'ana_atm':{
                    
                        #To take into account the analytical regime for this species	
                        'ana_therm':True,
                        
                        #Launch mode
                        #    - unused if analytical thermosphere structure is modeled		
                        #    - mode to calculate number of launched particles:
                        # + 'esc_rate': from input escape rate
                        #               will constrain the regime density profile (transition radius cannot be set by knudsen or density inputs in that case) unless 'decoupled' is used
                        # + 'null': no particles are launched
                        #    - if a reference species is used, density profile and escape rate for current species are scaled to the reference species values independently,
                        'launch_mode':'esc_rate', 
    #                    'launch_mode':'decoupled', 
    #                    'launch_mode':'null',
                        
                        #Escape rate
                        #    - in g/s, used if launch_mode='esc_rate' or 'decoupled'
                        #      if a reference species is used, the escape rate of current species will be scaled to that of the reference species
    #                    'esc_tau':4.3e7/1e4,     #TRAPPIST1b nominal
    #                    'esc_tau':1.1e7*0.0002,     #TRAPPIST1f nominal
    #                    'esc_tau':1e7,   #55 Cnc e
                        'esc_tau':1e7,   #GJ3470b
                        
                        #Reference distance for the escape rate
                        #    - set 'esc_tau_dist' to the distance from the star at which 'esc_tau' is defined :
                        # + 'sma' : semi-major axis
                        # + '1au' : 1 au
                        # + 'peri' : periastron
                        # + x (float) : specific distance, in au
                        #    - this is only relevant if the planet is on an eccentric orbit
                        'esc_tau_dist':'sma',
                        
                                            
                        #-------------------------------------------------
                        #Density properties
                        #-------------------------------------------------
    
                        #-------------------------------------------------
                        #Imported structure
                        #    - used if 'structure' = 'imp', see the body regime dictionary
                        #-------------------------------------------------  
            
    #                    'dens':{'path':'/Travaux/Evaporation/Modele_upperatm/Simu_results/WASP107b_ndensProf_Ttherm12000.0_tauTot1.00e+10.dat'},          
    
                        #-------------------------------------------------
                        #Constraints to scale common density profile
                        #    - it will be scaled for the species to the given density value, in atoms/cm3, at the transition radius
                        #    - this constraint is not used if 'launch_mode'='esc_rate'
                        #    - this constraint is automatically scaled along an eccentric orbit, assuming it is defined at 'a_planet' from the star
                        #------------------------------------------------- 
    
    #                    'dens':{'constr':{'dens_trans':1e10}},
    
                        #-------------------------------------------------
                        #Constraints for complex structure
                        #    - TODO: voir si contraintes comme abondance a definir pour initialiser ou contraindre le modele
                        #------------------------------------------------- 
    
    
    
                    },
    
                    #------------------------------------------------------------
    
    #                #Bow-shock        
    #                #    - comment/remove if unused
    #                #    - populate the body bow-shock with current species particles
    #                #    - shock geometry is independent of the species, but dependent on the body and stellar wind properties and must be defined in dico_gen_anareg_set['ana_bs'][body]
    #                'ana_bs':{
    #
    #                        #-------------------------------------------------
    #                        #Density profiles
    #                        #-------------------------------------------------
    #                        #    - TBD
    #                        #-------------------------------------------------
                    
    #                    
    #                        #Density properties 
    #                        #    - constr = ( radius [au] , density [atoms/m3] , alpha ) 
    #                        #    - density is set by dens(r_star)*(Rs/r_pl)^alpha
    #                        # + dens(r_star): density at the nose of the shock, set by the radius (r_star) & density (dens(r_star)) constraints below, and following the same variations
    #                        # with distance to the star as the stellar wind protons
    #                        # + Rs: stand-off distance of the shock, ie distance to the planet center (defined by the shock geometry)
    #                        # + r_pl: linear distance from a point of the shock to the planet (defined by the shock geometry) 
    #                        # + alpha: exponent describing how quickly the density changes with distance from the density at the nose 
    #                        'dens':{
    #                    		'funcname':'anabs_prop_densfromnose',
    #                    		'constr':{'rad':0.031,'dens':1.,'alpha':400}
    #                        },    
    #                
    #                }
    
                }, #end of main body
    
    #            #########################
    #            #Second body
    #            'body_1':{
    #
    #                'ana_atm':{
    #                
    #                    #Analytical regime	
    #                    'ana_therm':True,
    #                    
    #                    #Launch mode
    #                    'launch_mode':'esc_rate', 
    #                    
    #                    #Escape rate
    #                    'esc_tau':0.*1e8,
    #
    
    #                    #Density properties 
    #                    'dens':{
    #                        'prop':2,
    #                        'funcname':'ana_prop_hydrostat',
    #                        'constr':{'dens':1e10}
    #                    },
    #
    #                }
    #                
    #            }, #end of body
    #
    #            #########################
    #            #Third body
    #            'body_2':{
    #
    #                'ana_atm':{
    #                
    #                    #Analytical regime	
    #                    'ana_therm':True,
    #                    
    #                    #Launch mode
    #                    'launch_mode':'esc_rate', 
    #                    
    #                    #Escape rate
    #                    'esc_tau':0.*1e8,
    #
    #
    #                    #Density properties 
    #                    'dens':{
    #                        'prop':2,
    #                        'funcname':'ana_prop_hydrostat',
    #                        'constr':{'dens':1e10}
    #                    },
    
    #
    #                }
    #                
    #            }, #end of body
    #
    #            #########################
    #            #Fourth body
    #            'body_3':{
    #
    #                'ana_atm':{
    #                
    #                    #Analytical regime	
    #                    'ana_therm':True,
    #                    
    #                    #Launch mode
    #                    'launch_mode':'esc_rate', 
    #                    
    #                    #Escape rate
    #                    'esc_tau':0.*1e8,
    #
    #                    #Density properties 
    #                    'dens':{
    #                        'prop':2,
    #                        'funcname':'ana_prop_hydrostat',
    #                        'constr':{'dens':1e10}
    #                    },
    
    #
    #                }
    #                
    #            }, #end of body
    #
    
             	
            }, #end of dico_anareg
    
            #################################################################################################################
            #Plot and various properties
            #################################################################################################################
            
            #To tag the particles according to a given condition
            #    - condition must be defined within the code (eg created from ionization/recombination, from charge-exchange, etc.)
            #    - required only if species particles are present in the simulation 
            'tag':False,
            
            #To save the time launch of the particles
            #    - required only if species particles are present in the simulation
            'tlaunch_part':True,
            
            #To identify particles with a unique integer
            #    - integers are unique for all time steps of the simulation, but can be the same between different species
            #    - required only if species particles are present in the simulation
            'id_part':False,
            
            #Species-dependent plots 
            #    - set field in list to plot, otherwise leave empty or remove
            #    - possibilities:
            # + 'camera': view of the particle cloud from a given position
            # + 'above': view of the particle cloud from above the planetary system
            # + 'earth': view of the particle cloud along the LOS
            # + 'ana_coldens_grid': column density of the species for LOS absorption from analytical regimes
            #                       plotted only if absorption is required for the species, and at least one analytical regime transits
            #                       plotted for all bodies regimes independently, and for all regimes together
            # + 'ana_opa_grid': opacity/absorption grid and profiles in all bands absorbed by the analytical regimes populated by the species
            # + 'ana_coldens_SSgrid': column density of the species for SS absorption from the analytical regimes of all relevant bodies
            #                         plotted only if SS is required for the species
            # + '3D_anagrid': 3D grid of the analytical regime properties for the species
            
            #### definir comme un dico les props a plotter
            
            'plot':{
    
        #        'type':['above','earth','camera','ana_coldens_grid','ana_opa_grid','3D_anagrid'],   
                'type':['above','earth','camera'], 
            
                #Time interval within which save the plots
                #    - in h
                't_plot':[-1.,0.1]
        #        't_plot':[-30.,30.] 
            }
                
        }}) #end of main species in gases_settings
        
        
        
        
        
        
        
        
        
        
        
        
    #################################################################################################################
    #################################################################################################################
    #Other species properties
    #    - see similar main species properties for details
    #################################################################################################################
    #################################################################################################################
    
    #Neutral, ground-state helium
    if 0==1:
        sp_settings_set.update({
    
        'He_0':{
    
       	#Bands
              'bands_gas':{'He_Rayleigh':{
              
                  #Spectral resolution (A)  
                  'delta_w':1.,
                  
                  #Spectral range for theoretical absorption (A) 
                  #    - can overlap with several theoretical band spectra
                  'wrange':[5882.,5904.],
            
                    		} #end of current band
           			
        		}, #end of line/bands for current species
    
              #Analytical regime properties
              'dico_anareg':{'body_0':{
                  'ana_atm':{      
                   	#To take into account the analytical regime for this species	
                   	'ana_therm':True,
            
                   	#Launch mode
                   	'launch_mode':'null', 
    
          
    #                	#Density properties 
    #                	'dens':{
    #                		'prop':2,
    #                		'funcname':'',
    #                		'constr':[7e4]
    #                		},
    #                	
    #                	#Temperature properties 
    #                	'temp':{
    #                		'prop':2,
    #                		'funcname':'',  
    #                		'constr':[]
    #                		},	
                  }
              }},
        
     }})
    
    
    #Metastable helium
    if 0==1:
        sp_settings_set.update({
    
        #Gas species
        #    - see possibilities in constant_data.py
        'He_0+_23S1':{
    
            #Metaparticle properties
    #        'npermeta':1e27,   #HAT-P-11b
    #        'npermeta':4e29,   #WASP-107b  HST 
    #        'npermeta':1e27*10,   #WASP-107b  HST + CARM
            
            
            
            #################################################################################################################
            #Radiation processes
            #################################################################################################################
    
            #Absorption processes
            'abs_proc':{
            
                  #Electronic transition  
                  'HeI_10832d1':{
    #                  'contributors':['part','ana_reg'], 
    #                  'contributors':['part'],  
                      'contributors':['ana_reg'],
    #                  'vrange':[-300.,100.],       #HAT-P-11b, WASP-107b sans abs des wings
                      'vrange':[-300.,200.],       #10821.2179 ; 10839.28
                      'sp_res':2.,  
                      'plot_proc':[]     
                    }, #end of current process
                  'HeI_10833d2':{
    #                  'contributors':['part','ana_reg'],  
    #                  'contributors':['part'],  
                      'contributors':['ana_reg'],
                      'vrange':[-350.,200.],       #10820.569 ; 10840.44  
                      'sp_res':2.,  
                      'plot_proc':[]     
                    }, #end of current process
                  'HeI_10833d3':{
    #                  'contributors':['part','ana_reg'], 
    #                  'contributors':['part'],
                      'contributors':['ana_reg'],   
                      'vrange':[-365.,160.],      #10820.116 ; 10839.087  
                      'sp_res':2.,  
                      'plot_proc':[]     
                    }, #end of current process                
        		}, #end of absorption processes for current species
    
    
            #-----------------------------------------------------
    
    #        #Self-shielding processes
    #        'ss_proc':{ 
    #              'HeI_10832d1':{
    #                  'contributors':['part','ana_reg'], 
    #                  'vrange':[-300.,100.],
    #                  'sp_res':{'exogrid':10.,'mixgrid':10.,'anagrid':10.,'plgrid':10.},
    #                  'plot_proc':[] 
    #                },
    #              'HeI_10833d2':{
    #                  'contributors':['part','ana_reg'], 
    #                  'vrange':[-300.,100.],
    #                  'sp_res':{'exogrid':10.,'mixgrid':10.,'anagrid':10.,'plgrid':10.},
    #                  'plot_proc':[] 
    #                },
    #              'HeI_10833d3':{
    #                  'contributors':['part','ana_reg'], 
    #                  'vrange':[-300.,100.],
    #                  'sp_res':{'exogrid':10.,'mixgrid':10.,'anagrid':10.,'plgrid':10.},
    #                  'plot_proc':[] 
    #                },              
    #		
    #    		}, #end of self-shielding processes for current species
    #        
    #       #Particle dynamical selection for self-shielding
    #       #    - particles with velocity outside of the range (in km/s) will not contribute to the self-shielding of any process
    #       #      this can be useful when a few particles have very large velocities, to prevent extending the self-shielding tables uselessly
    #       #    - beware that the range should include all velocities from regions of the atmosphere that contributes significantly to self-shielding, 
    #       # unless there are no particles that can be affected by self-shielding at these velocities
    #       #    - because projected Doppler velocities are lower than absolute velocities, particles with high absolute velocities may not be taken into account
    #       #      when stellar wind interactions are involved, and because they are linked to the absolute particle velocities, make sure the boundaries extend to the
    #       # maximum absolute velocities of particles of interest 
    #       'vrange_self':[-315.,315.],   #GJ436b, GJ3470b
    ##       'vrange_self':[-300.,100.], 
    
    
    
            #-----------------------------------------------------
    
    #        #Radiation pressure
    #        #    - define the properties for the calculation of radiation pressure on particles
    #        'prad_proc':{
    #        
    #            #Electronic transition  
    #            'HeI_10832d1':{
    ##                 'vrange':[-500.,100.],   #HAT-P-11b
    #                'vrange':[-500.,100.],    #WASP-107b
    #                'shielded_proc':False,
    #                'plot_proc':[]  #['prad_part']                                                              
    #            },
    #
    #            #Electronic transition  
    #            'HeI_10833d2':{
    ##                 'vrange':[-500.,100.],   #HAT-P-11b
    #                'vrange':[-500.,100.],    #WASP-107b
    #                'shielded_proc':False,
    #                'plot_proc':[]  #['prad_part']                    
    #            },
    #            
    #            #Electronic transition  
    #            'HeI_10833d3':{
    ##                 'vrange':[-500.,100.],   #HAT-P-11b
    #                'vrange':[-500.,100.],     #WASP-107b
    #                'shielded_proc':False,
    #                'plot_proc':[]  #['prad_part']                               
    #            },            
    #        
    #        }, #end of radiation pressure processes for current species 
    
            #################################################################################################################
            #Changes of state
            #################################################################################################################
            
            #Photoionization of species
            'photo_ion':{
            
                #Condition for self-shielding
                'shielded_proc':False,    
             
            },        
    
            #Radiative de-excitation of species 
            'rad_deexc':{
            
                #Release lower-excitation level
                #    - set to False or undefined to prevent release
                #    - a dictionary with relevant properties must be defined for the released species
                'child_sp':False           
            },
         
            #################################################################################################################
            #Analytical regimes properties
            #################################################################################################################
            'dico_anareg':{
            
                #Main body
                'body_0':{
    
                    #Analytical atmosphere & transition properties 
                    'ana_atm':{
    
                        #To take into account the analytical regime for this species	
                        'ana_therm':True,
                    
                        #Launch mode
                        'launch_mode':'null', 
    #                    'launch_mode':'esc_rate', 
    #                    'launch_mode':'decoupled',   
                        
                        #Escape rate
                        'esc_tau':1e8, 
    
    #                     #Temperature (K) and LOS velocity (km/s) resolution of the analytical regime
    #                     'coldens_grid':{
    #                         'dtemp':100.,
    #                         'dvel':1.
    #                     },
                       
                        #-------------------------------------------------
                        #Density properties 
                        #-------------------------------------------------
    
    #                    'dens':{'path':'/Travaux/Evaporation/Modele_upperatm/Simu_results/WASP107b_ndensProf_Ttherm12000.0_tauTot1.00e+10.dat'},          
    
                        'dens':{'constr':{'dens_trans':1e-11}},
     
                    },
    
    
                }, #end of main body
    
            }, #end of dico_anareg
    
            #################################################################################################################
            #Plot and various properties
            #################################################################################################################
            
            #Species-dependent plots 
            'plot':{
    #        'type':['ana_coldens_grid','above','earth'],  # ['ana_coldens_grid','above','earth'],    #'3D_anagrid'
            'type':[],
            
            
            #Time interval within which save the plots
            't_plot':[-1.,0.],    #[-1.3,1.15]     #[0.-0.0083,0.0083]    #[-1.3,1.15]    
    #        't_plot':[-30,20.]             
            }    
            
        }}) #end of He_0 particles
    
    
    
    
    
    if 0==1:
        sp_settings_set.update({
    
        #Iron
        'Fe_0+_g':{
            
            #################################################################################################################
            #Radiation processes
            #################################################################################################################
    
            #Absorption processes
            'abs_proc':{
            
                  #Electronic transition  
                  'FeI_5893d5':{
                      'contributors':['ana_reg'],  
                      'vrange':[-150.,150.],       
                      'sp_res':0.5,  
                      'plot_proc':[]     
                    }, #end of current process               
        		}, #end of absorption processes for current species
        
            #################################################################################################################
            #Analytical regimes properties
            #################################################################################################################
            'dico_anareg':{
            
                #Main body
                'body_0':{
    
                    #Analytical atmosphere & transition properties 
                    'ana_atm':{
    
                        #To take into account the analytical regime for this species	
                        'ana_therm':True,
                    
                        #Launch mode
                        'launch_mode':'null',    
                        
                        #-------------------------------------------------
                        #Density properties 
                        #-------------------------------------------------
    
                        'dens':{'constr':{'dens_trans':1000.}},    
    
                    },
    
                }, #end of main body
    
            }, #end of dico_anareg
    
            #################################################################################################################
            #Plot and various properties
            #################################################################################################################
            
            #Species-dependent plots 
            'plot':{
        #        'type':['ana_coldens_grid','above','earth'],  # ['ana_coldens_grid','above','earth'],    #'3D_anagrid'
                'type':[],   #'latlon_dens'
            
                #Time interval within which save the plots
                't_plot':[-2.,2.],              
            }
            
        }}) #end of 'Fe_0+_g' particles
    
    
    
    
    
    if 0==1:
        sp_settings_set.update({
    
        #Nitrogen 4+
        'N_4+_g':{
    
            #Metaparticle properties
            'npermeta':1.6397e+30, 
            
            #################################################################################################################
            #Radiation processes
            #################################################################################################################
    
            #Absorption processes 
            'abs_proc':{
            
                  #Electronic transition  
                  'NV_1239':{
    
                      #Contributors
                      'contributors':['part'],  
    
                      #Spectral range for theoretical absorption (km/s) 
                      'vrange':[-100.,100.],
    
                      #Spectral resolution of the opacity profiles (km/s)
                      'sp_res':10.,
          
                    }, #end of current process
            
                  #Electronic transition  
                  'NV_1243':{
    
                      #Contributors
                      'contributors':['part'],  
    
                      #Spectral range for theoretical absorption (km/s) 
                      'vrange':[-100.,100.],
          
                    }, #end of current process
    
        		}, #end of absorption processes for current species
    
            #-----------------------------------------------------
    
            #Self-shielding processes 
            'ss_proc':{
            
                  #Electronic transition  
                  'NV_1239':{
    
                      #Contributors
                      'contributors':['part'],  
    
                      #Spectral range for theoretical absorption (km/s) 
                      'vrange':[-200.,200.],
    
                      #Spectral resolution of the opacity profiles in each self-shielding grid 
                      'sp_res':{'exogrid':10.,'mixgrid':5.,'anagrid':5.,'plgrid':5.},
    
                    }, #end of current process
    
                  #Electronic transition  
                  'NV_1243':{
    
                      #Contributors
                      'contributors':['part'],  
    
                      #Spectral range for theoretical absorption (km/s) 
                      'vrange':[-200.,200.],
    
                      #Spectral resolution of the opacity profiles in each self-shielding grid 
                      'sp_res':{'exogrid':10.,'mixgrid':5.,'anagrid':5.,'plgrid':5.},
    
                    }, #end of current process
            
        		}, #end of self-shielding processes for current species
            
          #Particle dynamical selection for self-shielding
          'vrange_self':[-200.,200.],    #55 Cnc e
    
            #-----------------------------------------------------
    
            #Radiation pressure
            #    - define the properties for the calculation of radiation pressure on particles
            'prad_proc':{
            
                #Electronic transition  
                'NV_1239':{
                
                    #Isotropic impulse	
                    'rad_iso':False,
    
                    #Spectral range for radiation pressure (in km/s)
                    'vrange':[-200.,200.], 
    
                    #Condition for self-shielding
                    'shielded_proc':True,
    
                    #Process-dependent plots 
                    'plot_proc':['prad_part']
                                                              
                },
    
                #Electronic transition  
                'NV_1243':{
                
                    #Isotropic impulse	
                    'rad_iso':False,
    
                    #Spectral range for radiation pressure (in km/s)
                    'vrange':[-200.,200.], 
    
                    #Condition for self-shielding
                    'shielded_proc':True,
    
                    #Process-dependent plots 
                    'plot_proc':['prad_part']
                                                              
                },
            
            }, #end of radiation pressure processes for current species 
    
            #Photoionization of species      
            'photo_ion':{
            
                #Condition for self-shielding
                'shielded_proc':True,        
    
            },        
    
            
            #################################################################################################################
            #Analytical regimes properties
            #################################################################################################################
            'dico_anareg':{
            
                #Main body
                'body_0':{
    
                    #Analytical atmosphere & transition properties 
                    #    - comment/remove if unused
                    'ana_atm':{
                    
                        #To take into account the analytical regime for this species	
                        'ana_therm':False,
                        
                        #Launch mode
                        'launch_mode':'esc_rate', 
                        
                        #Escape rate
                        'esc_tau':0.,  
                        
                    },
    
                }, #end of main body
                
            }, #end of dico_anareg
    
            #To tag the particles according to a given condition
            'tag':False,
            
            #To save the time launch of the particles
            'tlaunch_part':False,
            
            #To identify particles with a unique integer
            'id_part':False,
            
            #Species-dependent plots
            'plot':{
                'type':['above','earth'],  
        
                #Time interval within which save the plots
                't_plot':[-30.,30.] 
            }    
        }}) #end of main species in gases_settings
    
    
    
    if 0==1:
        sp_settings_set.update({ 
        #Singly ionized carbon
        'C_1+_g':{
    
            #Metaparticle properties
            'npermeta':2.36e+30, 
    
            #Absorption processes
            'abs_proc':{
            
                  #Electronic transition  
                  'CII':{
    
                      #Contributors
                      'contributors':['part'],  
    
                      #Spectral range for theoretical absorption (km/s) 
                      'vrange':[-70.,70.],  
    
                      #Spectral resolution of the opacity profiles (km/s)
                      'sp_res':10.,
    
                      #Process-dependent plots 
                      'plot_proc':[] 
        
                    } #end of current process
           			
        		}, #end of absorption processes for current species
    
            #-----------------------------------------------------
    
            #Radiation pressure
            'prad_proc':{
            
                #Electronic transition  
                'CII':{
                
                    #Isotropic impulse	
                    'rad_iso':True,
    
                    #Spectral range for radiation pressure (in km/s)
                    'vrange':[-80.,80.],
    
                    #Condition for self-shielding
                    'shielded_proc':True,
    
                    #Process-dependent plots 
                    'plot_proc':[]
                                                              
                },
            
            }, #end of radiation pressure processes for current species 
    
            #################################################################################################################
            #Analytical regimes properties
            #################################################################################################################
            'dico_anareg':{
            
                #Main body
                'body_0':{
    
                    #Analytical atmosphere & transition properties 
                    'ana_atm':{
                    
                        #To take into account the analytical regime for this species	
                        'ana_therm':False,
                        
                        #Launch mode
                        'launch_mode':'esc_rate', 
                        
                        #Escape rate
                        'esc_tau':1e7,
    
                    },
    
                }, #end of main body
    
            }, #end of dico_anareg
    
            #Species-dependent plots 
          'plot':{
                'type':['above','earth'],
                
                #Time interval within which save the plots
                't_plot':[-30.,30.] 
            }         
        
     }}) #end of C_+
    
    
    ###########################################################
    #Magnesium atoms
    if 0==1:
        sp_settings_set.update({
        'Mg_0+_g':{
            
            #Metaparticle properties
            'npermeta':1e30,
    
            #Radiation pressure
            'prad_proc':{        
                #Electronic transition  
                'MgI_2852':{
                    #Spectral range for radiation pressure (in km/s)
                    'vrange':[-300.,300.],                                             
                },
                'MgI_4572':{
                    #Spectral range for radiation pressure (in km/s)
                    'vrange':[-300.,300.],                                             
                },        
            }, 
    
            #Photoionization of species
            'photo_ion':{},  
    #
    #    	  #To take into account the analytical regime	
    #    	  'dico_anareg':{'body_0':{'ana_atm':{'ana_therm':False,
    #    			         'launch_mode':'null'}}},
    
            #Species-dependent plots 
          'plot':{
                'type':['above','earth'],
                
                #Time interval within which save the plots
                't_plot':[-30.,30.] 
            } 
    
    }}) 
        
        
        
    ###########################################################
    #Protons
    if 0==1:
        sp_settings_set.update({
        'H_1+_g':{
        
          #Metaparticle properties
        'npermeta':1e30,
    
            #Species-dependent plots 
          'plot':{
                'type':['above','earth'],
                
                #Time interval within which save the plots
                't_plot':[-30.,30.] 
            } 
            
    }}) #end of protons
        
    ############################################################
    #Species 3
    if 0==1:
        sp_settings_set.update({ 
        'Na_0':{
    
       	#Lines
       	'lines_gas':{'NaID1':{
       	
        		#Spectral resolution
        		'delta_v':0.2,
        
        		#Absorption
               	'abs':True,
        
                #Spectral range for theoretical absorption
        		'vrange':[-710.,386.],    #[-6000.,6500.],    #[-1600.,1300.],
    
        		#Self-shielding
        		'self_prad':False,  #True,
        
               	#Spectral resolution for the line in each self-shielding grid
               	'delta_v_self':{'exogrid':5.,'mixgrid':2.,'anagrid':2.,'plgrid':2.},
        
        		#Process-dependent plots
        		'plot_proc':[]  
        		
        				}, #end of NaID1
        				
        				'NaID2':{     
        		'delta_v':0.2,   
               	'abs':True,  
        		'vrange':[-405.,690.],    #[-500,500],    #[-6000.,6500.],  #[-1300.,1600.],  
    
        		'self_prad':False,   
               	'delta_v_self':{'exogrid':5.,'mixgrid':2.,'anagrid':2.,'plgrid':2.},
        		'plot_proc':[] 		
        				} #end of NaID2				
       					
       			}, #end of line/bands
    
          #Spectral range for radiation pressure
          'vrange':[-600.,600.],   #[-100.,50.],
    
          #Spectral range for self-shielding
          'vrange_self':[-600.,600.],   #[-320.,302.],  # 
    
       	#Change of state
    #    	'ion_mode':{
    #    		'phion':1,
    #    		'eion':0,
    #    		'erec':0,
    #    	},
      
       	#Stellar ionisation rate at 1 au (in s-1)
       	'phion_rate_1au':None, #1e-8,
    
       	#Analytical regime/launch properties
       	'dico_anareg':{
        
            'body_0':{
        
              'ana_atm':{        
        
                      #To take into account the analytical regime for this species    
            		'ana_therm':True,  #False,
              
            		#Launch mode	
            		'launch_mode':'null',   #'esc_rate',   #'null',
              
                      #Escape rate
            		'esc_tau':None,  #5e4,
              
            		#Temperature (K) and LOS velocity (km/s) resolution of the analytical regime
    #        		'coldens_grid':{'dtemp':50.,'dvel':0.4},
    
    
    #                	#Density properties
    #                	'dens':{
    #                         'prop':2,
    #                         'funcname':'ana_prop_hydrostat',
    #                         'constr':[1.,0.]
    #                	},     
    ##                	#Density properties	
    ##                	'dens':{
    ##                         'prop':2,
    ##                         'funcname':'ana_prop_3temp_hydrostat',
    ##                         'constr':[1.,1e5]
    ##                    	},   	
    #                	#Temperature properties 
    #                	'temp':{
    #                         'prop':2,
    #                         'funcname':'ana_prop_cst',  
    #                         'constr':[0.]     
    #                   },  
    ##                	#Temperature properties 
    ##                	'temp':{
    ##                         'prop':2,
    ##                         'funcname':'ana_prop_3templayers',  
    ##                         'constr':[1500.,1.1,3000.,1.2,3600.]   #[1500.,1.04,2300.,1.1,3000.]     
    ##                   },  
    ##                	#Upward velocity properties	
    ##                	'vert_vel':{
    ##                         'prop':2,	
    ##                         'funcname':'ana_prop_cst',
    ##                  	  'constr':[1.]  
    ##                	},        
    ##                	#Upward velocity properties	
    ##                	'long_vel':{
    ##                         'prop':2,	
    ##                         'funcname':'day2nightside_wind',
    ##                         'constr':[5.]  
    ##                	},               
                  }, #end of ana_atm
        
            }, #end of body
    
    #         'body_1':{  
    #           'ana_atm':{          
    #        		'ana_therm':False,        			
    #        		'launch_mode':'esc_rate',        
    #        		'esc_tau':5e4,	      		     	
    #                	'temp':{
    #                         'prop':2,
    #                         'funcname':'ana_prop_cst',  
    #                         'constr':[1000.]    
    #                         },                 	
    #                	'vert_vel':{
    #                		'prop':2,	
    #                          'funcname':'ana_prop_cst',
    #                		'constr':[1.]  
    #                		},        
    #               },
    #         }, #end of body
    #         'body_2':{  
    #           'ana_atm':{          
    #        		'ana_therm':False,        			
    #        		'launch_mode':'esc_rate',        
    #        		'esc_tau':1e6,	      		     	
    #                	'temp':{
    #                         'prop':2,
    #                         'funcname':'ana_prop_cst',  
    #                         'constr':[500.]    
    #                         },                 	
    #                	'vert_vel':{
    #                		'prop':2,	
    #                          'funcname':'ana_prop_cst',
    #                		'constr':[1.]  
    #                		},        
    #               },
    #         }, #end of body
    #         'body_3':{  
    #           'ana_atm':{          
    #        		'ana_therm':False,        			
    #        		'launch_mode':'esc_rate',        
    #        		'esc_tau':1e6,	      		     	
    #                	'temp':{
    #                         'prop':2,
    #                         'funcname':'ana_prop_cst',  
    #                         'constr':[500.]    
    #                         },                 	
    #                	'vert_vel':{
    #                		'prop':2,	
    #                          'funcname':'ana_prop_cst',
    #                		'constr':[1.]  
    #                		},        
    #               },
    #         }, #end of body
    
    
            
          },
        
       	#To tag the particles according to a given condition
       	'tag':False,
        
       	#To save the time launch of the particles
       	'tlaunch_part':False,
        
       	#To identify particles with a unique integer
       	'id_part':False,
        
            #Species-dependent plots 
          'plot':{
                'type':['above','earth'],
                
                #Time interval within which save the plots
                't_plot':[-30.,30.] 
            } 
       	
    }}) #end of 'Na_0'
        
    ###########################################################
    if 0==1:
        sp_settings_set.update({
        'Na_1+_g':{
    
        #Number of atoms per metaparticles
        'npermeta':1e31,     
    
       	#Change of state
       	'ion_mode':{
        		'phion':0,
        		'eion':0,
        		'erec':1,
       	},
       	#To take into account the analytical regime	
       	'dico_anareg':{'body_0':{'ana_atm':{'ana_therm':False,
        			         'launch_mode':'null'}}},
        
       	#To tag the particles according to a given condition
       	'tag':False,
        
       	#To save the time launch of the particles
       	'tlaunch_part':False,
        
       	#To identify particles with a unique integer
       	'id_part':False,
        
            #Species-dependent plots 
          'plot':{
                'type':['above','earth'],
                
                #Time interval within which save the plots
                't_plot':[-30.,30.] 
            } 
      
    }}) #end of gas4
        
        
    ##########################################################
    #Water
    if 0==1:
        sp_settings_set.update({
        'H2_0':{
    
        	   #Bands
            'bands_gas':{'H2_Rayleigh':{
              
                  #Spectral resolution (A)  
                  'delta_w':1.,
                  
                  #Spectral range for theoretical absorption (A) 
                  #    - can overlap with several theoretical band spectra
                  'wrange':[5882.,5904.],
            
                    } #end of current band
           			
        		}, #end of line/bands for current species
    
              #Species-dependent plots 
              'plot_sp':[],     #'ana_coldens_grid'
        
              #Analytical regime properties
              'dico_anareg':{'body_0':{
                  'ana_atm':{           
        
                   	#To take into account the analytical regime for this species	
                   	'ana_therm':True,
            
                   	#Launch mode
                   	'launch_mode':'null', 
                        
                   	#Density properties	
    #                	'dens':{
    #                         'prop':2,
    #                         'funcname':'ana_prop_3temp_hydrostat',
    #                         'constr':[1.,1e5]
    #                    	},   
                   	'dens':{
                            'prop':2,
                            'funcname':'ana_prop_hydrostat',
                            'constr':[1.,0.]
                       	},                        
                   	#Temperature properties 
    #                	'temp':{
    #                         'prop':2,
    #                         'funcname':'ana_prop_3templayers',  
    #                         'constr':[1500.,1.1,3000.,1.2,3600.]   
    #                   }, 
                   	'temp':{
                            'prop':2,
                            'funcname':'ana_prop_cst',  
                            'constr':[0.]    
                            },                     
    #                	#Upward velocity properties	
    #                	'long_vel':{
    #                         'prop':2,	
    #                         'funcname':'day2nightside_wind',
    #                         'constr':[5.]  
    #                	}, 	
                    }	
              }},
        
     }}) #end of water
    
        
        ###########################################################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #################################################################################################################
    #################################################################################################################
    #Dust species properties
    #################################################################################################################
    #################################################################################################################
        
    #Pyroxen 'pyr40'
    if 0==1:
        sp_settings_set.update({
    
        'pyrmg40':{
    
            #Metaparticle properties
            #    - 'npermeta' defines the number of dust grains per metaparticle 
            #    - a metaparticle will yield an opacity 'dtau' for a given process, within a spectral bin 'delta_v' or 'delta_w', in front of a surface 'dbox'
            #    - 'npermeta' should be defined to ensure that the elementary optical depth 'dtau' (calculated in a bin at the center of the line for an electronic transition, and
            # in the bin of maximum cross-section for a broadband process) for all absorption/emission processes remains low
            #       to this purpose the Summary file provides:
            # + the maximum elementary opacity from a metaparticle along the LOS and in the SS grids 
            # + the maximum number of particles per metaparticles to ensure that elementary opacity along the LOS remains below 'abs_proc' > 'dtau_thresh' 
            # 'npermeta':1e22,
            'npermeta':1e26, 


            #Launch size distribution 
            #    - define the size distribution n_part(s) for dust grains as:
            # + uniform ('funcname' = 'uf'): n_part(s) = dNpart(s)/ds = 1.
            #                                only if npermeta_alpha != 0   
            # + power law ('funcname' = 'pow_law'): n_part(s) = dNpart(s)/ds = (s/1.)^(-exp)
            # + new distributions can be coded in EVE_launch_coord.py
            #    - by construction each new metagrain contains Npermeta(s) grains, so that the effective size distribution of dust grains in the simulation is on average n_part[launch](s)*Npermeta(s)
            #      if the above size distribution was directly used, then the effective size distribution would actually describes Nmeta(s) = dNmeta(s)/ds
            #      to obtain the required size distribution for grains, the launch size distribution used in the code is thus n_part[launch](s) = n_part(s)/Npermeta(s), ie the size distribution of metagrains        
            #    - define the size boundaries of the distribution, ie the minimum and maximum grain size to be launched (in microns)
            #      any grain randomly drawn outside of these bounds will be set to the closest bound
            'siz_distrib':{
                'funcname':'pow_law',
                'size_bd':[0.01,100.],
                'exp':2.
            },
             

            #################################################################################################################
            #Radiation processes
            #    - processes can include:
            # + absorption (for particles and analytical regimes)
            # + self-shielding (for particles and analytical regimes, along stellar radii)        
            # + diffusion (for particles and analytical regimes)
            # + radiation pressure (for particles)   
            #    - for each absorption/emission process, define if they should be accounted for particles and analytical regimes
            # of all bodies that contain this species
            #    - cross-sections are defined in cross_sections.py 
            #    - beware that absorption can extend at high velocities because of damping wings/fast moving particles
            #    - the range of absorption/diffusion processes can overlap with several theoretical band spectra
            #    - remove field if no processes of a given type are required for the species
            #    - properties are common to all bodies harboring the species in the simulation 
            #    - tabulated cross-sections tables might be interpolated over a finer size grid   
            #    - for dust species, optical processes are tabulated and chosen among those available in EVE_mainproc/Tabulated_cs/. The process name must the start of the file name (before '_all') and can be of two types:
            # + 'Budaj2015_spZ' : computed for a specific dust species 'Z' by Budaj+2015 (see EVE > Method > EVE_preproc > Dust > Budaj2015 and the available list in constant_data.py)
            # + 'Mie_nX_kY' or 'Mie_spZ' : computed with Mie scattering code in EVE_preproc/Dust/Mie for achromatic refraction indexes 'n' = X and 'k' = Y, or for a specific species 'Z'     
            #################################################################################################################
    
            #Common size resolution of the interpolations of the cross section tables
            #   - set to None if not needed
            'cross_sec_resolution':{
                'dsiz_HR':0.01,
                'siz_ref':1.,
                },
     
            #Maximum opacity threshold
            #    - on the elementary opacity, for all absorption processes along the LOS
            'dtau_thresh':2./3.,            
       
            #Absorption processes
            #    - define the properties of the opacity profiles to be calculated for the species
            #      those processes will decrease the various bands of the stellar spectrum defined in 'theo_data', as seen by the observer at 1au and at Earth distance
            #    - opacity profiles will be calculated at the required resolution for each grid (using 'sp_res', unless tabulated), and interpolated 
            # over the stellar spectrum table (unless directly calculated over it)
            #    - opacity profile from a given process should be calculated with a resolution fine enough to capture its variations, either:
            # + at the resolution of the stellar spectrum, if it is close to the required resolution (set 0)
            # + at a coarser resolution (set in km/s for electronic transitions, in A for broadband processes)
            #      tabulated opacity profiles are pre-interpolated over the stellar spectrum table and needs no interpolation (no need to define 'sp_res')
            #    - define the contributors to this process:
            # + the particles population ('part')
            # + the analytical regimes ('ana_reg')
            #    - spectral range in A for broadband processes 
            'abs_proc':{

                  #Tabulated process  
                  'Budaj2015_sppyrmg40':{     
    
                      #Contributors
                      'contributors':['part'],  
    
                      #Spectral range for theoretical absorption (A) 
                      #    - can overlap with several theoretical band spectra
                      'wrange':[2e3,5e6],
    
                      #Process-dependent plots 
                      #    - set field in list to plot, otherwise leave empty or remove
                      #    - 'ana_opa_grid': opacity for LOS absortion in the line, from the analytical regime of all transiting bodies
                      # + plotted only if absorption is required for this line and the analytical regime transits
                      # + multiple calls for different lines of a same species are on the same plot
                      'plot_proc':[] 
    
                    } #end of current process
           			
        		}, #end of absorption processes for current species
    
    
            # #Scattering processes
            # #    - define the properties of the scattering profiles to be calculated for the species
                # 'scat_proc':{
                
                #       #Tabulated process
                #       #     - process is only yet defined for dust tabulated processes
                #       'Mie_n1.6_k0.01':{
                          
                #           #Contributors
                #           #     - process is not yet defined for ana_reg contributor
                #           'contributors':['part'],
                
                #           #Spectral range for theoretical scattering (A) 
                #           #    - can overlap with several theoretical band spectra
                #           'wrange':[2e3,5e6],
                          
                #           #Condition for self-shielding
                #           #    - set to False for the process to use the unshielded stellar spectrum
                #           'shielded_proc':True, 
                          
                #       }, #end of current process
                
                #   }, #end of scattering processes for current species 
    
            #-----------------------------------------------------
    
            #Self-shielding processes
            #    - define the properties of the opacity profiles to be calculated for the species
            #      those processes will decrease the various bands of the stellar spectrum defined in 'theo_data'
            #    - cross-section profiles are tabulated and pre-interpolated over the stellar spectrum, and need no interpolation
            #    - opacity profiles will be calculated at the required resolution for each grid (using 'sp_res', unless tabulated), and interpolated 
            # over the stellar spectrum table (unless directly calculated over its spectral bins if 'sp_res' is set to 0)
            #    - opacity profile from a given process should be calculated with a resolution fine enough to capture its variations, either:
            # + at the resolution of the stellar spectrum, if it is close to the required resolution (set 0)
            # + at a coarser resolution (set in km/s for electronic transitions, in A for broadband processes)
            #      tabulated opacity profiles are pre-interpolated over the stellar spectrum table and needs no interpolation (no need to define 'sp_res')
            #    - define the contributors to this process:
            # + the particles population ('part')
            # + the analytical atmospheres ('ana_reg')
            #    - spectral ranges in A 
            # 'ss_proc':{
            
            #       #Broadband process  
            #       'pyr40_abs_scat':{
    
            #           #Contributors
            #           'contributors':['part'],  
    
            #           #'sp_res':{'exogrid':10.,'mixgrid':10.,'anagrid':10.,'plgrid':10.},
    
            #           #Spectral range for theoretical absorption (A) 
            #           'wrange':[2e3,5e6],   
    
            #           #Process-dependent plots 
            #           #    - set field in list to plot, otherwise leave empty or remove
            #           'plot_proc':[] 
    
            #         }, #end of current process
    
            # },
    
            #Particle size selection for self-shielding (in microns) 
            #    - particles with size outside of the range will not contribute to the self-shielding of any process
            'sizrange_self':[1e-3,1e3], 

            #-----------------------------------------------------
    
            #Radiation pressure
            #    - define the properties for the calculation of radiation pressure on dust grains
            'prad_proc':{
    
                  #Absorption and radial scattering 
                  'Mie_sppyrmg40':{        
    
                        #Spectral range for radiation pressure (in A)
                        #    - the theoretical stellar spectrum bands used to calculate the line pressure will be limited to the corresponding wavelength range  
                        # 'wrange':[2e3,39995.],
                        'wrange':[2e3,5e6],
                        
                        #Self-shielding contributors
                        'contributors':['part'], 
    
                        #Condition for self-shielding
                        #    - set to False for the process to use the unshielded stellar spectrum
                        # 'shielded_proc':True, 
                        'shielded_proc':False,
        
                        #Process-dependent plots 
                        #    - set field in list to plot, otherwise leave empty or remove
                        #    - possibilities: 
                        # + 'prad_part': radial radiation pressure coefficient as a function of dust grains size
                        'plot_proc':['prad_part']
    
                  },
          
            }, #end of radiation pressure processes for current species 
    
            #################################################################################################################
            #Species state
            #################################################################################################################
    
            #Sublimation of species
            #    - if relevant for dust species, otherwise comment 
            #    - we assume that grain temperature is dependent on a single absorption process   
            #    - beware that the reference stellar bands should cover the most energetic / the most absorbed ranges of the spectrum
            #    - can release individual components of dust grains
            'sublim':{
            
                #Condition for self-shielding
                #    - set to False for the process to use the unshielded stellar spectrum
                # 'shielded_proc':True,        
                'shielded_proc':False, 
    
                #Select the relevant absorption process
                'abs_proc':'pyr40_abs_scat',
    
                #Spectral range for sublimation (in A)
                #    - the range should be large enough to calculate the dust grains temperature, which depends on the integral
                # of the absorption cross-section times the stellar flux over this range 
    #            'wrange':[5.,1e7],
                # 'wrange':[2e3,1e5],
                'wrange':[2e3,5e6],
    
                #Gas species released from sublimation
                #    - leave empty to ignore sublimation products
                #      otherwise indicate name of sublimation products (defined for each species in change_state/return_frac_sublim_prod_func)            
                'sp_d2g':['Mg_0+'],    
    
                #Typical velocity of the gas particle launched from sublimated dust
                #    - we use a gaussian distribution
                #    - in km/s
                #    - leave empty to deactivate
                'vel_d2g' : {'Mg_1+_g' : 5}
    
    
            }, 
    
            #################################################################################################################
            #Analytical regimes properties
            #    - can describe:
            # + atmospheres
            # + launch conditions for particles 
            #   dust grains are launched with an upward velocity but no thermal component
            #################################################################################################################
            'dico_anareg':{
            
                #Main body
                'body_0':{
    
                    #Analytical atmosphere & transition properties 
                    #    - comment/remove if unused
                    'ana_atm':{
                    
                        #To take into account the analytical regime for this species	
                        'ana_therm':False,
                        
                        #Launch mode		
                        #    - mode to calculate number of launched particles:
                        # + 'esc_rate': from input escape rate
                        # will constrain the analytical regime density profile (transition radius cannot be set by knudsen or density inputs in that case)
                        # + 'continuity': from density and upward velocity at the top of the thermosphere
                        # + 'null': no particles are launched
                        'launch_mode':'esc_rate', 
                        #'launch_mode':'null',
    
                        #Escape rate
                        #    - in g/s, used only if launch_mode='esc_rate' 
                        #    - define the total number of metaparticles launched with the chosen size distribution
                        #    - given when the planet is at 'a_planet' from the star
                        # 'esc_tau':1e9,
                        #'esc_tau':1.9e11, #Kepler1520 (1 M_T/Gyr)
                        'esc_tau':1e11,
    
                        #Species spatial launch distribution
                        #    - see first definition
                        'launch_distrib':{            
                       
                                #Uniform launch distribution
                                #    - random launch positions within theta and phi ranges
                                #    - constraints = [th_low,th_high,phi_low,phi_high], angular boundaries in rad
                                #    - possibilities:
                                #       + full surface: [-pi , pi , -pi/2 , pi/2]
                                #      valid for circular orbits only :
                                #       + dayside launch: [-3.*pi/2 , -pi , -pi/2 , pi/2] 
                                #       + terminator launch: [pi/2 - half_th , pi/2 + half_th , -pi/2 , pi/2] or [-pi/2 - half_th , -pi/2 + half_th , -pi/2 , pi/2]  
                                'funcname':'uniform',
                                'constr':[-pi/2 , -pi/2. , -pi/2 , pi/2],
                                
                                #Raised cosine launch distribution
                                #    - constraints = [th_mean,th_sig,phi_mean,phi_sig], mean and width in rad
                                # 'funcname':'cosine',
                                # 'constr':[pi , pi/4. , 0. , pi/4.] 
                        },
    
                   
                        #-------------------------------------------------
                        #Properties
                        #-------------------------------------------------
    
                        #Density properties 
                        #    - hydrostatic profile
                        #    - constr = ( radius [Rp], density [atoms/cm3] )	
                        #    - the profile is automatically scaled along an eccentric orbit assuming the constraints below are valid at 'a_planet' from the star
                        'dens':{
                            'prop':2,
                            'funcname':'ana_prop_hydrostat',
                            'constr':{'rad':1.,'dens':1e10}
                        },
    
                        #Temperature properties 
                        #    - uniform profile
                        #    - constr = ( temperature [K] ) 
                        'temp':{
                            'prop':2,
                            'funcname':'ana_prop_cst',  
                            'constr':{'temp':0.}    
                        },	
                        		
                        #Upward velocity properties 
                        #    - uniform profile
                        #    - constr = ( velocity [km/s] )  	
                        'vert_vel':{
                            'prop':2,	
                            'funcname':'ana_prop_cst',  
                            'constr':{'vel':1.}   
                        },
      
                    },
    
                }, #end of main body
    
            }, #end of dico_anareg
    
        #################################################################################################################
        #Plot and various properties
        #################################################################################################################
        
        #To tag the particles according to a given condition
        'tag':False,
        
        #To save the time launch of the particles
        'tlaunch_part':False,
        
        #To identify particles with a unique integer
        'id_part':False,       
    
        #Species-dependent plots 
        #    - set field in list to plot, otherwise leave empty or remove
        #    - possibilities:
        # + 'camera': view of the particle cloud from a given position
        # + 'above': view of the particle cloud from above the planetary system
        # + 'Earth': view of the particle cloud along the LOS
        'plot':{
            'type':[],
        
            #Time interval within which save the plots
            #    - in h
            't_plot':[-3,3.],   #WD1145+017
    #        't_plot':[-4.,2.],
    

            
            }, 
      
        # x_range = 2.*np.array([-a_planet,a_planet])
        # y_range = 2.*np.array([-a_planet,a_planet])   
        # x_range = 15.*np.array([-Rstar,Rstar])       #wasp107
        # y_range = np.array([-2.*a_planet,5.*Rstar])   
#        x_range = 4.*np.array([-Rstar,Rstar])       #hatp11
#        y_range = np.array([-1.4*a_planet,-0.8*a_planet])  
#        x_range = np.array([-3.5*a_planet,0.5*a_planet]) 
#        y_range = np.array([-2.5*a_planet,1.5*a_planet])           
        # x_range = np.array([pl_coord[1]-100*Rplanet,pl_coord[1]+100*Rplanet])
        # y_range = np.array([-pl_coord[0]-100*Rplanet,-pl_coord[0]+100*Rplanet] )
        # x_range = 1.4*np.array([-a_planet,a_planet])
        # y_range = 1.4*np.array([-a_planet,a_planet])
        # x_range = np.array([pl_coord[1]-Rstar,pl_coord[1]+Rstar])
        # y_range = np.array([-pl_coord[0]-Rstar,-pl_coord[0]+Rstar] )
        
        
        
     }}) #end of  dust species
        
        
    
    
    
    
    
    ### End of species dictionary 
    
    return None
