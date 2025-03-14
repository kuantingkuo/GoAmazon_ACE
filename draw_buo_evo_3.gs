exp_tag='control13579'
name='CTRL'
sels='1 3 8'
exps='0.06 0.16 0.29 0.36 0.51 0.66 0.83 0.99 1.17 1.35 1.55 1.76'
rc=gsfallow('on')
num=count_num(sels)
'reinit'
'set xsize 500 1000'
'q gxinfo'
line=sublin(result,2)
xpage=subwrd(line,4)-0.00001
ypage=subwrd(line,6)

path='/data/W.eddie/GoAmazon_ACE/ACE-runs/'
pattern='GoAmazon_idp314_kknw25cin_6aces-dynamic_means.??.ctl'
cases=sys('ls -d 'path%exp_tag'/'pattern'|awk -F/ ''{print $NF}''')

'set mproj off'
'set display white'
'c'
'set font 1'
'set xlopts 1 2 0.13'
'set ylopts 1 2 0.13'
j=1
while(j<=num)
    i=subwrd(sels,j)
    case=subwrd(cases,i)
    filename=sys('basename ""'case'"" .ctl')
    path='/data/W.eddie/GoAmazon_ACE/ACE-runs/'exp_tag'/'subwrd(filename,1)
    'open 'path'.ctl'
    'open 'path'_zm.ctl'
    'set x 1'
    'set y 1'
    'set lev 0 16'
    'set time 00Z 03Z'
    'buo=B.1'
    'cldc=qc'
    'set dfile 2'
    'wa=mf.2/rho.2'
    'set dfile 1'

    ypage1=ypage-j*ypage/3
    ypage2=ypage-(j-1)*ypage/3
    if(j>1)
        ypage1=ypage1+0.4*(j-1)
        ypage2=ypage2+0.4*(j-1)
    endif
    if(j=num)
        ypage1=0
    endif
    dy=ypage2-ypage1
    'set vpage 0 'xpage' 'ypage1' 'ypage2
say    'set vpage 0 'xpage' 'ypage1' 'ypage2
    xp1=0.8; xp2=xpage-0.3; yp1=dy-3.4; yp2=dy-0.5
    'set parea 'xp1' 'xp2' 'yp1' 'yp2
say    'set parea 'xp1' 'xp2' 'yp1' 'yp2
    'on'
    'set grads off'
    'set xlabs 00:00|00:30|01:00|01:30|02:00|02:30|03:00'
    'color -levs -0.05 -0.04 -0.03 -0.02 -0.01 -0.005 0.005 0.01 0.02 0.03 0.04 0.05 -kind blue-(5)->white->orange->red'
    'd buo'
    exp=subwrd(exps,i)
    if(j=1)
        'draw title Buoyancy, W, & Cloud'
    endif
    'set string 1 tl'
    'draw string 'xp1+0.05' 'yp2-0.05' ACE `0'name
    'draw string 'xp1+0.05' 'yp2-0.2' `0'exp
    if(j=num)
*        'xcbar3 -unit [m s`a-2`n]'
        'draw xlab Time'
    endif
    'draw ylab Height [km]'
    'off'
    'set gxout contour'
    'set cthick 3'
    'set clab masked'
*    'color -levs -2 -1 -0.5 -0.2 0.2 0.5 1 2 3 4 5 6 7 8 9 -kind black->black -gxout contour'
    'color -levs -6 -4 -2 -1 1 2 4 6 9 12 15 18 21 24 27 30 -kind black->black -gxout contour'
    'd wa'
    'set cthick 6'
    'set rgb 99 30 180 30'
    'set ccolor 99'
    'set clab masked'
    'set clevs 1e-5 1e-4 1e-3 1e-2'
    'd cldc'
    'close 2'
    'close 1'
    j=j+1
endwhile
'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Buo_evo_3_'exp_tag'.png white x500 y1000'
'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Buo_evo_3_'exp_tag'.svg white x500 y1000'
