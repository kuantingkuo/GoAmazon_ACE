x1=54;x2=75
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
'reg=if(R<2,1,reg)'
'reg=if(((R>=2)&(R<4)),2,reg)'
'reg=if(((R>=4)&(R<6)),3,reg)'
'reg=if(((R>=6)&(R<8)),4,reg)'
'reg=if(((R>=8)&(R<10)),5,reg)'
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
'color -levs -0.6 -0.3 -0.1 -0.06 -0.02 0.1 0.3 0.7 1.2 1.9 -kind blue-(4)->white->red -gxout grfill'
'd wnew'
'cbar3 [m s-`a1`n]'
'draw xlab X [km]'
'draw ylab Y [km]'
'draw title ACE'
'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Winit_map.png white'
'gxprint /data/W.eddie/GoAmazon_ACE_Figs/Winit_map.svg white'
