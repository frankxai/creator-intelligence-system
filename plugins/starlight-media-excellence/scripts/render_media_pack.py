#!/usr/bin/env python3
"""Deterministic conceptual media reference, not a production publisher.

One JSON scene generates original SVG, browser preview, PNG stills, a PDF carousel,
subtitled silent MP4 and a content-addressed receipt. Runtime: cairosvg, pymupdf,
ffmpeg, ffprobe. Never inserts unverified live-product claims or third-party art.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import subprocess
import textwrap
from pathlib import Path

CANVAS = (1080, 1350)
PAPER = '#F2F0E9'
INK = '#0A1520'
MUTED = '#9AA9AE'
ACCENT = '#91DFD5'
AMBER = '#EDAD7A'


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xml(value: str) -> str:
    return html.escape(str(value), quote=True)


def text(x: int, y: int, string: str, size: int, fill: str = PAPER,
         weight: int = 400, letter_spacing: float = -1) -> str:
    return (f'<text x="{x}" y="{y}" fill="{fill}" '
            f'font-family="Inter,Arial,sans-serif" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{letter_spacing}">{xml(string)}</text>')


def composition(scene: dict, index: int, width: int = 1080,
                height: int = 1350) -> str:
    """Single SVG scene renderer for all visual editions."""
    beat = scene['beats'][index]
    wide = width > height
    tall = height >= 1800
    stage = index + 1
    cx = 1340 if wide else 540
    cy = 525 if wide else (1130 if tall else 860)
    radius = 290 if wide else (285 if tall else 210)
    pad = 112 if wide else 90
    title_y = 350 if wide else (370 if tall else 300)
    tsize = 92 if wide else 86
    letters = []
    letters.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    letters.append(f'<rect width="{width}" height="{height}" fill="{INK}"/>')
    # Restrained star-field is deterministic, sparse and subordinate to content.
    for i in range(40):
        x = (i * 347 + 97) % width
        y = (i * 571 + 61) % height
        if (not wide and 205 < x < 880 and 595 < y < 1090) or (wide and 1040 < x < 1660 and 200 < y < 850):
            continue
        letters.append(f'<circle cx="{x}" cy="{y}" r="{1 if i % 3 else 2}" fill="{ACCENT}" opacity=".11"/>')
    letters.append(f'<path d="M{pad},{115 if wide else 100} H{width-pad}" stroke="#58717A" stroke-opacity=".5"/>')
    letters.append(text(pad, 92 if wide else 78, "STARLIGHT  /  MEDIA SYSTEM", 21, PAPER, 600, 3))
    letters.append(text(width-pad-165, 92 if wide else 78, f"0{stage} / 04", 20, ACCENT, 500, 3))
    letters.append(text(pad, title_y-100, beat['step'], 21, ACCENT, 600, 3))
    for k, line in enumerate(beat['headline']):
        letters.append(text(pad, title_y + k*106, line, tsize, PAPER, 600, -4.3))
    if wide:
        letters.append(text(pad, 642, beat['subline'], 31, MUTED, 400, -.5))
        letters.append(f'<path d="M{pad},739 H640" stroke="{ACCENT}" stroke-opacity=".4"/>')
    else:
        subtitle_lines = textwrap.wrap(beat['subline'], width=42, break_long_words=False)
        for sub_i, subtitle in enumerate(subtitle_lines):
            letters.append(text(pad, (610 if tall else 480) + sub_i*43, subtitle, 33, MUTED, 400, -.4))
    # Causal graph: three sources orbit one active, progressively named output.
    for ring_radius, opacity in [(radius+94,.11),(radius+38,.25),(radius,.6)]:
        letters.append(f'<circle cx="{cx}" cy="{cy}" r="{ring_radius}" fill="none" stroke="{ACCENT}" stroke-width="{2 if ring_radius == radius else 1}" opacity="{opacity}"/>')
    letters.append(f'<circle cx="{cx}" cy="{cy}" r="{radius-111}" fill="#102D36" stroke="{ACCENT}" stroke-opacity=".55" stroke-width="1"/>')
    letters.append(f'<circle cx="{cx}" cy="{cy}" r="{radius-146}" fill="#163A42"/>')
    letters.append(text(cx-(95 if len(beat['center']) <= 5 else 110), cy+17, beat['center'], 43, PAPER, 550, -1.5))
    for i, title in enumerate(beat['nodes']):
        angle = -math.pi/2 + (i * (2 * math.pi/3))
        px = cx + int((radius+39)*math.cos(angle))
        py = cy + int((radius+39)*math.sin(angle))
        line_end_x = cx + int((radius-110)*math.cos(angle))
        line_end_y = cy + int((radius-110)*math.sin(angle))
        letters.append(f'<path d="M{line_end_x},{line_end_y} L{px},{py}" stroke="{ACCENT}" stroke-opacity=".7" stroke-width="2"/>')
        letters.append(f'<circle cx="{px}" cy="{py}" r="12" fill="{AMBER}"/>')
        if wide:
            label_x = px - (55 if i == 0 else 78)
            label_y = py + (-29 if i == 0 else 38)
        else:
            label_x = px - (55 if i == 0 else 86)
            label_y = py + (-31 if i == 0 else 40)
        letters.append(text(label_x, label_y, title, 31, PAPER, 500, -.4))
    if wide:
        letters.append(text(pad, 890, beat['footer'], 24, MUTED, 400, -.2))
        fy = height-94
    else:
        letters.append(text(pad, 1670 if tall else 1210, beat['footer'], 31, MUTED, 400, -.2))
        fy = height-80
    letters.append(f'<path d="M{pad},{fy-47} H{width-pad}" stroke="#56737B" stroke-opacity=".45"/>')
    letters.append(text(pad, fy, "SOURCE → STORY → FORMATS → EVIDENCE", 17, ACCENT, 600, 2))
    letters.append(text(width-pad-54, fy, f"{stage:02}", 23, PAPER, 600, 1))
    letters.append('</svg>')
    return ''.join(letters)


def check(scene: dict) -> None:
    if scene.get('schema_version') != 'media-scene.v1':
        raise ValueError('scene schema must be media-scene.v1')
    if scene.get('kind') != 'authored-architecture-illustration':
        raise ValueError('reference renderer only permits authored architectural illustration')
    if len(scene.get('beats', [])) != 4:
        raise ValueError('reference scene requires four beats')
    for i, beat in enumerate(scene['beats']):
        for field in ('step', 'headline', 'subline', 'center', 'nodes', 'footer'):
            if field not in beat:
                raise ValueError(f'beat {i} missing {field}')
        if len(beat['headline']) != 2 or len(beat['nodes']) != 3:
            raise ValueError('each beat requires two headline lines and three graph nodes')
        if len(beat['subline']) > 76 or len(beat['footer']) > 80:
            raise ValueError('copy too long for fixed-size reference composition')
        if any(len(line) > 23 for line in beat['headline']):
            raise ValueError('headline line exceeds composition width')


def html_page(scene: dict) -> str:
    # Native static browser view: keyboard and click navigation without CDN dependencies.
    data = json.dumps(scene, ensure_ascii=False).replace('<', '\\u003c')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Starlight Media Reference · interactive story</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#061019;color:#f2f0e9;font-family:Inter,Arial,sans-serif}
main{min-height:100vh;display:grid;place-items:center;grid-template-columns:minmax(280px,740px) minmax(200px,330px);gap:clamp(22px,4vw,76px);padding:3vw 5vw}
figure{margin:0;max-height:88vh}figure img{height:min(85vh,900px);max-width:100%;object-fit:contain;border:1px solid #2b454d}
aside{align-self:center;max-width:340px}.kicker{font-size:12px;letter-spacing:.24em;color:#91dfd5;text-transform:uppercase}
h1{font-size:clamp(30px,4vw,55px);line-height:1.09;letter-spacing:-.05em;margin:20px 0}p{font-size:16px;line-height:1.65;color:#b0bdbe}
button{appearance:none;border:1px solid #6c878d;border-radius:2px;background:transparent;color:#f2f0e9;font-size:15px;padding:12px 21px;cursor:pointer}button:hover,button:focus{background:#163a42;outline:2px solid #91dfd5;outline-offset:2px}
.controls{display:flex;gap:12px;margin:32px 0}.counter{font-variant-numeric:tabular-nums;color:#91dfd5;font-size:13px;letter-spacing:.12em}
small{color:#79969c;font-size:12px;line-height:1.55;display:block;margin-top:30px}
@media(max-width:850px){main{grid-template-columns:1fr;padding:20px;gap:4px}figure{margin:auto}figure img{height:auto;max-height:65vh}aside{max-width:620px;width:100%;margin:0 auto}}
</style></head><body><main><figure><img id="visual" alt="" src="carousel-01.svg"></figure><aside><div class="kicker">Starlight / interactive reference</div>
<div class="counter" id="counter" aria-live="polite"></div><h1 id="heading"></h1><p id="copy"></p><div class="controls"><button id="prev" type="button" aria-label="Previous beat">← Back</button><button id="next" type="button" aria-label="Next beat">Next →</button></div>
<small>Original architectural illustration. No live app, deployed hooks or actual publication is represented. ← / → keys move between beats.</small></aside></main>
<script>const scene=__DATA__;let index=0;const visual=document.getElementById('visual');const heading=document.getElementById('heading');const copy=document.getElementById('copy');const counter=document.getElementById('counter');
function paint(){const b=scene.beats[index];visual.src=`carousel-${String(index+1).padStart(2,'0')}.svg`;visual.alt=`${b.step}: ${b.headline.join(' ')}. ${b.subline}`;heading.textContent=b.headline.join(' ');copy.textContent=b.subline;counter.textContent=`${index+1} / ${scene.beats.length}`}
function move(d){index=(index+d+scene.beats.length)%scene.beats.length;paint()}
document.getElementById('prev').addEventListener('click',()=>move(-1));document.getElementById('next').addEventListener('click',()=>move(1));document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')move(-1);if(e.key==='ArrowRight')move(1)});paint();</script></body></html>'''.replace('__DATA__', data)


def process(argv: list[str] | None = None) -> dict:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    default_scene = root/'examples/media-excellence/scene.json'
    if not default_scene.exists():
        default_scene = root/'assets/reference/scene.json'
    ap.add_argument('--scene', type=Path, default=default_scene)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--skip-video', action='store_true')
    args = ap.parse_args(argv)
    scene_path = args.scene.resolve()
    scene = json.loads(scene_path.read_text(encoding='utf8'))
    check(scene)
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    import cairosvg
    import fitz
    from PIL import Image

    artifacts=[]
    docs=[]
    for i in range(4):
        svg_path=out/f'carousel-{i+1:02d}.svg'
        png_path=out/f'carousel-{i+1:02d}.png'
        svg_path.write_text(composition(scene,i),encoding='utf8')
        cairosvg.svg2png(bytestring=svg_path.read_bytes(),write_to=str(png_path))
        docs.append(fitz.open(stream=cairosvg.svg2pdf(bytestring=svg_path.read_bytes()),filetype='pdf'))
        artifacts += [svg_path,png_path]
    merged=fitz.open()
    for doc in docs:
        merged.insert_pdf(doc)
        doc.close()
    pdf=out/'carousel.pdf'
    # PyMuPDF otherwise emits random PDF trailer IDs even for identical pages.
    # Seed both IDs from the frozen scene so repeated renders are byte-identical.
    source_digest = hashlib.sha256(scene_path.read_bytes()).hexdigest().upper()
    merged.xref_set_key(-1, 'ID', f'[<{source_digest[:32]}> <{source_digest[32:64]}>]')
    merged.save(str(pdf),garbage=4,deflate=True,no_new_id=True)
    merged.close()
    artifacts.append(pdf)
    wide=out/'wide-architecture.svg'
    wide.write_text(composition(scene,2,1920,1080),encoding='utf8')
    wide_png=out/'wide-architecture.png'
    cairosvg.svg2png(bytestring=wide.read_bytes(),write_to=str(wide_png))
    artifacts.extend([wide,wide_png])
    preview=out/'scene.html'
    preview.write_text(html_page(scene),encoding='utf8')
    artifacts.append(preview)
    if not args.skip_video:
        for i in range(4):
            portrait_svg = composition(scene, i, 1080, 1920)
            portrait_path = out/f'short-frame-{i+1:02d}.png'
            cairosvg.svg2png(bytestring=portrait_svg.encode('utf8'), write_to=str(portrait_path))
            artifacts.append(portrait_path)
    caption=out/'captions.vtt'
    cue=[]
    for i, beat in enumerate(scene['beats']):
        cue.append(f'{i+1}\n00:00:{i*2:02}.000 --> 00:00:{(i+1)*2:02}.000\n'+ ' '.join(beat['headline']) + '\n')
    caption.write_text('WEBVTT\n\n'+'\n'.join(cue),encoding='utf8')
    artifacts.append(caption)
    if not args.skip_video:
        # The four static compositions become a deterministic visual progression.
        # Each transition replaces the active graph and argument; no fake UI footage.
        vf=[]
        for i in range(4):
            src=out/f'short-frame-{i+1:02d}.png'
            # xfade input timestamp/loop behavior is affected by output timebase;
            # use explicit source durations, framerate and pixel format.
            vf += ['-loop','1','-framerate','24','-t','2.3','-i',str(src)]
        filters=[]
        for i in range(4):
            filters.append(f'[{i}:v]format=yuv420p,setsar=1,settb=AVTB,fps=24[v{i}]')
        filters += ['[v0][v1]xfade=transition=fade:duration=0.3:offset=1.7[x1]',
                    '[x1][v2]xfade=transition=fade:duration=0.3:offset=3.7[x2]',
                    '[x2][v3]xfade=transition=fade:duration=0.3:offset=5.7[vout]']
        video=out/'architecture-short.mp4'
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',*vf,'-filter_complex',';'.join(filters),'-map','[vout]',
             '-t','8','-c:v','libx264','-crf','22','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
        subprocess.run(cmd,check=True)
        artifacts.append(video)
    records=[{'path':p.name,'bytes':p.stat().st_size,'sha256':fingerprint(p)} for p in sorted(artifacts)]
    manifest={
        'schema_version':'media-rendition-receipt.v1',
        'work_id':scene['work_id'],
        'brand':scene['brand'],
        'kind':scene['kind'],
        'source_revision':fingerprint(scene_path),
        'source_path':str(scene_path.name),
        'rights':scene['rights'],
        'evidence_note':scene['evidence_note'],
        'artifacts':records,
        'state':{'render':'RENDERED','qa':'NOT_REVIEWED','approval':'NOT_GRANTED','publication':'NOT_PUBLISHED'},
        'claims':{'live_product_proof':False,'production_hooks_deployed':False},
        'runner':{'script':'scripts/render_media_pack.py','video_rendered':not args.skip_video},
    }
    manifest_path=out/'manifest.json'
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
    print(f'Generated {len(records)} render artifacts at {out}')
    return manifest


if __name__ == '__main__':
    process()
