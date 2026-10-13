"""Animated generic UI cards (visual, not wordy). Each builder returns f(u) -> RGBA image, u = seconds since the
element appeared. Times inside are offsets from the element's own t_in (remapped by the caller)."""
import math
from PIL import Image, ImageDraw, ImageFont
from stickers import finish, spring, POP_XB, POP_B, HAND, SKY, INK, WHITE, TOMATO, YELLOW, BROWN, NAVY, GRAY

GREEN = (46, 196, 110)
MUTED = (140, 136, 130)
ft = lambda s, w=POP_XB: ImageFont.truetype(w, s)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


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


def wrap(fn):
    """Cache finish() per distinct frame image to keep renders quick."""
    def g(u):
        return finish(fn(u), border=10)
    return g


# 1. fare that climbs after booking -----------------------------------------
def price_ticker(roll_at, chips_at):
    def draw(u):
        w, h = 780, 330
        img = card(w, h); d = ImageDraw.Draw(img)
        d.text((40, 30), 'your fare', font=ft(32, POP_B), fill=MUTED)
        k = ease((u - roll_at) / 1.4)
        val = int(389 + (1240 - 389) * k)
        col = tuple(int(a + (b - a) * k) for a, b in zip((34, 30, 28), TOMATO))
        d.text((40, 70), f'${val:,}', font=ft(110), fill=col)
        # rising trend line
        pts = [(470 + i * 26, 230 - 150 * ease((u - roll_at) / 1.4) * (i / 10) ** 1.6) for i in range(11)]
        d.line(pts[:max(2, int(11 * clamp((u - roll_at) / 1.2)) + 1)], fill=TOMATO, width=9, joint='curve')
        x = 40
        for i, t in enumerate(['+ bags', '+ seat', '+ change fee']):
            a = clamp((u - chips_at[i]) / 0.15)
            if a > 0:
                x += chip(d, x, 248, t, (255, 228, 224), (200, 50, 35), a=a) + 12
        return img
    return wrap(draw)


# 2. itinerary strip with a long layover -------------------------------------
def itinerary(grow_at, bag_at):
    def draw(u):
        w, h = 940, 340
        img = card(w, h); d = ImageDraw.Draw(img)
        L, R, y = 90, w - 90, 150
        g = ease((u - grow_at) / 0.6)
        mid = 300 + 120 * g                      # layover segment widens
        xs = [L, mid - 70, mid + 70 + 90 * g, R]
        d.line([xs[0], y, xs[1], y], fill=INK, width=8)
        d.line([xs[2], y, xs[3], y], fill=INK, width=8)
        for i in range(int((xs[2] - xs[1]) / 26)):   # dotted wait
            x = xs[1] + 13 + i * 26
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=MUTED)
        for x, lab in [(xs[0], 'SFO'), (xs[3], 'DEL')]:
            d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=WHITE, outline=INK, width=8)
            tw = d.textlength(lab, font=ft(40)); d.text((x - tw / 2, y + 34), lab, font=ft(40), fill=INK)
        for x in (xs[1], xs[2]):
            d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=INK)
        lay = f'{int(2 + 9 * g)}h layover'
        f = ft(36); tw = d.textlength(lay, font=f); cx = (xs[1] + xs[2]) / 2
        d.rounded_rectangle([cx - tw / 2 - 22, y - 92, cx + tw / 2 + 22, y - 38], radius=27, fill=YELLOW + (255,))
        d.text((cx - tw / 2, y - 88), lay, font=f, fill=BROWN)
        # plane travelling the route
        p = (u * 0.35) % 1.0
        px = xs[0] + (xs[3] - xs[0]) * p
        d.polygon([(px + 26, y), (px - 16, y - 20), (px - 8, y), (px - 16, y + 20)], fill=SKY)
        # crossed-out bag
        a = clamp((u - bag_at) / 0.2)
        if a > 0:
            bx, by = 120, 250
            d.rounded_rectangle([bx, by + 14, bx + 70, by + 70], radius=12, outline=INK + (int(255 * a),), width=7)
            d.rounded_rectangle([bx + 20, by, bx + 50, by + 18], radius=6, outline=INK + (int(255 * a),), width=6)
            d.line([bx - 10, by + 78, bx + 80, by - 4], fill=TOMATO + (int(255 * a),), width=10)
            d.text((bx + 100, by + 18), 'no checked bag', font=ft(34, POP_B), fill=(200, 50, 35, int(255 * a)))
        return img
    return wrap(draw)


