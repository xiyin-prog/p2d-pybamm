import argparse, os, sys, warnings
from pathlib import Path
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Wedge, FancyBboxPatch

parser = argparse.ArgumentParser(description="Draw P2D article figures from final_data.npz")
parser.add_argument("--data", default="data/final_data.npz", help="input npz (default: data/final_data.npz)")
parser.add_argument("--figs", default="figs", help="figure output directory (default: figs/)")
args = parser.parse_args()
figs_dir = Path(args.figs)
figs_dir.mkdir(parents=True, exist_ok=True)
data_path = Path(args.data)
if not data_path.is_file():
    sys.exit(f"error: data file not found: {data_path}\nrun python simulate.py first")

CJK = "Noto Sans CJK SC"
if any(f.name == CJK for f in font_manager.fontManager.ttflist):
    font_family = CJK
else:
    font_family = "DejaVu Sans"
    warnings.warn(
        f"{CJK} not found; falling back to {font_family}. Chinese labels may not render.",
        UserWarning,
        stacklevel=1,
    )

plt.rcParams.update({"font.family":font_family,"axes.unicode_minus":False,"mathtext.fontset":"cm",
 "font.size":12,"axes.grid":False,"grid.color":"#e3e3e3","grid.linewidth":0.8,"axes.edgecolor":"#444",
 "axes.spines.top":False,"axes.spines.right":False,"savefig.facecolor":"white","legend.frameon":False})
O = str(figs_dir) + os.sep
D = np.load(data_path)
CU="#c8794a";NEG="#5b7db8";SEP="#b9b9b9";POS="#c25b6a";AL="#a9b3bf";ELY="#dcecf7";INK="#222"
BL="#2a6fb0";RD="#c0392b";GR="#2e8b57";OR="#e08a1e";PU="#7d4fa0"
def save(f,n):
    f.savefig(O+n,dpi=200,bbox_inches="tight",pad_inches=0.08)
    from PIL import Image; w=Image.open(O+n).size[0]
    if w<1550: f.savefig(O+n,dpi=200*1600/w,bbox_inches="tight",pad_inches=0.08)
    plt.close(f)
def blank(w,h):
    f,a=plt.subplots(figsize=(w,h)); a.set_axis_off(); a.set_aspect("equal"); return f,a
def arrow(a,p,q,c=INK,lw=1.6,ms=14,st="-|>"):
    a.add_patch(FancyArrowPatch(p,q,arrowstyle=st,mutation_scale=ms,color=c,lw=lw))

# fig01 sandwich + porous zoom
f,a=blank(8,4.2)
lay=[(0,0.4,CU,"铜箔"),(0.4,3.4,NEG,"负极"),(3.8,1.2,SEP,"隔膜"),(5.0,3.4,POS,"正极"),(8.4,0.4,AL,"铝箔")]
for x0,w,c,t in lay:
    a.add_patch(Rectangle((x0,2.2),w,1.4,color=c,alpha=0.85 if c not in(CU,AL) else 1))
    a.text(x0+w/2,3.8,t,ha="center",fontsize=12)
arrow(a,(0,1.95),(9.3,1.95)); a.text(9.4,1.95,"$x$",va="center",fontsize=15)
a.text(0.1,1.55,"$x=0$",ha="center");a.text(8.6,1.55,"$x=L$",ha="center")
for xa,xb,t in[(0.4,3.8,"$L_n$"),(3.8,5.0,"$L_{sep}$"),(5.0,8.4,"$L_p$")]:
    a.annotate("",(xa,4.35),(xb,4.35),arrowprops=dict(arrowstyle="<->",color="#666"));a.text((xa+xb)/2,4.5,t,ha="center")
a.text(4.4,1.0,"总厚度约 200 μm；长、宽可达几十厘米到几米",ha="center",color="#555",fontsize=11)
# zoom
a.add_patch(Rectangle((1.6,2.4),1.0,1.0,fill=False,ec=INK,lw=1.2,ls="--"))
zx,zy,zs=10.2,0.8,3.2
a.add_patch(Rectangle((zx,zy),zs,zs,color=ELY,ec=INK,lw=1.2))
a.plot([2.6,zx],[3.4,zy+zs],"--",c="#888",lw=0.9);a.plot([2.6,zx],[2.4,zy],"--",c="#888",lw=0.9)
rng=np.random.default_rng(3)
for i in range(4):
    for j in range(4):
        a.add_patch(Circle((zx+0.4+i*0.8+rng.uniform(-.08,.08),zy+0.4+j*0.8+rng.uniform(-.08,.08)),0.33,color=NEG,ec="#2d4a7a",lw=0.8))
