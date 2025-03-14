exp_tag='control13579'
exp_cap='CTRL'
pattern='GoAmazon_idp314_kknw25cin_6aces-dynamic_means.??.ctl'
path='/data/W.eddie/GoAmazon_ACE/ACE-runs/'exp_tag'/'
cases=sys('ls 'path%pattern'|awk -F/ ''{print $NF}''')
say cases
rc=gsfallow('on')
exps='0.06 0.16 0.29 0.36 0.51 0.66 0.83 0.99 1.17 1.35 1.55 1.76'
sels='1 3 5 6 7 8 9 10 11 12'
num=count_num(sels)
say num

v1=0
v2=27
'color 2 'num' 1 -kind dark_jet'
colors=range(16,num+16-1)
'reinit'
'set mproj off'
'ini -l'
i=1
while(i<=num)
    j=subwrd(sels,i)
    case=subwrd(cases,j)
    'open 'path%case
    'set x 1'
    'set z 1'
    'set time 00Z 03Z'
** average over the inner 2 ACEs **
    'pa=3600*(pr(x=1)*0.25+pr(x=2)*2)/2.25'
    'set grads off'
    'set xlabs 00:00|00:30|01:00|01:30|02:00|02:30|03:00'
    color=subwrd(colors,i)
    'set ccolor 'color
    style=subwrd(styles,i)
    'set cmark 0'
    'set cthick 7'
    'set vrange 0 'v2
    'd pa'
    if i=1 
        'draw xlab Time'
        'draw ylab Precipitation Rate [mm h`a-1`n]'
        'draw title ACE 'exp_cap
        'off'
    endif
    'close 1'
    i=i+1
endwhile
num1=5
num2=5
exp1=''
i=1
while(i<=num1)
    j=subwrd(sels,i)
    exp1=exp1' 'subwrd(exps,j)
    i=i+1
endwhile
exp2=''
while(i<=num1+num2)
    j=subwrd(sels,i)
    exp2=exp2' 'subwrd(exps,j)
    i=i+1
endwhile
color1=range(16,16+num1-1)
color2=range(16+num1,16+num1+num2-1)
'legend tc 'num1' 'exp1' 'color1
'legend tr 'num2' 'exp2' 'color2
'gxprint /data/W.eddie/GoAmazon_ACE_Figs/prec_'exp_tag'_core.png white'
'gxprint /data/W.eddie/GoAmazon_ACE_Figs/prec_'exp_tag'_core.svg white'
