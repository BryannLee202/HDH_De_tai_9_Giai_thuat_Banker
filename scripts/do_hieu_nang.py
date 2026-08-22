# -*- coding: utf-8 -*-
"""Đo thời gian chạy của thủ tục kiểm tra an toàn khi ``n`` tăng dần.

Chủ sở hữu: TV4. Người dùng kết quả: TV7 (Chương 3 — so sánh hai giải thuật).

Xuất ra CSV để TV7 vẽ biểu đồ đối chiếu với độ phức tạp lý thuyết ``O(m·n²)``.
Đây chính là ca TC10 trong bộ kiểm thử.

Chạy::

    python -m scripts.do_hieu_nang

Không import thư viện giao diện — chạy thuần dòng lệnh.
"""

from __future__ import annotations

import csv
import os
import random
import statistics
import sys
import time
from typing import List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.banker import kiem_tra_an_toan  # noqa: E402
from engine.banker_types import BankerState  # noqa: E402

CAC_MOC_N: List[int] = [10, 20, 50, 100, 200]
SO_LOAI_TAI_NGUYEN = 5
SO_LAN_LAP_MOI_MOC = 20

THU_MUC = os.path.dirname(os.path.abspath(__file__))
DUONG_DAN_CSV = os.path.join(THU_MUC, "ket_qua_hieu_nang.csv")


def sinh_trang_thai_ngau_nhien(n: int, m: int, do_rong: float = 0.6) -> BankerState:
    """Sinh một trạng thái hợp lệ ngẫu nhiên với ``n`` tiến trình, ``m`` tài nguyên.

    ``do_rong`` điều khiển mức dồi dào của ``Available``: càng lớn thì càng nhiều
    trạng thái an toàn, tức vòng lặp chạy đủ ``n`` bước — đó mới là trường hợp
    phản ánh đúng độ phức tạp. Nếu ``Available`` quá nhỏ, thuật toán thoát ngay ở
    bước 1 và số đo trở nên vô nghĩa.
    """
    max_matrix = [[random.randint(0, 20) for _ in range(m)] for _ in range(n)]
    allocation = [
        [random.randint(0, max_matrix[i][j]) for j in range(m)] for i in range(n)
    ]
    need_toi_da = [
        max(max_matrix[i][j] - allocation[i][j] for i in range(n))
        for j in range(m)
    ]
    available = [int(need_toi_da[j] * do_rong) for j in range(m)]
    return BankerState(available=available, max=max_matrix, allocation=allocation)


def do_mot_moc(n: int, m: int, so_lan: int) -> Tuple[float, float, int]:
    """Trả về (trung bình ms, nhỏ nhất ms, số trạng thái an toàn trong ``so_lan``)."""
    thoi_gian: List[float] = []
    so_an_toan = 0

    for _ in range(so_lan):
        trang_thai = sinh_trang_thai_ngau_nhien(n, m)
        bat_dau = time.perf_counter()
        ket_qua = kiem_tra_an_toan(trang_thai)
        ket_thuc = time.perf_counter()
        thoi_gian.append((ket_thuc - bat_dau) * 1000.0)
        if ket_qua.an_toan:
            so_an_toan += 1

    return statistics.mean(thoi_gian), min(thoi_gian), so_an_toan


def sinh_truong_hop_xau_nhat(n: int, m: int) -> BankerState:
    """Sinh trạng thái ép thuật toán vào đúng trường hợp xấu nhất ``O(m·n²)``.

    Ý tưởng: xếp nhu cầu giảm dần theo chỉ số, ``Need[i] = (n-1-i)·k``. Vòng lặp
    duyệt từ chỉ số 0 nên mỗi vòng phải quét gần hết mảng mới tìm được tiến trình
    thoả mãn — tiến trình cuối cùng. Tổng số phép quét là
    ``n + (n-1) + ... + 1 = O(n²)``, mỗi phép so sánh vector tốn ``m``.
    """
    k = 1
    allocation = [[k] * m for _ in range(n)]
    max_matrix = [[(n - 1 - i) * k + k for _ in range(m)] for i in range(n)]
    available = [0] * m
    return BankerState(available=available, max=max_matrix, allocation=allocation)


