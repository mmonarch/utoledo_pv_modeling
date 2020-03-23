#!/usr/bin/python3
#
# r1_utils.py

import pvlib

toledo_lat = 41.653207
toledo_lon = -83.606533
toledo_alt = 187

# Return the location for toledo R1 array
def get_toledo(tz):
    return pvlib.location.Location(toledo_lat, toledo_lon, tz,
                    toledo_alt, 'UT-R1')

# Returns tuple containing model chains for all 4 rows of the R1 array
def create_r1_model(tz=4):
    UT_R1 = get_toledo(tz)

    #Module/inverter details
    sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod') #database for FS-55
    CEC_modules = pvlib.pvsystem.retrieve_sam('CECMod')       #database for FS-390
    CEC_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')#inverter database

    #import modules and inverters used in UT-R1 array
    FS_57 = sandia_modules['First_Solar_FS_55__2004__E__']  #for Rows 1 and 2
    FS_390 = CEC_modules['First_Solar__Inc__FS_390']        #for Rows 3 and 4

    inverter_1 = CEC_inverters['SMA_America__SB6000U__208V_']           #for row 1
    inverter_2 = CEC_inverters['SMA_America__SB7000TL_US__208V_']       #for row 2
    inverter_3 = CEC_inverters['SMA_America__SB10000TL_US_12__208V_']   #for row 3
    inverter_4 = CEC_inverters['SMA_America__SB10000TL_US_12__208V_']   #for row 4

    #Array Information

    #Rows 1 and 2:
    mods_per_str_1_2 = 6                                #modules per string
    str_per_inv_1_2 = 18                                #strings per inverter
    n_modules_1_2 = mods_per_str_1_2*str_per_inv_1_2    #modules per row

    #Rows 3 and 4:
    mods_per_str_3_4 = 9                                #modules per string
    str_per_inv_3_4 = 12                                #strings per inverter
    n_modules_3_4 = mods_per_str_3_4*str_per_inv_3_4    #modules per row

    #Other system parameters
    s_tilt = 35     #surface tilt +/-0.2 degrees
    azimuth = 180   #degrees south

    #Define Rows
    system1 = pvlib.pvsystem.PVSystem(module_parameters=FS_57, 
                                      inverter_parameters=inverter_1, 
                                      surface_tilt=s_tilt, 
                                      surface_azimuth=azimuth,
                                      modules_per_string=mods_per_str_1_2, 
                                      strings_per_inverter=str_per_inv_1_2, 
                                      aoi_model=None)

    system2 = pvlib.pvsystem.PVSystem(module_parameters=FS_57, 
                                      inverter_parameters=inverter_2, 
                                      surface_tilt=s_tilt, 
                                      surface_azimuth=azimuth,
                                      modules_per_string=mods_per_str_1_2, 
                                      strings_per_inverter=str_per_inv_1_2, 
                                      aoi_model=None)

    system3 = pvlib.pvsystem.PVSystem(module_parameters=FS_390, 
                                      inverter_parameters=inverter_3, 
                                      surface_tilt=s_tilt, 
                                      surface_azimuth=azimuth,
                                      modules_per_string=mods_per_str_3_4, 
                                      strings_per_inverter=str_per_inv_3_4, 
                                      aoi_model=None)

    system4 = pvlib.pvsystem.PVSystem(module_parameters=FS_390, 
                                      inverter_parameters=inverter_4, 
                                      surface_tilt=s_tilt, 
                                      surface_azimuth=azimuth,
                                      modules_per_string=mods_per_str_3_4, 
                                      strings_per_inverter=str_per_inv_3_4, 
                                      aoi_model=None)

    # Create models
    mc_1 = pvlib.modelchain.ModelChain(system1, UT_R1)
    mc_2 = pvlib.modelchain.ModelChain(system2, UT_R1)
    mc_3 = pvlib.modelchain.ModelChain(system3, UT_R1,
            aoi_model='ashrae', spectral_model='no_loss')
    mc_4 = pvlib.modelchain.ModelChain(system4, UT_R1,
            aoi_model='ashrae', spectral_model='no_loss')

    return (mc_1, mc_2, mc_3, mc_4)

