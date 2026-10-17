# AI 신용위기 리포트 차트 생성 (2026-10-17)
# 데이터 출처: 워크스페이스 individual_xlsx (분기 재무 워크북), SEC EDGAR XBRL,
#              이번 주 시장 뉴스(Benzinga/CNN/머니투데이/Reuters), 승도리 턴어라운드 강의 프레임
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MPLCONFIGDIR = os.environ.get("MPLCONFIGDIR", ".mplconfig")
OUT = "charts_ai_crisis"
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.family"] = "Apple SD Gothic Neo"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 170
plt.rcParams["savefig.dpi"] = 170
plt.rcParams["axes.edgecolor"] = "#BBBBBB"
plt.rcParams["axes.linewidth"] = 0.8

NAVY = "#1F3B5C"; BLUE = "#3D7AB8"; TEAL = "#2E8B8B"; GRAY = "#8A8F98"
RED = "#C0392B"; ORANGE = "#D9822B"; LIGHT = "#D8DEE6"; GREEN = "#2E7D4F"

def style_ax(ax):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=9)
    ax.grid(axis="x", color="#E5E5E5", lw=0.7, zorder=0)

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)

# ---------------------------------------------------------------- Chart 1
# 이자커버 스펙트럼 (TTM 영업이익 / TTM 이자비용) — symlog
cov = {"NVDA": 426.7, "GOOGL": 65.6, "MSFT": 50.4, "META": 44.0,
       "AMZN": 28.1, "ORCL": 4.8, "CRWV": -0.1, "NBIS": -2.1}
items = sorted(cov.items(), key=lambda kv: kv[1])
fig, ax = plt.subplots(figsize=(6.6, 4.4))
names = [k for k, _ in items]; vals = [v for _, v in items]
colors = [TEAL if v >= 20 else (ORANGE if v > 0 else RED) for v in vals]
y = np.arange(len(items))
ax.set_xscale("symlog", linthresh=1, linscale=0.6)
ax.set_xlim(-10, 900)
ax.barh(y, vals, color=colors, height=0.62, zorder=3)
for yi, v in zip(y, vals):
    if v >= 0:
        ax.text(v * 1.12 + 1, yi, f"{v:,.1f}x", va="center", ha="left", fontsize=9.5, fontweight="bold")
    else:  # 음수 라벨은 0축 오른쪽 고정 위치에 배치해 기업명과의 충돌 방지
        ax.text(15, yi, f"{v:,.1f}x", va="center", ha="left", fontsize=9.5, fontweight="bold", color=RED)
ax.axvline(20, color=GRAY, lw=1, ls="--", zorder=2)
ax.text(24, len(items) - 1.6, "관계선 20x", fontsize=8.5, color=GRAY)
ax.set_yticks(y, names, fontsize=10.5)
ax.set_xticks([-10, -1, 0, 1, 10, 100, 400])
ax.set_xlabel("TTM 이자커버 (영업이익 ÷ 이자비용, 대수축)", fontsize=9)
style_ax(ax); ax.grid(axis="x", which="both", color="#EEEEEE", lw=0.6)
ax.set_title("이자커버 스펙트럼: 하이퍼스케일러와 네오클라우드 사이에 ORCL", fontsize=12, fontweight="bold", loc="left")
save(fig, "01_interest_coverage")

# ---------------------------------------------------------------- Chart 2
# TTM FCF (USD billion)
fcf = {"NVDA": 127.0, "MSFT": 67.0, "GOOGL": 53.3, "META": 41.0,
       "AMZN": -11.6, "NBIS": -5.9, "CRWV": -13.7, "ORCL": -28.7}
items = sorted(fcf.items(), key=lambda kv: kv[1])
fig, ax = plt.subplots(figsize=(6.6, 4.4))
names = [k for k, _ in items]; vals = [v for _, v in items]
colors = [TEAL if v >= 0 else RED for v in vals]
y = np.arange(len(items))
ax.axvline(0, color="#999999", lw=1)
ax.barh(y, vals, color=colors, height=0.62, zorder=3)
for yi, v in zip(y, vals):
    ax.text(v + (2 if v >= 0 else -2), yi, f"{v:+,.1f}",
            va="center", ha="left" if v >= 0 else "right", fontsize=9.5, fontweight="bold")
ax.set_yticks(y, names, fontsize=10.5)
ax.set_xlabel("TTM 잉여현금흐름 (십억 달러, 영업현금흐름 - CapEx)", fontsize=9)
ax.set_xlim(-40, 145)
style_ax(ax)
ax.set_title("잉여현금흐름: 캐펙스를 자기돈으로 감당하는 기업 vs 그렇지 못한 기업", fontsize=12, fontweight="bold", loc="left")
save(fig, "02_ttm_fcf")