a.text(zx+zs/2,zy+zs+0.25,"多孔电极：颗粒 + 孔隙中的电解液",ha="center",fontsize=11)
a.text(zx+zs/2,zy-0.4,r"活性颗粒占 $\varepsilon_s$，电解液占 $\varepsilon_e$",ha="center",fontsize=11)
a.set_xlim(-0.3,13.6);a.set_ylim(0.2,4.9); save(f,"fig01_电池三明治结构.png")

# fig02 pseudo 2D
f,a=blank(8,3.6)
a.add_patch(Rectangle((0,0),3.4,0.25,color=NEG,alpha=.85));a.add_patch(Rectangle((3.4,0),1.2,0.25,color=SEP));a.add_patch(Rectangle((4.6,0),3.4,0.25,color=POS,alpha=.85))
arrow(a,(0,-0.3),(8.5,-0.3));a.text(8.6,-0.3,"$x$",va="center",fontsize=15)
for k,xc in enumerate(np.linspace(0.4,3.0,4)):
    a.plot([xc,xc],[0.25,1.1],":",c="#777");a.add_patch(Circle((xc,1.5),0.38,color=NEG,alpha=.25+0.18*k,ec="#2d4a7a"))
for k,xc in enumerate(np.linspace(5.0,7.6,4)):
    a.plot([xc,xc],[0.25,1.1],":",c="#777");a.add_patch(Circle((xc,1.5),0.38,color=POS,alpha=.25+0.18*(3-k),ec="#7a2d3a"))
a.text(4.0,0.55,"隔膜\n（无颗粒）",ha="center",fontsize=10,color="#444")
# zoomed sphere with r
cx,cy=10.7,1.1;a.add_patch(Circle((cx,cy),1.0,color=NEG,alpha=.5,ec="#2d4a7a"))
arrow(a,(cx,cy),(cx+0.98,cy),c=RD);a.text(cx+0.45,cy+0.12,"$r$",color=RD,fontsize=14)
a.text(cx,cy-1.75,"每个 $x$ 处挂一个小球\n球内只用半径 $r$ 描述",ha="center",fontsize=10.5)
a.plot([7.6+0.38,cx-1.0],[1.5,1.3],"--",c="#999",lw=.8)
a.text(4.0,2.45,"$x$（一维）＋ $r$（一维）＝ “伪二维”：小球之间不直接交换锂，只通过表面与电解液交换",ha="center",fontsize=11)
a.set_xlim(-0.3,12.0);a.set_ylim(-1.1,2.8);save(f,"fig02_伪二维.png")

# fig03 map
f,a=blank(8,3.4)
items=[("$c_s$","固相锂浓度","① 固相锂守恒",OR),("$c_e$","液相锂盐浓度","② 液相锂守恒",BL),("$\\phi_s$","固相电势","③ 固相电荷守恒",GR),("$\\phi_e$","液相电势","④ 液相电荷守恒",PU)]
for i,(s,n,l,c) in enumerate(items):
    x=i*2.6
    a.add_patch(FancyBboxPatch((x,1.6),2.2,1.3,boxstyle="round,pad=0.05,rounding_size=0.15",fc="white",ec=c,lw=2))
    a.text(x+1.1,2.5,s,ha="center",fontsize=18,color=c);a.text(x+1.1,1.9,n,ha="center",fontsize=11)
    a.text(x+1.1,1.25,l,ha="center",fontsize=11,color=c)
    arrow(a,(x+1.1,1.05),(5.0+(x+1.1-5.0)*0.35,0.55),c="#999",lw=1.1,ms=10)
a.add_patch(FancyBboxPatch((2.2,-0.2),5.6,0.7,boxstyle="round,pad=0.05,rounding_size=0.15",fc="#fdf3e1",ec=OR,lw=2))
a.text(5.0,0.15,"⑤ Butler-Volmer：在颗粒表面把四者连起来",ha="center",va="center",fontsize=12)
a.set_xlim(-0.2,10.4);a.set_ylim(-0.4,3.1);save(f,"fig03_四守恒一连接.png")

