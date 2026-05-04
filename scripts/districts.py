"""AC number → district mapping for Tamil Nadu (2008 delimitation, current 2026)."""

# Each entry is (district_name, list_of_ac_numbers)
DISTRICTS = [
    ("Tiruvallur",       [1, 2, 3, 4, 5, 6, 7]),
    ("Chennai",          [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]),
    ("Kanchipuram",      [29, 36, 37]),
    ("Chengalpattu",     [30, 31, 32, 33, 34, 35]),
    ("Ranipet",          [38, 39, 41, 42]),
    ("Vellore",          [40, 43, 44]),
    ("Tirupathur",       [45, 49, 50]),
    ("Vellore",          [46, 47, 48]),  # Gudiyattam, Vaniyambadi, Ambur
    ("Krishnagiri",      [51, 52, 53, 54, 55, 56]),
    ("Dharmapuri",       [57, 58, 59, 60, 61]),
    ("Tiruvannamalai",   [62, 63, 64, 65, 66, 67, 68, 69]),
    ("Viluppuram",       [70, 71, 72, 73, 74, 75]),
    ("Kallakurichi",     [76, 77, 78, 79, 80, 81]),
    ("Salem",            [82, 83, 84, 85, 86, 87, 88, 89, 90, 91]),
    ("Namakkal",         [92, 93, 94, 95, 96, 97]),
    ("Erode",            [98, 99, 100, 101, 102, 103, 104, 105, 106, 107]),
    ("The Nilgiris",     [108, 109, 110]),
    ("Coimbatore",       [111, 116, 117, 118, 119, 120, 121, 122]),
    ("Tiruppur",         [112, 113, 114, 115]),
    ("Coimbatore",       [123, 124, 125, 126]),  # Pollachi, Valparai, Udumalpet, Madathukulam
    ("Dindigul",         [127, 128, 129, 130, 131, 132, 133]),
    ("Karur",            [134, 135, 136, 137]),
    ("Tiruchirappalli",  [138, 139, 140, 141, 142, 143, 144, 145, 146]),
    ("Perambalur",       [147, 148]),
    ("Ariyalur",         [149, 150]),
    ("Cuddalore",        [151, 152, 153, 154, 155, 156, 157, 158, 159]),
    ("Mayiladuthurai",   [160, 161, 162]),
    ("Nagapattinam",     [163, 164, 165]),
    ("Tiruvarur",        [166, 167, 168, 169]),
    ("Thanjavur",        [170, 171, 172, 173, 174, 175, 176, 177]),
    ("Pudukkottai",      [178, 179, 180, 181, 182, 183]),
    ("Sivaganga",        [184, 185, 186, 187, 188]),
    ("Madurai",          [189, 190, 191, 192, 193, 194, 195, 196, 197, 198]),
    ("Theni",            [199, 200, 201]),
    ("Virudhunagar",     [202, 203, 204, 205, 206, 207, 208]),
    ("Ramanathapuram",   [209, 210, 211, 212]),
    ("Thoothukudi",      [213, 214, 215, 216, 217, 218]),
    ("Tenkasi",          [219, 220, 221, 222, 223]),
    ("Tirunelveli",      [224, 225, 226, 227, 228]),
    ("Kanniyakumari",    [229, 230, 231, 232, 233, 234]),
]


def ac_to_district() -> dict[int, str]:
    """Return dict mapping AC number → district name."""
    out: dict[int, str] = {}
    for name, acs in DISTRICTS:
        for ac in acs:
            out[ac] = name
    return out
