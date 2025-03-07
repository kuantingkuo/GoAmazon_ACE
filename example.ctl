DSET ^NCFILE
DTYPE netcdf
TITLE ACE output
UNDEF -9.99e8
XDEF 6 LINEAR 1 2
YDEF 1 LINEAR 1 1
ZDEF 401 LINEAR 0.05 0.1
TDEF TIMESTEP LINEAR 00:00Z01JAN2000 1mn
VARS 16
B=>B                    401 t,z,x buoyancy
RH=>RH                  401 t,z,x relative_humidity
T=>T                    401 t,z,x temperature
Tv=>Tv                  401 t,z,x virtual_temperature
dtheta_e_pr_accum=>dthetaepraccum  401 t,z,x dtheta_e_pr_accum
mf=>mf                  401 t,z,x mass_flux
pr_accum=>praccum       401 t,z,x precipitation_accumulation
qc=>qc                  401 t,z,x cloud_water_content
qi=>qi                  401 t,z,x ice_water_content
ql=>ql                  401 t,z,x liquid_water_content
qsat=>qsat              401 t,z,x saturation_specific_humidity
qt=>qt                  401 t,z,x total_specific_humidity
qv=>qv                  401 t,z,x water_vapor_content
theta=>theta            401 t,z,x potential_temperature
theta_e=>thetae        401 t,z,x equivalent_potential_temperature
pr=>pr                  401 t,z,x precipitation_rate
ENDVARS