# fig04 shell
f,a=blank(7,4)
a.add_patch(Circle((0,0),2.0,color="#f6d9a8",ec="#b88a3c",lw=1.2))
a.add_patch(Wedge((0,0),1.35,0,360,width=0.3,color="#8fb8d9",ec=BL,lw=1.2))
for ang in np.linspace(0,2*np.pi,12,endpoint=False):
    arrow(a,(0.75*np.cos(ang),0.75*np.sin(ang)),(1.0*np.cos(ang),1.0*np.sin(ang)),c=BL,lw=1,ms=8)
    arrow(a,(1.38*np.cos(ang),1.38*np.sin(ang)),(1.7*np.cos(ang),1.7*np.sin(ang)),c=RD,lw=1,ms=8)
a.plot([0,1.05*np.cos(0.6)],[0,1.05*np.sin(0.6)],c=INK,lw=1);a.text(0.25,0.42,"$r$",fontsize=13)
arrow(a,(0,0),(2.0*np.cos(-0.5),2.0*np.sin(-0.5)),c="#555",lw=1);a.text(1.05,-1.3,"$R_p$",fontsize=13)
tx=2.6
a.text(tx,1.5,"薄球壳：半径 $r$ ~ $r+dr$",fontsize=12)
a.text(tx,0.95,"体积 $4\\pi r^2\\,dr$",fontsize=12)
a.text(tx,0.4,"内表面流入 $(4\\pi r^2N)|_r$",fontsize=12,color=BL)
a.text(tx,-0.15,"外表面流出 $(4\\pi r^2N)|_{r+dr}$",fontsize=12,color=RD)
a.text(tx,-0.75,"内外表面积不同 → 对 $r^2N$ 整体求导",fontsize=11.5,color="#555")
a.text(tx,-1.35,"球心：$\\partial c_s/\\partial r=0$；表面：通量 $=j$",fontsize=11.5,color="#555")
a.set_xlim(-2.2,7.6);a.set_ylim(-2.2,2.2);save(f,"fig04_球壳控制体.png")

# fig05 a_s
f,a=blank(7,3.2)
for i in range(5):
    for j in range(5): a.add_patch(Circle((0.3+i*0.6,0.3+j*0.6),0.25,color=NEG,ec="#2d4a7a",lw=.8))
a.add_patch(Rectangle((0,0),3,3,fill=False,ec=INK,lw=1.2));a.text(1.5,-0.35,"单位电极体积内 $n$ 个半径 $R_p$ 的球",ha="center",fontsize=11)
a.text(3.6,2.3,"体积分数  $\\varepsilon_s=n\\cdot\\frac{4}{3}\\pi R_p^3$",fontsize=13)
a.text(3.6,1.5,"表面积    $a_s=n\\cdot4\\pi R_p^2$",fontsize=13)
a.text(3.6,0.6,"相除 → $a_s=3\\varepsilon_s/R_p$",fontsize=14,color=RD)
a.text(3.6,0.05,"颗粒越小，同体积内表面积越大",fontsize=11,color="#555")
a.set_xlim(-0.2,8.2);a.set_ylim(-0.6,3.1);save(f,"fig05_比表面积推导.png")

# fig07 currents along x (schematic linear)
f,a=plt.subplots(figsize=(7.5,4.2))
x=np.linspace(0,1,400);Ln,Ls=0.42,0.58
ie=np.where(x<Ln,x/Ln,np.where(x<Ls,1,(1-x)/(1-Ls)));is_=1-ie
a.axvspan(0,Ln,color=NEG,alpha=.10);a.axvspan(Ln,Ls,color=SEP,alpha=.25);a.axvspan(Ls,1,color=POS,alpha=.10)
a.plot(x,is_,c=GR,lw=2.5,label="固相电流 $i_s$（电子）");a.plot(x,ie,c=BL,lw=2.5,label="液相电流 $i_e$（离子）")
a.plot(x,ie+is_,"--",c="#666",lw=1.3,label="$i_s+i_e=I$")
for xc,tt in[(Ln/2,"负极"),((Ln+Ls)/2,"隔膜"),((1+Ls)/2,"正极")]: a.text(xc,1.12,tt,ha="center")
a.set_ylim(-0.05,1.2);a.set_xlim(0,1);a.set_xlabel("位置  x / L");a.set_ylabel("电流密度 / I")
a.legend(loc="upper center",bbox_to_anchor=(0.5,-0.16),ncol=3);a.set_title("放电时两股电流沿厚度方向的交接（示意，假设反应均匀）",fontsize=12)
save(f,"fig06_两相电流交接.png")

