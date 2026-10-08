#!/usr/bin/env python3
"""MyCampusForum Reel generator (1080x1920, H.264/AAC, faststart). Needs ffmpeg + Pillow.

Usage: python3 tools/make_reel.py spec.json OUT.mp4

Kind "slides" — fast-cut scenes with Ken Burns zoom + slide transitions (15–25s total):
{"kind":"slides","audio_from":"assets/video/story-of-growth-720p.mp4","audio_start":140,
 "scenes":[
   {"type":"text","pill":"POV: placement season","lines":["100+ applications.","0 replies."],"accent_last":true,"theme":"purple","dur":3},
   {"type":"shot","top":"They post a role. AI shortlists you in minutes.","shot":"screenshots/job-ai-matches.png","crop":[208,0,788,623],"bottom":"93% match. With the reason why.","theme":"purple","dur":5},
   {"type":"end","lines":["Warm intro",">","cold application."],"sub":"Tell your placement cell about MyCampusForum.","button":"Link in bio","dur":4}]}

Kind "clip" — cut moments from the brand film, framed 9:16 with captions:
{"kind":"clip","source":"assets/video/story-of-growth-720p.mp4","hook":["Nobody gets","hired alone."],
 "tag":"Every campus is a story of growth",
 "segments":[{"start":76,"dur":7,"caption":"It starts with a question."}, ...],
 "audio_start":76}
Known strong moments in story-of-growth (seconds): 24 "Strong roots", 78 "It starts with a question",
108 "Someone who's been there", 120 "Opportunity grows through people", 132 "Growth isn't a straight line",
141 "You're never growing alone", 147-155 "Offer accepted -> HIRED."
Themes: purple | teal | light
"""
import json, os, sys, subprocess, tempfile, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1080,1920; TEAL=(20,170,150); PURP=(104,72,180); ORNG=(240,125,30); INK=(30,27,58)
def ff(n):
    h=glob.glob(f"/usr/share/fonts/**/{n}",recursive=True); return h[0] if h else None
PB=ff("Poppins-Bold.ttf") or ff("DejaVuSans-Bold.ttf"); PM=ff("Poppins-Medium.ttf") or ff("DejaVuSans.ttf")
def P(p): return p if os.path.isabs(p) else os.path.join(ROOT,p)
def run(cmd): subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
LOGO=Image.open(P("assets/logo-icon.png")).convert("RGBA")
THEME={"purple":(PURP,(66,42,130),(255,255,255),(255,196,120)),"teal":(TEAL,(8,96,88),(255,255,255),INK),"light":((255,248,240),(243,236,255),INK,PURP)}

def grad(c1,c2):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3)))
    return im
def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else: out.append(cur);cur=w
    out.append(cur);return out
def ctext(d,y,t,size,fill,font=None,mw=W-160):
    f=ImageFont.truetype(font or PB,size)
    for l in wrap(d,t,f,mw):
        w=d.textlength(l,font=f); d.text(((W-w)/2,y),l,font=f,fill=fill); y+=int(size*1.2)
    return y
def pill(d,y,t,bg,fg,size=34):
    f=ImageFont.truetype(PB,size); w=d.textlength(t,font=f)
    d.rounded_rectangle([(W-w)/2-30,y,(W+w)/2+30,y+size+30],(size+30)//2,fill=bg); d.text(((W-w)/2,y+12),t,font=f,fill=fg)
def brand(im,y=1730,dark=False):
    d=ImageDraw.Draw(im); lg=LOGO.resize((80,69)); x0=W//2-190; im.paste(lg,(x0,y),lg)
    f=ImageFont.truetype(PB,40); x=x0+92
    for wd,c in (("My",TEAL if dark else (255,255,255)),("Campus",PURP if dark else (255,255,255)),("Forum",ORNG if dark else (255,230,200))):
        d.text((x,y+10),wd,font=f,fill=c); x+=d.textlength(wd,font=f)+6

def scene_png(sc,path):
    c1,c2,fg,acc=THEME[sc.get("theme","light" if sc["type"]=="end" else "purple")]
    im=grad(c1,c2); d=ImageDraw.Draw(im)
    if sc["type"] in ("text","end"):
        y=560 if sc["type"]=="text" else 520
        if sc.get("pill"): pill(d,y,sc["pill"],ORNG,(255,255,255)); y+=140
        lines=sc["lines"]
        for i,l in enumerate(lines):
            col=acc if (sc.get("accent_last") and i==len(lines)-1) or (sc["type"]=="end" and l.strip() in (">","+","=")) else fg
            y=ctext(d,y,l,104 if sc["type"]=="text" else 110,col)
        if sc.get("sub"): y=ctext(d,y+50,sc["sub"],44,(90,90,110) if fg==INK else (230,225,245),font=PM)
        if sc.get("button"): pill(d,y+40,sc["button"],INK if fg==INK else (255,255,255),(255,255,255) if fg==INK else INK,38)
        brand(im,dark=(fg==INK))
    else:
        y=ctext(d,170,sc["top"],70,fg)
        s=Image.open(P(sc["shot"])).convert("RGB")
        if sc.get("crop"): s=s.crop(tuple(sc["crop"]))
        w=980; s=s.resize((w,int(s.size[1]*w/s.size[0])),Image.LANCZOS)
        if s.size[1]>1150: s=s.crop((0,0,w,1150))
        sy=y+40; sh=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(sh).rounded_rectangle([58,sy+18,58+w,sy+s.size[1]+18],28,fill=(0,0,0,90))
        sh=sh.filter(ImageFilter.GaussianBlur(20)); im.paste(sh,(0,0),sh)
        m=Image.new("L",s.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,s.size[0]-1,s.size[1]-1],24,fill=255)
        im.paste(s,(50,sy),m)
        if sc.get("bottom"): ctext(d,sy+s.size[1]+50,sc["bottom"],54,fg)
    im.save(path)

