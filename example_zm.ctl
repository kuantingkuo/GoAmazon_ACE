DSET ^NCFILE
DTYPE netcdf
TITLE ACE output
UNDEF -9.99e8
XDEF 6 LINEAR 1 2
YDEF 1 LINEAR 1 1
ZDEF 401 LINEAR 0 0.1
TDEF TIMESTEP LINEAR 00:00Z01JAN2000 1mn
VARS 2
mf=>mf                  401 t,z,x mass_flux
rho_mf=>rho             401     z density on mass_flux level
ENDVARS