# fig08 BV curve
f,a=plt.subplots(figsize=(7,4.2))
eta=np.linspace(-0.15,0.15,400);ft=96485/8.314/298
bv=np.exp(0.5*ft*eta)-np.exp(-0.5*ft*eta)
a.plot(eta*1000,bv,c=INK,lw=2.4,label="Butler-Volmer")
a.plot(eta*1000,ft*eta,"--",c=BL,lw=1.6,label="小过电位线性近似（$R_{ct}$）")
a.plot(eta[eta>0.02]*1000,np.exp(0.5*ft*eta[eta>0.02]),":",c=RD,lw=2,label="大过电位 Tafel 近似")
a.set_ylim(-12,12);a.set_xlabel("过电位  η  (mV)");a.set_ylabel("$Fj\\,/\\,i_0$")
a.axhline(0,c="#999",lw=.8);a.axvline(0,c="#999",lw=.8);a.legend(loc="upper left")
a.text(70,-6,"η>0：脱锂（j>0）",color="#555");a.text(-150,2.5,"η<0：嵌锂（j<0）",color="#555")
a.set_title("Butler-Volmer 关系（$\\alpha_a=\\alpha_c=0.5$，25 ℃）",fontsize=12);save(f,"fig09_ButlerVolmer.png")

# fig09 BCs
f,a=blank(9,3.6)
a.add_patch(Rectangle((0,0),0.3,2,color=CU));a.add_patch(Rectangle((0.3,0),3.2,2,color=NEG,alpha=.25));a.add_patch(Rectangle((3.5,0),1.4,2,color=SEP,alpha=.5))
a.add_patch(Rectangle((4.9,0),3.2,2,color=POS,alpha=.25));a.add_patch(Rectangle((8.1,0),0.3,2,color=AL))
a.text(1.9,2.15,"负极",ha="center");a.text(4.2,2.15,"隔膜",ha="center");a.text(6.5,2.15,"正极",ha="center")
def box(x,y,lines,c):
    for k,l in enumerate(lines): a.text(x,y-0.45*k,l,ha="center",fontsize=12.5 if k==0 else 11.5,color=c,fontweight="bold" if k==0 else "normal")
box(0.6,-0.4,["集流体 x=0","电子能过，离子不能","$i_e=0,\\ i_s=I$","参考点 $\\phi_s=0$"],INK)
box(4.2,-0.4,["电极/隔膜界面","离子能过，电子不能","$i_s=0$","$c_e,\\phi_e,N_+,i_e$ 连续"],INK)
box(7.8,-0.4,["集流体 x=L","电子能过，离子不能","$i_e=0,\\ i_s=I$"],INK)
for xx in (): a.plot([xx,xx],[-0.2,0],c="#888",lw=1)
arrow(a,(-0.9,1.3),(0.25,1.3),c=GR);a.text(-0.9,1.45,"e$^-$",color=GR)
arrow(a,(2.6,0.7),(3.45,0.7),c=BL);arrow(a,(3.55,0.7),(4.85,0.7),c=BL);a.text(4.2,0.85,"Li$^+$",color=BL,ha="center")
a.text(3.5,1.3,"×",color=RD,fontsize=18,ha="center",va="center");a.text(2.7,1.4,"e$^-$",color=GR)
a.set_xlim(-1.2,9.4);a.set_ylim(-1.9,2.5);save(f,"fig10_边界条件.png")

