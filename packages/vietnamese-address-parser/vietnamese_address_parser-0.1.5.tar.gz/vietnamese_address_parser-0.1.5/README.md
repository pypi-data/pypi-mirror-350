# Vietnamese Address Format Guide

---

## API Note

⚠️ **This parser integrates with the OpenStreetMap Nominatim API** to enhance address accuracy through geolocation. Because of this, some lookups may take a few seconds to complete, depending on network speed and API rate limits.

---

## CLI Usage

When you run the command:

```bash
vietnamese_address_parser
```

it will print:

```text
Vietnamese Address Parser v0.1.4
Hello! Welcome to the Vietnamese Address Parser CLI.
Usage example:
    parser = VietnameseAddressParser()
    result = parser("54-55 Bàu Cát 4, Phường 14, Tân Bình, Hồ Chí Minh")
    print(result)
```

---

## 1. House Number & Street Name

**Format**

```
{house_number}\s{prefix?}\.?\s{street_name}
```

where `{prefix}` is one of:

* `Đ.`

*or just*

```
{house_number}\s{street_name}
```

**Valid Examples**

* `123A/32 Trần Hưng Đạo`
* `45A đường Nguyễn Huệ`
* `Đường Nam Kỳ Khởi Nghĩa`
* `Đ. XVNT`

> **Invalid:**
>
> * `Nam Kỳ Khởi Nghĩa`
>   (missing “Đường” prefix)

---

## 2. Phường / Xã

**Format Options**

```
{prefix}\.?\s{phuong_xa}
```

where `{prefix}` is one of:

* `X.`
* `Xa`
* `P.`
* `Phuong`
* `TT.`
* `Thi tran`

*or just*

```
{phuong_xa}
```

**Valid Examples**

* `P. 7`
* `P. BN`
* `P. Bến Nghé`
* `Phường Bến Nghé`

---

## 3. Quận / Huyện / Thị xã

**Format Options**

```
{prefix}\.?\s{quan_huyen}
```

where `{prefix}` is one of:

* `Q.`
* `Quan`
* `H.`
* `Huyen`
* `TX.`
* `Thi xa`

*or just*

```
{quan_huyen}
```

---

## 4. Tỉnh / Thành Phố

**Format Options**

```
{prefix}\.?\s{tinh_thanh_pho}
```

where `{prefix}` is one of:

* `T.`
* `Tỉnh`
* `TP.`
* `Thanh pho`

*or just*

```
{tinh_thanh_pho}
```

---

## Usage in Python

Import and use the parser in your Python code:

```python
from vietnamese_address_parser import VietnameseAddressParser

parser = VietnameseAddressParser()
address = "54-55 Bàu Cát 4, Phường 14, Tân Bình, Hồ Chí Minh"
result = parser(address)
print(result)
```

---

## General Notes

* **Keep abbreviations to two segments or fewer** for best search performance.
* **Separate all address components with commas**, in this order:

```
{dia_chi}, {extra_field}, {phuong_xa}, {quan_huyen}, {tinh_thanh_pho}, {Việt Nam}
```

### Full Examples

1. `TP. VT, Tỉnh BR-VT`
2. `Đường XVNT, Quận Bình Thạnh, TP. HCM, VN`
3. `Đường Lê Lợi, P.1, Q.1, TP. HCM`
4. `67 Trần Kế Xương, Q. PN, TP. HCM`
5. `218 Trần Quý Cáp, X. TL, TP. PT, Tỉnh Bình Thuận`
6. `Phú Thạnh, Tân Phú, Hồ Chí Minh, Việt Nam`
7. `218 Tran Quy Cap, Thanh pho Phan Thiet, Tinh Binh Thuan`
8. `43/47 Cù Chính Lan, Thanh Khê Đông, TK, ĐN`

---

*End of Guide.*