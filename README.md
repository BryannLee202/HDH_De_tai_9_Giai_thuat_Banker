# Bài tập lớn Hệ điều hành — Đề tài 9: Giải thuật Banker

Mô phỏng giải thuật Banker (deadlock avoidance) bằng phần mềm có giao diện, kèm quyển báo cáo.

| | |
|---|---|
| **Phần** | Deadlock |
| **Đề tài** | Giải thuật Banker |
| **Đối chứng so sánh** | Giải thuật đồ thị phân bổ tài nguyên (đề tài 10) |
| **Sản phẩm** | Quyển báo cáo + phần mềm có giao diện |
| **Nhân lực** | 8 thành viên · 4 tuần |

Kế hoạch phân công đầy đủ: [`docs/Phan-cong-De-tai-9-Giai-thuat-Banker.pdf`](docs/Phan-cong-De-tai-9-Giai-thuat-Banker.pdf)

---

## Tiến độ

| TV | Họ tên | Nhiệm vụ | Nhánh | Trạng thái |
|---|---|---|---|---|
| TV1 | Lê Minh Tài | Nhóm trưởng · hợp đồng dữ liệu · kiến trúc · xuất báo cáo | `tv1-kien-truc` | ✅ Xong |
| TV2 | Nguyễn Đức Khải | Chương 1 — lý thuyết Deadlock | `tv2-chuong-ly-thuyet` | ⬜ Chưa nộp |
| TV3 | Đặng Hoàng Phong | Chương 2 — đặc tả thuật toán | `tv3-dac-ta-thuat-toan` | ✅ Xong |
| TV4 | Nguyễn Minh Trí | Engine — mã nguồn lõi | `tv4-engine` | ✅ Xong |
| TV5 | Trần Đức Tân | Giao diện — nhập liệu và dữ liệu | `tv5-gui-nhap-lieu` | 🟡 Chạy được, cần hoàn thiện |
| TV6 | Nguyễn Thái | Giao diện — mô phỏng và trực quan | `tv6-gui-mo-phong` | 🟡 Chạy được, cần hoàn thiện |
| TV7 | Văn Hoàng | Chương 3 — so sánh hai giải thuật | `tv7-chuong-so-sanh` | ⬜ Chưa nộp — **đã có sẵn số liệu đo** |
| TV8 | Võ Nguyên Thảo | Chương 5 — kiểm thử và kết quả | `tv8-kiem-thu` | ⬜ Chưa nộp — 17 test đã chạy xanh |

---

## Chạy chương trình

Cài thư viện giao diện (chỉ TV5, TV6 cần):

```bash
pip install PyQt5
```

Chạy phần mềm:

```bash
python -m gui.GUI_TV6
```

Chạy engine từ dòng lệnh, không cần giao diện:

```bash
python -m engine.demo
```

Kết quả mong đợi với bộ dữ liệu chuẩn: **AN TOÀN**, chuỗi `P1 → P3 → P0 → P2 → P4`, `Work` cuối `(10, 5, 7)`.

Chạy kiểm thử:

```bash
python -m unittest discover -s tests -v
```

Đo hiệu năng, xuất CSV cho TV7:

```bash
python -m scripts.do_hieu_nang
```

---

## API của engine — đọc trước khi viết bất kỳ dòng nào

> **Quan trọng nhất trong README này.** Đã từng có ba bộ tên hàm khác nhau cùng tồn tại trong dự án, khiến giao diện gọi một engine không hề tồn tại và chương trình bung ngay khi khởi động. Giờ tất cả đi qua **một API duy nhất**. Đừng tự tạo module engine khác.

```python
from engine.banker_types import BankerState, Verdict, LoiDuLieu
from engine.banker import (
    kiem_tra_hop_le,        # ném LoiDuLieu nếu dữ liệu sai
    kiem_tra_an_toan,       # -> SafetyResult
    yeu_cau_tai_nguyen,     # -> RequestResult
    giai_phong,
    ket_thuc_tien_trinh,
    tat_ca_chuoi_an_toan,
)

tt = BankerState.from_json_file("data/vi-du-chuan.json")
kq = kiem_tra_an_toan(tt)
print(kq.an_toan, kq.chuoi_dep())      # True  'P1 → P3 → P0 → P2 → P4'

r = yeu_cau_tai_nguyen(tt, 1, [1, 0, 2])
print(r.ket_luan, r.ly_do)             # Verdict.CAP_PHAT  'Cấp phát: ...'
```

**Kiểu dữ liệu trả về**

| Lớp | Trường |
|---|---|
| `BankerState` | `available`, `max`, `allocation`, `need` (tự tính), `total`, `n`, `m`, `copy()` |
| `SafetyResult` | `an_toan`, `chuoi`, `nhat_ky` (danh sách `StepLog`), `treo`, `chuoi_dep()` |
| `StepLog` | `buoc`, `work_truoc`, `tien_trinh`, `need`, `allocation`, `work_sau`, `bo_qua` |
| `RequestResult` | `ket_luan` (`Verdict`), `ly_do`, `nhat_ky` |
| `Verdict` | `CAP_PHAT`, `CHO`, `LOI` |

