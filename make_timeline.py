# -*- coding: utf-8 -*-
import json, collections
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1320
PAPER = (238, 233, 221, 255)
INK   = (20, 19, 15, 255)
RED   = (168, 48, 31, 255)
GREY  = (120, 114, 102, 255)
RULE  = (176, 168, 152, 255)

F = "/System/Library/Fonts/Supplemental/Songti.ttc"
def song(size, idx=0): return ImageFont.truetype(F, size, index=idx)
def mono(size): return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size, index=0)

img = Image.new("RGBA", (W, H), PAPER)
d = ImageDraw.Draw(img)

repos = json.load(open('/tmp/gitee_repos.json'))
months = []
y, m = 2025, 9
while (y, m) <= (2026, 11):
    months.append(f"{y}-{m:02d}")
    m += 1
    if m == 13: y, m = y + 1, 1
cnt = collections.Counter(r['created_at'][:7] for r in repos)
pub = collections.Counter(r['created_at'][:7] for r in repos if not r['private'])

# ---- header
d.text((120, 96), "项目时间线", font=song(76, 0), fill=INK)
d.text((120 + int(d.textlength("项目时间线", font=song(76, 0))) + 34, 128),
       "2025.09 — 2026.11", font=mono(34), fill=GREY)
d.text((120, 214), "Gitee 账号 lushengjie 全部 110 个仓库，按创建月份排列", font=song(30, 3), fill=(70,66,58,255))
d.line([120, 268, W-120, 268], fill=INK, width=3)
d.text((120, 316), "2026.10 之前公开率 21%（13/62），之后 75%（36/48）", font=song(26, 3), fill=(90, 85, 74, 255))
d.text((120, 362), "2026.04 是唯一没有新建仓库的月份；10—11 两个月共 48 个，占总数 44%", font=song(26, 3), fill=(90, 85, 74, 255))

# ---- stats right
stats = [("110", "仓库"), ("49", "公开"), ("61", "私有"), ("48", "最近两月新建")]
sx = W - 120
for val, lab in reversed(stats):
    tw = d.textlength(val, font=song(52, 0)); lw = d.textlength(lab, font=song(20, 3))
    sx -= int(tw)
    d.text((sx, 300), val, font=song(52, 0), fill=INK)
    sx -= int(lw) + 10
    d.text((sx, 330), lab, font=song(20, 3), fill=GREY)
    sx -= 54

# ---- bars
left, right = 130, W - 130
top, base = 470, 940
n = len(months)
slot = (right - left) / n
bw = slot * 0.56
mx = max(cnt.values())
scale = (base - top) / mx

for i, mo in enumerate(months):
    x = left + slot * i + (slot - bw) / 2
    c, p = cnt[mo], pub[mo]
    if c == 0:
        d.text((x + bw/2, base - 26), "0", font=song(24, 3), fill=(150,144,132,255), anchor="mm")
        continue
    hp = p * scale; hn = (c - p) * scale
    d.rectangle([x, base - hn, x + bw, base], fill=(20, 19, 15, 46))
    if hp > 0:
        d.rectangle([x, base - hn - hp, x + bw, base - hn], fill=RED)
    d.text((x + bw/2, base - hn - hp - 34), str(c), font=song(26, 1), fill=INK, anchor="mm")

d.line([left, base, right, base], fill=INK, width=3)
for i, mo in enumerate(months):
    xc = left + slot * i + slot / 2
    d.line([xc, base, xc, base + 8], fill=RULE, width=3)
    d.text((xc, base + 30), mo[2:].replace("-", "."), font=mono(22), fill=GREY, anchor="mm")
    d.text((xc, base + 60), mo[:4], font=mono(18), fill=(150,144,132,255), anchor="mm")

# ---- phase strip
phases = [
    (0, 2, "复现\n与入门"),
    (2, 4, "论文\n与图像工具链"),
    (4, 7, "试衣产品化\n与 Agent"),
    (7, 10, "微服务化\n与小游戏"),
    (10, 12, "行业\nDemo"),
    (12, 13, "基础\n设施"),
    (13, 15, "RepoGo\n与品牌"),
]
py0 = base + 104
for a, b, label in phases:
    x0 = left + slot * a + 3
    x1 = left + slot * b - 3
    d.line([x0, py0, x1, py0], fill=RULE, width=3)
    d.line([x0, py0, x0, py0 + 12], fill=RULE, width=3)
    d.line([x1, py0, x1, py0 + 12], fill=RULE, width=3)
    lines = label.split("\n")
    yy = py0 + 34
    for ln in lines:
        d.text(((x0 + x1) / 2, yy), ln, font=song(24, 3), fill=(70, 66, 58, 255), anchor="ma")
        yy += 36

# ---- legend
lx, ly = left, 1180
d.rectangle([lx, ly, lx + 26, ly + 20], fill=RED)
d.text((lx + 38, ly - 6), "公开", font=song(22, 3), fill=GREY)
d.rectangle([lx + 120, ly, lx + 146, ly + 20], fill=(20, 19, 15, 46))
d.text((lx + 158, ly - 6), "私有", font=song(22, 3), fill=GREY)

d.text((W - 120, 1174), "数据：Gitee API v5 · 2026-11-11", font=song(20, 3), fill=(150, 144, 132, 255), anchor="ra")

img.convert("RGB").save("/tmp/tl/timeline.png", optimize=True)
print("ok")