# fig15 hybrid interface
f,a=blank(8,3.8)
a.add_patch(Rectangle((0,0),3,3,color="#c9d3ea"));a.add_patch(Rectangle((3,0),4.4,3,color=ELY))
a.text(1.5,3.15,"固相（颗粒）",ha="center",fontsize=12);a.text(5.2,3.15,"电解液",ha="center",fontsize=12)
arrow(a,(5.8,2.0),(1.2,2.0),c=OR,lw=2.2);a.text(3.5,2.25,"法拉第：Li$^+$ 穿过界面嵌入晶格 → $j$",ha="center",fontsize=11,color=OR)
for y in np.linspace(0.3,1.3,5): a.text(2.8,y,"−",ha="center",va="center",color=BL,fontsize=14);a.text(3.2,y,"+",ha="center",va="center",color=RD,fontsize=13)
a.text(3.5,0.8,"双电层：电荷在界面两侧排队\n不进入晶格 → $i_{dl}$",ha="left",va="center",fontsize=11,color=PU)
a.text(7.7,2.45,"NCM 颗粒：$Fj+i_{dl}$；活性炭：仅 $i_{dl}$",fontsize=11)
a.text(7.7,1.75,"颗粒扩散边界：只含法拉第 $j$",fontsize=11)
a.text(7.7,1.05,"盐源项多出 $(\\beta-t_+)\\,a_{dl}i_{dl}/F$",fontsize=11)
a.text(7.7,0.35,"预锂化硬碳：初始 $c_s$ 更高",fontsize=11)
a.set_xlim(-0.1,12.6);a.set_ylim(-0.2,3.5);save(f,"fig18_混合超级电容界面.png")

RT_F=8.314*298.15/96485; tp=0.2594
x=D["x"]*1e6; Ln,Ls=85.2,97.2
def regions(a,ytxt):
    a.axvspan(0,Ln,color=NEG,alpha=.08);a.axvspan(Ln,Ls,color=SEP,alpha=.22);a.axvspan(Ls,x[-1]+1,color=POS,alpha=.08)
    for xc,tt in[(Ln/2,"负极"),((Ln+Ls)/2,"隔膜"),((Ls+x[-1])/2,"正极")]: a.text(xc,ytxt,tt,ha="center",color="#444")

# fig07 modified Ohm decomposition (2C, 1500 s)
t2=D["t_2"];k=int(np.argmin(abs(t2-1500)));ce=D["ce_2"][:,k];pe=D["phie_2"][:,k]
tot=(pe-pe[0])*1000;conc=2*RT_F*(1-tp)*np.log(ce/ce[0])*1000;ohm=tot-conc
f,a=plt.subplots(figsize=(7.5,4.3));regions(a,25)
a.plot(x,tot,c=INK,lw=2.4,label="液相电势 $\\phi_e$（总）");a.plot(x,ohm,"--",c=BL,lw=2,label="欧姆项贡献");a.plot(x,conc,":",c=RD,lw=2.4,label="浓差项贡献")
a.axhline(0,c="#999",lw=.8);a.set_xlim(0,x[-1]+1);a.set_ylim(min(tot.min(),conc.min())-15,40)
a.set_xlabel("位置 x (μm)");a.set_ylabel("相对 x=0 处的电势 (mV)");a.legend(loc="lower left")
a.set_title("2C 放电 1500 s：液相电势降中欧姆项与浓差项的分解",fontsize=12);save(f,"fig07_修正欧姆定律.png")
print("fig07 totals mV: tot %.0f ohm %.0f conc %.0f"%(tot[-1],ohm[-1],conc[-1]))

# fig08 (1-t+) schematic
f,a=blank(8,3.4)
a.add_patch(Circle((1.2,1.5),1.0,color=NEG,alpha=.55,ec="#2d4a7a"));a.text(1.2,1.5,"颗粒",ha="center",va="center",fontsize=12,color="white")
a.add_patch(FancyBboxPatch((2.9,1.1),1.9,0.8,boxstyle="round,pad=0.05,rounding_size=0.12",fc="#fdf3e1",ec=OR,lw=1.8))
a.text(3.85,1.5,"放出 1 份 Li$^+$\n（源项 $a_s j$）",ha="center",va="center",fontsize=11)
arrow(a,(2.25,1.5),(2.85,1.5),c=OR,lw=2)
arrow(a,(4.9,1.75),(6.6,2.55),c=BL,lw=2.2);arrow(a,(4.9,1.25),(6.6,0.45),c=RD,lw=2.2)
a.text(6.75,2.55,"$t_+\\approx0.26$：随电流带走",va="center",fontsize=12,color=BL)
a.text(6.75,0.45,"$1-t_+\\approx0.74$：留在原地，只能靠扩散",va="center",fontsize=12,color=RD)
a.text(5.0,-0.35,"放电时负极侧盐越积越多，正极侧被越抽越少",ha="center",fontsize=11,color="#555")
a.set_xlim(0,12.6);a.set_ylim(-0.6,2.9);save(f,"fig08_电解液锂守恒.png")