def slides(spec,out,tmp):
    parts=[]
    for i,sc in enumerate(spec["scenes"]):
        png=f"{tmp}/s{i}.png"; scene_png(sc,png); du=sc.get("dur",4); n=int(du*30)
        mp=f"{tmp}/p{i}.mp4"
        run(["ffmpeg","-y","-loop","1","-i",png,"-vf",f"scale=2160:3840,zoompan=z='min(zoom+0.0006,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30,format=yuv420p","-t",str(du),"-c:v","libx264","-preset","veryfast","-crf","18",mp])
        parts.append((mp,du))
    inputs=[]; [inputs.extend(["-i",p]) for p,_ in parts]
    fc=[]; off=0; prev="0"; X=0.4; trans=["slideleft","slideleft","slideup","fade","slideleft","slideup"]
    for i in range(1,len(parts)):
        off+=parts[i-1][1]-X if i>1 else parts[0][1]-X
        lab=f"x{i}"; fc.append(f"[{prev}][{i}]xfade=transition={trans[(i-1)%len(trans)]}:duration={X}:offset={off:.2f}[{lab}]"); prev=lab
    total=sum(d for _,d in parts)-X*(len(parts)-1)
    vid=f"{tmp}/v.mp4"
    if len(parts)>1: run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(fc)+f";[{prev}]format=yuv420p[v]","-map","[v]","-c:v","libx264","-preset","medium","-crf","20",vid])
    else: os.rename(parts[0][0],vid)
    mux(vid,out,spec.get("audio_from"),spec.get("audio_start",0),total)

def mux(vid,out,afrom,ast,total):
    if afrom:
        run(["ffmpeg","-y","-i",vid,"-ss",str(ast),"-i",P(afrom),"-map","0:v","-map","1:a","-af",f"afade=t=in:d=0.4,afade=t=out:st={max(total-1.8,0):.2f}:d=1.8","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out])
    else:
        run(["ffmpeg","-y","-i",vid,"-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest","-movflags","+faststart",out])

def clip(spec,out,tmp):
    src=P(spec["source"]); segs=spec["segments"]
    o=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(o)
    y=250
    for i,l in enumerate(spec.get("hook",[])): y=ctext(d,y,l,84,(255,255,255) if i==0 else (255,196,120))
    if spec.get("tag"): ctext(d,y+20,spec["tag"],34,(220,215,240),font=PM)
    brand(o,1660); o.save(f"{tmp}/frame.png")
    lst=open(f"{tmp}/list.txt","w"); t=0; enables=[]
    for i,sg in enumerate(segs):
        run(["ffmpeg","-y","-ss",str(sg["start"]),"-t",str(sg["dur"]),"-i",src,"-an","-c:v","libx264","-preset","veryfast","-crf","18","-r","30",f"{tmp}/c{i}.mp4"])
        lst.write(f"file 'c{i}.mp4'\n")
        if sg.get("caption"):
            c=Image.new("RGBA",(W,H),(0,0,0,0)); cd=ImageDraw.Draw(c); big=len(sg["caption"])<10
            ctext(cd,1330,sg["caption"],96 if big else 58,(255,196,120) if big else (255,255,255)); c.save(f"{tmp}/cap{i}.png")
            enables.append((f"{tmp}/cap{i}.png",t+0.2,t+sg["dur"]))
        t+=sg["dur"]
    lst.close()
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",f"{tmp}/list.txt","-c","copy",f"{tmp}/joined.mp4"])
    ins=["-i",f"{tmp}/joined.mp4","-i",f"{tmp}/frame.png"]; fc=["[0:v]split[a][b]","[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[bg]","[b]scale=1080:-2,setsar=1[fg]","[bg][fg]overlay=0:620[v0]","[v0][1:v]overlay=0:0[v1]"]
    prev="v1"
    for k,(p,a,b) in enumerate(enables):
        ins+=["-i",p]; lab=f"v{k+2}"; fc.append(f"[{prev}][{k+2}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[{lab}]"); prev=lab
    run(["ffmpeg","-y",*ins,"-filter_complex",";".join(fc),"-map",f"[{prev}]","-c:v","libx264","-pix_fmt","yuv420p","-preset","medium","-crf","20","-r","30",f"{tmp}/v.mp4"])
    mux(f"{tmp}/v.mp4",out,spec["source"],spec.get("audio_start",segs[0]["start"]),t)

if __name__=="__main__":
    spec=json.load(open(sys.argv[1])); out=os.path.abspath(sys.argv[2]); os.makedirs(os.path.dirname(out),exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        (slides if spec["kind"]=="slides" else clip)(spec,out,tmp)
    print("saved",out)
