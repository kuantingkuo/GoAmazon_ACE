x1=54;x2=75
colors='20 18 17 23 25'
'reinit'
'set mproj off'
'ini -s'
'open /data/W.eddie/VVM/DATA/GoAmazon_line58_16_t06/gs_ctl_files/dynamic.ctl'
'xygrid'
'R=sqrt(pow(xgrid-64.5,2)+pow(ygrid-64.5,2))'
'set x 'x1' 'x2
'set y 'x1' 'x2
'set z 4'
'reg=const(w,6)'
'reg=if(R<=1,1,reg)'
'reg=if(((R>1)&(R<=3)),2,reg)'
'reg=if(((R>3)&(R<=5)),3,reg)'
'reg=if(((R>5)&(R<=7)),4,reg)'
'reg=if(((R>7)&(R<=9)),5,reg)'
'wnew=const(w,0)'
i=1
while(i<=5)
    'wm'i'=amean(maskout(w,reg='i'),x='x1',x='x2',y='x1',y='x2')'
    'wnew=if(reg='i',wm'i',wnew)'
    i=i+1
endwhile

x0=64.5
dx=0.5
xkm1=(x1-x0)*dx
xkm2=(x2-x0)*dx

'c'
'set grads off'
'set xaxis 'xkm1' 'xkm2
'set yaxis 'xkm1' 'xkm2
'color -levs -0.6 -0.27 -0.1 -0.06 -0.02 0.1 0.3 0.7 1.2 1.9 -kind (134,97,42)-(1)->(238,199,100)-(2)->white->salmon->(235,0,235) -gxout grfill'
'd wnew'
'cbar3 [m s-`a1`n]'
'draw xlab X [km]'
'draw ylab Y [km]'
'draw title ACE'

'q gr2xy 64.5 64.5'
x0=subwrd(result,3)
y0=subwrd(result,6)
i=1
while(i<=5)
    rt=64.5+10-(i-1)*2
    'q gr2xy 'rt' 'rt
    xr=subwrd(result,3)
    yt=subwrd(result,6)
    lb=64.5-10+(i-1)*2
    'q gr2xy 'lb' 'lb
    xl=subwrd(result,3)
    yb=subwrd(result,6)
    size=((xr-xl)+(yt-yb))/2
    'set line 'subwrd(colors,i)
    'draw mark 3 'x0' 'y0' 'size
    i=i+1
endwhile    

'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Winit_map.png white'
'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Winit_map.svg white'
