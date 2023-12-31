# TCP/UDP quote server
# Source of quotes: https://github.com/erossignon/qod4outlook/blob/master/quotes.txt

import base64, bz2, logging, random, sys, threading, time
from socketserver import (
        BaseRequestHandler, ThreadingTCPServer, ThreadingUDPServer)

HOST, PORT = "0.0.0.0", 1700

QUOTE_DATA = """
QlpoOTFBWSZTWdtCBoAAZEHf/XgQdu9/+v////s////xQAAMZkGwAQAIABAAYFtZmPvFgoAGh3oN
aSPdkigXYAoyqiKmQxUK0AAAANGnuy3hYcpL2Gq3mrwaBSlAWqtnp071nTLbJN60nCnnrBIF2KPb
1AB7YNLsc92uWR2rObYd3JO3uHuRFQUAAJbRSWxvCx2Sy8u12sXbWYwq713QVRqS6y7AklQBUoV6
zRq0KNQWhqUBswLRWFAvKBo92DZrWnHZrjoADcbWNJcsd3cq9gZrbD0HTu9A8PL03w00IAgCAIBB
KfoNI1T8KGRNG1Gm9UwBPUwR6g0DU8gIQJCBVPanpqDGlPImQDRkaAABoAAADTCSaAqepoapoP1G
kBtQaADQ0AAMT1AAAAJNJEIQjQTFKflMNGqbTJiCYQxGgxAGgBiAB3qMRpiDQGmgAAAZAaA0A0Aa
NAGQaAkQhATQQTIT0QGo1T8k9GBNJk1GamgNAAGg0ZdAD2edfejIQ/P99iyPw+97hn9rWiGV6X/I
09Vv7sH7/Tr+WPhc59KY5PG6R7e5jhQOKyB228/ozt4vJvh+6uOsXw8R/p7z8UFwgCTrPwiKEDer
XaOv9qUmmWyi6HHx+l5ifpbREO49zfpeiGn5NULH/CO2CSUbYfQw/x/ZaH9p+07TFmJNFNbYr+1X
6mchnrWCOPr6LsYGE1pXBhgepgRIF+OPV0tQKIy9WnGlJ43pPDhg0vGGLOOZFjgtWC/NnccyzL88
pZOMW9zXgqlfHR3qQOB2ZfY5M7MMPHaMazNn/HFn1pZRBw93Ps1ALaV1iGNnxp2y9BU5QHxTwlTe
gAs8QPv97gmSfuNSH42B/WwP33GoRZiFYTaB/4YH9iGvz2E36UkOkIsh5HdqKqPutfxs/PIfrYqa
6NIOjWPpmlbNNnoHqZWNIj1O3fcwx3/6d2zI9yoOnhOEMs++Pehe0sIyfcIIFBYkoE4yKjBAgqFm
9y3JoYVhcojwEl+735/UOiKckt+ULjoqD7+P+isGCHWoxMh3EF9/6KPQx+27T7C3nw7efXfh4d/C
+Iz/8Pxh4BmxproNbdud45lGIHpEKcwcsb5VJG2wo4jPXYiug1BlceSznhb/pvlXyInXkDjjVL0W
+deVqrXjPVxrhTW5PxZ7MpbsH366rmkWv0NM78WKGjDKMDy0vZNc64ulBIGbIgyjzkiDWk4tPScP
qepxVcKaZCtcNZklKnLKH+tk8TtE6/03ATeu58v9V8fuhytpijcoC/+e/Gn/P16ej8A0cB1odZcG
66D+XS21MBVrrUFbtVJQsvjSbMZzRjOPZbvD0FHnCJJUBQSq+nlrAg/CNwJKpmQ0DAhWAJYFTnlh
Jr0kMzAflrrSuhiN6WsAPGAHs4UejQz/HwsIzEzZFxYaMqrDGWUJeMjvjZ10EThDoYePKr0Hn8fc
07d9W7eR+HSYwyO7RHLybpCNgpvzbpxw5gVlwxreAf4sxlbx3ex+zpyFE6xrL03e8s5h+sIA4/ZD
XC/gZaqtkkGBlfzjfM8Y4+K2ivJZHLACsDAEvfqh2bD41mKU5ygo7DXKV5YzjDTW2o7R70gK9Vy4
NC7BYY8p0QQxj6zueMYuYw92z+WkY479EI0zqKjTCsTDlYQM6PFNAnQqg0cST0xxwrvGIGnauVry
ZpqpHWLaByCFVSj+Icykt++4YUttr6JUZ6nM+Pt3y/Ty+IfD1BfNUhv9cGQx3rK+wwXdrp2wqUSk
tMjF+fZWG8MrVA4HUAQFuCaDUGX24Bilc5lkLjnDybKkePCXkJds5twjTfLL4mWferuUJ616HA9C
M9H66wXnOGh0kFkSH3KFdhFH6h1MukBheNOOC2kIVPZvcw6wU4GcXY5BcjEZd8NiVz1wz86pwpaS
I9QwBmSwyr2ZXZbgZvAyFRv706uxcQWSIIjR5tjdQMdZZsiUCjpxP8yYYubYDt690YrI2EBSZnpC
a2NPiTb6/lj2fObFT7aHHMzk/2GmnyMYDa5c+JaHsOo1kyced9tPPxY4aPZui+SJl4Zj/lHCFPit
W0c1A9rEqg/gQbNU4qco9LFVj0D/iaBAVy+GZutXHjBTaNyzFEjUlgTEywlkSDOwi0RLM8CjUOcX
gXJUFCZutbLQyIyjl7efa0BcyDDI1dmozDnth1Lfj3FLfmbHu9OeIhmo/Mjq4bDUEEcU6GNlTyaR
KSwgEmMpxcFsIoiiEbKFttEKod4qPfq+Nai2q7bhZHvnCtEEB0gOA7iHhchVla4WxIv8j7LxluBU
u/8fUY6FgLm+LDZocnfH+NlsO2dg0Qjo6ROZtupPYc7pbQKGOw48DnYc8QrSWAzZpZOQyDYskknK
jCw00CJCkkhrTQ7ROyJ97I1WFt5RIDlYggr7mqH2Cfn8pb0KPSfRgizgMFAgtv7vUjsi/EsWnbEJ
suwfbjTyp0enXyjuDfXc1zztt5D+tYozNNo3evPjl5bL8WBmxa7xDFvJxUTtaSuVhyWmKGkHZwTj
fIQKVEEyxEe+tWeIUSZRgPDGzTc7xDmLy3KWTge7QbMeLnTMNVrx+C6YUOm0VRxQFBylkJAnJCb0
sBpmXw9wVuqnSciYCVVqwSlFs7gSVFLmj2hUKo6XWhib3GHiLyIj8sgtHmKuJDqFD4jLN45HF+cL
QRQQZz0wepf9b1alvjWEe6Zhn9y/tD0cwD5tj7bb2gcTM2Hz5PvL3XtRXII4jHPCNwBahe2f9G8V
i+q+H7JTcBw/PEDqOPV2//ohcuNXCdniOz09IDrxjAQFDllC0dG4X69LMMojHlGhgRAiRHZu2HB2
MLymyjLTaOvtJdFxwz2e6x9LEcjePCkseZjiWMetKzjZwTbat8tWGMh0CiaVui/vbs7B2tl4Pc7g
jk8TvXB1Z4lZbnQY40QsozvQMpZzEHh/flPVzXvE6H3MF7v4c8jmnFatmdMQSAx357VvU5ncnaga
IMrEYYRGHfSgBnbtkA74GA/zVXXbcZLtDsNIaF9TsQJlg+amAyJHDvOR3P0DZYimQrZEP3+chPuO
DxUFQG3CyLggZbfstQBhAYYhcKxtfOmXB8nmRPAbIb8qo+1jBdaGgcXYgk1jEO2X6hqVr5VZrttp
BiGE8LDR7G2j3TcxQulMLC4j2IqJliz/z/rp9eJjxx6ej7TphwdHjlSZkzTX8/LGJmMvR6v2vjXF
VLHnrk2dpcQmySOKjoaUjIzep237EKJlgiJLUC4cP78QLPG5rX2l3JBndbzqFdVeU1knyJDLLS0o
Bg3t21LcuC+0FLNHWW5q2JThg7V4+C/w0+1qwbbCLTT8PMb9NY0N0Bl2ffE/vFzwtt8aQ4nCHVHf
Lw545enEWGwa8YcR/hrb1de2oJofb7C2G55Ld6ch26Tm/lRD544zarVPBYcvEliQzw6VW88YgCjm
wjgnPu428qPzNti195sduguehviBa7RiyIMNOREnhiEXlX5N3zujrUDTr4LgbZtwFFHzBYwzAZgh
aIgw/vKdAm+h6+zx1OMnUOsxsfsN64cVmlqvU7Ndmqp/VIPuP5eLJlSjlJBmXt3Dvov0VEArV8s0
RioppyEjN5M5m7M/6HS39Dt+uoW89GC7re7Pl08pBPasUaYUsysoWVi1YAEto8SIf9yvXlDlOFRu
tuLhW+TMdhel3tyfd8S1hgmHz9QJMgmfp/xQezS0KEQ5Q2ye57xyoqHpDx1+fANLBZUXWkQ92h1p
F40k9NFix1VVI5BH0odLh9nHDzrhaz++24N/XSaDXw2ZhDDtCFTiLZCw089RfwhSJE5+TVPPgc2G
QNdqTgmdiv1/Cz82VyPr7av9x1BFkB3xXAo8LNPrOh/BDmihfX1qZ9VAyyBaalmI7X6M9CxYjbxH
S1mvOeO5Qtazlw4QYVxV2N9LOjPs4R2lgSRhEHf0TE0QFF5/msEJccLrmt13u8rL+qObh6M9Npwu
o0hNKW1DCIWbgQC0EleLdXjaNFEzMpiQbXb9ZSCJTytUk4Ks9psCOFp1zoRpfKFCJRZG0hhJ2vg2
lKYstuN7F6+zeepB169KYa2Yfu3Xb2fMt6FfS8TbzRFzr5FmI2sqUpyrCD5LAim8BEPetotASEUV
31dLEWHC3lw9QP2s6I5sbaQjzPWBxXIU7tgeldiYY3QQ+Ue5BlHvKzocn59LaF5FjXLttkq9m+Z+
ZY58CgXqq1mS+y8xEHGgDBx2dI8pUQ/X1EDwbyNdcCeTS4powWnFXmfhOd835NUySeuWMJP53qMc
jromsujGuHDh/2GhhsiPsUCIKA1VP2JGSw+qHDbZUxWclt71S7yM4YLBKwggULI+qTnGaU6OSyKB
pRfu7j1jRFN6IvKfafaGgcGBniamB7OGEnIYd1lhcEzXt7fqfyxYRDVp3blK9QvOutCPUytKkRZh
Bn83FGt0XKdM14xW1wUqypQ2PUgdO+MYiA/Mjsz+PT4R4Y8TLdab8MdnlRtrDgtlEOEBESaH8pkK
XlPCkcLUjAdl7lGIoMe2DumC0vaMaPjg+GLJYe9MERowKTX9FuRJkBsIIabWv5Jkx/Fsi11HKgUy
XGDqFwE+DwMVkm/4/o/f1rvhS1rI0ZH3ge9ou/ye4GOr8aIphYb9NBREgn6qrQcMOfhhyYn6Q+JJ
SGTjZbzxo1NRvisTBE8Pyyg4d2bZdHp2y8+1SS0ah4JwCakmfhbYeTy1tnPVQies95jSsVsJNX5G
4GR2aavZEjWX/mujewkyg4bC8oGFktAeWcEzFvFvvx8uD8+UEphqqvFNNIxLsHXqx7fippfKHesl
m9MWot7nbie+4+sUG+WbbkcMn30sajV3gb34+pkbNF9sQHK5dIDYND0OMhHzpuxKQJ0nZb+y6hTs
IXSGIPO5Y+6EMsUGCa1P6mt35v/duvVe45QHv0ujxtIe6xYnZggoUT02qxJKZeKB8lPsaGReeAY7
0fWhZiwhrlvG74o1weJXj/NasP8BBgbvfOghKT+vHMzKsbnc5iZlgtj7Z1mei1tTiZgSg++bB3BF
iJBDU08EjOJ9NntexbVHzvt+zPOFS5ftyHHYUsTbi/eBcqEvanfiUOuFpda45sgQdb3qmg8b7mPU
875Qvmn9ryPn1zbgaK1tr7UwybD/wedZ6Im3D168d1Qo9cX8dNItqCdZqYto7vhEe4uwSdDxmFly
SAw7ZpVU6QukcMpuYwiTlmamyQxAN3kVEWQjKaGkudS2beausZtAzLfvUpkxfuLFLRuN5nmyJerZ
YuqD6PV1gg7CG+l1FUJjNwHO+4sdRGisc6+OKsQM4I4CyDwoWnhN3xbcHOaRZtbRG4oi+0T+qNVw
p1e6gmtKW6G8xIsuGKlsZ4XzjiDu8/iwebUzzMDxqIj2hVBkeueCJ3M95sQCdi6o4YmuGGGJjrvh
zvM0ChzSZoB5RzAd6IqW1ckiYHXCB4xCiSiARrqvbXVzxbaGmHZ0tGfT9VWw/H6eJ7INYK5I6Q84
WF14m4auWoXNfYnRx9GDoMxQ49ed1fDEMJwy4gCuW8SDNGPBxH0O4q9dlxIZSkTiXU+rZh+YbkOO
vgq9Dj4evjaxXs1OF7Q680kwIgZRDYEvbPUBxU1MCUHdbu4xEDIQzc1IafxfExoUcx0YfKLDLqQZ
NUrrDBggRZXzNktkSxB4UNbcSNRETJT/NNCxmEXK42+szI4y7ZHgruHius+QL3Qt1D31MA3/UaDf
hb3Nd/HGpWRLW0H2j5ML6Qvv6V5rPrfTZzyN5EcvgwI2b2g5AYWHSp8Z/QpgHghiZVsOj57v8Dy7
rqDLVN5dlaDJN0wfXAlh/cmanmwq4DZxxf8k6NghzdGn+PS+UKrI5/6L1ExYq877yeJg5UtrJwLW
OnG8M2OpseJYwqIZKPv+saceZcpm5SxqF/A7nbhSQgV9xiL47tFvHHAKfQh/sRLeyhnkDI3tyqo5
1WnHsd/ftt+QG39CxDfMsRtiu+8Ly+qJ74neTyxrbMaUMIZiy+tPVJCxz1F1EfOfENiq10er6NeE
7FnsgTSCVeK6MO2n688HtMWvhDMLWg1fB8919rKx3Y1L69R1Ud+zjN7nDTjgLE59MBvi9Hg6Jl9s
Yyi0qTKEmGh3czXq4nbVQQ9GHBtNPZ1y6BM3l/ZBRpEQFw5cZB4QFFGBDGcJStAprWVeHNX1tThv
16cRpdQtNB+UqZTQHZ+XsiQQyZj8s2Ysk/Jfg7cbF/OtuFloexCDlalx9bbd0GF0Xdt5mSgdiHgH
SFWhfA5zlDhxpsLMIiWjYnyKXtOi02hAdb2ezV9fK/Lx+z/GCk/YklQFWEUiiie7jh9OP2JJYGA3
znKmmBTUNtlRfu59WTbl4E12nwiKf8vt6oEBkxBkwEjkw3YHc6bZn/LbpO/QOTX9Lp83ZpQ0bNjF
a8pG7BKmI9D0+2BX0/o/jj6NvXzfGS7nFkgvg4B/5YShiG//jQQgLJ/pakMSVBhBgCh8fw5j/L+i
/z/V5a+DfDZ46yD+zTif6udPLjRvV8i14VHuq/lLw+lZj6R+v6Dj0pXM8Ttn+etuOMsZtV2ymrO3
7NYXsTn+rj/AOMrG+vD11j1t8594ZM3Nbx41nF34dn5R/rr3+j+ID+NEKbdgEz3xXar6cmhiF/eY
bGoRSih62+xltvXd94+T15RYh5Ydi41mii9YLUBv32qE8J8lpt/tGZAzeGO7OpwxTrBB1MD+R4M/
o/hpk8Co/F/hnhzSF9ofunrlWfxL25YEHOCi1Y6NHOFlXCHhV6mEetOXK2F4VYdqQeBgyqRxNxhD
OYZ+3RmUzRIpoMBcRMvM/uG6e74a3Ir1NOM+WN37PceZktyWn+GY3IfXp6i1r8Ir++/23GI+OhqB
1uNp1kr9jJjWjK5JKruJrn9KDsQB9EP4w09+lM9QNW8KvomnSa0is9RYEOdyuBvFhf3REn7YvV/5
AwT71+1U5O6EqrMIczO6urNM1BxfzaHCN/s1+z7wwdTvaYHdfkml/ZLBtLpFDhPmCbm2utFiHCyv
EM2a1alGgtGC+UlYzZlMCOL/yeLt1/zGC6/thsVlJEO3+A/bdIIgxjtT+YPo2+anVVMzPYe4fv3H
9fnif+W3Zhz9N+QkRuOttfA24cuHYQChhKu7wQQ4eDj+akd4w6OMeuUHS02s5rFsmWr6Ko9Kwfzq
G+kfR06p8Oo/yHTj939O+2wy7NH2Pt+mW+XtM/aWM2cVqtGo+rW0N+WYiyMnKF2YUeEflRSGhKJG
Naziax9W6NKi/KF4VjcWmHkBBu5oMnlSnT4uAeNW5j7svs3GWROl+RgEXQX+RZ+f887SuJXvCCvQ
qNeFHJznNsjhG9Zu7SykMHD3cLiOzrdIjzlWM6Vxm3k83jOKIaC4Wq999X1vadD2vpnyjI9lUr/d
MtNf5D7gFLH/VEIR/Ps/yzloP+LAwwP6Gkf2MC71xPGv23SFJc+35J0t14cYn+2CJPtk2HCMRABc
G3Bd9iGQsDmJvgXIhX7JcbXAgso4XGRr/o3NNEIwbaKCLPaCdLBFhjCGI0a9v+/v5+I9fX6190bS
p6PKgekjlvCXtcMprb2tKAg8LTXL6l/Jr39OPHr2Ps/LfsEtKx/WQT8N/5j/Tun8jj9wqCysimtW
/0tm0Ddv8CXNG9FVFkyRqf0B/NTH2oHDDFtrwwOVGjKCDFRYfkQqpMQqaYdJUlZp1WwL3u0mGqTr
PnhtEVTsysLdPIfubyLIe3816fo/q/hzMrnA2wIYltMG7AKGLdwm2L6WWPUx+r+r+DjnmgIrCR7N
gswYoYlTvYUFgaGFQ6STENt23aQYhUh6/x/9cm+KjOUKLzf9SG96wuWAstKiS26SVjFEMVJ0Jv+X
1z/tOSqggqc0o3rDGYyjBGJUWSKUQVFayoqKsSIIHZnSTBog40IqguGE3+z10jszyZllAQwVDDvv
uTb+PxSSNtjDrzKHnGUQ/n3dNt/E7/P0H+LU/m+yhx1RZ2EUUltkO2awmhMaICgtjF58p9MA6PD9
GYYDmBsWXu9MvG3s9I6PA/5MzZo29RxZ8bdQhaG/fZnwu2TEqpUih/b5LpmmQH6rViyJ2fb6lCpw
JsQozlsYeTR5eRBkSdvn+K3kNLNrVoWHLDVNFDh8mSIsEFX0qzeWYwUDFSB39315jnx885Zz1e6S
qxirIsRUSIijpoiIigopMbEQUVjEiyo6bJclbSE/scRTytgCh7km2Q9qej0hUPs/rocbKRehnhlg
qp+BxmIqkUgsT65a9NR0NINoH+H9o/Z/X/R9c/l/NSfp4Yft/cXDwP9Q1EcP8d1qEDSQ/gZDGDGE
D/1+f+iUhXaLtA2GGI1iC7poN97htjLLOc+czG/nUQiRkcEJN56VxMwXNMHlRYVYIJOUr9QgmpiJ
J/j3/ChLM/r2j8Wo7l8f8tZOma3QStNJNMD/rpqB/O+EP4q/nkjMFsoI4tPG+JIBVuhccVgxQhKf
Ip93VaJ77GFTBvPAdnRQVoranlfp/zzJaKa2z9gZqkIp+bDAsTrH0edIy8aJFjXcSAcHqUwS1UHX
AURPlw7gndh7OTbr34/Xjc61Wby4bxoe/eqvhWMcw/PrS8D0zkzG2vd7SdnQDYn3kEMY2xo3z8D9
otLXtDJQiPjvXq6csrRarEuJxNJ1BMs8M30fJr6O7QLgIj5rX8XPWM3f8NDroAIkafgUvDfQ11jo
wvEHlEJtIs1gZzDFR5aY3232icTK7SWsWtYsfLse9rvy9MtFYOZJB3eDTeUo+DEKajkMlfcxBVB4
fuVl2gHMZCyDic/eGkGLcx9xsUhZtIRnoW19fq+UPwxzzQ2mzq9fWDOGXn0/flHFN/RK4wsrFB5F
KsLhwXaIRIKSWoBsxTtlkwKc5Cutm/utE2WjvGjM2c73DEQQSlVtBi2A335TK6XPAVa2G+/HJ1Wx
53u9QsQlSAdCEFhFFiikPkyH5elK73MQQsbeYdq/hxmpSPkIhGgJhjqXLIrO50S477wjI0Gp09lk
fIcacyR5xAwaZl6t5oHkPem0BbB2YlCQCxKoB9tdEHuVZxHvcdNvlVNjbwW8oI7d2W7Pe5cDhkRB
1hQfExrhHkR/CtTfw3bOkOCP9rzld8nOqLlJFfM377I9mV9RsTGMUEFWE96UDy4wMYC66sMUVgsV
kQUIoKHAlHzSrdznXr61bPx/El+yPYHniwQcktTI7/DOkrnzKF1VBYfwyOZ+j50hEwxloqZ6KkCN
i2gvqGYMq3aYDwAMsX4HeFfL5fM8HmCm94ePqqiWlI1L52b1SW/Tea25cwWJE2RJEtOQghpK1dGG
3SapfVpt2oWMZnDHrZGtZ8mfT6XtzeMaknl6/SmZYg2DzbYFDsXtwAnwjaSjUJVGVlBkqIkLWgVo
wtKUVaUFgjFgSsERz7x5GGzDwGI7cHibFvh3KcHGZ3O7fJzV2WlyRBdlMmHFRg7HbkZHtDF8okCD
2WW85/tVhPruNYiiEQG1JsmgMQo0JWLatBs4OzESd2BRVMZEuqLfhUoTAEE6izBhmbJvfPAECwjS
nHxy5eo8QDAYIG5sIPuaX1E+CIOtM0smYWOwCNS4mdvkFIvz+g2bElZmGkoyiJvEwsvi1yS9l1zy
m3eRBqzOP3ewi52uByHkw+XLzHhAFobukCUISBeGU5BZAcCPnKXyiLCowIS5cqhoQx1840jknMHL
5Ib8WLwtchL3YUYTIaPsvB/ZP05sgoBH0tIUsSMMSWV4Dr++DW/JLLjt8B9LLbYukMbNFAGMH0Ds
JEdcHjRzzKznkMVgpFBEFgrpKIi8akhcym4mJjTZr2+zlXOmeEnQEUe3pfkgd0O0DfXJjud5DiQx
gQ8T9N4OKB/oThDBCV4qE8vyAYrqXsvPAoRiASTaXskhyws0EmyTB61pEUQKjT1H3gvLPFlRlcTh
DTEQ0WI5N6mJrRcaxZUcznmc9+f2u/QJhBKQuDV4jJ1azkEAggg64Ft2O7OE6QCymCVRBSaoLHCv
OA62qgNQq10mixZYjFMwGCcQrexznGLD8uJmwTu1wCQVwKyMBIqDN1xreBuNMQDBqbNkwoktZaIi
hYVIXKt0l0mzjwWHzfTVkIdvjQzv/FhsQVGIhDSAKBD9pJXIixSB/Iz0M9TNosn2e4sPizYh+4zq
fC+Z2JYAxdSnwIYUvvZ8L5yKFGVuFqGWllfvW8XWXExRUylFHeXFVspWUz3M57E8pzAWg1QCAxmg
wTuEbOS21gkyMTKKiFgNFAXLdtsW0GfQ0IrXfiwR3kYuUSyaBta0w5vQmoexmmHAaqEqlu/F52Zu
iwRDvTfBq6u9F0mxuZXEtiotzMcylyhvdxE0NNOORrMdYGOVN6rOKcBxm9FdOIjLsUwq1zdomDQe
Gu7bxk3xu5N4V4GxGCxdN4aHCa2UK62W7Y6wyadjgqpt3kuNLZWaqq0BCI1gqF3gyJtAmiMIFYhE
ENBksy0wrzeWxN2mSt2jYayy6nFvsygHZhCfHMyPdLHwcHdP5HQsmXTvXLMZCswdsmmCzSWmmDIb
66TnUhwnCCQxKZNG3VqXm2Zo8qQzg5tJM4sIfYdtMDZSEy8GVXApoLFZRNoUxU5FSM55XRhC/BOG
HXLtNJUzndwyzRVg7nQhCsIT4R41SSceVOd2JE97QfC2yaOZDGPCVncS6tozrVPEnV8HbfaQWBa/
PvkYZ29e8CUCY0gJFQSCDYuZixNQsZ3nD9L8Sfbw92N/aI56v4zp799/G/nRwT0ydVRio1Y5gILI
Nys6pSOPEvzjMsx8g4NMBBOn07ZHWI3pMyyGaJiW7MmN8rnnC432JRgY8ttSxna5ifsyhq27xRG7
NsG9x8XU8VI1r0wbT8X8JYIIAJwFt86EIU3WaxPke3g1RWCGOJGsRgR3PVACrsZoTIzb8Ptyc8DY
7MjrvgTDdSH1tkaOAKlDkasaT2XVNvSZ0JMXymE0sKMZbAyeX/P4hqZnecOaMDElPrQy9bQE99sc
9z42Z6JAbbOfL31W0zAQ3MB6EHLJ0E+WbtLYUQgMQgwzgL5cMOI3oD9bjQHT9yu5nlxjliRpV0+Y
7UYHgcmMd5x6Hv1GNwNFuCgR1puWXm/WRz5kcc5PCwReU3qW4eTvWVtl1KxJMw7uJIdLgquG282+
EeZ5Maz2O+N6q+ZHHM7katP0tcd7hiy4rhweU5RcQRIYbBe1BNlclQNzxqJxRUYSIUIYHFxfiy/V
BxzTF3EEaSjri61abWUECAtuIiO67el4RL0lYte71jOeU1yt1+mFZppmkELkbSdOfbElYV2seRDF
26oZfHqaYBjP6lBogaLUFgkDOrYOQVHjkoEGHDMcDr1VuIXNvhOPjdxgQDrKFekxxj26cRUAUyNK
7zYzy1qjpoDhBh0m521yM7D1hyNHgjmJoahwSQWKXpgKjgsB2V0eWAkE9Z7dz65AiXCKHjCReacX
TdZB4emxkOhL7JOtGEL6taCxlMF9rHDhaoTiMDrLzFd6OOkCcGWHEwwBA1CDF+yKDdKAx+mfG7ii
AcvpxvrqX5Fb9PQbq+WcZce5LI0V6+XfONRytm9QWEt2+DQlc8Z2mNs5h6gfJGr8TXoQHOFCWCjl
rCoewvjfV9LCS6OdmfhC1ZkaOdTMTHAaqB5vMq79XFvUOz+HLgcP646MDXvnkwPXlPyi3EsXyu03
RPWeLmBC44jZzArIuFDiDtbf9E0Ryap7h0zCM4uhMetbzmWblLfikaJ9cLNazQ5gn6/KD/vf7fTI
ly/CVDG94kgIUOWp882SfVtxKRtnf9mlmm9EdWxW+e/XyDkqVt5MubXoxXCmG615+ihxVhyS2D5w
/Do+W+6FSSsWLPvWoMX9BT0He9ynQlCkkQ03jEcESAukbJotET6d00nAy5hDNPvpuqTmek02mRRN
sjNpsufWHLSfLTtQacD6mBcBjM+ZEYqPXRUxvBh4KwxfgYwXzL45sIN079qIJ+9R14ytT2hPnGZg
Hdnh0HfTJtiIdaMdpzf3oMeKpu620ElidTL0g5gdyKwPoUVBoRSKQbOSKefLEI5IClOXDEIZKIAj
f7Zr4Qsyi9tRSyBhy6rDL/rdmHLpl08Qr9iOyGww2yKFOVmvam4UL495/QzxGYgj1a56dLaphxmn
wlFiETf41omhSGQROOOCCfCY4fvV6fHu5MdOHCtLjTrUfg+Z2F+y1QZpf3y1gEUI+IBS3n1R+sud
2T1KgRXkW6x8iWTge/fDqgSQ4jkgGfv0G4sQZso4E1qjA9i2itJRGiCLzDE8wOZ4z3pOu85La0yc
m+ceKRweJsUGuBsyTaDcrYyiQ6bMPt3r6P3eXO9eBKrWnu1Mx04ZcSiWltqy2KplINLydaLToyH1
wd/sga5sozCE31i7DUFAcKXZSk1elXaEgST35EsIJZJBpkBedYDPjWngKfksKqvrBEDj0QZjIi+p
OOrjCYoOg35FJxbEkUfyEBiJIkj5hfEn500jHRxrKypnUOQTRAyFxsLO5EiQ4fS1hxNkAZSRB38R
i9VGOvgZo5IF4Kg4v6g31Q6NDmWsujI5pcGRRhobdRRx8FVr5HeKNiYSnpnVKgpUojpN0GwjDC0A
zflV8Ies4TnLapmgieFJiiSQONsxPGUC5K7oIueTRRK1U8cwxGLQxZVrDl+GYMRiBmy2HAfHGfvj
R+hFA7BEMtkkD0VgeIK0KzNoF8T4JrjmVvz0/nvAl7huHg+x8yVW95vHR+R97rj2ET0Kdvr5wM57
kDyRRQiqKfRIX4+W6g+KAx810c8FkPRLjEQiSA74I693QibP4vvAyE5CC2LmIITsE5edzMQ7/eQJ
+7PrErjq6DRVI6KFB5+C4NqsJHkYmgIWBVlUDx4YOHCx5XDiAFy3rpytbu+KdeAONxZ84UJfFvvv
ZoCIuw1rOOypHZ4+GuBHvaONoAO6Q3pHstn5q4yz70aTjGHm7l9s/oa7KLvNnjdoCt53MIOyVt8J
zmJWGTS4/Wb0IDrXFMcI6ir5n5CWTZ6M+k7M2obFqC1Jmks65QrgO27nnuN8b8xjtVroOu/1+mrn
PnqY52THLA+Mnc5k35qeQaetoKPg2wPj+Hw71pg3Yu9yNbQSQTKDpho4NKRN8RTy2EQFD69KxY3L
9YUVpXm8eB5GJ0bK/D9MYERYKA0lFCvr5QSAA5gz5AosgOkdpIMAiAiuKl1BQgOq5kfJVJ4cmgH3
ULPfLdspgDtyQC7kdK9CQScw6BPoPUp3sO63F4XXlaZ1yj2AA9oJRwHTDWa8cBflXDpMg2Hb8VdE
S4SPNAlz6pvqve0RBXV/IdXbs8tFgHZE/X37MNHlrnddBoe8Fb/L3GtdsGORwG4H3sCUmklW7gyK
U+3hJEMoYlDD6Yt5e3hnM8imZEe4093r0+h+d3PePpu4bvO/n+GIh/fR+VwYoB21YTGSVJiW0Bif
HZpwIfp3ZDTCThCosLuyCmKIFQZZYFsUFII3GP3zanGmR8wwF+1hml814JRcUt00391Ip06gYGYr
7FlndFkVaUSoFE/hCCSY1lZMcjSMs+kCLsOLhALRuHGfWA+NgkrtaTgAyCnfZO+eMsP1W9zKZSnZ
kJia8HCdlcmBSKhCBlzv0wcnmrsK8fK2VlcgS5NGuHk5BQhoZKwUCBgkJWBCYiwA4SGbOFl158Gj
BB2ZUocKq+yK0jhYVwSltLVN+eobzo5sX7cNs57nnJ2Lm5jKqxpzOysI9vYHg1OTnruZZDlmICjD
BqAisYqR2cnRrYckcwhhBla2ElVrmWV0Kw3EFKbiFwMyLpECom2Q32dBcNTp0ySna1hDRxzZ79de
PEOeuTrvD97sfP2Cig/bHtkqJ6NVUQba2ntcEQRWYqURipWFGVhS4zLcmRWC5cG3O8gk+6frZNmu
3RxvnoiMkEsM4klTR4yc6lCdcSUIcB8gYv1pCp+ZKMi0bGRSRZlqwtKxIpiFBWKiiiaLRxaMySHv
ZCJ5l15CGxgiAsIoyKuFqoApAVYPeyVgsFgsVQRiwigKqogIsQFigIwixEWLFiwxkoyRYRZEYsWS
KLDHIcDncTtc3OEhvFKQPQ7ypzbxmYxrUqVBw6GydmBONl0xixYlDimQuYi8pKiamWg9p2lB2FNM
FERYKRYsJo0R/Rm5B1wzfiYbPzUOOICSLBRGAosNxgE4xhTR8NZgsV7VQjUhUTfaFzFmWAhcbALI
vlcu7Ggrpq+g88sXRQF4pEhhiloL0JEqRsRxAGDERm+tzue6nZPweL5qQj3xgFu+/bNU3laFOy+y
9T6hPvKKOvxI6tlh37VRNFPxOJHghVYfuH1K9Ct4lfX9Zad7sk67yhU4KUkwd3yBE0aHEGUcxSqC
hiQpWnNJBoOmieThRM1yIQV+SMh4BPTpdEFJImGHSZwh3f0eERwGAA4Z2e6TOA0RO2z5XVHDAiZY
tDO/M9kTNmCFBxUegwe4wVpgR/SuO5Foh79t9Ne32yqO6FR3HBI3RvEpMGlzNTXtp588uWsYHAyv
ArZ2ZLAnNM0RGHzO5UgaDxKBbURa1v+EcRzH34fK59I3AsjjkroCqpgNwUUgloqM+XBAm46o9v6/
owgzEeLELjn3d5x6iAlkEeTQ+1P85R359ovGDC8LX82KmB9J5gGfmd8QgbDwaSYz3u2kkZqBOrDp
1DeGk/Ub0dBtMMy/iN2JOZuBonQhP2EIdHspd7DA3n4t1gglgwoBTW+3g1pJBThpXW5UeY2NL82f
Y14M5sS5tENJtNpsES18+VKnTcsz8vI8YUse/U6/ObZv3QhdsuQ4aJNmdq8wd6RwdC/ywoGvn+ef
Hvh+o7xKjg8OpCV4oLXmiZ6puUD6BU9GC6p8MA8fGG2gGUCOrb3/X0/KoSB8yvfaPyyuRkQfwvUL
Ikb7lg8v12ahk/MjwsexzquGw144ChXc4EDuYcTAe6kRnt9S1ZuciV8iwrgLZBsXOOIIM5QTjXv7
Md+cdhRwX688gcx2GYdNtZNeX4OOQ7bpZeNxox3YWec3vQTN2oyWjBqH2UXjQSP2SesYUqphS/Lr
GAqlZh1cJpcMNdO/yDk1O+m27B5nftA+6ACG2BWm8Jfe1+b090cgxAYrcks0v0pDF17t7KgfdUSK
GLhncl6I5SL3/q8tfXkHg03owR4NQTREgpKgVgAsYIsPS4YBUDIxCyAU+Dt3onm9HHlAPZbW22IJ
BKKUDHuKCEQSNedu8qaIQ6P8YelUqNU/CkwPYoCDwWFwU01ymLPX37H5wA82KRSCDAWEFgeiBPik
mMWZaLIsgCkkQZzq8Jw+AO836mE6sLxDnhjiVje90teCP6qEGK3yBmoooGIlFzkkXaOFnB1aSW0Y
c2aAIYurpi4v6V6Xf6vVcNXzYdp5FZljZ9/PzgF62klDpMRxlKLwllC01ysgzdUC661Tg+WjILcE
ixHIzbiQxYhy40YkhHY1j56GCMGEYUciDSEIYnlGduqod2GM5xwiAj5A0vmIK1bCFqm5E5827GlD
ARaiRdD84IGhEbUbsOsPHksxJVHR00Dj7EoNk+3mUBeIdTVOUh/D116fVPJKcqKXHTh53ZcuFsqI
C5GQb2VMhwENqKjcgog9ontcHMFVUGKCLBiCRrRBRi1jmWst3GLmJTZLiAaNGhQsVfRudy5DFQ2E
T2jdeAeunA1MdEbRhBIDdhU4Miqp0mFG2Mp0vWV3ZNTBHyIPuIxfIGNs0QhkDP3X2a1gTFaPm+Hb
BVgoGZTJ4t4bxaqiMUdbw4dJMZiRyrjDDKO28WilS6sgzMUx1ZMMs1low0josWqSmxtxEQ7X3CrN
HAvSv5mblHbtyQSjO6IjMKWQ3HlEbNPKvUeFZ11ZWRaP8ED7kUKSyASPkeVtFXubZJWB8GV3kzJF
ojctca1FKW6kV7o7u28z7exDVvZO5EbMB6XoZS2d07Tre8QebLtvNoC/oQqwUxs6ahLrNYtSAUzC
cDUiAKAQx2YY4lKFfssMqQY9gBOrKaIgiB9KgI3A43mA1phtwlWF1XWdpcjSC/Dj7tF52MOYhQHE
bJsJ4x3L1WAyx8z4qOY02a+Wuds3cVHWMkHZpd13C4vcIS5bYtmut0CM/qW8rXo4X57vw0DZ9b+c
i5dEX53AokY2JpppsZYdxBwNJ7025orDAqEtonpZmW2hEtKV04fptn6tb1oUeWcuQRawqIzRTjnW
hVdWoPDeYjTSNuOtBk0XSA5kmXMwsNMNIYwWVmJrv5G+5BxBZH1Xk82FNL0Mj9I0jLaw2vVvBtr4
tjkQr+rrsewNLe+V80dSn3agUN0+6nkCnNhQp74JPmaKRxrrGQWYLRtkHgxc7v0NjSJU29/c8Z3B
EwmdD6vqpgxBIoEaBJ4bWUGmaHHkoMpLzG1uNRlMwBp1V7b7+fqKGtrCz+EVjxkGjuaXsNZ0QG5C
xboQ8lHtbEIjIS8DjzrHHMMxjQ5Lxk1jaJRoaQ21gsHiOMeSC4wtc/EZJ72sgaNGkljAMbXd7Cho
SWrPTChnpnOiHw7WdodiWR8Rpx9TnFp3k/LxDYhundCpwIdYZuGFzw5jq0P/bSLmo4Ybs41rKMu7
bZXAlTO1M3fFJQx+Pf13h8qVjql+rMwdDp4Ny+RXpMxrMh3RyBRmmO6sMGYyqKh8zhmxuSDUMLhB
lSF5MM2eOlYMDHnB2HDdJQzrrROwTmGICwWFPhodBxhZiIK7oEWQZJJ5wkDaSIRM7Z1lo9Fl8DJX
HhOzJNpDnRSebJ+RKzXi9uYL3e3Y2m+ZNWnNvjRgwEyAWTbHLJm2w+aFiZsySEds9jURFVVEFE6I
XiihyZhBAiOFi4B8CM0qaHJfETSywGcC22VPPLisVp5OMN0zPAwzbaXZiVOBCjxBIULYotMJtqm7
I7pYDKsIIrRH1VYEshO1TGdVg0pg0wpSLRqyKA2e9trKo3jWt6pZsytaOZgopPpe27vZWNrZixec
0a+q9OaCtti8TWax2mTVpm0FaJJoBOE3GJUWrDIiBmkEzhipGCRiCEZQGhUC5US7siFDvSgOCCgk
bCBbUmkl6unYQI0YwdSIAytUEQQlk40WvOBnLhl2u9Zec3qmm0uY5ZioVBCK9Zdez5ZqI/Gw5ZM4
pUHL/Ch3TIPFiBkQjboPnAw6xTxbqERKqJsrKENVGocQPJk1RatmWCohHF6JVumKmxYZOrF0O84w
1a8IopMcZKJlqjUY3VdFZhf8m9B6pC7OBhxhcyGMgpKw7sm2FQNM0hrLA3uypr4tnCCyQ1uwUhXN
ZcozSTXF1kXeLNXNFV2tA3Odlxqb4MMmSkXU4N61uFOchtzvOPc9M2wTLCtjMTHw0ZpsWKMFeH2I
8wXEVADjsuAqjnPqztZUWztZAyuUrGkL4ipMzVwsXkoFDQu7NE0zo1xUMGBm0koEFkILCYkrIEMS
oRRZAqBUkiogqyBYT2lrlqHDfXImZDOKSwFMAoUTr+jpfY4jk1zMC+rfEP0eNx3hN75Rm8y9263t
g2dxzZne0Z4sUoGrVRYlpIztIM3JdXRCaiGtNs41rDWSYeqqoKUN6opCGj6mjDSw7PVFyZfUby22
LffnATTBSLJ9jWSeVqwizsJO/BDt9Na1wALM+UiyCj/asIZz7OIcys7COpZLob7nNU0iwqYVoxuU
McRcyYe2IYmlV9WKG4gYoiic4bgyKNsMMqIoKKa1TTWYyaFtKixBEQdNBQWmSgYOW4TlqC8Cjv1T
U4eQGZIybTVkzBfk71ozGIk2rBTWsCiOefjIGcX4jDvqN646O7FkmLBrJrOzD0YfPdOzmUbYZrAc
0MzL9N35n1T67x1havr7bmaqmkaMMGRqSkoYOINZKP5qDnDTQwOBDFZD99JdcYcjUN7JCzaJ97ht
JsVmxoMDzuQSb24kMPO5ky5rrM4gNLwhSTdk4gtfGCchYuS6cSXGiZmZfeyuDKzfNL26xYmUi7YQ
6085HuWYJLC5aFeymWOxEKSCC1uJqmj5+NpRBfS/0fevltuSUv0LJLj70R6l3VKSH0/EDFxWSO4Z
y3O3h6uwv1ZLhiKaF7kGA8nH2eSBtCb1Yg7evx5gjT1Ct67efQ+5o5NH2+CEJaNAB8NhQjkyJ8pK
B8ikWDGKCyHYPU788yEDQh4sjyEW+z1uFyzA4YNsf1K76Gp0Dnp7JBWJtYg/pIzS/GQn22/Cr/hZ
hmmvZg6J4vsg0o35XDgglEbCa9DNQ1q0QwTiIGRnwLqjAQw8x58o0uT2/ZYfadQOAySdeKeNTAcT
uwUOI1iyRZO8pQWApFkGRIKe2bDaJiZFBueukcuG0J8kScCUGxCM2qsgbo1SzOyFGthMQh+7xveh
Ic5cFWghWKfZ2BYn39/rJ4VU4tMyvTKwrA7MDs/Fk7Rn4DQfEnA/hGoeczW4JYn1JNOLO1y9GHUa
yPEe54jvEMYx8cZ2zbQi6yC7uhE5Xtght92UxkMN2heUOGHXRzhXQzasTt4rdGmRsuBpjAbTncXy
nU969zEekQmTBHO2IyI+89yNa2R/ctJEDMaiorwP5LwF8aeshdEimRTl52MKJFIW5Fq80CslPFR6
oD5J4k4b33ShdmiWUM8/IqUVbnKkK90qflizlg2IeCZCNYp55UTJr1ZKNU/W4MlY87Ja8+mQxsaa
8XAwGxthvEPxI0O9QiO/1nYy+U3P3MAhpBy+NU3CqgGzeLZ9GPDwISsD36J3YS6kklCgUDBThtPt
COviPYagfx6LAwIPPf3nlAHYcU8AvL5evdySMMTvEs9fstStp6kka+UI8GClNIN2Ipj9OaR2NM/g
sanU4RzqAHMECnV4nitlobn+LLj4/b9/1kkWKKCrCKSIyLIooRUkvHf3nd8vNZppWg6MPh4ez3e5
WbXcwiIhjY00GDbaVpR11N35Z+DJyfBmmU9YHlGHuErLaLFRQraz02d4fr+Z+N0cdDO3Se9Pofh+
wPS8bd/Vm/bryiZN+415NUG2paWwEKqFFVtlT8t8ydu4Q61jmGJOJ6LO2t7lE+ed35WijHjdrrUq
ffZtyS7Gw+8xPV48r/RS9w3m2Z50SSQwG0uRTTiFWhDAwMCpyintBT06S9yBBP4St19gSR2I+TLc
qAX5MyHMB63yeJioxa3TLiK/JWtDVFMPv/GFowNrkPb7JSniy5aeCbM0QtmOYHZNxXKjIuWM0Cwu
Ti0KfwIFQK4WhEg0FqER6KrbFFdNg3wQWjMjgGG6vfKcbmrx00gW40xl1cYM8UqSK5lA6ZJruUyD
IzwcmcsziTAwstBSRfceekBGTovTTGLRiwLDDGihLvMs3PRDv2p0MO0e7NIdJjOEkANM/AkoCIzw
dZDLz3p6eDQXHilLXjTA+s+dJIUnLa8oMHDNpcQkmfraISYBZm7DLMyU4aaSVxmOMKlkYMEcNYVA
xXSaMuCLqmsuUppus1hWtVKlFmaMuWZHGsmMKw9mqaDTW5hUM3cMtaa1hqaraWOmoYwaUs05hcy5
VYW0bRRsxyuMxrWQ02tYoMbZg5cMJgxVdawxxMxaBUjma1NMwRY5YFbErCsMuYTEMQi5/FgIFIJB
QGWfe6Qh9KgfMH3TGBiKzlTz94+Yt6QxYVsoevJL3weMpAFup+iFL8xyi8YntcrPUz99tru8A8PD
DHg4G4dmNt/XxOZ4de/HM3ZGhrSmEws0FzWUGRQrUqUQx05FEUIiwYGm/qu8s27zWtTSadEFkxzC
uJvdUNWz+64KqPFrK7SXgpRUF0iReCyjC5RMKbSY6EbYUHRlPYm0NItTRbNpgFoLpWiMt0yGPGsy
Yhg7KlKWzVloso2uWrD2E9GveohC47YNRUjnybaUoV3BxBL8i/RcNMgVybG7FHiqPF5pMGDytzB3
JWcIgUColB9oVPIrkxa8ssqRkXgVhotyv9bkrBjpJ3F75MigLjFPz62z1kV5D7EQA+pzdEQzSbaD
UdnG0EB+yMa12pb5o4YA0QmmmP/9OzfrFuoXxj6ZlmHTdtA5JNQMUBUy5xA+RAz0njpSGKjEvgtI
KPO4dg5U2aci1G/X1At+S5ko3S8Ky34fWXWYMBRY+ywsYnlZMjCYT0yFRMCtEtbqZQFMi0O5Ey3A
SJMSZhlzQ89kj9tIB7fbQ8Mh80iilZRgCikioiJBQUA8S5ynwD77CHXIfH3SecwXLc80QqY8CvGS
TeVp57B15xS8LoW13jWDtyHbaJ7yr3MJlUqebqfJNJklRpN5YErKwrFrLZZiLiVxWBiFRUSKIxMz
CjVka0YTcIyGMk0y0qVoi21tRaIJbq2aV+mEut4YUKiu8LRz5B+3O0k+1PeMEGcz5WfEprruD3R8
ezWvbtn2AjbNd0zcK6ulHALFTJipKsWcUVXWoJ4M5CReAVCDHcQjQ+Xq3Hh5FcfKMsfzMPzkW6Qt
6fQxN01I/qdjggVjAtv6WYFcan3I/NifuCYW6UNIwwkzNyHJYoOnJCY5POZVcoPBmWOXG9jLOG2O
7J3tzsbtOkvA50/5qdqoAnClcsEThpTviy2tsnuIGNakDY/HMovsv2tsdfoLHKr2dteZ2GsaeKl3
GQRnLObaZqurEshqcweVl7IyO6eYkFD0idg8OiYoPmCARZlxKATJhoh8cZ3r1sMtRoetPp8YTW6H
VAdxuhLK4imiqoSo+OYaU1Ar62EzxN6Q9FzHpSPZURjEdu2BIJnU6P2PgoCJ92qjBdJNZbGONlQ4
9ND4uu9nrSq+PPyeyE7O3s4Kh4hlYtoEwoA3L54bIL96tZyGFgfJYyaBLlVbMWBXJuoo1zdevWdH
18TRJFwuH15yIDSlQXGctIPhrPcbDg7kdMnJOcenWIJb64djGk7Tv6xrBhRgLhZJI7jadME0Uimi
aUGGSXI3mZ4fSW4TbqYIql1e7Dk0jrS2QBnOn5+Tt6Q3ba50Nkbo1kZyNu9u8C4966bd71lZsS96
C9uEz68vGSL+Wj3AzrhgyZsXwm646h/Xzblxka5YDnSOCHSPLUht2HkyX75mZ4fOWFqOGVmDLoul
nWITBnTu9hzvc7ebJzKd5VwQ59IPC2WNnIobFOp4iI3p/fOi06pi0rdZ3Ts3mQjcrdcbSDLZyg9V
BlZQQZnTl0m2meO7kLzT1gKbaUmeDCoD6WHGRaTHGcooe0Jpp+d0QyDW7nOzo/Kgp3eHjapKoLYy
4ViIenpsTgJZeUi5pmuyMChG0LOHwhy7tYFPIiFkmd5ssgyt8L67mqMDDEWJ2u1IwahKW6grkM40
vv8tVBkHNEjZtU9jsfraVKEDhaDaBsjSq3EwpQhSQnY9cCWuAwWVtw1uMVCCsMKD7myGcVgFoQDM
sUUWVzB6qCmKXi6qTkMEMZDWaTQl0GC+loD8WIy9p689Z414HRbGV4KgXTGWKnxmsY+pEOTt17aQ
R4RazPdYXd0R1QNosFgeqERh01gOY6ZoNWxaEvvyBt06Zunx7ccanFOxeV1rG4aZrbeOMRxqlBtB
YTLkBCJlFESmgGxG4QiQaEMgcREBngRi8zdKAoOzgAwCgUWxSoS4QqzpFnWck1Y0yRe5Q0iTK+l0
FJXOiCZE41g4xvboNxY5CmibOkXd3A7+04ZILoy67TM5liqWlSzOaYM+S8WQ7mYXOtAFkfh2Nk6R
JyetNoJDYk/Ahm/KgMaakYYPnSz8IVVffL0oDBumCIDvUcssCTCRxjAkfhPOqm6GTHnShPWUMsWE
tAMmb2EGqinsXpsCbmr2rXJXxC5mxtIXYI0BCNhuCbkXfsnD2vYma6UYS1+yX0/FJ9pjwNqtVym3
O9Xy4mNsQ234B1iFLSrmJvipUNpw6ug/HGGa4p3Y5d3ysIRwTWgdyxJlZ4bNQDvCIYU5e+JDENAh
ikCVftEYeWWLRXbOSNxndi46HSCEX1nm7O7yHFnI1BpwXdAOWxayd9w995GePNVgOeATeW4Llm8f
sFi5E1WJ1kNRoRZiKh7UAXcVMuseVD3CpU1swjMWGVsZwxUwGUMft11p78oQwToKDnDvlmIWntrh
t1FTVPxWSGvFmnCxo4eIlw5DFWhUU3JwjNISatZK0Q4nLJraSem1y0Pqx3nnVVI4iPTYoPwSJhXB
eG7WLNYTgHDRm4VkiZtIusIZF5iAHMSaYI0sYkjHRRAOGCfBdohjwV21BF5hVW+1DYpz2/ksXF53
UEZOe3uE1vRcQEMssMCCbLETe0Ml1kbZ3jUBjVQ6y/V31k9rZo2uXG2MWCa7/TjU3rCnbwWBVTsi
IsDvyWGuDszDWimcbOQeUuusmTXFFFzKVPBqqMy7Zi5Yg7yi4ZT6vZmTlb4OZEJyIJx8ZKCBxE6Z
iCdgjMoO6g9vlzUGHYaVxLaUEp6YuRcRBV5T2ZMJjCMSOi/fjYEV0L5rJGNeJcM0XmKPBLgKyiOj
jCOIIhhZsyjBVcpwmC9c86zODU4Lfn4zOkl6IOU5enEL1J9OKVkeadAh5gC9dHl3kPRUKk4QKyRW
vpj0GkCIwgH1tAW3hIBfkxJejEXGI/ewSF0aSD5mHl0Pk1nLYxRSahMSoeiE8kkO7wc2vqUVnOOG
DcuMbczM6zWgkns4nG/XUm0jno4AwIazauTzKiQ8JOz1fg5IN4Ms7G2mkMBl1qrgjRpjG1qKsweM
zLWjSO+08znDnKXR41N76LJZ3TswHLJp5TVSmRKyaJqFmzVxVnCZAbmkRZA0hxc2cZIsEWDTCTMI
mcla5uBuZocnBFbEkKsUJi89l+yn073jrPHOdHpJyMAAUJFAFgqBaDEbjW6M0Dh8Hqyz303yNbwI
0bGycBHqZzTsGxCDEmbPCCtAZRJzltZuid5sOmFa/xotaKm1QPSprK7V0BCTQwY/JlmGIHN7gN7E
gFZI067OJ9IOyVMEGFLUOWiaLGIb7mmsEIIo64fjYokXiwiw6YbBAMZULRbNZcLDU0ZpTnsevXQr
37sobMjMiG4eshuasdGfchBKpeHKEB3q4jneBatDaRkzd2YWZTSpyx84Qcur0RN2t+dN619bqy07
W4IWy1thfRQgBpFJz08gWZ7uHb+7+lpUTaS45ZXnZfhpm56WiT71+F6R1Cw9XP2FBYfUeWcRdwVB
FUjD8Xy2eEfwVs24rstUOpvs7mC5fOVJLGIQFhD6MfgMUOAIA4oSPXIe3UWv2QRQtpRLOU/rz/f7
/3cL08y7B6+XyLxoAXl5GOjOT9uXiM3PBTOSgPQuC47Xu0O8st6bk/szittc2yDwnfrR0A6NWAe6
hPWDJmfSOzwmgafijoEyIw1hNdZCiW+a/T3UbtAfWwAkeMoI/dOdC8fGuMI925BJUy1Q7TEEKGd7
jfF2/CjJLvwxoyKo1OTGRAER4fl4+lz50+SIPvH2J2yhm/bgegm3T6udWr5jiYednqMRVQVREmMP
yvyGPz2rxr3mfCD5Cg3n8O8xuOaKoUgoT0Kp4evLmgCyHYYIU10RivV9zgxVkLaLbJWDAVVqSsZM
QxnjAqGbZHhrhdsAhUW2S265/FhZebNVcyIFx04zxHJIpDtruJ6cq2HiQlKhMuKhJgKANw3eUINO
YRiM5GGtVEP0tErTGrlmYXY5+rezhhWu2l25BcKcYSsEUrRjcchdCa6Nkm9ysb+9VLsv0C7yTTAU
qRRyWmNOK4G2+NliIvNK1TgEkkl5ItJC8X+vMZCFZrGEIEYcCD6mM1VrcpecPid5gbeiw7UzjnWa
OC7HdNSgotQqiWMrIIgjI2xVCoo/t2aIYwl9h63r82pD7woRQFARkefh1CTurIehFEU7JAO1KdT4
0Dp1IkcglikhPu0tkJP08SnhADm/j1o6iw+MG1ZygR9jSw0ixgBtJH0PAB9LsNPVpRSQnCHZIsJw
BVX35r831bVFx+mWILD0YLoHpIbSGmBK7dp7rfm5nwvuEMUDq/NspC0pGc/ZqFJPAsx93lAO4qy2
mQmpFA7u2yPuOM0v20HN6GV/HWSPvLawsXSmxDQDYONlhtp6NBKiRg02k0MJGjEgySDcdaEJpMsw
7pEgnk+xxhGAcqLeM4s1JQzKxULphTh5SoUIBGXgSEnhsKQnRTC7anBthLKkITO4ZkSRNtVQJ/bB
Xg3ltJBVZB2wQwi9kCG8vYgHBzFMebkHXpk01QUSpEEflQotuHwCCz7cOyO47grU+FzBpYUSzvJS
ZyCSHtNiEsmPa+BS9x+LfU9bJEe3QWaAwsiTD8qJPDOOeNU1woLZjRnfpkIsZK413eNkjZJAjVHa
4ddwNGhjA24t0R7mNjfD8FQuY23+P8/Wqb8dzntM8qLSOeyoYu3Y+uypRWvo8YSAP70kCQv/4IEh
f3g00l9VBZeOPZBPWH445D+dQ/qZUVBktqqRbaIijbYqqlaMFVRUtLEUltGLaVGxn+r9vfo2+/17
dj6cwDVg2v6GDGIP/MXtn/1inT1PMeM/1U5Zcvy/hikBEpdRLod2IJJDqFQEp5KFLHaCHHnBDQO1
xCMXyXXqX7gBf2sQkKVLQHe02Gryf9zD7WIl3favGQNeUIDRiD/44/PVhDX9lA/OyENMhpPx832i
STwgG0AALF0hp/F3JFOFCQ20IGgA
"""

