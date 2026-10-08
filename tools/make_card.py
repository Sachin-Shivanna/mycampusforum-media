#!/usr/bin/env python3
"""MyCampusForum LinkedIn image generator (1200x1200).

Screenshot card:
  python3 tools/make_card.py shot --eyebrow "Feature spotlight" --headline "..." --sub "..." \
      --shot screenshots/job-ai-matches.png --out linkedin/2026-10/2026-10-20-matching.png
Text / question card:
  python3 tools/make_card.py text --eyebrow "Sunday question" --headline "..." [--note "..."] \
      [--option "A:WhatsApp groups" --option "B:..."] --out linkedin/...png
"""
import argparse, os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEAL=(20,170,150); PURP=(104,72,180); ORNG=(240,125,30); INK=(30,27,58); MUTED=(96,96,120)
W=H=1200

def find_font(names):
    for n in names:
        hits=glob.glob(f"/usr/share/fonts/**/{n}",recursive=True)
        if hits: return hits[0]
    return None
FB=find_font(["Poppins-Bold.ttf","DejaVuSans-Bold.ttf"])
FM=find_font(["Poppins-Medium.ttf","DejaVuSans.ttf"])
FT=find_font(["Inter-Medium.otf","Inter-Regular.otf","DejaVuSans.ttf"])
def F(p,s): return ImageFont.truetype(p,s) if p else ImageFont.load_default()

def bg():
    c=Image.new("RGB",(W,H)); top=(240,250,247); bot=(244,240,252)
    for y in range(H):
        t=y/H; c.paste(tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3)),[0,y,W,y+1])
    blob=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(blob)
    bd.ellipse([820,-220,1420,380],fill=TEAL+(40,)); bd.ellipse([-260,820,340,1420],fill=PURP+(35,)); bd.ellipse([980,980,1300,1300],fill=ORNG+(35,))
    blob=blob.filter(ImageFilter.GaussianBlur(60)); c.paste(blob,(0,0),blob); return c

def brand(c):
    d=ImageDraw.Draw(c)
    logo=Image.open(os.path.join(ROOT,"assets","logo-icon.png")).convert("RGBA").resize((66,57),Image.LANCZOS)
    c.paste(logo,(64,58),logo); f=F(FB,30); x=142
    for word,col in (("My",TEAL),("Campus",PURP),("Forum",ORNG)):
        d.text((x,70),word,font=f,fill=col); x+=d.textlength(word,font=f)+(8 if word!="Forum" else 0)
    return d

def wrap(d,text,font,maxw):
    lines=[];cur=""
    for w in text.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines

def footer(c):
    d=ImageDraw.Draw(c); t="mycampusforum.com  ·  Free 30-day pilots"; f=F(FB,20); w=d.textlength(t,font=f)
    d.rounded_rectangle([W-64-w-36,H-86,W-64,H-40],23,fill=INK); d.text((W-64-w-18,H-63),t,font=f,fill=(255,255,255),anchor="lm")

def rounded(im,r):
    m=Image.new("L",im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.size[0]-1,im.size[1]-1],r,fill=255)
    out=Image.new("RGBA",im.size); out.paste(im,(0,0),m); return out

def shot(a):
    c=bg(); d=brand(c); y=170; hs=a.size
    d.text((64,y),a.eyebrow.upper(),font=F(FB,20),fill=ORNG); y+=42
    f=F(FB,hs)
    for l in wrap(d,a.headline,f,W-128): d.text((64,y),l,font=f,fill=INK); y+=int(hs*1.22)
    if a.sub:
        y+=16; fs=F(FT,26)
        for l in wrap(d,a.sub,fs,W-128): d.text((64,y),l,font=fs,fill=MUTED); y+=38
    s=Image.open(a.shot).convert("RGB"); width=1080; s=s.resize((width,int(s.size[1]*width/s.size[0])),Image.LANCZOS)
    top=y+40
    if top+s.size[1]<H-140: top=y+40+((H-130)-(y+40)-s.size[1])//2
    x=(W-width)//2
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([x+6,top+14,x+width+6,top+s.size[1]+14],22,fill=(40,30,90,70))
    sh=sh.filter(ImageFilter.GaussianBlur(18)); c.paste(sh,(0,0),sh)
    fr=Image.new("RGB",(width+16,s.size[1]+16),(255,255,255)); fr.paste(s,(8,8)); fr=rounded(fr,22); c.paste(fr,(x-8,top-8),fr)
    fade=Image.new("RGBA",(W,140),(0,0,0,0)); fd=ImageDraw.Draw(fade)
    for i in range(140): fd.line([(0,i),(W,i)],fill=(244,240,252,int(255*(i/140)**1.6)))
    c.paste(fade,(0,H-140),fade); footer(c); return c

def text(a):
    c=bg(); d=brand(c); opts=[o.split(":",1) for o in (a.option or [])]
    y0=250 if not opts else 230
    d.text((64,y0),a.eyebrow.upper(),font=F(FB,22),fill=ORNG)
    f=F(FB,70 if not opts else 62); y=y0+50
    for l in wrap(d,a.headline,f,W-128): d.text((64,y),l,font=f,fill=INK); y+=int(f.size*1.2)
    y+=30; cols=[TEAL,PURP,ORNG,(10,120,190)]
    for i,(k,v) in enumerate(opts[:4]):
        d.rounded_rectangle([64,y,W-64,y+92],46,fill=(255,255,255),outline=(225,222,240),width=2)
        d.ellipse([80,y+14,144,y+78],fill=cols[i]); d.text((112,y+46),k.strip(),font=F(FB,30),fill=(255,255,255),anchor="mm")
        d.text((168,y+46),v.strip(),font=F(FM,30),fill=INK,anchor="lm"); y+=112
    if a.note:
        fs=F(FT,30)
        for l in wrap(d,a.note,fs,W-128): d.text((64,y),l,font=fs,fill=MUTED); y+=44
    footer(c); return c

p=argparse.ArgumentParser(); p.add_argument("kind",choices=["shot","text"])
p.add_argument("--eyebrow",required=True); p.add_argument("--headline",required=True)
p.add_argument("--sub"); p.add_argument("--shot"); p.add_argument("--note"); p.add_argument("--option",action="append")
p.add_argument("--size",type=int,default=56,help="headline font size for shot cards (48-60)")
p.add_argument("--out",required=True); a=p.parse_args()
img=shot(a) if a.kind=="shot" else text(a)
os.makedirs(os.path.dirname(os.path.abspath(a.out)),exist_ok=True); img.save(a.out,optimize=True); print("saved",a.out)
