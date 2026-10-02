"""Streamlit dashboard: Capital Bikeshare (Washington D.C.), Jan 2011 - Dec 2012.

Run from the project root:  streamlit run dashboard/dashboard.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

DATA_PATH = Path(__file__).resolve().parent / "main_data.csv"

# Design tokens (same as the notebook)
GRAY, BLUE, RED, GREEN, ORANGE = "#B8BEC7", "#2F5D8C", "#C0392B", "#2E8B6B", "#E8833A"
INK, MUTED, WE_COLOR = "#2B2F36", "#5B6270", "#7C8696"
REG, CAS = BLUE, ORANGE
SOURCE = "Sumber: Capital Bikeshare (UCI Bike Sharing Dataset), 1 Jan 2011 – 31 Des 2012"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
SEASON_ORDER = ["Dingin", "Semi", "Panas", "Gugur"]
WEATHER_ORDER = ["Cerah", "Berkabut/Mendung", "Hujan/Salju ringan"]
DAY_GROUPS = ["Hari kerja", "Akhir pekan & libur"]
SEGMENTS = ["Dini hari (00–05)", "Pagi (06–09)", "Siang (10–15)", "Sore (16–19)", "Malam (20–23)"]
TEMP_LABELS = ["<0", "0–5", "5–10", "10–15", "15–20", "20–25", "25–30", "30–35", "≥35"]
TIERS = ["Rendah (<3.000)", "Sedang (3.000–6.000)", "Tinggi (>6.000)"]
TIER_COLORS = [RED, GRAY, GREEN]
COMMUTE = [7, 8, 9, 16, 17, 18, 19]

plt.rcParams.update({
    "figure.dpi": 100, "font.size": 10, "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#E8EAEE", "axes.axisbelow": True,
})


def idn(x, decimals=0):
    """Format a number with Indonesian separators, e.g. 1.234,5."""
    return f"{x:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# --------------------------------------------------------------------------- data
@st.cache_data(show_spinner="Memuat data...")
def load_data():
    """Hourly cleaned data plus a daily table."""
    df = pd.read_csv(DATA_PATH, parse_dates=["datetime"])
    df["date"] = df["datetime"].dt.normalize()
    df["segment"] = pd.cut(df["hour"], bins=[-1, 5, 9, 15, 19, 23], labels=SEGMENTS)
    df["temp_bin"] = pd.cut(df["temp_c"], bins=[-10, 0, 5, 10, 15, 20, 25, 30, 35, 50], labels=TEMP_LABELS, right=False)
    daily = (df.groupby("date")
               .agg(cnt=("cnt", "sum"), casual=("casual", "sum"), registered=("registered", "sum"), year=("year", "first"),
                    month=("month", "first"), season=("season", "first"), day_group=("day_group", "first"),
                    weather=("weather_day", "first"))
               .reset_index())
    daily["tier"] = pd.cut(daily["cnt"], bins=[0, 3000, 6000, np.inf], labels=TIERS, include_lowest=True)
    return df, daily


# --------------------------------------------------------------------------- charts
def add_titles(fig, title, subtitle):
    """Left-aligned takeaway title, subtitle and source note."""
    fig.suptitle(title, x=0.01, y=0.985, ha="left", fontsize=13, fontweight="bold", color=INK)
    fig.text(0.01, 0.915, subtitle, ha="left", fontsize=9.5, color=MUTED)
    fig.text(0.01, 0.012, SOURCE, ha="left", fontsize=8, color=MUTED)


def finish(fig, bottom=0.04):
    fig.tight_layout(rect=[0, bottom, 1, 0.9])
    return fig


def mark(ax, x, y, text, color, dx, dy, ha):
    """Dot on a peak with a label in the same color."""
    ax.scatter([x], [y], color=color, s=36, zorder=3)
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=9, color=color, fontweight="bold")


def chart_hours(wk, we, peaks, reg):
    """Hourly profile (workday vs weekend) and user mix at the peak hours."""
    am, pm, wp = peaks
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4), gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axes[0]
    ax.plot(wk.index, wk.values, color=BLUE, lw=2.8)
    ax.plot(we.index, we.values, color=WE_COLOR, lw=2.4)
    mark(ax, am, wk[am], f"Hari kerja {am:02d}:00\n{wk[am]:.0f} sewa/jam", BLUE, -8, 6, "right")
    mark(ax, pm, wk[pm], f"Hari kerja {pm:02d}:00\n{wk[pm]:.0f} sewa/jam", BLUE, 8, 2, "left")
    mark(ax, wp, we[wp], f"Akhir pekan & libur {wp:02d}:00\n{we[wp]:.0f} sewa/jam", WE_COLOR, 0, 10, "center")
    ax.set_xlim(0, 23.5)
    ax.set_ylim(0, max(wk.max(), we.max()) * 1.25)
    ax.set_xticks(range(0, 24, 3))
    ax.set_xlabel("Jam (waktu setempat)")
    ax.set_ylabel("Rata-rata penyewaan per jam")

    ax = axes[1]
    cats = [f"Hari kerja\n{am:02d}:00", f"Hari kerja\n{pm:02d}:00", f"Akhir pekan & libur\n{wp:02d}:00"]
    reg = np.array(reg)
    y = np.arange(3)[::-1]
    ax.barh(y, reg, color=REG, height=0.55)
    ax.barh(y, 100 - reg, left=reg, color=CAS, height=0.55)
    for yi, r in zip(y, reg):
        ax.text(r / 2, yi, f"{r:.0f}%", ha="center", va="center", color="white", fontweight="bold")
        ax.text(r + (100 - r) / 2, yi, f"{100 - r:.0f}%", ha="center", va="center", color="white", fontweight="bold")
    ax.set_yticks(y, cats)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Persentase penyewa pada jam tersebut (%)")
    ax.grid(axis="y", visible=False)
    ax.legend(handles=[Patch(color=REG, label="Registered"), Patch(color=CAS, label="Casual")], loc="upper center",
              bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False)
    add_titles(fig, f"Hari kerja: dua puncak komuter ({am:02d}:00 dan {pm:02d}:00); akhir pekan: satu puncak siang ({wp:02d}:00)",
               "Rata-rata penyewaan per jam (kiri) dan komposisi pengguna pada jam puncak (kanan), hari terfilter.")
    return finish(fig)


def group_bars(ax, daily, col, order, colors, labels, rng):
    """Mean daily rentals per group, with every day shown as a faint dot."""
    stats = daily.groupby(col, observed=True)["cnt"].agg(["mean", "count"]).reindex(order)
    x = np.arange(len(order))
    bars = ax.bar(x, stats["mean"], color=colors, width=0.62, zorder=2)
    for i, g in enumerate(order):
        pts = daily.loc[daily[col] == g, "cnt"]
        ax.scatter(i + rng.uniform(-0.2, 0.2, len(pts)), pts, s=7, color=INK, alpha=0.2, zorder=3)
    ax.bar_label(bars, labels=labels, padding=3, fontsize=9, fontweight="bold",
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.9))
    ax.set_xticks(x, [f"{g}\nn={int(c)} hari" for g, c in zip(order, stats["count"])])
    ax.set_ylim(0, daily["cnt"].max() * 1.12)
    ax.set_ylabel("Penyewaan per hari")
    ax.grid(axis="x", visible=False)


def hi_lo_colors(means):
    """Green for the highest mean, red for the lowest, gray otherwise."""
    hi, lo = means.idxmax(), means.idxmin()
    return [GREEN if k == hi else RED if (k == lo and hi != lo) else GRAY for k in means.index]


def chart_weather_season(daily):
    """Mean daily rentals by weather and by season."""
    rng = np.random.default_rng(7)
    w_order = [w for w in WEATHER_ORDER if (daily["weather"] == w).any()]
    s_order = [s for s in SEASON_ORDER if (daily["season"] == s).any()]
    w_mean = daily.groupby("weather")["cnt"].mean().reindex(w_order)
    s_mean = daily.groupby("season")["cnt"].mean().reindex(s_order)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), gridspec_kw={"width_ratios": [max(len(w_order), 1) + 0.2, max(len(s_order), 1) + 0.6]})
    base = w_mean.get("Cerah")
    w_labels = [f"{idn(m)}" + (f"\n({(m / base - 1) * 100:+.0f}%)" if base and w != "Cerah" else "") for w, m in w_mean.items()]
    group_bars(axes[0], daily, "weather", w_order, hi_lo_colors(w_mean), w_labels, rng)
    group_bars(axes[1], daily, "season", s_order, hi_lo_colors(s_mean), [idn(m) for m in s_mean], rng)
    axes[0].set_xlabel("Kondisi cuaca")
    axes[1].set_xlabel("Musim")
    add_titles(fig, f"Musim {s_mean.idxmax().lower()} tertinggi dan musim {s_mean.idxmin().lower()} terendah" if len(s_mean) > 1 else "Penyewaan harian per cuaca dan musim",
               "Rata-rata penyewaan harian per cuaca (kiri) dan per musim (kanan); titik = hari individual. Hijau = tertinggi, merah = terendah.")
    return finish(fig)


def chart_growth(monthly, year_mix):
    """Monthly totals, YoY growth per month and user mix per year."""
    yoy = (monthly[2012] / monthly[2011] - 1) * 100
    total = (monthly[2012].sum() / monthly[2011].sum() - 1) * 100
    best, worst = int(yoy.idxmax()), int(yoy.idxmin())
    fmt_k = FuncFormatter(lambda v, _: f"{v / 1000:.0f}")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.4), gridspec_kw={"width_ratios": [1.25, 1.25, 0.7]})

    ax = axes[0]
    ax.plot(range(12), monthly[2011].values, color=BLUE, lw=2.4, marker="o", ms=4)
    ax.plot(range(12), monthly[2012].values, color=GREEN, lw=2.8, marker="o", ms=4)
    ax.text(11.25, monthly.loc[12, 2011], "2011", color=BLUE, va="center", fontweight="bold")
    ax.text(11.25, monthly.loc[12, 2012], "2012", color=GREEN, va="center", fontweight="bold")
    ax.set_xticks(range(12), MONTHS)
    ax.set_xlim(-0.4, 12.2)
    ax.set_ylim(0, monthly.max().max() * 1.12)
    ax.yaxis.set_major_formatter(fmt_k)
    ax.set_ylabel("Total penyewaan per bulan (ribu)")

    ax = axes[1]
    colors = [GREEN if m == best else RED if m == worst else GRAY for m in yoy.index]
    bars = ax.bar(range(12), yoy.values, color=colors, width=0.7)
    ax.bar_label(bars, fmt="%+.0f%%", padding=2, fontsize=8.5)
    ax.axhline(total, color=INK, ls="--", lw=1, label=f"Total 2012 vs 2011: {total:+.1f}%")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.set_xticks(range(12), MONTHS)
    ax.set_ylim(0, yoy.max() * 1.15)
    ax.set_ylabel("Pertumbuhan year-over-year (%)")
    ax.grid(axis="x", visible=False)

    ax = axes[2]
    casual = year_mix["casual"] / year_mix["cnt"] * 100
    ax.bar([0, 1], 100 - casual.values, color=REG, width=0.6)
    ax.bar([0, 1], casual.values, bottom=100 - casual.values, color=CAS, width=0.6)
    for i, c in enumerate(casual.values):
        ax.text(i, (100 - c) / 2, f"{100 - c:.1f}%", ha="center", va="center", color="white", fontweight="bold")
        ax.text(i, 100 - c / 2, f"{c:.1f}%", ha="center", va="center", color="white", fontweight="bold")
    ax.set_xticks([0, 1], ["2011", "2012"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Porsi pengguna (%)")
    ax.grid(axis="x", visible=False)
    ax.legend(handles=[Patch(color=REG, label="Registered"), Patch(color=CAS, label="Casual")], loc="upper center",
              bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=8.5)
    add_titles(fig, f"Penyewaan tumbuh {total:.1f}% pada 2012: tercepat {MONTHS[best - 1]}, terlambat {MONTHS[worst - 1]}",
               "Total bulanan (kiri), pertumbuhan year-over-year per bulan (tengah; hijau = tertinggi, merah = terendah), dan komposisi pengguna (kanan).")
    return finish(fig)


def chart_bins(seg_share, by_temp):
    """Share of rentals per time segment and mean hourly rentals per temperature bin."""
    best, worst = by_temp["mean"].idxmax(), by_temp["mean"].idxmin()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axes[0]
    x = np.arange(len(SEGMENTS))
    for off, grp, color in [(-0.2, DAY_GROUPS[0], BLUE), (0.2, DAY_GROUPS[1], WE_COLOR)]:
        if grp in seg_share.columns:
            bars = ax.bar(x + off, seg_share[grp].values, width=0.38, color=color, label=grp)
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=8.5)
    ax.set_xticks(x, [s.replace(" (", "\n(") for s in SEGMENTS])
    ax.set_ylim(0, max(seg_share.max().max() * 1.15, 1))
    ax.set_ylabel("Porsi penyewaan harian (%)")
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, loc="upper left")

    ax = axes[1]
    colors = [GREEN if b == best else RED if (b == worst and best != worst) else GRAY for b in by_temp.index]
    bars = ax.bar(range(len(by_temp)), by_temp["mean"], color=colors, width=0.7)
    ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=9)
    ax.set_xticks(range(len(by_temp)), [f"{b}\nn={c:,}" for b, c in zip(by_temp.index, by_temp["count"])], fontsize=8)
    ax.set_ylim(0, by_temp["mean"].max() * 1.15)
    ax.set_xlabel("Suhu (°C) dan jumlah jam pengukuran (n)")
    ax.set_ylabel("Rata-rata penyewaan per jam")
    ax.grid(axis="x", visible=False)
    add_titles(fig, f"Rata-rata penyewaan per jam tertinggi pada suhu {best}°C",
               "Porsi penyewaan per segmen waktu (kiri) dan rata-rata penyewaan per jam menurut bin suhu (kanan; hijau = tertinggi, merah = terendah).")
    return finish(fig)


def stacked(ax, table, title):
    """100% stacked horizontal bars of demand tiers."""
    rows = list(table.index[::-1])
    left = np.zeros(len(rows))
    for tier, color in zip(TIERS, TIER_COLORS):
        vals = table.loc[rows, tier].values
        ax.barh(rows, vals, left=left, color=color, height=0.6, label=tier)
        for i, (v, l) in enumerate(zip(vals, left)):
            if v >= 5:
                ax.text(l + v / 2, i, f"{v:.0f}%", ha="center", va="center", fontsize=8.5, color="white" if tier != TIERS[1] else INK)
        left += vals
    ax.set_xlim(0, 100)
    ax.set_xlabel("Persentase hari (%)")
    ax.set_title(title, fontsize=10.5)
    ax.grid(axis="y", visible=False)


def chart_tiers(daily):
    """Demand tiers by season and by weather."""
    def tier_table(col, order):
        order = [o for o in order if (daily[col] == o).any()]
        return pd.crosstab(daily[col], daily["tier"], normalize="index").reindex(index=order, columns=TIERS, fill_value=0) * 100
    overall = daily["tier"].value_counts(normalize=True).reindex(TIERS).fillna(0).to_frame("Semua hari").T * 100
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.9))
    stacked(axes[0], pd.concat([overall, tier_table("season", SEASON_ORDER)]), "Per musim")
    stacked(axes[1], pd.concat([overall, tier_table("weather", WEATHER_ORDER)]), "Per kondisi cuaca")
    fig.legend(handles=[Patch(color=c, label=t) for t, c in zip(TIERS, TIER_COLORS)], loc="lower center", ncol=3,
               frameon=False, bbox_to_anchor=(0.5, 0.05))
    add_titles(fig, f"{overall.loc['Semua hari', TIERS[2]]:.0f}% hari berpermintaan tinggi dan {overall.loc['Semua hari', TIERS[0]]:.0f}% rendah",
               f"Tier permintaan harian: rendah < 3.000, sedang 3.000–6.000, tinggi > 6.000 sewa (n = {len(daily)} hari).")
    return finish(fig, bottom=0.1)


def show(fig):
    st.pyplot(fig)
    plt.close(fig)


# --------------------------------------------------------------------------- page
def main():
    st.set_page_config(page_title="Dashboard Bike Sharing", page_icon="🚲", layout="wide")
    df, daily = load_data()
    d_min, d_max = df["date"].min().date(), df["date"].max().date()

    with st.sidebar:
        st.header("Filter")
        picked = st.date_input("Rentang tanggal", value=(d_min, d_max), min_value=d_min, max_value=d_max)
        seasons = st.multiselect("Musim", SEASON_ORDER, default=SEASON_ORDER)
        weathers = st.multiselect("Cuaca harian", WEATHER_ORDER, default=WEATHER_ORDER)
        if isinstance(picked, (tuple, list)) and len(picked) == 2:
            start, end = picked
        else:
            start, end = d_min, d_max
            st.info("Pilih tanggal akhir untuk menerapkan rentang; sementara seluruh periode ditampilkan.")
        st.divider()
        st.caption("**Musim** memakai pemetaan yang telah dikoreksi: Dingin (Des–Mar), Semi (Mar–Jun), Panas (Jun–Sep), Gugur (Sep–Des).")
        st.caption("**Tier permintaan harian:** rendah < 3.000, sedang 3.000–6.000, tinggi > 6.000 sewa.")

    if not seasons or not weathers:
        st.warning("Pilih minimal satu musim dan satu kondisi cuaca pada panel filter.")
        st.stop()

    t0, t1 = pd.Timestamp(start), pd.Timestamp(end)
    d = df[df["season"].isin(seasons) & df["weather_day"].isin(weathers) & (df["date"] >= t0) & (df["date"] <= t1)]
    dd = daily[daily["season"].isin(seasons) & daily["weather"].isin(weathers) & (daily["date"] >= t0) & (daily["date"] <= t1)]
    if d.empty or dd.empty:
        st.warning("Tidak ada data untuk kombinasi filter ini. Perluas rentang tanggal atau pilihan musim/cuaca.")
        st.stop()

    st.title("🚲 Dashboard Penyewaan Sepeda (Capital Bikeshare)")
    st.caption(f"{start:%d %b %Y} – {end:%d %b %Y} · {len(dd):,} hari · {len(d):,} jam · Washington D.C.")

    hourly_all = d.groupby("hour")["cnt"].mean()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total penyewaan", idn(dd["cnt"].sum()))
    k2.metric("Rata-rata per hari", idn(dd["cnt"].mean()))
    k3.metric("Porsi registered", f"{dd['registered'].sum() / dd['cnt'].sum() * 100:.1f}%", help="Sisanya adalah pengguna casual.")
    k4.metric("Jam puncak", f"{int(hourly_all.idxmax()):02d}:00", help=f"Rata-rata {hourly_all.max():.0f} sewa/jam pada hari terfilter.")

    tabs = st.tabs(["1 · Jam", "2 · Cuaca & musim", "3 · Pertumbuhan", "Analisis lanjutan"])

    # ---- Q1: hours
    with tabs[0]:
        st.subheader("Kapan puncak penyewaan dan siapa penyewanya?")
        prof = d.pivot_table(index="hour", columns="day_group", values="cnt", aggfunc="mean")
        if not all(g in prof.columns for g in DAY_GROUPS):
            st.info("Filter saat ini hanya berisi satu jenis hari. Sertakan hari kerja dan akhir pekan/libur untuk membandingkan pola jam.")
        else:
            wk, we = prof[DAY_GROUPS[0]], prof[DAY_GROUPS[1]]
            am, pm, wp = int(wk.loc[6:10].idxmax()), int(wk.loc[15:20].idxmax()), int(we.idxmax())
            gh = d.groupby(["day_group", "hour"])[["registered", "cnt"]].sum()
            pct = lambda g, h: gh.loc[(g, h), "registered"] / gh.loc[(g, h), "cnt"] * 100
            reg = [pct(DAY_GROUPS[0], am), pct(DAY_GROUPS[0], pm), pct(DAY_GROUPS[1], wp)]
            show(chart_hours(wk, we, (am, pm, wp), reg))
            wk_rows = d[d["day_group"] == DAY_GROUPS[0]]
            commute = wk_rows.loc[wk_rows["hour"].isin(COMMUTE), "cnt"].sum() / wk_rows["cnt"].sum() * 100
            st.info(f"Hari kerja memuncak pukul **{am:02d}:00** ({wk[am]:.0f}) dan **{pm:02d}:00** ({wk[pm]:.0f} sewa/jam); akhir pekan/libur pukul "
                    f"**{wp:02d}:00** ({we[wp]:.0f}). Tujuh jam komuter menampung **{commute:.0f}%** penyewaan hari kerja. Pengguna *registered* "
                    f"**{min(reg[0], reg[1]):.0f}–{max(reg[0], reg[1]):.0f}%** pada puncak hari kerja, tetapi hanya **{reg[2]:.0f}%** pada puncak akhir pekan.")

    # ---- Q2: weather & season
    with tabs[1]:
        st.subheader("Seberapa besar cuaca dan musim memengaruhi penyewaan?")
        show(chart_weather_season(dd))
        w_mean = dd.groupby("weather")["cnt"].mean()
        s_mean = dd.groupby("season")["cnt"].mean()
        text = ""
        if "Cerah" in w_mean.index:
            for w in WEATHER_ORDER[1:]:
                if w in w_mean.index:
                    text += f"Dibanding hari cerah ({idn(w_mean['Cerah'])} sewa/hari), cuaca **{w.lower()}** {(w_mean[w] / w_mean['Cerah'] - 1) * 100:+.0f}% ({idn(w_mean[w])}). "
        if len(s_mean) > 1:
            text += (f"Musim **{s_mean.idxmax()}** tertinggi ({idn(s_mean.max())}/hari) dan **{s_mean.idxmin()}** terendah ({idn(s_mean.min())}/hari), "
                     f"selisih {(s_mean.max() / s_mean.min() - 1) * 100:.0f}%.")
        st.info(text or "Pilih lebih dari satu kondisi cuaca atau musim untuk membandingkan.")

    # ---- Q3: growth (filters ignored so both years are compared on the same footing)
    with tabs[2]:
        st.subheader("Seberapa cepat layanan tumbuh dan siapa yang tumbuh?")
        st.caption("Tab ini memakai seluruh data 2011–2012 agar perbandingan antartahun adil; filter tidak berlaku.")
        monthly = daily.pivot_table(index="month", columns="year", values="cnt", aggfunc="sum")
        year_mix = daily.groupby("year")[["casual", "registered", "cnt"]].sum()
        show(chart_growth(monthly, year_mix))
        yoy = (monthly[2012] / monthly[2011] - 1) * 100
        g = lambda c: (year_mix.loc[2012, c] / year_mix.loc[2011, c] - 1) * 100
        share = year_mix["casual"] / year_mix["cnt"] * 100
        st.info(f"Total penyewaan naik dari {idn(year_mix.loc[2011, 'cnt'])} menjadi {idn(year_mix.loc[2012, 'cnt'])} (**{g('cnt'):+.1f}%**). "
                f"Tertinggi {MONTHS[int(yoy.idxmax()) - 1]} ({yoy.max():+.0f}%), terendah {MONTHS[int(yoy.idxmin()) - 1]} ({yoy.min():+.0f}%). "
                f"*Registered* tumbuh {g('registered'):+.0f}% dan *casual* {g('casual'):+.0f}%, sehingga porsi *casual* turun dari {share[2011]:.1f}% ke {share[2012]:.1f}%.")

    # ---- Advanced: binning
    with tabs[3]:
        st.subheader("Binning: segmen waktu, suhu, dan tier permintaan")
        seg_tab = d.pivot_table(index="segment", columns="day_group", values="cnt", aggfunc="sum", observed=True)
        seg_share = seg_tab / seg_tab.sum() * 100
        by_temp = d.groupby("temp_bin", observed=True)["cnt"].agg(mean="mean", count="count")
        show(chart_bins(seg_share, by_temp))
        st.info(f"Rata-rata penyewaan per jam tertinggi pada suhu **{by_temp['mean'].idxmax()}°C** ({by_temp['mean'].max():.0f} sewa/jam) dan terendah pada "
                f"**{by_temp['mean'].idxmin()}°C** ({by_temp['mean'].min():.0f}). Segmen pagi dan sore menampung "
                f"{seg_share.loc[[SEGMENTS[1], SEGMENTS[3]], DAY_GROUPS[0]].sum():.0f}% penyewaan hari kerja." if DAY_GROUPS[0] in seg_share.columns else
                f"Rata-rata penyewaan per jam tertinggi pada suhu **{by_temp['mean'].idxmax()}°C** ({by_temp['mean'].max():.0f} sewa/jam).")
        show(chart_tiers(dd))
        st.caption("Tier permintaan menjadi aturan operasional sederhana: prakiraan musim dan cuaca dikonversi menjadi jumlah sepeda dan petugas.")
        st.download_button("Unduh data harian terfilter (CSV)", dd.drop(columns=["tier"]).to_csv(index=False),
                           file_name="penyewaan_harian_terfilter.csv", mime="text/csv")

    st.divider()
    st.caption(SOURCE + " · Pembersihan data dan analisis lengkap ada di notebook.ipynb.")


if __name__ == "__main__":
    main()