# fig11 coupling matrix
f,a=blank(8,3.8)
cols=["$c_s$","$c_e$","$\\phi_s$","$\\phi_e$","$j$"];rows=[("① 固相扩散","微分",[1,0,0,0,1]),("② 液相锂守恒","微分",[0,1,0,0,1]),("③ 固相电荷","代数",[0,0,1,0,1]),("④ 液相电荷","代数",[0,1,0,1,1]),("⑤ Butler-Volmer","代数",[1,1,1,1,1])]
for i,cn in enumerate(cols): a.text(3.2+i*1.1,5.4,cn,ha="center",fontsize=16)
a.text(9.3,5.4,"类型",ha="center",fontsize=12)
for r,(nm,ty,m) in enumerate(rows):
    y=4.6-r*0.9; a.text(0,y,nm,va="center",fontsize=12)
    for i,v in enumerate(m):
        if v: a.add_patch(Circle((3.2+i*1.1,y),0.2,color=OR if i==4 else BL))
        else: a.add_patch(Circle((3.2+i*1.1,y),0.06,color="#ccc"))
    a.text(9.3,y,ty+("（含 ∂/∂t）" if ty=="微分" else "（无 ∂/∂t）"),ha="center",va="center",fontsize=11,color=GR if ty=="微分" else PU)
a.text(4.85,-0.15,"$j$ 出现在每一行，而 $j$ 又依赖全部场量 → 必须联立求解（DAE）",ha="center",fontsize=11.5,color="#444")
a.set_xlim(-0.2,10.4);a.set_ylim(-0.5,5.8);save(f,"fig11_P2D方程总览.png")

# fig12 rate curves
f,a=plt.subplots(figsize=(7.5,4.3))
for C,c in zip([0.5,1,2,3],["#1b9e77",BL,OR,RD]): a.plot(D[f"Q_{C}"],D[f"V_{C}"],c=c,lw=2.2,label=f"{C}C（{D[f'Q_{C}'][-1]:.2f} A·h）")
a.set_xlabel("放电容量 (A·h)");a.set_ylabel("端电压 (V)");a.legend(title="放电倍率");a.set_xlim(0,5.3)
a.set_title("不同倍率恒流放电至 2.5 V（DFN，Chen2020，5 A·h）",fontsize=12);save(f,"fig12_倍率放电曲线.png")

# fig13 3C ce profiles
t3=D["t_3"];ce3=D["ce_3"]
f,a=plt.subplots(figsize=(7.5,4.3));regions(a,3.75)
ts=[0,30,70,140,280,t3[-1]]
for i,tt in enumerate(ts):
    k=int(np.argmin(abs(t3-tt)));a.plot(x,ce3[:,k]/1000,c=plt.cm.viridis(i/5.5),lw=2.2,label=f"{t3[k]:.0f} s")
k2=int(np.argmin(abs(t2-850)));a.plot(x,D["ce_2"][:,k2]/1000,"--",c="#888",lw=1.6,label="2C, 850 s（对照）")
a.set_ylim(-0.05,4.0);a.set_xlim(0,x[-1]+1);a.set_xlabel("位置 x (μm)");a.set_ylabel("电解液浓度 $c_e$ (mol/L)")
a.legend(title="3C 放电时间",loc="center left",bbox_to_anchor=(1.01,0.5));a.set_title("3C 放电：正极集流体侧的盐在几分钟内被抽干",fontsize=12)
save(f,"fig13_正极电解液浓度分布.png")

# fig14 3C jp
xp=(D["xp"]-D["xp"][0])*1e6;jp=D["jp_3"]
f,a=plt.subplots(figsize=(7.5,4.3))
for i,tt in enumerate([0,70,140,280,420]):
    k=int(np.argmin(abs(t3-tt)));a.plot(xp,jp[:,k],c=plt.cm.plasma(i/5),lw=2.2,label=f"{t3[k]:.0f} s")
