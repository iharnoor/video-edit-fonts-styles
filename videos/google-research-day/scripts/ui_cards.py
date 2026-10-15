"""Animated generic UI cards for the Google Research@ reel (pattern from videos/travelopod/scripts/ui_cards.py).
Each builder returns f(u) -> RGBA sticker, u = seconds since the card appeared. Offsets passed in are relative
to the card's own t_in, so cards re-sync automatically when the word timings change."""
import math, os
from PIL import Image, ImageDraw, ImageFont
from common import *
from stickers import finish

ft = lambda s, w=POP_XB: ImageFont.truetype(w, s)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    return 1 - (1 - clamp(x)) ** 3


def card(w, h, r=36, fill=WHITE):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=fill + (255,))
    return img


def chip(d, x, y, text, bg, ink, size=30, a=1.0):
    f = ft(size, POP_B)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 36, y + size + 22], radius=(size + 22) // 2, fill=bg + (int(255 * a),))
    d.text((x + 18, y + 8), text, font=f, fill=ink + (int(255 * a),))
    return tw + 36


def header(d, n, title, w):
    """Small '1/7' counter + title, so the list structure reads at a glance."""
    d.rounded_rectangle([30, 26, 118, 74], radius=24, fill=INK + (255,))
    d.text((48, 30), f'{n}/7', font=ft(30), fill=WHITE)
    d.text((136, 28), title, font=ft(36), fill=INK)


def wrap(fn):
    return lambda u: finish(fn(u), border=10)


def fig(name):
    return Image.open(os.path.join(PAGES, name)).convert('RGBA')


