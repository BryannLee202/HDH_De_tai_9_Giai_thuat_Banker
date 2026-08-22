# -*- coding: utf-8 -*-
"""Giải thuật đồ thị phân bổ tài nguyên (Resource-Allocation Graph).

Đây là **giải thuật đối chứng** cho Chương 3 — đề tài 10 của Phần Deadlock.
Cài đặt ở đây để TV7 có số liệu đo thật khi so sánh với giải thuật Banker,
thay vì phải trích số từ nguồn ngoài.

Mô hình đồ thị có hướng, hai loại đỉnh:

- Đỉnh tiến trình ``P0, P1, …`` — vẽ hình tròn
- Đỉnh tài nguyên ``R0, R1, …`` — vẽ hình vuông

Ba loại cạnh:

===================  ==========  ==================================================
Loại cạnh            Hướng       Ý nghĩa
===================  ==========  ==================================================
Cạnh cấp phát        ``R → P``   Tài nguyên R đang được cấp cho tiến trình P
Cạnh yêu cầu         ``P → R``   Tiến trình P đang chờ được cấp tài nguyên R
Cạnh nhu cầu         ``P ⇢ R``   P có thể sẽ xin R trong tương lai (vẽ nét đứt)
===================  ==========  ==================================================

**Giới hạn cốt lõi** — phải nêu rõ trong báo cáo: kết luận *"có chu trình thì
có deadlock"* chỉ đúng khi **mỗi loại tài nguyên có đúng một thực thể**. Khi một
loại có nhiều thực thể, chu trình mới chỉ là *điều kiện cần*, chưa phải điều
kiện đủ — xem :func:`chu_trinh_co_nghia_la_deadlock`. Đây chính là lý do giải
thuật Banker vẫn cần tồn tại song song.

Độ phức tạp phát hiện chu trình bằng DFS: ``O(V + E)`` với ``V = n + m`` đỉnh và
``E ≤ 2·n·m`` cạnh, tức ``O(n·m)``. Trong tài liệu kinh điển thường ghi
``O((n + m)²)`` khi biểu diễn bằng ma trận kề.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from .banker_types import BankerState

Do_Thi = Dict[str, List[str]]


def ten_tien_trinh(i: int) -> str:
    return "P{}".format(i)


def ten_tai_nguyen(trang_thai: BankerState, j: int) -> str:
    return "R{}".format(trang_thai.ten_tai_nguyen[j])


def xay_dung_do_thi(trang_thai: BankerState) -> Do_Thi:
    """Dựng đồ thị phân bổ tài nguyên từ trạng thái hệ thống.

    - ``allocation[i][j] > 0`` → cạnh cấp phát ``Rj → Pi``
    - ``need[i][j] > 0``       → cạnh yêu cầu ``Pi → Rj``
    """
    dt: Do_Thi = {}
    need = trang_thai.need

    for i in range(trang_thai.n):
        dt.setdefault(ten_tien_trinh(i), [])
    for j in range(trang_thai.m):
        dt.setdefault(ten_tai_nguyen(trang_thai, j), [])

    for i in range(trang_thai.n):
        p = ten_tien_trinh(i)
        for j in range(trang_thai.m):
            r = ten_tai_nguyen(trang_thai, j)
            if trang_thai.allocation[i][j] > 0:
                dt[r].append(p)          # cạnh cấp phát R -> P
            if need[i][j] > 0:
                dt[p].append(r)          # cạnh yêu cầu  P -> R
    return dt


def tim_chu_trinh(do_thi: Do_Thi) -> Optional[List[str]]:
    """Tìm một chu trình trong đồ thị có hướng bằng DFS, trả về đường đi.

    Trả về ``None`` nếu đồ thị không có chu trình. Độ phức tạp ``O(V + E)``.
    """
    TRANG, XAM, DEN = 0, 1, 2
    mau: Dict[str, int] = {u: TRANG for u in do_thi}
    cha: Dict[str, Optional[str]] = {u: None for u in do_thi}

    def dfs(u: str) -> Optional[List[str]]:
        mau[u] = XAM
        for v in do_thi.get(u, ()):
            if mau.get(v, TRANG) == XAM:          # gặp lại đỉnh đang duyệt -> chu trình
                chu_trinh = [v, u]
                w = cha[u]
                while w is not None and w != v:
                    chu_trinh.append(w)
                    w = cha[w]
                if w == v:
                    chu_trinh.append(v)
                chu_trinh.reverse()
                return chu_trinh
            if mau.get(v, TRANG) == TRANG:
                cha[v] = u
                kq = dfs(v)
                if kq is not None:
                    return kq
        mau[u] = DEN
        return None

    for u in do_thi:
        if mau[u] == TRANG:
            kq = dfs(u)
            if kq is not None:
                return kq
    return None


def co_chu_trinh(trang_thai: BankerState) -> bool:
    """Đồ thị của trạng thái này có chu trình hay không."""
    return tim_chu_trinh(xay_dung_do_thi(trang_thai)) is not None


def chu_trinh_co_nghia_la_deadlock(trang_thai: BankerState) -> bool:
    """Chu trình có thực sự kéo theo deadlock trong trạng thái này không?

    Chỉ đúng khi **mọi loại tài nguyên đều chỉ có một thực thể**. Hàm này trả về
    ``True`` khi kết luận của giải thuật đồ thị là đáng tin, ``False`` khi có ít
    nhất một loại tài nguyên nhiều thực thể — lúc đó chu trình chỉ là điều kiện
    cần và phải dùng giải thuật Banker để kết luận.
    """
    return all(tong == 1 for tong in trang_thai.total)


def cap_phat_duoc(trang_thai: BankerState, i: int, j: int) -> bool:
    """Có nên chấp thuận yêu cầu của ``Pi`` với tài nguyên loại ``j`` không?

    Quy tắc của giải thuật đồ thị: thử biến cạnh yêu cầu ``Pi → Rj`` thành cạnh
    cấp phát ``Rj → Pi``; nếu thao tác đó **không tạo ra chu trình** thì chấp
    thuận, ngược lại bắt chờ.
    """
    thu = trang_thai.copy()
    thu.allocation[i][j] += 1
    if thu.allocation[i][j] > thu.max[i][j]:
        thu.max[i][j] = thu.allocation[i][j]
    thu.available[j] -= 1
    return not co_chu_trinh(thu)