# ---------------------------------------------------------------- Chart 3
# CapEx / 매출 (%)
cx = {"NVDA": 2.4, "AMZN": 22.3, "GOOGL": 29.7, "MSFT": 34.9,
      "META": 39.1, "ORCL": 105.4, "CRWV": 271.0, "NBIS": 822.2}
items = sorted(cx.items(), key=lambda kv: kv[1])
fig, ax = plt.subplots(figsize=(6.6, 4.4))
names = [k for k, _ in items]; vals = [v for _, v in items]
colors = [TEAL if v < 100 else RED for v in vals]
y = np.arange(len(items))
ax.barh(y, vals, color=colors, height=0.62, zorder=3)
for yi, v in zip(y, vals):
    ax.text(v + 10, yi, f"{v:,.1f}%", va="center", fontsize=9.5, fontweight="bold")
ax.axvline(100, color=RED, lw=1.2, ls="--", zorder=2)
ax.text(103, 0.1, "매출 100% 선\n(캐펙스가 매출 초과)", fontsize=8.5, color=RED)
ax.set_yticks(y, names, fontsize=10.5)
ax.set_xlabel("TTM CapEx ÷ TTM 매출 (%)", fontsize=9)
ax.set_xlim(0, 950)
style_ax(ax)
ax.set_title("산업 차원의 스프레드: 캐펙스가 매출을 초과하면 부채로 메운다", fontsize=12, fontweight="bold", loc="left")
save(fig, "03_capex_ratio")

# ---------------------------------------------------------------- Chart 4
# GOOGL 보고 vs 조정 순이익 (분기별, USD million)
q = ["25년 3Q", "25년 4Q", "26년 1Q", "26년 2Q"]
reported = [34979, 34455, 62578, 112193]
adjusted = [26295, 32593, 32714, 35093]
x = np.arange(len(q)); w = 0.36
fig, ax = plt.subplots(figsize=(6.6, 4.4))
b1 = ax.bar(x - w/2, reported, w, color=BLUE, label="보고 순이익", zorder=3)
b2 = ax.bar(x + w/2, adjusted, w, color=NAVY, label="조정 순이익(평가손익 제외, 추정)", zorder=3)
for b in list(b1) + list(b2):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1500,
            f"{b.get_height()/1000:,.1f}", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x, q, fontsize=10)
ax.set_ylabel("순이익 (십억 달러)", fontsize=9)
ax.set_ylim(0, 125000)
ax.legend(fontsize=9, frameon=False, loc="upper left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#EEEEEE", lw=0.7, zorder=0)
ax.set_title("GOOGL: 보고 이익의 절반 이상이 지분증권 평가손익(SpaceX·Anthropic)", fontsize=12, fontweight="bold", loc="left")
save(fig, "04_googl_reported_vs_adjusted")

# ---------------------------------------------------------------- Chart 5
# ORCL 경제적 총의무 구성 변화 (USD million)
dates = ["2026-02-28", "2026-05-31", "2026-08-31"]
bond = [134605, 128073, 125337]   # 회사채·CP (유동+비유동)
fin_lease = [6250, 7701, 9185]
op_lease = [21310, 30190, 34621]
purchase = [11000, 13309, 34150]
x = np.arange(len(dates)); w = 0.55
fig, ax = plt.subplots(figsize=(6.6, 4.4))
p1 = ax.bar(x, bond, w, color=NAVY, label="회사채·CP", zorder=3)
p2 = ax.bar(x, fin_lease, w, bottom=bond, color=TEAL, label="자본리스", zorder=3)
p3 = ax.bar(x, op_lease, w, bottom=[a+b for a, b in zip(bond, fin_lease)], color=BLUE, label="운용리스", zorder=3)
p4 = ax.bar(x, purchase, w, bottom=[a+b+c for a, b, c in zip(bond, fin_lease, op_lease)], color=RED, label="미인식 구매의무(오프밸런스)", zorder=3)
for xi, comps in zip(x, zip(bond, fin_lease, op_lease, purchase)):
    total = sum(comps)
    ax.text(xi, total + 4000, f"총 {total/1000:,.0f}", ha="center", fontsize=10, fontweight="bold")
