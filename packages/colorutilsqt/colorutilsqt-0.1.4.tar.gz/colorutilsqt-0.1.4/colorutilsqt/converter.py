def rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise ValueError("HEX string moet 6 karakters zijn.")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(r, g, b):
    r, g, b = [x / 255.0 for x in (r, g, b)]
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2

    if mx == mn:
        h = s = 0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return round(h * 360), round(s * 100), round(l * 100)

def hsl_to_rgb(h, s, l):
    h = h % 360
    s /= 100
    l /= 100

    def hue_to_rgb(p, q, t):
        t = t % 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p

    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h / 360 + 1/3)
        g = hue_to_rgb(p, q, h / 360)
        b = hue_to_rgb(p, q, h / 360 - 1/3)

    return round(r * 255), round(g * 255), round(b * 255)

def hex_to_hsl(hex_str):
    r, g, b = hex_to_rgb(hex_str)
    return rgb_to_hsl(r, g, b)

def hsl_to_hex(h, s, l):
    r, g, b = hsl_to_rgb(h, s, l)
    return rgb_to_hex(r, g, b)
