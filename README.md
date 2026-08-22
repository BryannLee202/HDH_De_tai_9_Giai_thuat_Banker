# Bài tập lớn Hệ điều hành — Đề tài 9: Giải thuật Banker

Mô phỏng giải thuật Banker (deadlock avoidance) bằng phần mềm có giao diện PyQt5, kèm quyển báo cáo.

| | |
|---|---|
| **Phần** | Deadlock |
| **Đề tài** | Giải thuật Banker |
| **Đối chứng so sánh** | Giải thuật đồ thị phân bổ tài nguyên (đề tài 10) |
| **Sản phẩm** | Quyển báo cáo + phần mềm có giao diện |
| **Ngôn ngữ** | Python 3.8+ |
| **Giao diện** | PyQt5 |

---

## Mục lục

- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Hướng dẫn chạy demo chi tiết](#hướng-dẫn-chạy-demo-chi-tiết)
- [Tính năng phần mềm](#tính-năng-phần-mềm)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [API của engine](#api-của-engine)
- [Dữ liệu mẫu](#dữ-liệu-mẫu)
- [Kiểm thử tự động](#kiểm-thử-tự-động)
- [Đo hiệu năng và so sánh hai giải thuật](#đo-hiệu-năng-và-so-sánh-hai-giải-thuật)
- [Xuất báo cáo](#xuất-báo-cáo)

---

## Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|---|---|
| **Python** | 3.8 trở lên |
| **Hệ điều hành** | Windows / macOS / Linux |
| **Thư viện bắt buộc** | `PyQt5` (chỉ cần cho giao diện) |
| **Thư viện tùy chọn** | `openpyxl` (xuất Excel), `matplotlib` (vẽ hình so sánh cho Chương 3) |

> **Lưu ý:** Engine (giải thuật Banker) **không phụ thuộc** bất kỳ thư viện ngoài nào. Có thể chạy engine từ dòng lệnh mà không cần cài PyQt5.

---

## Cài đặt

### Bước 1 — Kiểm tra phiên bản Python

```bash
python --version
```

Yêu cầu Python 3.8 trở lên. Nếu chưa có, tải tại [python.org](https://www.python.org/downloads/).

### Bước 2 — Tải mã nguồn

```bash
git clone https://github.com/BryannLee202/HDH_De_tai_9_Giai_thuat_Banker.git
cd HDH_De_tai_9_Giai_thuat_Banker
```

Hoặc tải file ZIP từ GitHub rồi giải nén.

### Bước 3 — Cài thư viện

**Bắt buộc** (để chạy giao diện):

```bash
pip install PyQt5
```

**Tùy chọn** (nếu muốn xuất Excel hoặc vẽ hình so sánh):

```bash
pip install openpyxl matplotlib
```

---

## Hướng dẫn chạy demo chi tiết

### Cách 1 — Chạy phần mềm giao diện (khuyên dùng)

```bash
python -m gui.GUI_TV6
```

Cửa sổ chính hiện ra gồm **3 panel** nằm cạnh nhau:

#### Panel 1 — Nhập liệu (bên trái)

1. **Chọn số tiến trình (n) và số loại tài nguyên (m)**, bấm **"Tạo ma trận"** để tạo lưới trống.
2. **Nhập dữ liệu** vào 3 bảng:
   - **Available** — tài nguyên hiện có trong hệ thống.
   - **Max** — nhu cầu tối đa mỗi tiến trình đã khai báo.
   - **Allocation** — số tài nguyên đang được cấp cho mỗi tiến trình.
3. Bấm **"Kiểm tra & Tính Need"** → phần mềm tự tính `Need = Max - Allocation`, hiển thị bảng Need (chỉ đọc) và tổng tài nguyên Total.
4. **Hoặc** bấm **"Mở JSON"** để nạp sẵn bộ dữ liệu mẫu từ thư mục `data/`.
5. **Hoặc** bấm **"Sinh ngẫu nhiên"** để tạo dữ liệu ngẫu nhiên hợp lệ.
6. Bấm **"Lưu JSON"** để lưu bộ dữ liệu hiện tại ra file `.json`.

> **Dữ liệu mặc định khi mở phần mềm:** bộ ví dụ chuẩn (5 tiến trình, 3 tài nguyên A/B/C), trạng thái an toàn.

#### Panel 2 — Mô phỏng thuật toán (giữa)

1. Bấm **"▶ Chạy Từng Bước"** → hiển thị từng vòng lặp của thủ tục kiểm tra an toàn.
2. Bấm **"⏩ Chạy Tự Động"** → chạy tự động với tốc độ tùy chỉnh bằng thanh trượt (200–2000 ms mỗi bước).
3. Bảng nhật ký hiện: **Bước**, **Tiến trình được chọn**, **Kiểm tra Need ≤ Work**, **Work sau**, **Trạng thái**.
4. Thanh trạng thái phía trên hiện:
   - **Xanh lá** — `HỆ THỐNG AN TOÀN` kèm chuỗi an toàn.
   - **Đỏ** — `HỆ THỐNG BẤT AN TOÀN (CÓ THỂ XẢY RA DEADLOCK)`.
5. Bấm **"↺ Đặt Lại"** để chạy lại từ đầu.

#### Panel 3 — Yêu cầu tài nguyên, giải phóng, biểu đồ (bên phải)

1. **Gửi yêu cầu tài nguyên:** chọn tiến trình (P0–P4), nhập vector yêu cầu (ví dụ: `1 0 2`), bấm **"Gửi yêu cầu"**.
   - Kết quả có **3 kết cục** với 3 câu lý do khác nhau:
     - 🟢 **CẤP PHÁT** — trạng thái sau khi cấp vẫn an toàn.
     - 🟡 **CHỜ** — không đủ tài nguyên rảnh hoặc cấp vào thì không an toàn.
     - 🔴 **LỖI** — yêu cầu vượt quá Need đã khai báo.
2. **Giải phóng tài nguyên:** nhập vector, bấm **"Giải phóng"**.
3. **Kết thúc tiến trình:** bấm **"Kết thúc tiến trình"** → trả toàn bộ tài nguyên của tiến trình đó về hệ thống.
4. **Hoàn tác:** bấm **"Hoàn tác"** để quay về trạng thái trước đó.
5. **Biểu đồ cột** — tỉ lệ tài nguyên đã cấp / tổng cho mỗi loại.
6. **Đồ thị phân bổ tài nguyên** — đỉnh tròn (tiến trình), đỉnh vuông (tài nguyên), đường xanh liền (cạnh cấp phát R→P), đường đỏ đứt (cạnh yêu cầu P→R).

#### Demo mẫu — bước theo bước

```
1. Mở phần mềm:  python -m gui.GUI_TV6
2. Dữ liệu mặc định đã được nạp sẵn (5 tiến trình, 3 tài nguyên)
3. Bấm "Kiểm tra & Tính Need" → thấy bảng Need và Total
4. Sang panel giữa, bấm "⏩ Chạy Tự Động"
5. Quan sát thuật toán chạy từng bước:
   Bước 1: Work (3,3,2) → chọn P1 (Need ≤ Work) → Work = (5,3,2)
   Bước 2: Work (5,3,2) → chọn P3 → Work = (7,4,3)
   Bước 3: Work (7,4,3) → chọn P0 → Work = (7,5,3)
   Bước 4: Work (7,5,3) → chọn P2 → Work = (10,5,5)
   Bước 5: Work (10,5,5) → chọn P4 → Work = (10,5,7)
   → KẾT LUẬN: AN TOÀN, chuỗi P1 → P3 → P0 → P2 → P4
6. Sang panel phải, chọn P1, nhập "1 0 2", bấm "Gửi yêu cầu"
   → Kết quả: CẤP PHÁT (trạng thái sau khi cấp vẫn an toàn)
7. Chọn P4, nhập "3 3 0", bấm "Gửi yêu cầu"
   → Kết quả: CHỜ (không đủ tài nguyên rảnh)
```

### Cách 2 — Chạy engine từ dòng lệnh (không cần PyQt5)

```bash
python -m engine.demo
```

Kết quả in ra terminal:

```
n = 5 tien trinh, m = 3 loai tai nguyen
Available = [3, 3, 2]
Total     = [10, 5, 7]
Need      =
  P0: [7, 4, 3]
  P1: [1, 2, 2]
  P2: [6, 0, 0]
  P3: [0, 1, 1]
  P4: [4, 3, 1]

KET LUAN: AN TOAN
Chuoi an toan: P1 → P3 → P0 → P2 → P4

Nhat ky tung buoc:
  Buoc 1: Work [3, 3, 2] -> chon P1 -> [5, 3, 2]
  Buoc 2: Work [5, 3, 2] -> chon P3 -> [7, 4, 3]
  Buoc 3: Work [7, 4, 3] -> chon P0 -> [7, 5, 3]
  Buoc 4: Work [7, 5, 3] -> chon P2 -> [10, 5, 5]
  Buoc 5: Work [10, 5, 5] -> chon P4 -> [10, 5, 7]
```

### Cách 3 — Chạy trong Python script

```python
from engine.banker_types import BankerState, Verdict
from engine.banker import kiem_tra_an_toan, yeu_cau_tai_nguyen

# Nạp bộ dữ liệu chuẩn
tt = BankerState.from_json_file("data/vi-du-chuan.json")

# Kiểm tra trạng thái an toàn
kq = kiem_tra_an_toan(tt)
print(kq.an_toan)       # True
print(kq.chuoi_dep())   # P1 → P3 → P0 → P2 → P4

# Gửi yêu cầu tài nguyên
r = yeu_cau_tai_nguyen(tt, 1, [1, 0, 2])
print(r.ket_luan)       # Verdict.CAP_PHAT
print(r.ly_do)          # Cấp phát: trạng thái sau khi cấp vẫn an toàn
```

---

## Tính năng phần mềm

| # | Tính năng | Mô tả |
|---|---|---|
| 1 | Nhập liệu ma trận | Nhập Available, Max, Allocation; tự tính Need |
| 2 | Import / Export JSON | Nạp và lưu bộ dữ liệu từ file `.json` |
| 3 | Sinh ngẫu nhiên | Tạo bộ dữ liệu ngẫu nhiên hợp lệ |
| 4 | Kiểm tra an toàn | Chạy thủ tục kiểm tra an toàn, trả chuỗi an toàn |
| 5 | Mô phỏng từng bước | Hiển thị từng vòng lặp của thuật toán |
| 6 | Chạy tự động | Tốc độ tùy chỉnh 200–2000 ms/bước |
| 7 | Yêu cầu tài nguyên | 3 kết cục: Cấp phát / Chờ / Lỗi |
| 8 | Giải phóng tài nguyên | Trả bớt hoặc toàn bộ tài nguyên |
| 9 | Kết thúc tiến trình | Trả toàn bộ Allocation về Available |
| 10 | Hoàn tác | Quay về trạng thái trước đó |
| 11 | Biểu đồ cột | Tỉ lệ đã cấp / tổng mỗi loại tài nguyên |
| 12 | Đồ thị phân bổ | Cạnh cấp phát (xanh) và cạnh yêu cầu (đỏ) |
| 13 | Xuất báo cáo | HTML (chuyển PDF) hoặc Excel |
| 14 | Liệt kê tất cả chuỗi an toàn | Quay lui, chứng minh chuỗi không duy nhất |

---

## Cấu trúc thư mục

```
engine/              Thuật toán Banker, không phụ thuộc giao diện
  __init__.py          Package marker
  banker_types.py      Hợp đồng dữ liệu: BankerState, SafetyResult, StepLog,
                         RequestResult, Verdict, LoiDuLieu
  banker.py            5 hàm chính: kiem_tra_hop_le, kiem_tra_an_toan,
                         yeu_cau_tai_nguyen, giai_phong, ket_thuc_tien_trinh,
                         tat_ca_chuoi_an_toan
  demo.py              Chạy thử engine từ dòng lệnh
  do_thi_phan_bo.py    Giải thuật đồ thị phân bổ tài nguyên (đối chứng)

gui/                 Giao diện phần mềm PyQt5
  __init__.py          Package marker
  GUI_TV6.py           Cửa sổ chính: nhập liệu (TV5) + mô phỏng (TV6)
  bang_yeu_cau.py      Yêu cầu tài nguyên, giải phóng, hoàn tác, biểu đồ cột,
                         đồ thị phân bổ
  engine_adapter.py    Cầu nối engine ↔ giao diện (chuyển StepLog → dict)
  xuat_bao_cao.py      Xuất kết quả ra HTML / Excel

data/                3 bộ dữ liệu mẫu .json
  vi-du-chuan.json     5P × 3R, trạng thái an toàn
  khong-an-toan.json   5P × 3R, Available = (0,0,0) → không an toàn
  bien-mot-tai-nguyen.json  3P × 1R, ca biên m = 1

scripts/             Đo hiệu năng và so sánh
  do_hieu_nang.py      Đo thời gian kiem_tra_an_toan khi n tăng
  so_sanh_hai_giai_thuat.py  So sánh Banker vs đồ thị, vẽ 4 hình
  ket_qua_hieu_nang.csv     Kết quả đo hiệu năng
  ket_qua_so_sanh.csv       Kết quả so sánh hai giải thuật

tests/               Bộ kiểm thử tự động
  test_banker.py       17 ca kiểm thử

docs/                Đề bài, kiến trúc, ảnh demo
  Phan-cong-De-tai-9-Giai-thuat-Banker.pdf
  kien-truc.md         Kiến trúc chương trình, 4 biểu đồ Mermaid
  anh-demo/            Ảnh giao diện và hình Chương 3

report/              Quyển báo cáo — mỗi chương một thư mục riêng
```

---

## API của engine

> **Quan trọng:** Giao diện không gọi thẳng engine mà đi qua [`gui/engine_adapter.py`](gui/engine_adapter.py). Nếu engine đổi thì chỉ phải sửa một chỗ.

```python
from engine.banker_types import BankerState, Verdict, LoiDuLieu
from engine.banker import (
    kiem_tra_hop_le,        # ném LoiDuLieu nếu dữ liệu sai
    kiem_tra_an_toan,       # -> SafetyResult
    yeu_cau_tai_nguyen,     # -> RequestResult
    giai_phong,             # trả bớt tài nguyên
    ket_thuc_tien_trinh,    # trả toàn bộ tài nguyên
    tat_ca_chuoi_an_toan,   # liệt kê mọi chuỗi an toàn (quay lui)
)
```

### Kiểu dữ liệu

| Lớp | Trường chính |
|---|---|
| `BankerState` | `available`, `max`, `allocation`, `need` (tự tính), `total`, `n`, `m`, `ten_tai_nguyen`, `copy()`, `from_json_file()`, `to_json_file()` |
| `SafetyResult` | `an_toan`, `chuoi`, `nhat_ky` (danh sách `StepLog`), `treo`, `chuoi_dep()` |
| `StepLog` | `buoc`, `work_truoc`, `tien_trinh`, `need`, `allocation`, `work_sau`, `bo_qua`, `ghi_chu` |
| `RequestResult` | `ket_luan` (`Verdict`), `ly_do`, `nhat_ky` |
| `Verdict` | `CAP_PHAT`, `CHO`, `LOI` |
| `LoiDuLieu` | `ma`, `thong_diep` — ngoại lệ cho dữ liệu sai |

### Nguyên tắc thiết kế

- `Need` **không phải** dữ liệu lưu trữ mà là thuộc tính tính ra từ `Max - Allocation` mỗi lần đọc → không bao giờ lệch.
- Engine **không import** bất kỳ thư viện giao diện nào (PyQt, tkinter…) → chạy và kiểm thử được từ dòng lệnh.
- Mọi hàm trả về **nhật ký từng bước** (`StepLog`), không chỉ đúng/sai.

### Giải thuật đối chứng — đồ thị phân bổ tài nguyên

File [`engine/do_thi_phan_bo.py`](engine/do_thi_phan_bo.py) cài đặt giải thuật đồ thị (đề tài 10) để so sánh:

```python
from engine.do_thi_phan_bo import (
    xay_dung_do_thi,               # dựng đồ thị từ BankerState
    tim_chu_trinh,                 # DFS tìm chu trình, O(V+E)
    co_chu_trinh,                  # bool: có chu trình?
    chu_trinh_co_nghia_la_deadlock, # True nếu mỗi loại TN chỉ 1 thực thể
    cap_phat_duoc,                 # thử cấp phát, kiểm tra chu trình
)
```

**Giới hạn quan trọng:** kết luận _"có chu trình → có deadlock"_ **chỉ đúng** khi mỗi loại tài nguyên có **đúng 1 thực thể**. Khi có nhiều thực thể, chu trình chỉ là điều kiện cần.

---

## Dữ liệu mẫu

| File | Mô tả | Kết quả |
|---|---|---|
| [`data/vi-du-chuan.json`](data/vi-du-chuan.json) | 5 tiến trình, 3 tài nguyên (A, B, C). Total = (10, 5, 7) | **AN TOÀN**, chuỗi `P1 → P3 → P0 → P2 → P4` |
| [`data/khong-an-toan.json`](data/khong-an-toan.json) | Cùng Max và Allocation, nhưng Available = (0, 0, 0) | **KHÔNG AN TOÀN** |
| [`data/bien-mot-tai-nguyen.json`](data/bien-mot-tai-nguyen.json) | 3 tiến trình, 1 tài nguyên — ca biên m = 1 | **AN TOÀN** |

### Định dạng file JSON

```json
{
  "n": 5,
  "m": 3,
  "ten_tai_nguyen": ["A", "B", "C"],
  "available": [3, 3, 2],
  "max": [[7,5,3], [3,2,2], [9,0,2], [2,2,2], [4,3,3]],
  "allocation": [[0,1,0], [2,0,0], [3,0,2], [2,1,1], [0,0,2]]
}
```

Trường `need` **không cần** và **không nên** đưa vào file JSON — `BankerState` tự tính từ `Max - Allocation`.

---

## Kiểm thử tự động

Chạy toàn bộ 17 ca kiểm thử:

```bash
python -m unittest discover -s tests -v
```

Kết quả mong đợi:

```
test_tc01_trang_thai_ban_dau_an_toan ... ok
test_tc01_co_ghi_nhat_ky_tung_buoc ... ok
test_tc02_p1_xin_1_0_2_duoc_cap_phat ... ok
test_tc03_p4_xin_3_3_0_phai_cho_vi_thieu_tai_nguyen ... ok
test_tc04_p0_xin_0_2_0_bi_tu_choi_vi_khong_an_toan ... ok
test_tc04_trang_thai_khong_bi_hong_sau_khi_tu_choi ... ok
test_tc05_xin_vuot_qua_need_thi_bao_loi ... ok
...
----------------------------------------------------------------------
Ran 17 tests in 0.0xxs

OK
```

### Các nhóm test

| Nhóm | Số ca | Nội dung |
|---|---|---|
| `TestCauTrucDuLieu` | 2 | Need tính đúng, Total là hằng số |
| `TestKiemTraAnToan` | 4 | Trạng thái an toàn / không an toàn / biên |
| `TestYeuCauTaiNguyen` | 6 | 3 kết cục, rollback, 3 lý do khác nhau |
| `TestDuLieuKhongHopLe` | 4 | Allocation > Max, giá trị âm, sai cột |
| `TestCaBoSungTV8` | 5 | Giải phóng giúp chạy, xin vừa đủ, xin rỗng, tiến trình không tồn tại |

---

## Đo hiệu năng và so sánh hai giải thuật

### Đo hiệu năng Banker

```bash
python -m scripts.do_hieu_nang
```

Đo thời gian `kiem_tra_an_toan()` với n = 10, 20, 50, 100, 200 (m = 5 cố định, lặp 20 lần). Xuất kết quả ra `scripts/ket_qua_hieu_nang.csv`.

### So sánh Banker vs đồ thị phân bổ tài nguyên

```bash
python -m scripts.so_sanh_hai_giai_thuat
```

> **Yêu cầu:** `pip install matplotlib`

Sản phẩm:

| File | Nội dung |
|---|---|
| `scripts/ket_qua_so_sanh.csv` | Bảng số liệu Banker vs đồ thị |
| `docs/anh-demo/hinh-3-1.png` | Đồ thị không có chu trình |
| `docs/anh-demo/hinh-3-2.png` | Đồ thị có chu trình, bị từ chối |
| `docs/anh-demo/hinh-3-3.png` | Phản ví dụ: chu trình nhưng không deadlock |
| `docs/anh-demo/hinh-3-4.png` | Biểu đồ thời gian chạy theo n |

---

## Xuất báo cáo

### Xuất HTML (chuyển PDF bằng trình duyệt)

```python
from gui.xuat_bao_cao import xuat_html
from engine.banker import kiem_tra_an_toan
from engine.banker_types import BankerState

tt = BankerState.from_json_file("data/vi-du-chuan.json")
kq = kiem_tra_an_toan(tt)
xuat_html("ket-qua.html", tt, kq)
# Mở file HTML → Ctrl+P → Lưu thành PDF
```

### Xuất Excel

```python
from gui.xuat_bao_cao import xuat_excel

xuat_excel("ket-qua.xlsx", tt, kq)
```

> **Yêu cầu:** `pip install openpyxl`

---

## Tóm tắt lệnh chạy nhanh

| Mục đích | Lệnh |
|---|---|
| Mở giao diện | `python -m gui.GUI_TV6` |
| Chạy engine dòng lệnh | `python -m engine.demo` |
| Chạy kiểm thử | `python -m unittest discover -s tests -v` |
| Đo hiệu năng | `python -m scripts.do_hieu_nang` |
| So sánh hai giải thuật | `python -m scripts.so_sanh_hai_giai_thuat` |

---

## Video demo

*(Dán link Google Drive vào đây)*