ax.annotate("한 분기 +21십억 달러\n→ +157%", xy=(2, 185000), xytext=(1.15, 232000),
            fontsize=9.5, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.set_xticks(x, dates, fontsize=10)
ax.set_ylabel("의무 (십억 달러)", fontsize=9)
ax.set_ylim(0, 250000)
ax.legend(fontsize=8.5, frameon=False, loc="upper left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#EEEEEE", lw=0.7, zorder=0)
ax.set_title("ORCL: 대차대조표 밖 구매의무가 한 분기에 2.6배 폭증", fontsize=12, fontweight="bold", loc="left")
save(fig, "05_orcl_hidden_debt")

# ---------------------------------------------------------------- Chart 6
# CRWV 부채 vs 분기 매출
qc = ["24-3Q", "24-4Q", "25-1Q", "25-2Q", "25-3Q", "25-4Q", "26-1Q", "26-2Q"]
crwv_debt = [6278, 10620, 11897, 14563, 18810, 29823, 35147, 51613]
crwv_rev = [584, 747, 982, 1212, 1365, 1572, 2078, 2575]
x = np.arange(len(qc))
fig, ax = plt.subplots(figsize=(6.6, 4.4))
ax.bar(x, [d/1000 for d in crwv_debt], 0.55, color=RED, label="총부채 (좌축, 십억 달러)", zorder=3)
ax2 = ax.twinx()
ax2.plot(x, [r/1000 for r in crwv_rev], color=NAVY, lw=2.2, marker="o", ms=4.5, label="분기 매출 (우축, 십억 달러)")
ax.set_xticks(x, qc, fontsize=9.5)
ax.set_ylabel("총부채 (십억 달러)", fontsize=9)
ax2.set_ylabel("분기 매출 (십억 달러)", fontsize=9)
ax.set_ylim(0, 60); ax2.set_ylim(0, 6)
ax.annotate("부채 2년간 8.2배\n매출은 4.4배", xy=(7, 51.6), xytext=(4.6, 42),
            fontsize=9.5, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=8.5, frameon=False, loc="upper left")
for s in ["top"]:
    ax.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
ax.grid(axis="y", color="#EEEEEE", lw=0.7, zorder=0)
ax.set_title("CRWV: 부채 속도가 매출 속도를 앞지르는 구조", fontsize=12, fontweight="bold", loc="left")
save(fig, "06_crwv_debt_vs_revenue")

# ---------------------------------------------------------------- Chart 7
# 이번 주 시장 급락 (주간 수익률 %)
wk = {"KOSPI": -14.46, "SK하이닉스": -24.3, "삼성전자": -17.8,
      "필라델피아 반도체": -7.88, "나스닥100": -3.07}
items = sorted(wk.items(), key=lambda kv: kv[1])
fig, ax = plt.subplots(figsize=(6.6, 3.6))
names = [k for k, _ in items]; vals = [v for _, v in items]
y = np.arange(len(items))
ax.barh(y, vals, color=RED, height=0.6, zorder=3)
for yi, v in zip(y, vals):
    ax.text(v - 0.5, yi, f"{v:+.2f}%", va="center", ha="right", fontsize=10, fontweight="bold")
ax.set_yticks(y, names, fontsize=10.5)
ax.axvline(0, color="#999999", lw=1)
ax.set_xlabel("2026-10-12 ~ 10-16 주간 수익률 (%)", fontsize=9)
ax.set_xlim(-28, 2)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="x", color="#EEEEEE", lw=0.7, zorder=0)
ax.set_title("이번 주: KOSPI 2008년 이후 최대 주간 낙폭", fontsize=12, fontweight="bold", loc="left")
save(fig, "07_weekly_market")

# ---------------------------------------------------------------- Chart 8
# 네비우스 조정 EBITDA 마진의 실체 (워터폴, 억 달러)
steps = [
    ("AI 클라우드\n매출",        "total", 5.75, "100%", NAVY),
    ("매출원가·판관비\n등",       "dec",   2.89, "",     GRAY),
    ("조정 EBITDA",             "total", 2.86, "49.7%", BLUE),
    ("감가상각비",               "dec",   2.60, "",     RED),
    ("영업이익\n(이자 전)",       "total", 0.26, "≈4.5%", TEAL),
]
fig, ax = plt.subplots(figsize=(6.6, 4.4))
x = np.arange(len(steps))
cum = 0.0
prev_top = None
for xi, (label, kind, v, pct, color) in zip(x, steps):
    if kind == "total":
        cum = v
        ax.bar(xi, v, 0.58, color=color, zorder=3)
    else:  # dec: 이전 수준에서 v만큼 하강하는 부동 막대
        cum -= v
        ax.bar(xi, v, 0.58, bottom=cum, color=color, zorder=3)
    if prev_top is not None:
        ax.plot([xi - 1 + 0.29, xi - 0.29], [prev_top, prev_top], color="#AAAAAA", lw=1, zorder=2)
    prev_top = cum
    if pct:
        ax.text(xi, cum + 0.14, pct, ha="center", fontsize=10.5, fontweight="bold", color=NAVY)
ax.axhline(0, color="#999999", lw=1)
ax.set_xticks(x, [s[0] for s in steps], fontsize=9.5)
ax.set_ylabel("금액 (억 달러)", fontsize=9)
ax.set_ylim(0, 6.8)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#EEEEEE", lw=0.7, zorder=0)
ax.set_title("네비우스 '조정 EBITDA 마진 49.7%'의 실체: 감가상각이 이익을 먹는 구조", fontsize=11.5, fontweight="bold", loc="left")
save(fig, "08_nebius_margin_illusion")

print("ALL CHARTS DONE")