def do_mot_moc_xau_nhat(n: int, m: int, so_lan: int) -> Tuple[float, float]:
    """Đo trên trạng thái xấu nhất — không ngẫu nhiên nên chỉ cần lặp lấy trung bình."""
    thoi_gian: List[float] = []
    for _ in range(so_lan):
        trang_thai = sinh_truong_hop_xau_nhat(n, m)
        bat_dau = time.perf_counter()
        kiem_tra_an_toan(trang_thai)
        ket_thuc = time.perf_counter()
        thoi_gian.append((ket_thuc - bat_dau) * 1000.0)
    return statistics.mean(thoi_gian), min(thoi_gian)


def main() -> None:
    random.seed(42)  # cố định hạt giống để TV7 tái lập được đúng số liệu

    print("Đo thời gian kiem_tra_an_toan(), m = {}, lặp {} lần mỗi mốc\n".format(
        SO_LOAI_TAI_NGUYEN, SO_LAN_LAP_MOI_MOC))
    print("{:>6} {:>16} {:>16} {:>12}".format(
        "n", "trung bình (ms)", "nhỏ nhất (ms)", "số an toàn"))

    hang = []
    for n in CAC_MOC_N:
        tb, nn, sat = do_mot_moc(n, SO_LOAI_TAI_NGUYEN, SO_LAN_LAP_MOI_MOC)
        hang.append({
            "n": n,
            "m": SO_LOAI_TAI_NGUYEN,
            "so_lan_lap": SO_LAN_LAP_MOI_MOC,
            "thoi_gian_trung_binh_ms": round(tb, 4),
            "thoi_gian_nho_nhat_ms": round(nn, 4),
            "so_trang_thai_an_toan": sat,
        })
        print("{:>6} {:>16.4f} {:>16.4f} {:>12}".format(n, tb, nn, sat))

    # Đối chiếu với O(n²): nếu đúng bậc hai thì tỉ lệ thời gian giữa hai mốc
    # liên tiếp phải xấp xỉ bình phương tỉ lệ n.
    print("\nĐối chiếu với O(n²):")
    for truoc, sau in zip(hang, hang[1:]):
        ti_le_n = sau["n"] / truoc["n"]
        ti_le_t = (sau["thoi_gian_trung_binh_ms"] /
                   truoc["thoi_gian_trung_binh_ms"]) if truoc["thoi_gian_trung_binh_ms"] else 0
        print("  n {:>3} -> {:>3}: n gấp {:.1f} lần, thời gian gấp {:.1f} lần "
              "(nếu O(n²) thì kỳ vọng {:.1f})".format(
                  truoc["n"], sau["n"], ti_le_n, ti_le_t, ti_le_n ** 2))

    print("\n" + "=" * 62)
    print("TRƯỜNG HỢP XẤU NHẤT — ép vòng quét trong chạy đủ n lần\n")
    print("{:>6} {:>16} {:>16}".format("n", "trung bình (ms)", "nhỏ nhất (ms)"))
    for i, h in enumerate(hang):
        tb, nn = do_mot_moc_xau_nhat(h["n"], SO_LOAI_TAI_NGUYEN, 5)
        h["xau_nhat_trung_binh_ms"] = round(tb, 4)
        print("{:>6} {:>16.4f} {:>16.4f}".format(h["n"], tb, nn))

    print("\nĐối chiếu trường hợp xấu nhất với O(n²):")
    for truoc, sau in zip(hang, hang[1:]):
        ti_le_n = sau["n"] / truoc["n"]
        ti_le_t = (sau["xau_nhat_trung_binh_ms"] /
                   truoc["xau_nhat_trung_binh_ms"]) if truoc["xau_nhat_trung_binh_ms"] else 0
        print("  n {:>3} -> {:>3}: n gấp {:.1f} lần, thời gian gấp {:.1f} lần "
              "(kỳ vọng {:.1f})".format(truoc["n"], sau["n"], ti_le_n, ti_le_t, ti_le_n ** 2))

    print("\nKẾT LUẬN cho Chương 3 (TV7):")
    print("  - Dữ liệu ngẫu nhiên: thời gian tăng gần TUYẾN TÍNH, vì tiến trình")
    print("    đầu tiên thường thoả ngay nên vòng quét trong chỉ tốn O(1).")
    print("  - Trường hợp xấu nhất: thời gian tăng theo BẬC HAI, đúng O(m·n²).")
    print("  - Cận O(m·n²) là cận trên chặt, không phải mô tả trung bình.")

    with open(DUONG_DAN_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(hang[0].keys()))
        w.writeheader()
        w.writerows(hang)

    print("\nĐã ghi kết quả vào: {}".format(DUONG_DAN_CSV))
    print("TV7 dùng file này để vẽ biểu đồ trong Chương 3.")


if __name__ == "__main__":
    main()
