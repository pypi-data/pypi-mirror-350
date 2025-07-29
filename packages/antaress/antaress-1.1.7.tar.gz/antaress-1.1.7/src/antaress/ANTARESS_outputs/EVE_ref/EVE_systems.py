from antaress.ANTARESS_general.constant_data import Mjup,Msun,Rsun,Rjup,AU_1,Mearth,Rearth,pc_1

def get_system_params():
    r"""**Planetary system properties.**    

    Returns dictionary with properties of planetary systems. Format with minimum required properties is 

    >>> all_system_params={
        'star_name':{
            'star':{
                'XX': val,
                },      
            'body_k':{
                'XX':    val,
            },           
        },
    }
    
    Simulated bodies can be planets or comets, and be single or multiple. Required and optional properties are defined as follows.
    
    **Star properties**
    
     - `veq` [km/s] : equatorial rotational velocity     

      - `ci` [km/s] : coefficients of the :math:`\mu`-dependent convective blueshift velocity polynomial
    
          + convective blueshift is defined as :math:`\mathrm{rv}_\mathrm{cb} = \sum_{i}{c_i \mu^i}` 

     - `dstar` [pc] : distance from Earth 
     
     - 'Nh' [/cm2] : column density of neutral hydrogen in the ISM along the LOS
     
          + required to calculate ISM extinction by dust
          + relevant for systems at large distances from Earth

    **Body properties**
    
    Args:
        None
    
    Returns:
        all_system_params (dict) : dictionary with planetary system properties
    
    """     

    ############################################################################
    #Parameters definition
    #  -> indicate the conversion unit at the end of the file
    ############################################################################

    #------------------------------------------------------------------------    
    #Star properties (common to all bodies of the chosen planetary system)
    #------------------------------------------------------------------------
    # Mstar= star mass (in solar mass)
    # Rstar= star radius (in Rsun) -> AU   
    # veq_star= true stellar equatorial velocity (km/s)
    # alpha_dr= differential rotation rate (no unit)
    #           + if null or not required, set to 0
    # istar= stellar inclination (deg), angle counted from the LOS toward the stellar spin axis   
    #        + not used if no differential rotation, otherwise from 0 to 180 degrees  
    # Tstar= star effective temperature (in K)
    # rvstar= star radial velocity with respect to the Sun (km/s)
    # 		
    #------------------------------------------------------------------------    
    #Bodies bulk and orbital properties
    #------------------------------------------------------------------------
    # t_0      = Mid-transit time - 2400000 (days)
    # + if only the time of pericenter is known for an eccentric orbit, calculate t_0 as:
    #       True_anom_TR=(pi/2.)-omega_deg 
    #       Ecc_anom_TR=2.*atan( tan(True_anom_TR/2.)*sqrt((1.-ecc)/(1.+ecc)) )
    #       Mean_anom_TR=Ecc_anom_TR-ecc*np.sin(Ecc_anom_TR)
    #       if (Mean_anom_TR<0.):Mean_anom_TR=Mean_anom_TR+2.*pi  
    #       t_0 = t_peri + (Mean_anom_TR*period/(2.*pi))
    # period   = orbital period (days)
    # ecc      = eccentricity
    # omega_deg= angle between the ascending node an the periastron in the orbital plane (deg) -> rad
    # inclination = orbital inclination (deg) -> rad
    #            + angle usually provided by catalogs, counted from the LOS to the normal of the orbital plane (the normal is the oriented spin axis of the planet along its orbit)
    #            + inclination is limited to [0,90] in the catalogs
    #            + beware that for multiple bodies, the sky-projected normal is set to the Z axis of the simulation only for the main body, if they have different obliquities
    #            + with no other information, a photometric transit is degenerate between the upper and lower hemispheres of the star, any of which can be the one transited. With an aligned star
    #              (istar=90), one can set in the planet properties below:
    #                   for a southern transit: inclination = Inclin(catalog)
    #                   for a northern transit: inclination = pi - Inclin(catalog)
    #              where Inclin(catalog) is that given in the catalogs    
    #            + if we assume solid body rotation for the star, there is a degeneracy between (lambda,Inclin) and (-lambda,180-Inclin), with
    #              lambda the obliquity. In that case we assume Inclin is within [0,180] and let obliquity vary from 0 to 360 (thus 180-Inclin will cover the 
    #              range 180 to 360 which is not overlapping with the Inclin range)       
    #            + with differential rotation, the following combinations are equivalent:
    #                   (Inclin,lambda,istar) and (-Inclin,lambda,180-istar)
    #                   (Inclin,lambda,istar) and (pi-Inclin,-lambda,180-istar)
    #                   (Inclin,lambda,istar) and (Inclin,180+lambda,-istar)    
    #              we thus limit Inclin to [0;90], lambda in [0;360] and istar in [0,180] (we could also invert the ranges for lambda / istar)
    #              WARNING: the results obtained with the CLB technique corresponds to inclination = Inclin(catalog), ie a southern transit by default
    # a_planet = semi-major axis of planet orbit (in au)
    # omega_p  = orbital frequency (rad year-1)
    # Mplanet   = mass   (in Mjup) -> Msol
    # Rplanet   = radius (in Rjup) -> AU
    # Kpl      = radial velocity semi-amplitude of the star induced motion [km/s]
    # RpRs      = [UNUSED IN EVE] radius (in unit of stellar radius)    
    # b_impact  = impact parameter (in stellar radius) = a_planet*cos(inclination)/Rstar  
    # aRs       = [UNUSED IN EVE] semi-major axis (in units of star radius)
    # lambda    = sky-projected obliquity (in degrees)
    #             + angle counted positively from the projection of the stellar spin axis to the projection of the normal to the orbital plane (projection in the plane of sky)
    #               from 0 to 360 degrees
    #             + the sy-projected normal to the main body orbital plane is taken as vertical axis of the simulation rest frame (Z axis)
    # B_eq      = the value of the dipolar magnetic field at the magnetic equator at the planet surface (in Tesla = kg A-1 s-2)

    ############################################################################
    
    all_system_params={
        
        'Arda':{
            'star':{
                'Mstar':1.,
                'Tstar':4875.,
                'Rstar':0.9,
                'dstar':19.,
                'alpha_dr':0.6,    
                'veq_star':4.45,       
                'istar':92.5,          
                'rvstar':-2.545,
                },  
     
            'Valinor':{
                't_0':54279.436714,       
                'period':2.21857567,       
                'ecc':0.,
                'omega_deg':90.,            
                'Rplanet':1.1938696528743737, 
                'RpRs':0.15712,            
                'lambda':-0.42,        
                'aRs':8.863,           
                'a_planet':0.0321838670552953,  
                'inclination':85.71, 
                'Mplanet':1.162,  
                'b_impact':0.6636, 
                'Ks':0.20196,      
            },
    
            'Numenor':{
                't_0':54279.436714,       
                'period':2.21857567,       
                'ecc':0.,
                'omega_deg':90.,            
                'Rplanet':1.1938696528743737, 
                'RpRs':0.15712,            
                'lambda':-0.42,        
                'aRs':8.863,           
                'a_planet':0.0321838670552953,  
                'inclination':85.71, 
                'Mplanet':1.162,  
                'b_impact':0.6636, 
                'Ks':0.20196, 
            },           
        },
        
        'HAT_P_11':{
            #Star
            'star':{ 
                'Mstar':0.810,                   # Morton et al. 2016
                'Rstar':0.74,                    # Morton et al. 2016
                'dstar':37.84,                   # GAIA EDR3 2020
                'Tstar':4653.,                   # Morton et al. 2016
                #'rvstar':-63.4288,            
                'alpha_dr':0.,                   # non required          
                'veq_star':1.96,                 # Bourrier et al. in prep
                'istar':160.,                    # Bourrier et al. in prep
                
                
            },
            #Planet
            'HAT_P_11b':{        
                't_0':54957.813207,              # Huber et al. 2017
                'period':4.8878024,              # Huber et al. 2017
                'ecc':0.2644,                    # Allart et al. 2018
                'omega_deg':342.2,               # Allart et al. 2018
                'RpRs':0.05850000,               # Huber et al. 2017
                'Rplanet':0.421,                 # RpRs*Rstar*Rsun/Rjup
                'lambda':133.9,                  # Bourrier et al. in prep
                'aRs':16.50,                     # Allart et al. 2018
                'a_planet':0.05678220525634794,  # a/Rs*Rstar
                'inclination':89.05,             # Huber et al. 2017
                'Mplanet':0.0736,                # Yee et al. 2018
                'b_impact':0.209                 # Huber et al. 2017
            }        
        },
        
    }    

    return all_system_params

###########################################################################