QUOTES = None
def get_quotes():
    global QUOTES
    if not QUOTES:
        quote_bytes = bz2.decompress(base64.decodebytes(QUOTE_DATA.encode()))
        QUOTES = [q.strip() for q in quote_bytes.decode().split("\n")]
    return QUOTES

def get_random_quote(prefix):
    quotes = get_quotes()
    n = random.randint(0, len(quotes)-1)
    return f"{prefix}{n:03}: {quotes[n]}"

def delay():
    time.sleep(0.5)

def tcp_server(host, port):
    class TCPClientHandler(BaseRequestHandler):
        def handle(self):
            logging.info(f"TCP client connected from {self.client_address}")
            delay()
            with self.request as cs:
                cs.sendall(get_random_quote("T").encode())

    server = ThreadingTCPServer((host, port), TCPClientHandler)
    def run_server():
        with server:
            logging.info(f"TCP server started, listening on {(host, port)}")
            server.serve_forever()
            logging.info("TCP server exited")

    threading.Thread(target=run_server).start()
    return server

def udp_server(host, port):
    class UDPClientHandler(BaseRequestHandler):
        def handle(self):
            logging.info(f"UDP client request from {self.client_address}")
            delay()
            _, sock = self.request
            sock.sendto(get_random_quote("U").encode(), self.client_address)

    server = ThreadingUDPServer((host, port), UDPClientHandler)
    def run_server():
        with server:
            logging.info(f"UDP server started, bound to {(host, port)}")
            server.serve_forever()
            logging.info("UDP server exited")

    threading.Thread(target=run_server).start()
    return server

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT
    servers = (tcp_server(host, port), udp_server(host, port))
    logging.info("Press Ctrl-C to terminate the server")
    try:
        while True:
            time.sleep(1000)
    except:
        pass
    finally:
        logging.info("Exiting")
        for server in servers:
            server.shutdown()

