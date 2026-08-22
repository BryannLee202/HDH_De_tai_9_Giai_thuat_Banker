# -*- coding: utf-8 -*-
"""Đo và vẽ hình so sánh giải thuật Banker với giải thuật đồ thị phân bổ tài nguyên.

Chủ sở hữu: TV7 — dùng cho Chương 3.

Script sinh ra toàn bộ số liệu và hình cho Chương 3, chạy lại lúc nào cũng ra
kết quả tái lập được vì đã cố định hạt giống ngẫu nhiên::

    python -m scripts.so_sanh_hai_giai_thuat

Sản phẩm:

- ``scripts/ket_qua_so_sanh.csv``      — bảng số liệu đưa vào mục 3.5
- ``docs/anh-demo/hinh-3-1.png``       — trạng thái không có chu trình
- ``docs/anh-demo/hinh-3-2.png``       — trạng thái có chu trình, bị từ chối
- ``docs/anh-demo/hinh-3-3.png``       — phản ví dụ: chu trình nhưng không deadlock
- ``docs/anh-demo/hinh-3-4.png``       — biểu đồ thời gian chạy theo n

Hình do chính script này vẽ nên nhóm giải thích được từng nét, không dùng hình
lấy từ nguồn ngoài.
"""

from __future__ import annotations

import csv
import os
import random
import statistics
import sys
import time
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.setrecursionlimit(10000)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle  # noqa: E402

from engine.banker import kiem_tra_an_toan  # noqa: E402
from engine.banker_types import BankerState  # noqa: E402
from engine.do_thi_phan_bo import (  # noqa: E402
    chu_trinh_co_nghia_la_deadlock,
    co_chu_trinh,
    tim_chu_trinh,
    xay_dung_do_thi,
)

CAC_MOC_N = [10, 25, 50, 100, 150, 200, 300]
SO_LOAI_TAI_NGUYEN = 5
SO_LAN_LAP = 20

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THU_MUC_ANH = os.path.join(GOC, "docs", "anh-demo")
DUONG_DAN_CSV = os.path.join(GOC, "scripts", "ket_qua_so_sanh.csv")

plt.rcParams["font.family"] = ["Segoe UI", "DejaVu Sans"]


# --------------------------------------------------------------------------
# Đo hiệu năng
# --------------------------------------------------------------------------

def sinh_ngau_nhien(n: int, m: int) -> BankerState:
    mx = [[random.randint(0, 20) for _ in range(m)] for _ in range(n)]
    alloc = [[random.randint(0, mx[i][j]) for j in range(m)] for i in range(n)]
    need_max = [max(mx[i][j] - alloc[i][j] for i in range(n)) for j in range(m)]
    avail = [int(need_max[j] * 0.6) for j in range(m)]
    return BankerState(available=avail, max=mx, allocation=alloc)


def do_hai_giai_thuat(n: int, m: int, so_lan: int) -> Tuple[float, float]:
    """Trả về (thời gian Banker ms, thời gian đồ thị ms), đều là trung bình."""
    t_banker: List[float] = []
    t_do_thi: List[float] = []

    # Vòng khởi động: lần gọi đầu tiên luôn chậm bất thường do Python còn phải
    # nạp mã, không tính vào số đo.
    for _ in range(3):
        khoi_dong = sinh_ngau_nhien(n, m)
        kiem_tra_an_toan(khoi_dong)
        co_chu_trinh(khoi_dong)

    for _ in range(so_lan):
        tt = sinh_ngau_nhien(n, m)

        b = time.perf_counter()
        kiem_tra_an_toan(tt)
        t_banker.append((time.perf_counter() - b) * 1000.0)

        b = time.perf_counter()
        co_chu_trinh(tt)
        t_do_thi.append((time.perf_counter() - b) * 1000.0)

    return statistics.mean(t_banker), statistics.mean(t_do_thi)


# --------------------------------------------------------------------------
# Vẽ đồ thị phân bổ tài nguyên
# --------------------------------------------------------------------------