# 0. hook: "Google Research" badge + chatbots struck out -------------------------------------
def research_badge():
    def draw(u):
        f = ft(56); tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        tw = tmp.textlength('Google Research', font=f)
        img = card(int(tw) + 130, 120, r=60); d = ImageDraw.Draw(img)
        x = 40
        for i, c in enumerate([GBLUE, (234, 67, 53), (251, 188, 5), (52, 168, 83)]):     # four-dot accent, not the logo
            d.ellipse([x + (i % 2) * 22, 34 + (i // 2) * 22, x + 18 + (i % 2) * 22, 52 + (i // 2) * 22], fill=c + (255,))
        d.text((104, 26), 'Google Research', font=f, fill=INK)
        return img
    return wrap(draw)


def not_chatbots(strike_at):
    def draw(u):
        img = card(560, 250); d = ImageDraw.Draw(img)
        d.rounded_rectangle([40, 40, 420, 130], radius=30, fill=(54, 120, 255, 255))
        d.text((70, 58), 'hi! how can I help?', font=ft(34, POP_B), fill=WHITE)
        d.rounded_rectangle([140, 150, 520, 220], radius=28, fill=GRAY + (255,))
        d.text((170, 162), 'another chatbot…', font=ft(32, POP_B), fill=INK)
        k = ease((u - strike_at) / 0.25)
        if k > 0:
            d.line([30, 220, 30 + 500 * k, 40 + 0 * k], fill=TOMATO, width=16)
        return img
    return wrap(draw)


# 1. Earth AI: questions -> map answers -> agent workflow -----------------------------------------
def earth_query(q_ats, pin_at):
    qs = ['where do I build a data center?', 'which areas flood?', 'where to invest?']
    def draw(u):
        w, h = 900, 400
        img = card(w, h); d = ImageDraw.Draw(img)
        header(d, 1, 'Earth AI', w)
        # map panel
        mx, my, mw, mh = 30, 100, 400, 270
        d.rounded_rectangle([mx, my, mx + mw, my + mh], radius=24, fill=(214, 236, 222, 255))
        for i in range(6):
            d.line([mx, my + 45 * i, mx + mw, my + 20 + 45 * i], fill=(190, 220, 200, 255), width=4)
        d.ellipse([mx + 180, my + 60, mx + 360, my + 240], fill=(124, 198, 255, 110))              # river/flood blob
        for k, (px, py, col) in enumerate([(110, 150, TOMATO), (290, 120, SKY), (220, 230, YELLOW)]):
            a = ease((u - pin_at - k * 0.25) / 0.3)
            if a > 0:
                r = 22 * a; cx, cy = mx + px, my + py
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,), outline=WHITE, width=5)
        # questions typing in
        y = 108
        for i, qt in enumerate(q_ats):
            n = int(len(qs[i]) * clamp((u - qt) / 0.6))
            if n > 0:
                d.rounded_rectangle([450, y, 870, y + 72], radius=26, fill=GRAY + (255,))
                d.text((472, y + 18), qs[i][:n], font=ft(25, POP_B), fill=INK)
            y += 88
        return img
    return wrap(draw)


def agent_workflow(src_ats, step_ats):
    srcs = [('satellite', SKY), ('weather', YELLOW), ('population', TOMATO), ('70+ tools', INK)]
    steps = ['plan', 'gather data', 'spatial analysis']
    def draw(u):
        w, h = 900, 400
        img = card(w, h); d = ImageDraw.Draw(img)
        d.rounded_rectangle([340, 40, 560, 110], radius=34, fill=GBLUE + (255,))
        d.text((380, 52), 'Gemini', font=ft(40), fill=WHITE)
        x = 30
        for i, (s, c) in enumerate(srcs):
            a = clamp((u - src_ats[i]) / 0.2)
            if a > 0:
                tw = chip(d, x, 140, s, c if c != INK else INK, WHITE if c in (TOMATO, INK) else INK, size=27, a=a)
                d.line([x + tw / 2, 140, 450, 112], fill=(200, 200, 205, int(255 * a)), width=3)
                x += tw + 14
        x = 40
        for i, s in enumerate(steps):
            on = u >= step_ats[i]
            f = ft(32, POP_B); tw = d.textlength(s, font=f)
            d.rounded_rectangle([x, 260, x + tw + 50, 330], radius=20, fill=(GREEN if on else GRAY) + (255,))
            d.text((x + 25, 274), s, font=f, fill=WHITE if on else MUTED)
            if i < 2:
                d.text((x + tw + 62, 268), '›', font=ft(44), fill=INK if on else MUTED)
            x += tw + 110
        return img
    return wrap(draw)


# 2. AI scientists: agents wiring up + catheter sim bar ------------------------------------------
def agents_graph(link_at, sim_at, hyp_at):
    nodes = [(170, 190), (330, 120), (330, 280), (490, 200)]
    def draw(u):
        w, h = 900, 400
        img = card(w, h); d = ImageDraw.Draw(img)
        header(d, 2, 'AI scientists', w)
        k = clamp((u - link_at) / 0.9)
        for i, (a, b) in enumerate([(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)]):
            kk = clamp(k * 5 - i)
            if kk > 0:
                (x1, y1), (x2, y2) = nodes[a], nodes[b]
                d.line([x1, y1, x1 + (x2 - x1) * kk, y1 + (y2 - y1) * kk], fill=(160, 160, 170, 255), width=5)
        for i, (x, y) in enumerate(nodes):
            d.ellipse([x - 38, y - 38, x + 38, y + 38], fill=[SKY, YELLOW, TOMATO, GREEN][i] + (255,))
            d.text((x - 14, y - 22), '◆' if i == 3 else '•', font=ft(36), fill=WHITE)
        # catheter simulation
        d.text((590, 110), 'catheter sim', font=ft(28, POP_B), fill=MUTED)
        d.rounded_rectangle([590, 150, 870, 190], radius=20, fill=GRAY + (255,))
        s = ease((u - sim_at) / 1.2)
        if s > 0:
            d.rounded_rectangle([590, 150, 590 + 280 * s, 190], radius=20, fill=GREEN + (255,))
            d.text((590, 200), 'fewer infections', font=ft(26, POP_B), fill=(30, 140, 80))
            d.text((590, 234), '(in simulation)', font=ft(24, POP_B), fill=MUTED)
        if u >= hyp_at:
            a = clamp((u - hyp_at) / 0.2)
            chip(d, 590, 300, 'new hypothesis', YELLOW, BROWN, size=28, a=a)
        return img
    return wrap(draw)


# 3. Deep Review: doc gets checked, mistakes flagged, counter ------------------------------------
def deep_review(scan_at, flag_ats, count_at):
    def draw(u):
        w, h = 900, 420
        img = card(w, h); d = ImageDraw.Draw(img)
        header(d, 3, 'Deep Review', w)
        d.rounded_rectangle([30, 100, 470, 400], radius=20, fill=(248, 248, 250, 255))
        rows = [(60, 130, 400), (60, 170, 360), (60, 210, 420), (60, 250, 300), (60, 290, 400), (60, 330, 340), (60, 370, 380)]
        for x, y, ln in rows:
            d.rounded_rectangle([x, y, x + ln, y + 14], radius=7, fill=(205, 205, 212, 255))
        for i, r in enumerate([2, 5]):
            a = clamp((u - flag_ats[i]) / 0.2)
            if a > 0:
                x, y, ln = rows[r]
                for k in range(0, ln, 16):
                    d.line([x + k, y + 22, x + k + 8, y + 30, x + k + 16, y + 22], fill=TOMATO + (int(255 * a),), width=4)
        s = clamp((u - scan_at) / 1.6)
        if 0 < s < 1:
            yy = 110 + 280 * s
            d.rectangle([30, yy, 470, yy + 6], fill=SKY + (255,))
        # counter
        n = int(16000 * ease((u - count_at) / 1.2))
        if u >= count_at:
            d.text((510, 140), f'{n:,}+', font=ft(84), fill=INK)
            d.text((514, 240), 'research papers', font=ft(30, POP_B), fill=MUTED)
            d.text((514, 280), 'reviewed by an', font=ft(30, POP_B), fill=MUTED)
            d.text((514, 320), 'earlier version', font=ft(30, POP_B), fill=MUTED)
        return img
    return wrap(draw)


# 4. Edge AI: official chip photo + devices + on-device ------------------------------------------
def edge_chip(dev_ats, local_at):
    devs = ['glasses', 'watch', 'camera', 'voice']
    photo = fig('fig_03.png')
    def draw(u):
        w, h = 900, 420
        img = card(w, h); d = ImageDraw.Draw(img)
        header(d, 4, 'Edge AI chip', w)
        ph = photo.copy(); ph.thumbnail((400, 260))
        img.alpha_composite(ph, (30, 110))
        d.text((40, 372), 'Synaptics chip · next to a coin', font=ft(24, POP_B), fill=MUTED)
        y = 110
        for i, s in enumerate(devs):
            a = clamp((u - dev_ats[i]) / 0.2)
            if a > 0:
                chip(d, 470, y, s, SKY if i % 2 == 0 else YELLOW, INK if i % 2 == 0 else BROWN, size=30, a=a)
            y += 64
        if u >= local_at:
            a = clamp((u - local_at) / 0.25)
            d.rounded_rectangle([660, 300, 880, 370], radius=34, fill=GREEN + (int(255 * a),))
            d.text((690, 314), 'on-device', font=ft(32, POP_B), fill=WHITE + (int(255 * a),))
        return img
    return wrap(draw)


# 5. AI for numbers: forecast line drawing + table filling --------------------------------------
def numbers(line_at, table_at):
    import random
    rnd = random.Random(7)
    hist = [120 + 25 * math.sin(i / 2.2) + rnd.uniform(-12, 12) for i in range(26)]
    def draw(u):
        w, h = 900, 400
        img = card(w, h); d = ImageDraw.Draw(img)
        header(d, 5, 'TimesFM + TabFM', w)
        x0, y0 = 40, 340
        k = clamp((u - line_at) / 1.4)
        n = max(2, int(len(hist) * k))
        pts = [(x0 + i * 14, y0 - hist[i]) for i in range(n)]
        d.line(pts, fill=INK, width=5, joint='curve')
        if k >= 1:
            f = clamp((u - line_at - 1.4) / 0.8)
            fp = [(x0 + (25 + i) * 14, y0 - (hist[-1] + 30 * math.sin(i / 2.2 + 1) + i * 3)) for i in range(int(14 * f) + 1)]
            if len(fp) > 1:
                d.line([pts[-1]] + fp, fill=TOMATO, width=6, joint='curve')
            d.text((x0 + 26 * 14, 110), 'forecast', font=ft(26, POP_B), fill=TOMATO)
        # table
        tx = 620
        for r in range(5):
            for c in range(2):
                a = clamp((u - table_at - (r * 2 + c) * 0.08) / 0.15)
                col = (GRAY if r else SKY)
                d.rounded_rectangle([tx + c * 125, 110 + r * 50, tx + c * 125 + 115, 150 + r * 50], radius=10, fill=col + (int(255 * max(a, 0.25)),))
        return img
    return wrap(draw)


# 6. Medical AI: AMIE study ring --------------------------------------------------------------
def amie_study(pat_at, ring_at, caution_at):
    def draw(u):
        w, h = 900, 400
        img = card(w, h); d = ImageDraw.Draw(img)
        header(d, 6, 'AMIE · medical AI', w)
        n = int(98 * ease((u - pat_at) / 0.9))
        if u >= pat_at:
            d.text((50, 120), f'{n}', font=ft(110), fill=INK)
            d.text((54, 260), 'patients before', font=ft(30, POP_B), fill=MUTED)
            d.text((54, 298), 'urgent care', font=ft(30, POP_B), fill=MUTED)
        cx, cy, r = 650, 230, 120
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GRAY, width=26)
        p = 0.75 * ease((u - ring_at) / 1.2)
        if p > 0:
            d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * p, fill=GREEN, width=26)
            pct = f'{int(round(p * 100))}%'
            f = ft(64); tw = d.textlength(pct, font=f)
            d.text((cx - tw / 2, cy - 44), pct, font=f, fill=INK)
            d.text((cx - 80, cy + 30), 'helped prep', font=ft(24, POP_B), fill=MUTED)
        if u >= caution_at:
            chip(d, 360, 330, 'research · not for diagnosis', YELLOW, BROWN, size=24, a=clamp((u - caution_at) / 0.2))
        return img
    return wrap(draw)


