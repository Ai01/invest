# -*- coding: utf-8 -*-
"""
基金经理郑希旗下主要基金年度收益率可视化
数据来源：基金定期报告（易方达官网、晨星、证券之星等公开数据）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ---------- 中文字体 ----------
import os
# 显式注册系统中已有的中文字体
cjk_candidates = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
]
for path in cjk_candidates:
    if os.path.exists(path):
        try:
            fm.fontManager.addfont(path)
        except Exception as e:
            print(f"[warn] addfont {path} failed: {e}")

font_candidates = [
    "Noto Sans CJK SC", "Noto Sans CJK JP", "AR PL UMing CN",
    "PingFang SC", "Microsoft YaHei", "SimHei",
]
available = {f.name for f in fm.fontManager.ttflist}
font_name = next((f for f in font_candidates if f in available), None)

if font_name:
    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False
else:
    print("[warn] no CJK font found, Chinese may not render correctly")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

# ---------- 数据 ----------
# 易方达信息产业混合A (001513) 2016-09-27 成立，2017年起有完整年度
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
xxish = [20.85, -18.34, 75.59, 43.98, 24.79, -24.12, -8.83, 24.91, 108.05]   # 信息产业混合A
bench_xxish = [-4.00, -24.85, 37.94, 11.31, 3.46, -21.87, 3.57, 14.84, 31.18]

# 易方达信息行业精选股票A (010013) 2020-08-24 成立，202 axon起有完整年度
years2 = [2020, 2021, 2022, 2023, 2024, 2025]
xxjs = [5.13, 9.26, -27.72, -10.27, 16.50, 104.31]                          # 信息行业精选A
bench_xxjs = [-2.84, -0.98, -24.53, 0.23, 19.00, 46.51]

# 易方达科创板两年定开混合 (506002) 2020-07-28 成立
years3 = [2020, 2021, 2022, 2023, 2024, 2025]
kc = [4.64, 20.61, -19.15, -10.75, 6.93, 67.03]                             # 科创板两年定开

# 易方达全球成长精选混合(QDII) (012920 A人民币) 2022-01-11 成立
years4 = [2022, 2023, 2024, 2025]
qq = [-12.42, 13.02, 37.03, 83.95]                                         # 全球成长精选A

# 2026年（截至二季度末，季度数据拼接）
# 信息产业混合A：2026Q1 3.39%（C类）/ 信息产业A 2026Q1 ~3.4%，Q2 95.79%(C)
# 信息行业精选A：2026Q1 3.38%，Q2 97.14%
# 科创板定开：2026Q1 6.75%，Q2 89.14%
# 全球成长精选A：2026Q1 10.88%(C)，Q2 89.61%(C)
# 注：为不完全年度，标注在图表说明

# ---------- 图1：易方达信息产业混合A 年度收益 ----------
fig, ax = plt.subplots(figsize=(10, 5.8))
x = np.arange(len(years))
colors = ["#c0392b" if v >= 0 else "#2e86de" for v in xxish]
bars = ax.bar(x, xxish, width=0.55, color=colors, label="易方达信息产业混合A（任期年化收益）")
ax.plot(x, bench_xxish, color="#555555", marker="o", ls="--", lw=1.4, label="业绩基准（中证TMT）")
for xi, v in zip(x, xxish):
    ax.text(xi, v + (2 if v >= 0 else -7), f"{v:+.1f}%", ha="center",
            va="bottom" if v >= 0 else "top", fontsize=9)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years])
ax.set_title("郑希代表作：易方达信息产业混合A 年度收益率（2017–2025，任期自2016-09）", fontsize=13)
ax.set_ylabel("年度收益率 %")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("/home/bhh/Desktop/invest/zhengxi_info_industry.png", dpi=150)
plt.close(fig)

# ---------- 图2：4只基金年度收益对比热图/条形 ----------
fig, ax = plt.subplots(figsize=(11, 6.5))
# 构建矩阵 (基金 x 年份 2017-2025)
funds = {
    "信息产业混合A(001513)": {2017: 20.85, 2018: -18.34, 2019: 75.59, 2020: 43.98,
                           2021: 24.79, 2022: -24.12, 2023: -8.83, 2024: 24.91, 2025: 108.05},
    "信息行业精选A(010013)": {2020: 5.13, 2021: 9.26, 2022: -27.72, 2023: -10.27,
                           2024: 16.50, 2025: 104.31},
    "科创板两年定开(506002)": {2020: 4.64, 2021: 20.61, 2022: -19.15, 2023: -10.75,
                           2024: 6.93, 2025: 67.03},
    "全球成长精选(QDII)(012920)": {2022: -12.42, 2023: 13.02, 2024: 37.03, 2025: 83.95},
}
all_years = list(range(2017, 2026))
names = list(funds.keys())
data = np.full((len(names), len(all_years)), np.nan)
for ri, name in enumerate(names):
    for yi, y in enumerate(all_years):
        if y in funds[name]:
            data[ri, yi] = funds[name][y]

vmax = 110
vmin = -30
cmap = plt.cm.RdYlGn
norm = plt.matplotlib.colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
im = ax.imshow(data, cmap=cmap, norm=norm, aspect="auto")
ax.set_xticks(np.arange(len(all_years)))
ax.set_xticklabels([str(y) for y in all_years])
ax.set_yticks(np.arange(len(names)))
ax.set_yticklabels([n.split("(")[0] for n in names], fontsize=9)
# 标注数值
for ri in range(len(names)):
    for ci in range(len(all_years)):
        v = data[ri, ci]
        if not np.isnan(v):
            ax.text(ci, ri, f"{v:+.1f}", ha="center", va="center", fontsize=9,
                    color="white" if abs(v) > 45 else "black")
ax.set_title("郑希管理主要基金年度收益率对比（%）\n注：科创板、QDII、信息行业精选为成立后年度，\n2025年后为AI为主的大幅增长期", fontsize=12)
cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("年度收益率 %")
plt.tight_layout()
plt.savefig("/home/bhh/Desktop/invest/zhengxi_compare.png", dpi=150)
plt.close(fig)

print("done.")
print("available fonts sample:", font_name)