# 3. calendar: flight moves earlier, fee appears ------------------------------
def calendar(interview_at, drag_at, fee_at):
    """Two-week view (8th-21st): interview pops on the 12th, the flight drags from the 20th to the 12th, fee shakes in."""
    def draw(u):
        w, h = 900, 420
        img = card(w, h); d = ImageDraw.Draw(img)
        d.text((40, 24), 'March', font=ft(46), fill=INK)
        cw, ch, x0, y0 = 118, 132, 37, 110
        cell = lambda day: (x0 + ((day - 8) % 7) * cw, y0 + ((day - 8) // 7) * ch)
        for day in range(8, 22):
            x, y = cell(day)
            d.rounded_rectangle([x + 4, y + 4, x + cw - 4, y + ch - 4], radius=16, fill=(246, 245, 242, 255))
            d.text((x + 14, y + 10), str(day), font=ft(30, POP_B), fill=MUTED)
        ia = clamp((u - interview_at) / 0.2)
        if ia > 0:
            x, y = cell(12)
            d.rounded_rectangle([x + 4, y + 4, x + cw - 4, y + ch - 4], radius=16, fill=(255, 224, 102, int(255 * ia)))
            d.text((x + 14, y + 10), '12', font=ft(30, POP_B), fill=(90, 61, 0, int(255 * ia)))
            d.ellipse([x + cw - 40, y + 16, x + cw - 18, y + 38], fill=(255, 93, 74, int(255 * ia)))
            d.text((x + 12, y + 84), 'interview', font=ft(22, POP_B), fill=(90, 61, 0, int(255 * ia)))
        k = ease((u - drag_at) / 0.7)
        (ax, ay), (bx, by) = cell(20), cell(12)
        fx = ax + (bx - ax) * k; fy = ay + (by - ay) * k - 70 * math.sin(math.pi * k)
        yoff = 46 if k < 0.999 else 46
        d.rounded_rectangle([fx + 10, fy + yoff, fx + cw - 10, fy + yoff + 38], radius=19, fill=SKY + (255,))
        d.polygon([(fx + 36, fy + yoff + 19), (fx + 20, fy + yoff + 8), (fx + 25, fy + yoff + 19), (fx + 20, fy + yoff + 30)], fill=INK)
        d.text((fx + 42, fy + yoff + 4), 'flight', font=ft(24, POP_B), fill=INK)
        fa = clamp((u - fee_at) / 0.15)
        if fa > 0:
            shake = 8 * math.sin((u - fee_at) * 60) * math.exp(-(u - fee_at) * 6)
            chip(d, 560 + shake, 24, '+ change fee', TOMATO, WHITE, size=34, a=fa)
        return img
    return wrap(draw)


# 4. incoming call from a real human ------------------------------------------
def call_screen():
    def draw(u):
        w, h = 560, 520
        img = card(w, h, r=48, fill=(0, 39, 100)); d = ImageDraw.Draw(img)   # Travelopod brand navy
        d.text((w / 2 - d.textlength('incoming call', font=ft(28, POP_B)) / 2, 34), 'incoming call', font=ft(28, POP_B), fill=(170, 186, 220))
        cx, cy = w / 2, 210
        for k in range(3):                        # pulsing rings
            ph = (u * 0.9 + k / 3) % 1.0
            r = 70 + 90 * ph
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(124, 198, 255, int(200 * (1 - ph))), width=5)
        d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=GREEN + (255,))
        d.arc([cx - 34, cy - 30, cx + 34, cy + 38], 200, 340, fill=WHITE, width=10)   # headset
        d.rounded_rectangle([cx - 44, cy - 2, cx - 26, cy + 30], radius=6, fill=WHITE)
        d.rounded_rectangle([cx + 26, cy - 2, cx + 44, cy + 30], radius=6, fill=WHITE)
        from stickers import logo_img
        lg = logo_img(330, white=True)
        img.alpha_composite(lg, (int(cx - lg.width / 2), 372))
        for txt, y, f, c in [('support · a real human · 24/7', 372 + lg.height + 20, ft(30, POP_B), (255, 210, 120))]:
            d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=c)
        return img
    return wrap(draw)


# 5. 2 AM lock screen: mom texts, chatbot fails --------------------------------
def lock_screen(mom_at, bot_at):
    def draw(u):
        w, h = 560, 600
        img = card(w, h, r=56, fill=(24, 26, 40)); d = ImageDraw.Draw(img)
        for txt, y, f in [('2:00', 60, ft(130)), ('AM · Tuesday', 220, ft(32, POP_B))]:
            d.text((w / 2 - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=WHITE)
        def notif(y, who, msg, a, ink=INK):
            if a <= 0:
                return
            oy = (1 - ease(a)) * -30
            d.rounded_rectangle([30, y + oy, w - 30, y + 118 + oy], radius=28, fill=(240, 240, 245, int(255 * clamp(a))))
            d.text((56, y + 14 + oy), who, font=ft(28), fill=INK + (int(255 * clamp(a)),))
            d.text((56, y + 58 + oy), msg, font=ft(30, POP_B), fill=ink + (int(255 * clamp(a)),))
        notif(300, 'Mom', 'flight got cancelled??', (u - mom_at) / 0.25)
        notif(440, 'Airline bot', "I didn't understand that.", (u - bot_at) / 0.25, ink=(200, 50, 35))
        return img
    return wrap(draw)


# 6. comment box typing the keyword ------------------------------------------
def comment_box(word='Travelopod', type_at=0.15, per=0.07):
    def draw(u):
        w, h = 860, 170
        img = card(w, h, r=85); d = ImageDraw.Draw(img)
        d.ellipse([28, 30, 138, 140], fill=SKY + (255,))
        n = int(clamp((u - type_at) / (per * len(word))) * len(word))
        txt = word[:n] if n else 'Add a comment…'
        d.text((170, 50), txt, font=ft(58) if n else ft(44, POP_B), fill=INK if n else MUTED)
        if n and n < len(word) and int(u * 4) % 2 == 0:
            x = 170 + d.textlength(txt, font=ft(58)) + 6
            d.rectangle([x, 56, x + 6, 118], fill=INK)
        sa = clamp((u - (type_at + per * len(word))) / 0.15)
        d.ellipse([w - 140, 30, w - 30, 140], fill=(TOMATO if sa > 0 else GRAY) + (255,))
        d.polygon([(w - 108, 60), (w - 52, 85), (w - 108, 110), (w - 98, 85)], fill=WHITE)
        return img
    return wrap(draw)