**Hai điều đừng làm**

- Đừng tự tính `Need` rồi lưu lại. `BankerState.need` tự tính từ `max − allocation` mỗi lần đọc nên không bao giờ lệch.
- Đừng import PyQt hay tkinter vào `engine/`. Engine phải chạy được từ dòng lệnh để TV8 kiểm thử tự động.

Giao diện không gọi thẳng engine mà đi qua [`gui/engine_adapter.py`](gui/engine_adapter.py) — nếu engine đổi thì chỉ phải sửa một chỗ.

---

## Cấu trúc thư mục

```
engine/    Thuật toán Banker, không phụ thuộc giao diện        TV4
  banker_types.py   Hợp đồng dữ liệu dùng chung                TV1
  banker.py         Hai thủ tục chính của giải thuật           TV4
  demo.py           Chạy thử từ dòng lệnh                      TV4
gui/       Giao diện phần mềm                                  TV5, TV6
  GUI_TV6.py        Cửa sổ chính, nhập liệu, mô phỏng          TV5, TV6
  bang_yeu_cau.py   Yêu cầu, giải phóng, hoàn tác, biểu đồ     TV6
  engine_adapter.py Cầu nối giữa engine và giao diện           TV6
  xuat_bao_cao.py   Xuất kết quả ra HTML / Excel               TV1
scripts/   Đo hiệu năng, xuất CSV cho Chương 3                 TV4
tests/     Kiểm thử tự động — 17 ca                            TV8
data/      3 bộ dữ liệu mẫu .json                              TV5
docs/      Đề bài, kế hoạch, kiến trúc chương trình            TV1
report/    Quyển báo cáo — mỗi chương một thư mục riêng
```

**Quy tắc quan trọng nhất:** mỗi thư mục có đúng một chủ sở hữu, và **chỉ chủ sở hữu được sửa file bên trong**.

File Word là file nhị phân — Git không merge được. Hai người cùng sửa một file `.docx` sẽ tạo ra xung đột không gỡ được, buộc phải bỏ hẳn một bản.

---

## Bắt đầu làm việc

### Bước 1 — Khai báo danh tính (làm một lần, trên máy của chính mình)

Email phải **trùng với email đăng ký GitHub của bạn**. Nếu sai, commit không gắn được vào tài khoản và biểu đồ đóng góp sẽ trống — đúng thứ giáo viên nhìn để đánh giá.

```bash
git config --global user.name "Họ Tên Thật"
```

```bash
git config --global user.email "email-github-cua-ban@gmail.com"
```

### Bước 2 — Tải repo về máy

```bash
git clone https://github.com/BryannLee202/HDH_De_tai_9_Giai_thuat_Banker.git
```

### Bước 3 — Sang nhánh của mình

Tám nhánh đã tạo sẵn nên **không dùng `-b`**. Repo cũng đang chặn tạo nhánh mới, gõ `git checkout -b` sẽ bị từ chối — đó không phải lỗi Git.

```bash
git checkout tv4-engine
```

### Bước 4 — Lấy bản mới nhất trước khi làm

```bash
git pull origin main
```

### Bước 5 — Làm việc rồi lưu lên

```bash
git add . && git commit -m "TV4: cai dat ham kiem_tra_an_toan" && git push
```

### Bước 6 — Tạo pull request

Vào GitHub bấm **Compare & pull request**, gán TV1 duyệt. **Không ai đẩy thẳng vào `main`** — repo đã bật ràng buộc chặn.

---

## Nếu bạn không code (TV2, TV3, TV7)

Không cần dùng dòng lệnh. Chọn một trong hai cách:

- **GitHub Desktop** — cài đặt, đăng nhập, kéo file vào rồi bấm nút.
- **Ngay trên web GitHub** — đổi nhánh sang nhánh của mình, mở đúng thư mục chương, bấm **Add file → Upload files**, kéo file `.docx` vào, gõ mô tả rồi **Commit changes**.

Cả hai cách đều tính là commit của bạn, miễn là đăng nhập bằng tài khoản của chính mình.

**Đừng nộp bằng file `.zip`.** GitHub không diff được file nén nên không ai review từng dòng hay góp ý được, và `.gitignore` đã chặn sẵn `*.zip`.

---

## Quy ước commit

Mở đầu bằng mã thành viên, viết không dấu để tránh lỗi phông trên máy khác:

```
TV3: bo sung vi du chay tay 5 vong lap
TV5: chan du lieu khi Allocation vuot qua Max
TV8: them 5 ca kiem thu bien
```

**Mỗi người tối thiểu 5 commit, rải đều 4 tuần.** Commit dồn hết vào đêm trước hạn nộp thì nhìn lịch sử là biết ngay.

---

