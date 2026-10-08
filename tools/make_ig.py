#!/usr/bin/env python3
"""MyCampusForum Instagram image generator (1080x1350 portrait).

Usage:  python3 tools/make_ig.py spec.json OUT_DIR
spec.json = {"slides": [ {...}, {...} ]}   -> OUT_DIR/01.png, 02.png ...

Slide kinds (all text fields plain; emoji only in "emoji" fields):
  {"kind":"cover","kicker":"Placement season","title":"5 things your seniors wish they knew","theme":"purple"}
  {"kind":"tip","num":1,"title":"Your seniors are your best job board","body":"..."}
  {"kind":"shot","title":"...","shot":"screenshots/job-ai-matches.png","caption":"...","crop":[x0,y0,x1,y1]}
  {"kind":"quote","text":"Hostel friends -> co-founders.","sub":"Tag yours","theme":"orange"}
  {"kind":"poll","question":"Placement season?","a":"Excited","a_emoji":"😎","b":"Stressed","b_emoji":"😵","sub":"Comment 1 or 2"}
  {"kind":"meme","top":"Me applying on 200 job portals","top_emoji":"😐","bottom":"One referral from a senior","bottom_emoji":"🤩"}
  {"kind":"cta","title":"Save this for placement season","body":"...","button":"Link in bio"}
Themes: purple | teal | orange | light | ink
"""
import json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1350
TEAL=(20,170,150); PURP=(104,72,180); ORNG=(240,125,30); INK=(30,27,58); CREAM=(255,248,240)
THEMES={"purple":(PURP,(66,42,130),(255,255,255),(255,196,120)),
        "teal":(TEAL,(8,96,88),(255,255,255),INK),
        "orange":(ORNG,(214,82,30),(255,255,255),INK),
        "light":(CREAM,(243,236,255),INK,PURP),
        "ink":(INK,(45,30,90),(255,255,255),(255,196,120))}

def ff(names):
    for n in names:
        h=glob.glob(f"/usr/share/fonts/**/{n}",recursive=True)
        if h: return h[0]
FB=ff(["Poppins-Bold.ttf","DejaVuSans-Bold.ttf"]); FM=ff(["Poppins-Medium.ttf","DejaVuSans.ttf"])
FE=ff(["NotoColorEmoji.ttf"])
def F(p,s): return ImageFont.truetype(p,s)

def grad(c1,c2):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3)))
    # playful blobs
    b=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(b)
    bd.ellipse([760,-160,1260,340],fill=(255,255,255,28)); bd.ellipse([-200,1050,260,1510],fill=(255,255,255,22))
    im.paste(b,(0,0),b); return im

def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else: out.append(cur); cur=w
    out.append(cur); return out

def block(d,x,y,t,size,fill,font=None,mw=W-160,align="left",lh=1.18):
    f=F(font or FB,size)
    for l in wrap(d,t,f,mw):
        lx = x if align=="left" else (W-d.textlength(l,font=f))/2
        d.text((lx,y),l,font=f,fill=fill); y+=int(size*lh)
    return y

def emoji(im,ch,x,y,size):
    if not FE or not ch: return
    try:
        f=ImageFont.truetype(FE,109); tmp=Image.new("RGBA",(160,160),(0,0,0,0))
        ImageDraw.Draw(tmp).text((0,0),ch,font=f,embedded_color=True)
        bb=tmp.getbbox()
        if not bb: return
        e=tmp.crop(bb).resize((size,int(size*(bb[3]-bb[1])/(bb[2]-bb[0]))),Image.LANCZOS)
        im.paste(e,(int(x),int(y)),e)
    except Exception: pass

def header(im,dark_text,idx=None,total=None):
    d=ImageDraw.Draw(im)
    lg=Image.open(os.path.join(ROOT,"assets","logo-icon.png")).convert("RGBA").resize((58,50))
    im.paste(lg,(60,56),lg)
    f=F(FB,26); x=126
    cols=((TEAL,PURP,ORNG) if dark_text==INK else ((255,255,255),(255,255,255),(255,225,190)))
    for w,c in zip(("My","Campus","Forum"),cols):
        d.text((x,66),w,font=f,fill=c); x+=d.textlength(w,font=f)+5
    if idx and total and total>1:
        t=f"{idx}/{total}"; fs=F(FB,24); tw=d.textlength(t,font=fs)
        d.rounded_rectangle([W-60-tw-28,60,W-60,104],22,outline=dark_text,width=2)
        d.text((W-60-tw-14,68),t,font=fs,fill=dark_text)

def footer_swipe(im,fg,last):
    d=ImageDraw.Draw(im); f=F(FB,28)
    if last:
        t="@mycampusforum"; w=d.textlength(t,font=f); d.text((W-60-w,H-90),t,font=f,fill=fg)
    else:
        t="swipe"; w=d.textlength(t,font=f); x=W-60-w-56; d.text((x,H-90),t,font=f,fill=fg)
        ax=W-60-40; ay=H-72; d.line([(ax,ay),(ax+38,ay)],fill=fg,width=4); d.line([(ax+24,ay-12),(ax+38,ay),(ax+24,ay+12)],fill=fg,width=4,joint="curve")