def _ve_do_thi(ax, tt: BankerState, tieu_de: str, to_chu_trinh: bool = True) -> None:
    dt = xay_dung_do_thi(tt)
    chu_trinh = tim_chu_trinh(dt) if to_chu_trinh else None
    canh_chu_trinh = set()
    if chu_trinh:
        canh_chu_trinh = {(chu_trinh[k], chu_trinh[k + 1])
                          for k in range(len(chu_trinh) - 1)}

    n, m = tt.n, tt.m
    vi_tri: Dict[str, Tuple[float, float]] = {}
    for i in range(n):
        vi_tri["P{}".format(i)] = ((i + 1) * 10.0 / (n + 1), 3.0)
    for j in range(m):
        vi_tri["R{}".format(tt.ten_tai_nguyen[j])] = ((j + 1) * 10.0 / (m + 1), 0.6)

    need = tt.need
    for i in range(n):
        p = "P{}".format(i)
        for j in range(m):
            r = "R{}".format(tt.ten_tai_nguyen[j])
            if tt.allocation[i][j] > 0:
                canh, mau, net = (r, p), "#16a34a", "-"
            elif need[i][j] > 0:
                canh, mau, net = (p, r), "#dc2626", "--"
            else:
                continue
            trong_ct = canh in canh_chu_trinh
            ax.add_patch(FancyArrowPatch(
                vi_tri[canh[0]], vi_tri[canh[1]],
                arrowstyle="-|>", mutation_scale=13,
                shrinkA=17, shrinkB=17,
                linewidth=2.4 if trong_ct else 1.2,
                linestyle=net,
                color="#7c3aed" if trong_ct else mau,
                zorder=3 if trong_ct else 1))

    for i in range(n):
        x, y = vi_tri["P{}".format(i)]
        ax.add_patch(Circle((x, y), 0.42, facecolor="#bfdbfe",
                            edgecolor="#1e3a8a", linewidth=1.4, zorder=4))
        ax.text(x, y, "P{}".format(i), ha="center", va="center",
                fontsize=10, zorder=5)

    for j in range(m):
        ten = tt.ten_tai_nguyen[j]
        x, y = vi_tri["R{}".format(ten)]
        ax.add_patch(Rectangle((x - 0.42, y - 0.42), 0.84, 0.84,
                               facecolor="#fde68a", edgecolor="#92400e",
                               linewidth=1.4, zorder=4))
        ax.text(x, y, "R{}".format(ten), ha="center", va="center",
                fontsize=10, zorder=5)
        for k in range(tt.total[j]):
            ax.plot(x - 0.22 + k * 0.22, y + 0.26, "o", markersize=2.6,
                    color="#92400e", zorder=6)

    ax.set_xlim(0, 10); ax.set_ylim(-0.4, 4.0)
    ax.set_title(tieu_de, fontsize=11)
    ax.axis("off")


def ve_ba_hinh_do_thi() -> None:
    os.makedirs(THU_MUC_ANH, exist_ok=True)

    # Hình 3.1 — không có chu trình, yêu cầu được chấp thuận
    tt1 = BankerState(available=[0, 1], max=[[1, 1], [1, 1]],
                      allocation=[[1, 0], [0, 0]], ten_tai_nguyen=["1", "2"])
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    _ve_do_thi(ax, tt1, "Hình 3.1 — Không có chu trình: yêu cầu được chấp thuận")
    fig.tight_layout(); fig.savefig(os.path.join(THU_MUC_ANH, "hinh-3-1.png"), dpi=160)
    plt.close(fig)

    # Hình 3.2 — có chu trình, yêu cầu bị từ chối
    tt2 = BankerState(available=[0, 0], max=[[1, 1], [1, 1]],
                      allocation=[[1, 0], [0, 1]], ten_tai_nguyen=["1", "2"])
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    _ve_do_thi(ax, tt2, "Hình 3.2 — Chu trình P0→R2→P1→R1→P0: yêu cầu bị từ chối")
    fig.tight_layout(); fig.savefig(os.path.join(THU_MUC_ANH, "hinh-3-2.png"), dpi=160)
    plt.close(fig)

    # Hình 3.3 — phản ví dụ: R1 có 2 thực thể, có chu trình nhưng không deadlock
    tt3 = BankerState(available=[0, 0], max=[[1, 1], [1, 1], [1, 0]],
                      allocation=[[1, 0], [0, 1], [1, 0]], ten_tai_nguyen=["1", "2"])
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    _ve_do_thi(ax, tt3,
               "Hình 3.3 — R1 có 2 thực thể: có chu trình nhưng KHÔNG deadlock")
    fig.tight_layout(); fig.savefig(os.path.join(THU_MUC_ANH, "hinh-3-3.png"), dpi=160)
    plt.close(fig)


