#!/usr/bin/env python3
"""X/Twitter header banner (1500x500). Usage: python3 tools/make_x_header.py OUT.png
Keeps text clear of the profile-photo zone (bottom-left) and the mobile top/bottom crop."""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1500,500; TEAL=(20,170,150); PURP=(104,72,180); ORNG=(240,125,30); INK=(30,27,58)
def ff(n):
    h=glob.glob(f"/usr/share/fonts/**/{n}",recursive=True); return h[0]
FB=ff("Poppins-Bold.ttf"); FM=ff("Poppins-Medium.ttf")
F=ImageFont.truetype
im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
for x in range(W):
    t=x/W; c1=(58,34,120); c2=(24,90,110)
    d.line([(x,0),(x,H)],fill=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3)))
b=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(b)
bd.ellipse([-160,-260,420,260],fill=(255,255,255,18)); bd.ellipse([1180,280,1700,760],fill=(20,170,150,60))
bd.ellipse([760,-220,1160,140],fill=(240,125,30,40))
for i in range(0,W,38):
    for j in range(0,H,38): bd.ellipse([i,j,i+3,j+3],fill=(255,255,255,14))
im.paste(b,(0,0),b); d=ImageDraw.Draw(im)
# screenshots, stacked cards on the right
def card(path,w,crop=None):
    s=Image.open(os.path.join(ROOT,path)).convert("RGB")
    if crop: s=s.crop(crop)
    s=s.resize((w,int(s.size[1]*w/s.size[0])),Image.LANCZOS)
    m=Image.new("L",s.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,s.size[0]-1,s.size[1]-1],18,fill=255)
    s.putalpha(m); return s
def place(c,xy,rot):
    c=c.rotate(rot,expand=True,resample=Image.BICUBIC)
    sh=Image.new("RGBA",(c.size[0]+80,c.size[1]+80),(0,0,0,0))
    a=c.split()[-1].point(lambda v: 110 if v else 0); sh.paste((0,0,0,255),(40,52),a)
    sh=sh.filter(ImageFilter.GaussianBlur(16)); im.paste(sh,(xy[0]-40,xy[1]-40),sh); im.paste(c,xy,c)
place(card("screenshots/community-channel-chat.png",470),(1000,70),4)
place(card("screenshots/job-ai-matches.png",380,(208,0,788,623)),(905,150),-5)
# text block: everything above y~380 so the profile photo (bottom-left) never covers it
x=70; y=62
lg=Image.open(os.path.join(ROOT,"assets/logo-icon.png")).convert("RGBA").resize((52,45)); im.paste(lg,(x,y),lg)
fx=x+64
for wd,c in (("My",(120,230,210)),("Campus",(255,255,255)),("Forum",(255,190,130))):
    d.text((fx,y+4),wd,font=F(FB,30),fill=c); fx+=d.textlength(wd,font=F(FB,30))+4
y+=68
d.text((x,y),"Where your campus",font=F(FB,60),fill=(255,255,255)); y+=70
d.text((x,y),"grows ",font=F(FB,60),fill=(255,255,255)); gx=x+d.textlength("grows ",font=F(FB,60))
d.text((gx,y),"together.",font=F(FB,60),fill=(255,196,120)); y+=90
f=F(FM,22); fx=x
for i,it in enumerate(["AI job matches","Alumni referrals","Mentor sessions","Course materials"]):
    if i: d.ellipse([fx+7,y+14,fx+13,y+20],fill=(255,196,120)); fx+=22
    d.text((fx,y),it,font=f,fill=(235,232,250)); fx+=d.textlength(it,font=f)+8
y+=48; t="mycampusforum.com"; f=F(FB,24); w=d.textlength(t,font=f)
d.rounded_rectangle([x,y,x+w+44,y+46],23,fill=ORNG); d.text((x+22,y+7),t,font=f,fill=(255,255,255))
t2="Free 30-day pilots for colleges"; d.text((x+w+64,y+9),t2,font=F(FM,22),fill=(255,255,255))
out=sys.argv[1]; os.makedirs(os.path.dirname(os.path.abspath(out)),exist_ok=True); im.save(out,optimize=True); print("saved",out)