# 7. Disasters: flood events counter on the official map + 24h alert ------------------------------
def groundsource(count_at, alert_at):
    m = fig('fig_07.png')
    def draw(u):
        w, h = 900, 440
        img = card(w, h); d = ImageDraw.Draw(img)
        header(d, 7, 'Groundsource', w)
        mp = m.copy(); mp.thumbnail((520, 320))
        img.alpha_composite(mp, (20, 100))
        v = 2.6 * ease((u - count_at) / 1.3)
        if u >= count_at:
            d.text((560, 120), f'{v:.1f}M', font=ft(84), fill=INK)
            d.text((566, 222), 'flood events', font=ft(30, POP_B), fill=MUTED)
        if u >= alert_at:
            a = clamp((u - alert_at) / 0.2)
            d.rounded_rectangle([560, 300, 880, 400], radius=26, fill=TOMATO + (int(255 * a),))
            d.text((588, 312), 'flash flood', font=ft(30, POP_B), fill=WHITE + (int(255 * a),))
            d.text((588, 350), '24 hrs ahead', font=ft(32), fill=WHITE + (int(255 * a),))
        return img
    return wrap(draw)


# takeaway: text -> reasoning over the world ---------------------------------------------------
def takeaway(shift_at, item_ats):
    items = [('planet data', SKY), ('science checks', YELLOW), ('medical', TOMATO), ('devices', GREEN)]
    def draw(u):
        w, h = 900, 300
        img = card(w, h); d = ImageDraw.Draw(img)
        d.rounded_rectangle([40, 40, 330, 120], radius=30, fill=GRAY + (255,))
        d.text((70, 58), 'AI = text', font=ft(36, POP_B), fill=INK)
        if u >= shift_at:
            d.line([60, 82, 310, 82], fill=TOMATO, width=10)
            d.line([370, 82, 450, 82], fill=INK, width=9)                       # drawn arrow (Poppins has no → glyph)
            d.line([425, 60, 452, 82, 425, 104], fill=INK, width=9, joint='curve')
            d.text((480, 58), 'AI that reasons', font=ft(36, POP_B), fill=INK)
        x, y = 40, 160
        for i, (s, c) in enumerate(items):
            if u >= item_ats[i]:
                tw = chip(d, x, y, s, c, WHITE if c in (TOMATO, GREEN) else INK, size=32, a=clamp((u - item_ats[i]) / 0.2))
                x += tw + 16
                if i == 1:
                    x, y = 40, 225
        return img
    return wrap(draw)


# CTA: poll card ---------------------------------------------------------------------------------
def poll(bar_at):
    opts = ['Earth AI', 'AI scientists', 'Deep Review', 'Edge chip', 'TimesFM', 'Medical AI', 'Flood AI']
    vals = [0.8, 0.55, 0.7, 0.45, 0.5, 0.35, 0.6]
    def draw(u):
        w, h = 900, 470
        img = card(w, h); d = ImageDraw.Draw(img)
        d.text((40, 26), 'which would you build with?', font=ft(40), fill=INK)
        for i, o in enumerate(opts):
            y = 96 + i * 52
            k = ease((u - bar_at - i * 0.08) / 0.6) * vals[i]
            d.rounded_rectangle([40, y, 40 + 820 * max(k, 0.02), y + 40], radius=20, fill=(SKY if i % 2 == 0 else YELLOW) + (255,))
            d.text((58, y + 2), o, font=ft(28, POP_B), fill=INK)
        return img
    return wrap(draw)