def ve_bieu_do(hang: List[dict]) -> None:
    ns = [h["n"] for h in hang]
    tb = [h["banker_ms"] for h in hang]
    td = [h["do_thi_ms"] for h in hang]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(ns, tb, "o-", color="#1d4ed8", linewidth=2, label="Banker — O(m·n²)")
    ax.plot(ns, td, "s-", color="#b45309", linewidth=2,
            label="Đồ thị phân bổ tài nguyên — O(n·m)")
    ax.set_xlabel("Số tiến trình n  (m = {} cố định)".format(SO_LOAI_TAI_NGUYEN))
    ax.set_ylabel("Thời gian trung bình (ms)")
    ax.set_title("Hình 3.4 — Thời gian chạy của hai giải thuật theo n")
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(THU_MUC_ANH, "hinh-3-4.png"), dpi=160)
    plt.close(fig)


# --------------------------------------------------------------------------

def main() -> None:
    random.seed(2026)
    os.makedirs(THU_MUC_ANH, exist_ok=True)

    print("Đo hai giải thuật, m = {}, lặp {} lần mỗi mốc\n".format(
        SO_LOAI_TAI_NGUYEN, SO_LAN_LAP))
    print("{:>6} {:>14} {:>16} {:>10}".format(
        "n", "Banker (ms)", "Đồ thị (ms)", "tỉ lệ"))

    hang: List[dict] = []
    for n in CAC_MOC_N:
        tb, td = do_hai_giai_thuat(n, SO_LOAI_TAI_NGUYEN, SO_LAN_LAP)
        hang.append({"n": n, "m": SO_LOAI_TAI_NGUYEN, "so_lan_lap": SO_LAN_LAP,
                     "banker_ms": round(tb, 4), "do_thi_ms": round(td, 4),
                     "ti_le_banker_tren_do_thi": round(tb / td, 2) if td else 0})
        print("{:>6} {:>14.4f} {:>16.4f} {:>9.2f}x".format(n, tb, td, tb / td if td else 0))

    with open(DUONG_DAN_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(hang[0].keys()))
        w.writeheader(); w.writerows(hang)
    print("\nĐã ghi:", DUONG_DAN_CSV)

    ve_ba_hinh_do_thi()
    ve_bieu_do(hang)
    print("Đã vẽ 4 hình vào:", THU_MUC_ANH)

    # Phản ví dụ trên chính bộ dữ liệu chuẩn của nhóm
    chuan = BankerState.from_json_file(os.path.join(GOC, "data", "vi-du-chuan.json"))
    print("\nPHẢN VÍ DỤ trên bộ dữ liệu chuẩn của nhóm:")
    print("  Tổng thực thể mỗi loại:", chuan.total, "-> nhiều thực thể")
    print("  Đồ thị phát hiện chu trình :", co_chu_trinh(chuan))
    print("  Kết luận của đồ thị đáng tin:", chu_trinh_co_nghia_la_deadlock(chuan))
    print("  Banker kết luận             :",
          "AN TOÀN" if kiem_tra_an_toan(chuan).an_toan else "KHÔNG AN TOÀN")
    print("  => Đồ thị báo có chu trình nhưng hệ vẫn an toàn. Chu trình chỉ là")
    print("     điều kiện CẦN khi tài nguyên có nhiều thực thể.")


if __name__ == "__main__":
    main()
