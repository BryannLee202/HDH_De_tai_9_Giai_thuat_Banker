# -*- coding: utf-8 -*-
"""Giải thuật Banker — phần cài đặt.

Chủ sở hữu: TV4.

Logic thuật toán do TV4 viết (bản nộp trong `tv4_engine.zip`, PR #6), đã được
chuyển sang đúng hợp đồng dữ liệu chung ở `engine/banker_types.py` để giao diện
của TV5, TV6 và module xuất báo cáo của TV1 ghép vào là chạy.

Hai quy tắc không được vi phạm:

1. File này **không import bất kỳ thư viện giao diện nào** (PyQt, tkinter…).
   Engine phải chạy được từ dòng lệnh, tách rời hoàn toàn khỏi giao diện.
2. Mọi hàm trả về **nhật ký từng bước**, không chỉ trả về đúng/sai. Giao diện
   của TV6 cần nhật ký này để chiếu lại từng vòng lặp cho người xem.

Chạy thử:  ``python -m engine.demo``
Chạy test: ``python -m unittest discover -s tests -v``
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from .banker_types import (
    BankerState,
    LoiDuLieu,
    RequestResult,
    SafetyResult,
    StepLog,
    Vector,
    Verdict,
    cong,
    nho_hon_hoac_bang,
)


# --------------------------------------------------------------------------
# Kiểm tra tính hợp lệ của dữ liệu đầu vào
# --------------------------------------------------------------------------

def kiem_tra_hop_le(trang_thai: BankerState) -> None:
    """Ném ``LoiDuLieu`` nếu dữ liệu đầu vào sai.

    Thông điệp lỗi viết bằng tiếng Việt và chỉ rõ ô nào sai, vì giao diện của
    TV5 hiển thị thẳng chuỗi này cho người dùng.
    """
    m = trang_thai.m

    if len(trang_thai.allocation) != len(trang_thai.max):
        raise LoiDuLieu(
            "E01",
            "Số hàng của Max ({}) khác số hàng của Allocation ({})".format(
                len(trang_thai.max), len(trang_thai.allocation)),
        )

    for j, v in enumerate(trang_thai.available):
        if not isinstance(v, int) or v < 0:
            raise LoiDuLieu(
                "E02",
                "Available cột {}: phải là số nguyên không âm, đang là {}".format(
                    trang_thai.ten_tai_nguyen[j], v),
            )

    for i in range(trang_thai.n):
        for ten, hang in (("Max", trang_thai.max[i]),
                          ("Allocation", trang_thai.allocation[i])):
            if len(hang) != m:
                raise LoiDuLieu(
                    "E01",
                    "Hàng P{} của {} có {} cột, phải có {} cột".format(
                        i, ten, len(hang), m),
                )
            for j, v in enumerate(hang):
                if not isinstance(v, int) or v < 0:
                    raise LoiDuLieu(
                        "E02",
                        "Ô P{}–{} của {}: phải là số nguyên không âm, đang là {}".format(
                            i, trang_thai.ten_tai_nguyen[j], ten, v),
                    )

        for j in range(m):
            if trang_thai.allocation[i][j] > trang_thai.max[i][j]:
                raise LoiDuLieu(
                    "E03",
                    "Ô P{}–{}: đã cấp {} nhưng khai báo tối đa {}".format(
                        i, trang_thai.ten_tai_nguyen[j],
                        trang_thai.allocation[i][j], trang_thai.max[i][j]),
                )


# --------------------------------------------------------------------------
# Thủ tục 1 — Kiểm tra trạng thái an toàn
# --------------------------------------------------------------------------

def kiem_tra_an_toan(trang_thai: BankerState) -> SafetyResult:
    """Thủ tục kiểm tra trạng thái an toàn.

    Mã giả (Chương 2, TV3)::

        1. Work <- Available;  Finish[i] <- false với mọi i;  chuoi <- []
        2. Tìm chỉ số i thoả:  Finish[i] = false VÀ Need[i] <= Work
           Nếu không tìm được -> sang bước 4
        3. Work <- Work + Allocation[i]
           Finish[i] <- true;  chuoi.thêm(Pi);  quay lại bước 2
        4. Nếu Finish[i] = true với mọi i -> (AN TOÀN, chuoi)
           ngược lại                       -> (KHÔNG AN TOÀN, rỗng)

    Độ phức tạp ``O(m·n²)``: vòng ngoài lặp tối đa ``n`` lần, mỗi lần quét ``n``
    tiến trình, mỗi phép so sánh vector tốn ``m``.

    Duyệt theo thứ tự chỉ số tăng dần và lấy tiến trình đầu tiên thoả mãn, nên
    với ví dụ chuẩn kết quả là ``<P1, P3, P0, P2, P4>``. Chuỗi an toàn không duy
    nhất — xem :func:`tat_ca_chuoi_an_toan`.
    """
    need = trang_thai.need
    n = trang_thai.n

    work: Vector = list(trang_thai.available)
    finish: List[bool] = [False] * n
    chuoi: List[int] = []
    nhat_ky: List[StepLog] = []
    buoc = 0

    while True:
        buoc += 1
        chon: Optional[int] = None
        bo_qua: List[Tuple[int, str]] = []

        for i in range(n):
            if finish[i]:
                continue
            if nho_hon_hoac_bang(need[i], work):
                chon = i
                break
            thieu = [trang_thai.ten_tai_nguyen[j]
                     for j in range(trang_thai.m) if need[i][j] > work[j]]
            bo_qua.append((i, "Need vượt Work ở " + ", ".join(thieu)))

        if chon is None:
            treo = [i for i in range(n) if not finish[i]]
            nhat_ky.append(StepLog(
                buoc=buoc,
                work_truoc=list(work),
                tien_trinh=None,
                need=None,
                allocation=None,
                work_sau=list(work),
                bo_qua=bo_qua,
                ghi_chu="Không tiến trình nào có Need ≤ Work",
            ))
            return SafetyResult(an_toan=False, chuoi=[],
                                nhat_ky=nhat_ky, treo=treo)

        work_truoc = list(work)
        work = cong(work, trang_thai.allocation[chon])
        finish[chon] = True
        chuoi.append(chon)

        nhat_ky.append(StepLog(
            buoc=buoc,
            work_truoc=work_truoc,
            tien_trinh=chon,
            need=list(need[chon]),
            allocation=list(trang_thai.allocation[chon]),
            work_sau=list(work),
            bo_qua=bo_qua,
        ))

        if all(finish):
            return SafetyResult(an_toan=True, chuoi=chuoi,
                                nhat_ky=nhat_ky, treo=[])


# --------------------------------------------------------------------------
# Thủ tục 2 — Xử lý yêu cầu tài nguyên
# --------------------------------------------------------------------------

def yeu_cau_tai_nguyen(trang_thai: BankerState, i: int,
                       request: Vector) -> RequestResult:
    """Thủ tục xử lý yêu cầu tài nguyên của tiến trình ``i``.

    Ba kết cục dùng **ba câu lý do khác nhau** — gộp chung một câu là dấu hiệu
    chưa hiểu thuật toán và bị trừ điểm.

    Bước 4 là chỗ hay cài sai nhất: thao tác trên bản sao qua ``trang_thai.copy()``
    rồi mới ghi đè khi an toàn, tuyệt đối không sửa trực tiếp rồi trừ ngược lại.
    """
    if not 0 <= i < trang_thai.n:
        raise LoiDuLieu("E04", "Không có tiến trình P{}".format(i))
    if len(request) != trang_thai.m:
        raise LoiDuLieu(
            "E01", "Vector yêu cầu phải có {} phần tử".format(trang_thai.m))

    need_i = trang_thai.need[i]
    ten = trang_thai.ten_tai_nguyen

    # Bước 1 — xin vượt quá nhu cầu đã khai báo
    if not nho_hon_hoac_bang(request, need_i):
        j = next(j for j in range(trang_thai.m) if request[j] > need_i[j])
        return RequestResult(
            ket_luan=Verdict.LOI,
            ly_do="Từ chối: yêu cầu vượt quá Need đã khai báo của P{} "
                  "(xin {} đơn vị {}, chỉ còn được xin {})".format(
                      i, request[j], ten[j], need_i[j]),
        )

    # Bước 2 — không đủ tài nguyên rảnh
    if not nho_hon_hoac_bang(request, trang_thai.available):
        j = next(j for j in range(trang_thai.m)
                 if request[j] > trang_thai.available[j])
        return RequestResult(
            ket_luan=Verdict.CHO,
            ly_do="Chờ: không đủ tài nguyên rảnh, cần {} đơn vị {} "
                  "nhưng chỉ còn {}".format(
                      request[j], ten[j], trang_thai.available[j]),
        )

    # Bước 3 — giả lập cấp phát trên BẢN SAO
    thu = trang_thai.copy()
    for j in range(trang_thai.m):
        thu.available[j] -= request[j]
        thu.allocation[i][j] += request[j]

    # Bước 4 — chỉ ghi đè trạng thái thật khi kết quả an toàn
    kq = kiem_tra_an_toan(thu)
    if kq.an_toan:
        trang_thai.available = thu.available
        trang_thai.allocation = thu.allocation
        return RequestResult(
            ket_luan=Verdict.CAP_PHAT,
            ly_do="Cấp phát: trạng thái sau khi cấp vẫn an toàn",
            nhat_ky=kq.nhat_ky,
        )

    return RequestResult(
        ket_luan=Verdict.CHO,
        ly_do="Chờ: đủ tài nguyên rảnh nhưng cấp vào thì trạng thái "
              "không còn an toàn, đã hoàn tác",
        nhat_ky=kq.nhat_ky,
    )


def giai_phong(trang_thai: BankerState, i: int, vector: Vector) -> None:
    """Tiến trình ``i`` trả bớt tài nguyên về hệ thống."""
    if not 0 <= i < trang_thai.n:
        raise LoiDuLieu("E04", "Không có tiến trình P{}".format(i))
    for j in range(trang_thai.m):
        if vector[j] > trang_thai.allocation[i][j]:
            raise LoiDuLieu(
                "E05",
                "P{} chỉ đang giữ {} đơn vị {}, không trả được {}".format(
                    i, trang_thai.allocation[i][j],
                    trang_thai.ten_tai_nguyen[j], vector[j]),
            )
    for j in range(trang_thai.m):
        trang_thai.allocation[i][j] -= vector[j]
        trang_thai.available[j] += vector[j]


def ket_thuc_tien_trinh(trang_thai: BankerState, i: int) -> None:
    """Tiến trình ``i`` kết thúc, trả TOÀN BỘ ``allocation[i]`` về ``available``.

    TV6 gắn hàm này vào nút "Kết thúc tiến trình" — mảnh còn thiếu để phần mềm
    mô phỏng trọn chu trình yêu cầu, sử dụng, giải phóng mà đề bài đòi hỏi.
    """
    giai_phong(trang_thai, i, list(trang_thai.allocation[i]))


# --------------------------------------------------------------------------
# Điểm cộng — liệt kê tất cả chuỗi an toàn
# --------------------------------------------------------------------------

def tat_ca_chuoi_an_toan(trang_thai: BankerState,
                         gioi_han: int = 1000) -> List[List[int]]:
    """Liệt kê mọi chuỗi an toàn bằng quay lui.

    Chứng minh được chuỗi an toàn **không duy nhất**: với ví dụ chuẩn, cả
    ``<P1,P3,P0,P2,P4>`` lẫn ``<P1,P3,P4,P2,P0>`` đều hợp lệ.

    ``gioi_han`` chặn số chuỗi trả về để không treo khi ``n`` lớn — số chuỗi có
    thể tăng theo giai thừa.
    """
    need = trang_thai.need
    n = trang_thai.n
    ket_qua: List[List[int]] = []

    def quay_lui(work: Vector, xong: List[bool], chuoi: List[int]) -> None:
        if len(ket_qua) >= gioi_han:
            return
        if all(xong):
            ket_qua.append(list(chuoi))
            return
        for i in range(n):
            if xong[i] or not nho_hon_hoac_bang(need[i], work):
                continue
            xong[i] = True
            chuoi.append(i)
            quay_lui(cong(work, trang_thai.allocation[i]), xong, chuoi)
            chuoi.pop()
            xong[i] = False

    quay_lui(list(trang_thai.available), [False] * n, [])
    return ket_qua