a.axhline(0,c="#999",lw=.8)
a.set_xlabel("正极内位置 (μm)（左：隔膜侧 → 右：集流体侧）");a.set_ylabel("界面电流密度 $Fj$ (A/m²)（负 = 嵌锂）")
a.legend(title="3C 放电时间",loc="center left",bbox_to_anchor=(1.01,0.5));a.set_title("3C 放电：集流体侧反应归零，电流挤向隔膜侧",fontsize=12)
save(f,"fig14_正极反应分布.png")

# fig15 thick vs thin
f,ax=plt.subplots(1,2,figsize=(9,3.9),sharey=True)
for a,I in zip(ax,[5,10]):
    a.plot(D[f"thin_Q_{I}"],D[f"thin_V_{I}"],c=BL,lw=2.2,label=f"原电池 5 A·h（{D[f'thin_Q_{I}'][-1]:.2f} A·h）")
    a.plot(D[f"thick_Q_{I}"],D[f"thick_V_{I}"],c=RD,lw=2.2,label=f"加厚电池 10 A·h（{D[f'thick_Q_{I}'][-1]:.2f} A·h）")
    a.set_title(f"{I} A 放电",fontsize=12);a.set_xlabel("放电容量 (A·h)");a.legend(loc="upper right",fontsize=9.5);a.set_xlim(0,10.5)
ax[0].set_ylabel("端电压 (V)");save(f,"fig15_厚电极对比.png")

# fig16 plating
f,a=plt.subplots(figsize=(7.5,4.4))
for tag,c,lab in[("1C",BL,"1C"),("3C",RD,"3C"),("3Cthick",PU,"3C，负极加厚一倍")]:
    d=D[f"pl_{tag}"];xx=D[f"plx_{tag}"];xx=xx/xx[-1];m=d.min(axis=1)*1000
    a.plot(xx,m,c=c,lw=2.3,label=f"{lab}（最低 {m.min():.0f} mV）")
    tt=D[f"plt_{tag}"];below=np.where(d.min(axis=0)<0)[0]
    if len(below) and tag!="3Cthick": a.plot([1.0],[m[-1]],"o",c=c,ms=6)
a.axhline(0,c=INK,lw=1.1);a.axhspan(-240,0,color=RD,alpha=.05);a.text(0.02,-225,"φs − φe < 0：析锂风险区",color=RD)
a.annotate("3C：t≈30 s 首先在此跌破 0",(1.0,-134),(0.45,-170),arrowprops=dict(arrowstyle="->",color=RD),color=RD,fontsize=10.5)
a.annotate("1C：t≈1800 s 才在此跌破 0",(1.0,-15),(0.66,42),arrowprops=dict(arrowstyle="->",color=BL),color=BL,fontsize=10.5)
a.set_xlim(0,1.04);a.set_ylim(-240,110);a.set_xlabel("负极内归一化位置 x / L$_n$（0：集流体 → 1：隔膜）");a.set_ylabel("充电全程中 min(φs − φe) (mV)")
a.legend(loc="center left",bbox_to_anchor=(0.0,0.38),fontsize=10);a.set_title("10% SOC 起恒流充电至 4.2 V：负极各处的析锂判据",fontsize=12);save(f,"fig16_快充析锂判据.png")

# fig17 SPM/SPMe/DFN
f,ax=plt.subplots(1,2,figsize=(9,3.9),sharey=True)
for a,C in zip(ax,[0.5,2]):
    for m,c,ls in[("SPM",RD,"-"),("SPMe",OR,"--"),("DFN",BL,"-")]: a.plot(D[f"{m}_Q_{C}"],D[f"{m}_V_{C}"],c=c,ls=ls,lw=2,label=("P2D (DFN)" if m=="DFN" else m)+f"  {D[f'{m}_Q_{C}'][-1]:.2f} A·h")
    a.set_title(f"{C}C 放电",fontsize=12);a.set_xlabel("放电容量 (A·h)");a.set_xlim(0,5.3);a.legend(loc="lower left",fontsize=10)
ax[0].set_ylabel("端电压 (V)");save(f,"fig17_SPM_SPMe_DFN对比.png")
