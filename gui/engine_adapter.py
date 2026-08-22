# -*- coding: utf-8 -*-
"""Lớp cầu nối giữa engine và giao diện.

Giao diện của TV6 hiển thị nhật ký bằng một danh sách ``dict``, còn engine của
TV4 trả về ``SafetyResult`` chứa các ``StepLog``. File này chuyển đổi giữa hai
bên để không phải sửa code giao diện, cũng không phải sửa engine.

**Vì sao cần file này:** bản đầu của giao diện gọi ``core.banker_engine.BankerEngine``
— một module chưa từng tồn tại trong repo — nên chương trình bung ngay khi khởi
động. Engine thật nằm ở ``engine/banker.py``, gọi qua các hàm module chứ không
qua lớp. Mọi lời gọi engine từ giao diện nên đi qua file này.
"""

from __future__ import annotations

from typing import Any, Dict, List

from engine.banker import kiem_tra_an_toan, kiem_tra_hop_le
from engine.banker_types import BankerState, SafetyResult


def tao_trang_thai(dataset: Dict[str, Any]) -> BankerState:
    """Đổi ``dict`` của màn hình nhập liệu (TV5) thành ``BankerState``.

    Trường ``need`` trong dataset bị bỏ qua có chủ ý: ``BankerState`` tự tính
    ``Need = Max − Allocation`` nên không bao giờ lệch.
    """
    return BankerState(
        available=list(dataset["available"]),
        max=[list(h) for h in dataset["max"]],
        allocation=[list(h) for h in dataset["allocation"]],
    )


def _vec(v) -> str:
    return "(" + ", ".join(str(x) for x in v) + ")"


def cac_buoc_mo_phong(trang_thai: BankerState) -> List[Dict[str, Any]]:
    """Chạy thuật toán và trả về danh sách bước theo đúng định dạng bảng của TV6.

    Mỗi phần tử có các khoá: ``step``, ``process``, ``check``, ``work_new``,
    ``status``, ``is_safe``, ``safe_seq``.
    """
    kq: SafetyResult = kiem_tra_an_toan(trang_thai)
    chuoi_ten = ["P{}".format(i) for i in kq.chuoi]
    buoc_list: List[Dict[str, Any]] = []

    for b in kq.nhat_ky:
        if b.tien_trinh is None:
            treo = ", ".join("P{}".format(i) for i in kq.treo)
            buoc_list.append({
                "step": b.buoc,
                "process": "—",
                "check": "Không tiến trình nào có Need ≤ Work {}".format(
                    _vec(b.work_truoc)),
                "work_new": _vec(b.work_sau),
                "status": "Bế tắc — còn treo: {}".format(treo),
                "is_safe": False,
                "safe_seq": [],
            })
        else:
            buoc_list.append({
                "step": b.buoc,
                "process": "P{}".format(b.tien_trinh),
                "check": "Need {} ≤ Work {}".format(
                    _vec(b.need), _vec(b.work_truoc)),
                "work_new": "{} + {} = {}".format(
                    _vec(b.work_truoc), _vec(b.allocation), _vec(b.work_sau)),
                "status": "Hoàn thành, giải phóng tài nguyên",
                "is_safe": True,
                "safe_seq": chuoi_ten,
            })

    return buoc_list


def kiem_tra_du_lieu(dataset: Dict[str, Any]) -> str:
    """Trả về chuỗi rỗng nếu dữ liệu hợp lệ, ngược lại trả về thông điệp lỗi.

    Giao diện hiển thị thẳng chuỗi này cho người dùng nên không cần bắt ngoại lệ.
    """
    from engine.banker_types import LoiDuLieu
    try:
        kiem_tra_hop_le(tao_trang_thai(dataset))
    except LoiDuLieu as e:
        return e.thong_diep
    except Exception as e:  # dữ liệu méo mó ngoài dự kiến
        return "Dữ liệu không hợp lệ: {}".format(e)
    return ""
