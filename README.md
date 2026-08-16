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

## Phân công và nhánh làm việc

| TV | Họ tên | Nhiệm vụ | Nhánh | Thư mục sở hữu |
|---|---|---|---|---|
| TV1 | *(điền)* | Nhóm trưởng · hợp đồng dữ liệu · kiến trúc · module xuất báo cáo | `tv1-kien-truc` | `engine/banker_types.py`, `docs/`, `report/chuong-4-tv1/` |
| TV2 | *(điền)* | Chương lý thuyết Deadlock | `tv2-chuong-ly-thuyet` | `report/chuong-1-tv2/` |
| TV3 | *(điền)* | Đặc tả thuật toán · mã giả · chạy tay | `tv3-dac-ta-thuat-toan` | `report/chuong-2-tv3/` |
| TV4 | *(điền)* | Engine — mã nguồn lõi | `tv4-engine` | `engine/` |
| TV5 | *(điền)* | Giao diện — nhập liệu và dữ liệu | `tv5-gui-nhap-lieu` | `gui/`, `data/` |
| TV6 | *(điền)* | Giao diện — mô phỏng và trực quan | `tv6-gui-mo-phong` | `gui/` |
| TV7 | *(điền)* | Chương so sánh hai giải thuật | `tv7-chuong-so-sanh` | `report/chuong-3-tv7/` |
| TV8 | *(điền)* | Kiểm thử · chương kết quả · phản biện | `tv8-kiem-thu` | `tests/`, `report/chuong-5-tv8/` |

---

## Cấu trúc thư mục

```
engine/    Thuật toán Banker, không phụ thuộc giao diện
gui/       Giao diện phần mềm
tests/     Kiểm thử tự động
data/      Bộ dữ liệu mẫu .json
docs/      Đề bài, kế hoạch, biểu đồ thiết kế
report/    Quyển báo cáo — mỗi chương một thư mục riêng
```

**Quy tắc quan trọng nhất:** mỗi thư mục có đúng một chủ sở hữu, và **chỉ chủ sở hữu được sửa file bên trong**.

File Word là file nhị phân — Git không merge được. Hai người cùng sửa một file `.docx` sẽ tạo ra xung đột không gỡ được, buộc phải bỏ hẳn một bản. Chia thư mục theo người là cách duy nhất để chuyện đó không bao giờ xảy ra.

---

## Bắt đầu làm việc

### Bước 1 — Khai báo danh tính (làm một lần, trên máy của chính mình)

Email phải **trùng với email đăng ký GitHub**, nếu không commit sẽ không gắn được vào tài khoản của bạn và không hiện trong biểu đồ đóng góp — đúng thứ giáo viên nhìn vào để đánh giá.

```bash
git config --global user.name "Họ Tên Thật"
```

```bash
git config --global user.email "email-github-cua-ban@gmail.com"
```

### Bước 2 — Tải repo về máy

```bash
git clone <đường-dẫn-repo> && cd HDH
```

### Bước 3 — Sang nhánh của mình

```bash
git checkout -b tv4-engine
```

### Bước 4 — Làm việc, rồi lưu lên

```bash
git add . && git commit -m "TV4: cai dat ham is_safe" && git push -u origin tv4-engine
```

### Bước 5 — Tạo pull request

Vào GitHub, bấm **Compare & pull request**, gán TV1 duyệt. **Không ai đẩy thẳng vào `main`.**

---

## Nếu bạn không code (TV2, TV3, TV7)

Không cần dùng dòng lệnh. Chọn một trong hai cách:

- **GitHub Desktop** — cài đặt, đăng nhập, kéo file vào rồi bấm nút. Đơn giản nhất nếu bạn nộp file thường xuyên.
- **Ngay trên web GitHub** — vào đúng thư mục chương của mình, bấm **Add file → Upload files**, kéo file `.docx` vào, gõ mô tả rồi bấm **Commit changes**. Xong.

Cả hai cách đều tính là commit của bạn, miễn là bạn đăng nhập bằng tài khoản của chính mình.

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

- Repo để chế độ **private** trong lúc làm.
- Bật khoá nhánh `main` ở **Settings → Branches** để không ai đẩy thẳng vào.
- **Không commit video demo** — GitHub chặn file trên 100 MB. Để trên Google Drive rồi dán link vào mục dưới đây.
- Họp 2 buổi mỗi tuần, biên bản lưu ở `report/bien-ban-hop/`.
- Hạn nội bộ sớm hơn hạn nộp 3 ngày.

---

## Chạy chương trình

```bash
python -m engine.demo
```

Kết quả mong đợi với bộ dữ liệu chuẩn: trạng thái **an toàn**, chuỗi `<P1, P3, P4, P2, P0>`.

Chạy kiểm thử:

```bash
python -m unittest discover -s tests -v
```

---

## Video demo

*(TV6 dán link Google Drive vào đây)*