## Quy tắc chung

- **Không ai đẩy thẳng vào `main`**, tất cả qua pull request. Chỉ TV1 được bấm Merge.
- **Không tạo nhánh mới** — 8 nhánh đã đủ, repo đang chặn.
- **Không dùng `git push --force`.** Đây là lệnh duy nhất có thể xoá vĩnh viễn lịch sử. Repo có chặn nhưng đừng tập thói quen đó.
- **Không commit video demo** — GitHub chặn file trên 100 MB. Để trên Google Drive rồi dán link vào mục cuối README.
- **Repo đang ở chế độ public.** Nhóm khác đọc được, nên **đừng đẩy quyển báo cáo hoàn chỉnh lên trước khi nộp**. Code và khung thư mục thì công khai không sao.
- Họp 2 buổi mỗi tuần, biên bản lưu ở `report/bien-ban-hop/`.
- Hạn nội bộ sớm hơn hạn nộp 3 ngày.

---

## Việc tiếp theo của từng người

**TV2** — Chương 1: 4 điều kiện Coffman, 4 hướng xử lý, phân biệt deadlock / starvation / livelock, bài toán 5 triết gia. Tối thiểu 5 hình tự vẽ, nộp kèm file nguồn `.drawio`.

**TV5, TV6** — Cài PyQt5 rồi chạy `python -m gui.GUI_TV6` để kiểm tra bằng mắt. Phần còn thiếu: tô sáng hàng tiến trình đang xét trên bảng `Need`, hộp thoại xác nhận khi xoá trắng, và quay video demo 3–5 phút.

**TV7** — Chương 3. Số liệu đo đã có sẵn trong `scripts/ket_qua_hieu_nang.csv`, chạy lại bằng `python -m scripts.do_hieu_nang`. Kết quả cho thấy **dữ liệu ngẫu nhiên tăng gần tuyến tính, còn trường hợp xấu nhất mới đúng bậc hai** — nêu được điều này là điểm cộng, vì `O(m·n²)` là cận trên chặt chứ không phải mô tả trung bình. Hình đồ thị phân bổ tài nguyên lấy từ phần mềm (`gui/bang_yeu_cau.py`).

**TV8** — Chương 5. 17 ca kiểm thử trong `tests/test_banker.py` đã xanh; bổ sung tối thiểu 5 ca của riêng mình, chạy phần mềm thật và chụp màn hình từng ca. Soạn 15 câu hỏi phản biện cho cả nhóm.

---

## Tài liệu học theo vai trò

### Dùng chung cho cả 8 người

| Tài liệu | Ở đâu |
|---|---|
| Kế hoạch phân công đầy đủ | `docs/Phan-cong-De-tai-9-Giai-thuat-Banker.pdf` — **mục 03 là phần ai cũng phải nắm** |
| Kiến trúc chương trình, 4 biểu đồ | [`docs/kien-truc.md`](docs/kien-truc.md) — GitHub tự vẽ ra hình, chụp màn hình chèn thẳng vào Word |
| Ảnh đề bài gốc | `docs/de-bai/de-bai-goc.jpg` |
| Silberschatz — *Operating System Concepts*, chương **Deadlocks** | https://www.os-book.com |
| Slide bài giảng của thầy | Nguồn sát đề nhất. Nếu ký hiệu khác sách thì **theo slide**, vì thầy chấm theo đó |

### Theo vai trò

- **TV1** — [Pull request](https://docs.github.com/en/pull-requests) · [Vẽ UML](https://app.diagrams.net) · [openpyxl](https://openpyxl.readthedocs.io) · [PyInstaller](https://pyinstaller.org/en/stable/)
- **TV2** — Silberschatz các mục đầu chương Deadlocks. Bài toán 5 triết gia nằm ở chương **Synchronization**, không phải chương Deadlocks
- **TV3** — Mã giả đã có sẵn trong chú thích của `engine/banker.py`; kết quả kỳ vọng nằm trong `tests/test_banker.py`
- **TV4** — [dataclass](https://docs.python.org/3/library/dataclasses.html) · [sao chép sâu](https://docs.python.org/3/library/copy.html) · [unittest](https://docs.python.org/3/library/unittest.html)
- **TV5** — [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/) · [QTableWidget](https://doc.qt.io/qt-5/qtablewidget.html) · [JSON](https://docs.python.org/3/library/json.html)
- **TV6** — [QTimer](https://doc.qt.io/qt-5/qtimer.html) · [QSlider](https://doc.qt.io/qt-5/qslider.html) · lớp `StepLog` chính là cấu trúc cột của bảng nhật ký
- **TV7** — Silberschatz mục **Resource-Allocation Graph** · phát hiện chu trình trong đồ thị có hướng
- **TV8** — [unittest](https://docs.python.org/3/library/unittest.html) · [GitHub Issues](https://docs.github.com/en/issues)

---

## Video demo

*(TV6 dán link Google Drive vào đây)*
