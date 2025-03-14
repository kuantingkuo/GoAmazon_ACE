exp_tags='control13579'
exps='0.06 0.16 0.29 0.36 0.51 0.66 0.83 0.99 1.17 1.35 1.55 1.76'
rc=gsfallow('on')
num=count_num(exp_tags)

tag=1
while(tag<=num)
path='/data/W.eddie/GoAmazon_ACE/ACE-runs/'
exp_tag=subwrd(exp_tags,tag)
pattern='GoAmazon_idp314_kknw25cin_6aces-dynamic_means.??.ctl'
cases=sys('ls -d 'path%exp_tag'/'pattern'|awk -F/ ''{print $NF}''')
num=count_num(cases)
'reinit'
'set mproj off'
'ini -l'
i=1
while(i<=num)
    case=subwrd(cases,i)
    filename=sys('basename ""'case'"" .ctl')
    path='/data/W.eddie/GoAmazon_ACE/ACE-runs/'exp_tag'/'subwrd(filename,1)
    'open 'path'.ctl'
    'open 'path'_zm.ctl'
    'set x 1'
    'set y 1'
    'set lev 0 13.9606'
    'set time 00Z 03Z'
    'buo=B.1'
    'cldc=qc'
    'set dfile 2'
    'wa=mf.2/rho.2'
    'set dfile 1'
    'c'
    'on'
    'set grads off'
    'set xlabs 00:00|00:30|01:00|01:30|02:00|02:30|03:00'
    'color -levs -0.05 -0.04 -0.03 -0.02 -0.01 -0.005 0.005 0.01 0.02 0.03 0.04 0.05 -kind blue-(5)->white->orange->red'
    'd buo'
    'xcbar3 -unit [m s`a-2`n]'
    exp=subwrd(exps,i)
    'draw title Buoyancy & Cloud  `0'exp
    'draw xlab Time'
    'draw ylab Height [km]'
    'off'
    'set cthick 4'
    'set clab masked'
    'color -levs -2 -1 -0.5 -0.2 0.2 0.5 1 2 3 4 5 6 7 8 9 -kind black->black -gxout contour'
    'd wa'
    'set cthick 6'
    'set rgb 99 30 180 30'
    'set ccolor 99'
    'set clab masked'
    'set clevs 1e-5 1e-4 1e-3 1e-2'
    'd cldc'
    'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Buo_evo_core_'exp_tag'_'exp'.png white'
    'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Buo_evo_core_'exp_tag'_'exp'.svg white'
    'close 2'
    'close 1'
    i=i+1
endwhile
tag=tag+1
endwhile