def pill(d,x,y,t,bg,fg,size=30,center=False):
    f=F(FB,size); w=d.textlength(t,font=f)
    if center: x=(W-w)/2-26
    d.rounded_rectangle([x,y,x+w+52,y+size+28],(size+28)//2,fill=bg); d.text((x+26,y+11),t,font=f,fill=fg)

def render(s,idx,total):
    th=THEMES.get(s.get("theme"), THEMES["purple" if s["kind"] in ("cover","shot") else "light" if s["kind"] in ("tip","cta") else "orange"])
    c1,c2,fg,acc=th; im=grad(c1,c2); d=ImageDraw.Draw(im); header(im,fg,idx,total); k=s["kind"]; last=idx==total
    if k=="cover":
        if s.get("kicker"): pill(d,60,330,s["kicker"].upper(),acc if fg!=INK else PURP,(255,255,255) if fg==INK or acc==INK else INK,28)
        block(d,60,440,s["title"],96,fg,lh=1.12)
        if s.get("emoji"): emoji(im,s["emoji"],W-260,H-330,170)
    elif k=="tip":
        f=F(FB,300); d.text((52,230),str(s.get("num","")),font=f,fill=acc)
        y=block(d,60,640,s["title"],84,fg,lh=1.12)
        if s.get("body"): block(d,60,y+40,s["body"],44,(90,90,115) if fg==INK else (235,230,250),font=FM,lh=1.4)
    elif k=="shot":
        y=block(d,60,170,s["title"],62,fg,lh=1.15)
        sh=Image.open(os.path.join(ROOT,s["shot"]) if not os.path.isabs(s["shot"]) else s["shot"]).convert("RGB")
        if s.get("crop"): sh=sh.crop(tuple(s["crop"]))
        w=960; sh=sh.resize((w,int(sh.size[1]*w/sh.size[0])),Image.LANCZOS)
        maxh=H-y-(260 if s.get("caption") else 170)
        if sh.size[1]>maxh: sh=sh.crop((0,0,w,maxh))
        sy=y+40; shadow=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(shadow).rounded_rectangle([66,sy+18,66+w,sy+sh.size[1]+18],26,fill=(0,0,0,90))
        shadow=shadow.filter(ImageFilter.GaussianBlur(18)); im.paste(shadow,(0,0),shadow)
        m=Image.new("L",sh.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,sh.size[0]-1,sh.size[1]-1],22,fill=255)
        im.paste(sh,(60,sy),m)
        if s.get("caption"): block(d,60,sy+sh.size[1]+36,s["caption"],40,fg,font=FB,lh=1.25)
    elif k=="quote":
        d.text((50,200),"“",font=F(FB,300),fill=acc)
        y=block(d,60,470,s["text"],92,fg,lh=1.12)
        if s.get("sub"): pill(d,60,y+50,s["sub"],INK if fg!=INK else PURP,(255,255,255),32)
        if s.get("emoji"): emoji(im,s["emoji"],W-280,H-340,180)
    elif k=="poll":
        y=block(d,60,200,s["question"],84,fg,lh=1.12)
        top=max(y+50,520)
        for i,(lab,em,col) in enumerate(((s["a"],s.get("a_emoji"),TEAL),(s["b"],s.get("b_emoji"),PURP))):
            yy=top+i*280; d.rounded_rectangle([60,yy,W-60,yy+240],40,fill=(255,255,255))
            d.ellipse([100,yy+60,220,yy+180],fill=col); d.text((160,yy+120),str(i+1),font=F(FB,64),fill=(255,255,255),anchor="mm")
            d.text((260,yy+120),lab,font=F(FB,64),fill=INK,anchor="lm")
            emoji(im,em,W-230,yy+60,120)
        if s.get("sub"): block(d,60,top+580,s["sub"],38,fg,font=FB,align="center")
    elif k=="meme":
        for i,(t,em) in enumerate(((s["top"],s.get("top_emoji")),(s["bottom"],s.get("bottom_emoji")))):
            yy=170+i*560; bg=(255,255,255) if i==0 else INK; tf=INK if i==0 else (255,255,255)
            d.rounded_rectangle([60,yy,W-60,yy+520],40,fill=bg)
            if i==1: d.rounded_rectangle([60,yy,W-60,yy+520],40,outline=ORNG,width=8)
            block(d,110,yy+150,t,58,tf,mw=560,lh=1.15); emoji(im,em,W-340,yy+130,240)
    elif k=="cta":
        y=block(d,60,420,s["title"],100,fg,lh=1.12)
        if s.get("body"): y=block(d,60,y+40,s["body"],44,(90,90,115) if fg==INK else (235,230,250),font=FM,lh=1.4)
        pill(d,60,y+60,s.get("button","Link in bio"),INK if fg==INK else (255,255,255),(255,255,255) if fg==INK else INK,36)
    if s["kind"] in ("cover","tip","shot") and total>1: footer_swipe(im,fg,last)
    elif last: footer_swipe(im,fg,True)
    return im

if __name__=="__main__":
    spec=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
    sl=spec["slides"]
    for i,s in enumerate(sl,1):
        render(s,i,len(sl)).save(os.path.join(out,f"{i:02d}.png"),optimize=True); print("saved",os.path.join(out,f"{i:02d}.png"))
