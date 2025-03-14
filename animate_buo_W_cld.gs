exp_tag='control13579'
case='16'
infile='inic_ctrl.txt'
path='/data/W.eddie/GoAmazon_ACE/ACE-runs/'exp_tag'/'
rc=gsfallow('on')
'reinit'
'set mproj off'
'ini -l'
'open 'path'GoAmazon_idp314_kknw25cin_6aces-dynamic_means.'case'.ctl'
'open 'path'GoAmazon_idp314_kknw25cin_6aces-dynamic_means.'case'_zm.ctl'
'set lev 0 7'

t=1
while(t<=181)
'c'
'on'
'set grads off'
'set t 't
rc=make_sym('B','symB')
rc=make_sym('qc*1e3','symqc')
'set dfile 2'
'set x 1'
'set z 1 71'
'rho=rho.2'
'set x -3 5'
'W=mf.2/rho'
rc=make_sym('W','symW')
'set dfile 1'
'set xaxis -4 4'
*'color -levs -0.02 -0.016 -0.012 -0.008 -0.004 -0.002 0.002 0.004 0.008 0.012 0.016 0.02'
'color -levs -0.05 -0.04 -0.03 -0.02 -0.01 -0.005 0.005 0.01 0.02 0.03 0.04 0.05 -kind blue-(5)->white->orange->red'
'd symB'
'cbar3 [m s`a-2`n]'
'draw xlab [km]'
'draw ylab Height [km]'
ttt=math_format('%03g',t-1)
'draw title Buoyancy (shaded)                         `0'ttt' min.\Cloud Water [g kg`a-1`n] (green contours) & W [m s`a-1`n] (black contours)'
'off'
'set ccolor 4'
'set clab masked'
'color -levs 0.01 0.1 0.3 0.6 1 -kind lightgreen->green -gxout contour'
'set cthick 8'
'd symqc'
'set ccolor 1'
'set clab masked'
'set cthick 4'
'set clevs -1 -0.8 -0.6 -0.4 -0.2 0.2 0.4 0.6 0.8 1'
'd symW'
'gxprint /data/W.eddie/GoAmazon_ACE_temp/GoAmazon_'exp_tag'_'case'_'ttt'.png white'
t=t+1
endwhile

function make_sym(var,new)
    'set x -3 5'
    'set z 1 71'
    ''new'=const('var',0,-u)'
    k=1
    while(k<=71)
        i=-3
        while(i<1)
            'set z 'k
            'set x 'i
            'lon0=lon'
            'lev0=lev'
            'set x '2-i
            'd 'var
            temp=subwrd(result,4)
            'set x -3 5'
            'set z 1 71'
            ''new'=const(maskout('new',(lon!=lon0)|(lev!=lev0)),'temp',-u)'
            i=i+1
        endwhile
    k=k+1
    endwhile

    return