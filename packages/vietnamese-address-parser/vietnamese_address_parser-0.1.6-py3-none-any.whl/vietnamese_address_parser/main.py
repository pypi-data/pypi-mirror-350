import re
import json
import unicodedata
import requests
from typing import Dict, List, Optional
import importlib.resources

class VietnameseAddressParser:
    """
    A class to normalize Vietnamese addresses with support for abbreviation expansion
    and OpenStreetMap Nominatim API integration.
    """
    
    # Administrative abbreviations, see more at https://vi.wikipedia.org/wiki/Ph%C3%A2n_c%E1%BA%A5p_h%C3%A0nh_ch%C3%ADnh_Vi%E1%BB%87t_Nam
    ADMIN_ABBREVIATIONS = {
        't': 'Tỉnh', 'tp': 'Thành phố',             # cấp tỉnh/thành phố trực thuộc trung ương
        'q': 'Quận', 'h': 'Huyện', 'tx': 'Thị xã',  # cấp huyện/quận
        'x': 'Xã', 'p': 'Phường', 'tt': 'Thị trấn', # cấp xã/phường
        'đ': 'Đường', 'đt': 'Đường',                # địa chỉ đường
        'kdc': 'Khu dân cư', 'kp': 'Khu phố'        # dưới cấp xã/phường, có thể thêm  làng / thôn / bản / buôn / sóc / ấp // khu dân cư / khu phố / khu vực / khóm / ấp
        # 'neighbourhood': 'Xóm'
    }
    
    # City abbreviations
    CITY_ABBREVIATIONS = {
        'hcm': 'Hồ Chí Minh', 'hn': 'Hà Nội', 'đn': 'Đà Nẵng', 
        'ct': 'Cần Thơ', 'h': 'Huế', 'hp': 'Hải Phòng',  # thành phố trực thuộc trung ương
        'td': 'Thủ Đức', 'tn': 'Thủy Nguyên'
    }
    
    # Province abbreviations
    PROVINCE_ABBREVIATIONS = { # có vài tỉnh như 'đn': 'Đắk Nông' bị trùng với 'đn': 'Đồng Nai', nên sử dụng vì OpenStreetMap thường không search được từ viết tắt
        'tth': 'Thừa Thiên Huế', 'ag': 'An Giang', 'bd': 'Bình Dương', 
        'bh': 'Biên Hòa', 'bl': 'Bạc Liêu', 'bp': 'Bình Phước', 
        'brvt': 'Bà Rịa - Vũng Tàu', 'br-vt': 'Bà Rịa - Vũng Tàu',
        'bt': 'Bình Thuận', 'cm': 'Cà Mau', 'dl': 'Đắk Lắk',
        'dt': 'Đồng Tháp', 'gl': 'Gia Lai', 'hg': 'Hậu Giang',
        'kg': 'Kiên Giang', 'la': 'Long An', 'ld': 'Lâm Đồng',
        'nb': 'Ninh Bình', 'nd': 'Nam Định', 'nt': 'Ninh Thuận',
        'pt': 'Phú Thọ', 'qb': 'Quảng Bình', 'qt': 'Quảng Trị',
        'st': 'Sóc Trăng', 'tg': 'Tiền Giang', 'tn': 'Tây Ninh',
        'tv': 'Trà Vinh', 'vl': 'Vĩnh Long'
    }
    
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    LOCATION_FILE = "tinh_qh_px_20_05_2025.json"
    
    def __init__(self, user_agent='AddressNormalizer/1.0 (contact@gmail.com)'):
        self.user_agent = user_agent
        self._compile_patterns()
        try:
            with importlib.resources.files("vietnamese_address_parser").joinpath("tinh_qh_px_20_05_2025.json").open("r", encoding="utf-8") as f:
                self.location_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load location.json from package.")
    
    def __call__(self, address: str) -> Dict[str, str]:
        return self.parser(address)

    def _compile_patterns(self):
        vn_suffix_pattern = r"(?:[\s,]*\b(vn|vietnam|việt\s*nam)\b)?[\s,]*$"
        self.admin_pattern = re.compile(r"\b(" + "|".join(sorted(self.ADMIN_ABBREVIATIONS.keys(), key=len, reverse=True)) + r")\.?(?=(?!,)[\s\.]|$)",flags=re.IGNORECASE)
        self.city_pattern = re.compile(r"\b(thành phố|tp)\.?\s*(" + "|".join(self.CITY_ABBREVIATIONS.keys()) + r")\b" + vn_suffix_pattern,flags=re.IGNORECASE)
        self.province_pattern = re.compile(r"\b(tỉnh|t)\.?\s*(" + "|".join(self.PROVINCE_ABBREVIATIONS.keys()) + r")\b" + vn_suffix_pattern,flags=re.IGNORECASE)
        self.vn_suffix_pattern = re.compile(r"[\s,]*(vn|vietnam|việt\s*nam)\s*$",flags=re.IGNORECASE)

    def expand_abbreviations(self, text: str) -> str:
        text = unicodedata.normalize('NFC', text)
        def replace_admin_terms(m: re.Match) -> str:
            return self.ADMIN_ABBREVIATIONS.get(m.group(1).lower(), m.group(0))
        def replace_city_abbr(m: re.Match) -> str:
            return f"{m.group(1)} {self.CITY_ABBREVIATIONS.get(m.group(2).lower(), m.group(2).lower())}{" Việt Nam" if m.group(3) else ""}"
        def replace_province_abbr(m: re.Match) -> str:
            return f"{m.group(1)} {self.PROVINCE_ABBREVIATIONS.get(m.group(2).lower(), m.group(2).lower())}{" Việt Nam" if m.group(3) else ""}"
        text = self.admin_pattern.sub(replace_admin_terms, text)
        text = self.city_pattern.sub(replace_city_abbr, text)
        text = self.province_pattern.sub(replace_province_abbr, text)
        for r in self.ADMIN_ABBREVIATIONS.values():
            text = re.sub(fr"(?<={re.escape(r)})\.?(?=[\d])", " ", text)    
        # text = re.sub(r"(?<=Quận)(?=[\.\d]", " ", text)
        text = self.vn_suffix_pattern.sub(", Việt Nam", text)
        return text.strip()
    
    def geocode_address(self, address: str) -> Optional[Dict[str, str]]:
        n = unicodedata.normalize('NFKD', address) # Remove accents for better matching with Nominatim
        normalized_address = ''.join([c for c in n if not unicodedata.combining(c)]) # stripping accents
        params = {'q': normalized_address,'format': 'jsonv2','addressdetails': 1,'limit': 1}
        headers = {'User-Agent': self.user_agent}
        try:
            resp = requests.get(self.NOMINATIM_URL, params=params, headers=headers, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return None
            address_data = data[0].get('address', {})
            result = {k: address_data.get(k, '') for k in address_data.keys()} # TODO: fix
            return result if address_data.get('country', '') == 'Việt Nam' else None
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"Error geocoding address with Nominatim: {e}")
            print(f"Check your Internet connection or API provider")
            return None
        
    def strip_accents(self, text: str) -> str: # Remove diacritics from a string.
        return ''.join(c for c in unicodedata.normalize('NFD', text)if unicodedata.category(c) != 'Mn')
    
    def abbreviate(self, full_name: str, keep_prefix: bool = False, keep_full: bool = False) -> str:
        name = full_name.strip()
        if not name:
            return ""
        prefix_pattern = r"^(Tỉnh|Thành phố|Quận|Huyện|Thị xã|Xã|Phường|Thị trấn)\s+"
        match = re.match(prefix_pattern, name, flags=re.IGNORECASE)
        prefix_abbr = ""
        full_prefix = ""
        if match:
            full_prefix = match.group(1)
            if keep_prefix:
                prefix_abbr = ''.join(w[0] for w in self.strip_accents(full_prefix).split()).upper()
            name = re.sub(prefix_pattern, "", name, flags=re.IGNORECASE).strip()
        if keep_full:
            raw = self.strip_accents((full_prefix + " " if keep_prefix and full_prefix else "") + name).lower()
            return re.sub(r"[\s\-–]", "", raw)
        clean = self.strip_accents(name)
        parts = re.split(r"[\s\-–]+", clean)
        body_abbr = parts[0].upper() if len(parts) == 1 else ''.join(p[0] for p in parts if p).upper()
        return prefix_abbr + body_abbr

    def match_locations(self, segments: list[str]) -> list[str]:
        n = len(segments)
        if n not in (2, 3): # sliding windows with 2 seg (there is bugs)
        # if n != 3:
            return segments
        key_abbr = "".join(self.abbreviate(seg) for seg in segments)                        # First pass: abbreviation match
        key_full = "".join(self.abbreviate(seg, keep_full=True) for seg in segments)        # Second pass: full-mode concatenation using abbreviate
        abbr_matches = []
        full_matches = []
        if n == 3:
            for city, districts in self.location_data.items():
                for district, wards in districts.items():
                    for ward in wards:
                        composite = (self.abbreviate(ward) +self.abbreviate(district) +self.abbreviate(city))
                        composite_full = (self.abbreviate(ward, keep_full=True) +self.abbreviate(district, keep_full=True) +self.abbreviate(city, keep_full=True))
                        if composite == key_abbr:
                            abbr_matches.append((ward, district, city))
                        if composite_full == key_full:
                            full_matches.append((ward, district, city))
        else:
            for city, districts in self.location_data.items():
                for district in districts:
                    composite = self.abbreviate(district) + self.abbreviate(city)
                    composite_full = (self.abbreviate(district, keep_full=True)
                                + self.abbreviate(city, keep_full=True))
                    if composite == key_abbr:
                        abbr_matches.append((district, city))
                    if composite_full == key_full:
                        full_matches.append((district, city))
        if len(abbr_matches) == 1:
            return list(abbr_matches[0])
        if len(full_matches) == 1:
            return list(full_matches[0])
        return segments # No unambiguous match: return original segments
            
    def no_accents(self, seg_list):
        prefix_pattern = re.compile(r"^(tỉnh|thành\s*phố|quận|huyện|thị\s*xã|xã|phường|thị\s*trấn|đường)\.?\s+(\S+.*)$", re.IGNORECASE)
        street_pattern = re.compile(r"^(?:(?P<st_num>\d+\S*)\s+(?P<rt>.+)|(?P<rt_only>[Đđ]ường\s+.+))$")
        street_match = street_pattern.match(seg_list[0])
        for s in seg_list[1:] if street_match else seg_list:
            if self.strip_accents(s) == s:
                return True
            match = prefix_pattern.match(s)
            if not match:
                return True
            name = match.group(2)
            if name.isalpha() and len(name) == 1:
                return True
        return False

    def parser(self, address: str) -> str:
        addr = unicodedata.normalize('NFC', address.strip())
        expanded = self.expand_abbreviations(addr)
        segments = [seg.strip() for seg in expanded.split(',')]
        
        st_num = ""
        rt_name = ""
        street_pattern = re.compile(r"^(?:(?P<st_num>\d+\S*)\s+(?P<rt>.+)|(?P<rt_only>[Đđ]ường\s+.+))$")
        street_match = street_pattern.match(segments[0])
        if street_match:
            st_num = street_match.group('st_num') or ""
            rt_name = street_match.group('rt') if street_match.group('rt') else street_match.group('rt_only')
            segments[0] = f"{st_num} {rt_name}".strip()

        if len(segments) > 6:
            return "Input have too many fields. Try shorten your address"
        
        applied = False
        if len(segments) >= 3: # (a) Try 3-segment windows -> ward, district, city
            matches3 = []
            for i in range(len(segments) - 2):
                window = segments[i:i+3]
                corr = self.match_locations(window)
                if corr != window:
                    matches3.append((i, corr))
            if len(matches3) == 1:
                i, corr = matches3[0]
                segments[i:i+3] = corr
                applied = True
        if not applied and len(segments) >= 2: # (b) Otherwise try 2-segment windows -> district, city
            matches2 = []
            for i in range(len(segments) - 1):
                window = segments[i:i+2]
                corr = self.match_locations(window)
                if corr != window:
                    matches2.append((i, corr))
            if len(matches2) == 1:
                i, corr = matches2[0]
                segments[i:i+2] = corr
                applied = True

        enhanced_addr = ', '.join(segments)
        
        if self.no_accents(segments):
            geo = self.geocode_address(enhanced_addr)
            # print(f"Need geocoding: {enhanced_addr}\nGeocoding: {geo}")
            if geo:
                raw_parts = [geo.get(k, '') for k in ['road','village','town','quarter','suburb','city_district','county','city','state','country']]
                parts = [p for p in raw_parts if p
                        # and ( any(self.strip_accents(p).lower() == self.strip_accents(orig).lower() for orig in segments)
                        # or any(self.abbreviate(p) == self.abbreviate(orig) for orig in segments)
                            # )
                        ]
                if geo.get('road') and street_match and st_num:
                    parts[0] = f"{st_num} {geo.get('road')}".strip()
                parts = [p.upper() if p.isalpha() and len(p.split()) == 1 else p for p in parts]
                return ', '.join(parts)

        prefix_pattern = re.compile(r"^(?:tỉnh|thành\s*phố|quận|huyện|thị\s*xã|xã|phường|thị\s*trấn)\.?,?\s*(.+)$",flags=re.IGNORECASE)
        street_pattern = re.compile(r"^(?:(?P<st_num>\d+\S*)\s+(?P<rt>.+)|(?P<rt_only>[Đđ]ường\s+.+))$")
        s = street_pattern.match(segments[0])
        valid_segments = []
        for idx, seg in enumerate(segments):
            seg = seg.strip()
            m = prefix_pattern.match(seg)
            if s and idx == 0:
                part = (s.group('rt') if s.group('rt') else s.group('rt_only')).strip()
                if part.lower().startswith('Đường'.lower()):
                    part = part[len('Đường'):].strip()
                cleaned_part = part
            elif m:
                temp = m.group(1).strip()
                cleaned_part = temp if not temp.isnumeric() else seg
            else:
                cleaned_part = seg
            valid_segments.append(cleaned_part)
            
        if all(len(p.split()) >= 2 for p in valid_segments) and not self.strip_accents(enhanced_addr) == enhanced_addr:
            valid_segments = ''

        comps = {} # Use Nominatim API to enhance address information
        if valid_segments:
            address_cleaned = ', '.join(valid_segments)
            comps = self.geocode_address(address_cleaned) or {}
            # print(f"{segments}\nGeocoding address: {address_cleaned}\nGeocoding result: {comps}")

        if street_match and len(rt_name.split()) == 1 and comps.get('road'): # If we have a short route name and got data from Nominatim, use it
            segments[0] = f"{st_num} {comps.get('road', rt_name)}".strip() if st_num else f"Đường {comps.get('road', rt_name)}".strip() 
        
        parts: List[str] = []
        # Format each segment
        for seg in segments:
            street_pattern = re.compile(r"^(?:(?P<st_num>\d+\S*)\s+(?P<rt>.+)|(?P<rt_only>[Đđ]ường\s+.+))$")
            street_match = street_pattern.match(segments[0])
            if street_match:
                st_num = street_match.group('st_num') or ""
                rt_name = street_match.group('rt') if street_match.group('rt') else street_match.group('rt_only')
                segments[0] = f"{st_num} {rt_name}".strip()
            match = re.match(r"^(tỉnh|thành\s*phố|quận|huyện|thị\s*xã|đường|xã|phường|thị\s*trấn)\.?\s+(\S+)$", seg, flags=re.IGNORECASE)
            if match:
                prefix = match.group(1)
                name = match.group(2)
                if (comps and len(name.split()) == 1 and name.isalpha()) or self.strip_accents(name) == name: # Try to enhance with Nominatim data
                    prefix_lower = prefix.lower().strip()
                    def safe_get(*keys):
                        for key in keys:
                            value = comps.get(key)
                            if value:
                                return value
                        return name  # fallback to original
                    if comps.get("city") and not comps.get("state") and comps["city"].lower() != "thành phố thủ đức":
                    # no state, special Thủ Đức check
                        mapping = {"thành phố": "city","quận": "suburb","huyện": "city_district","phường": "quarter","thị xã": "town","thị trấn": "town","xã": "village","đường": "road"}
                    else:
                        # state exists or Thủ Đức case
                        mapping = {'tỉnh': 'state','thành phố': 'city',"huyện": "county","phường": "suburb","thị xã": "town","thị trấn": "town","xã": "village","đường": "road"}
                    key = mapping.get(prefix_lower)
                    if key:
                        full_value = safe_get(key)
                        if full_value and self.abbreviate(name).lower() == self.abbreviate(full_value).lower():
                            name = full_value
                name = re.sub(r"^(tỉnh|thành\s*phố|quận|huyện|thị\s*xã|đường|xã|phường|thị\s*trấn)\s+", '', name, flags=re.IGNORECASE).strip()
                formatted = f"{prefix} {' '.join(name.split())}"
                parts.append(formatted)
            else:
                parts.append(' '.join(seg.split()))
        return ', '.join(parts).title()