import colorsys
import random

__all__ = ["Color"]


class Color:
    # Primary Colors
    BLACK = (0, 0, 0)  # rgb(0, 0, 0)
    WHITE = (255, 255, 255)  # rgb(255, 255, 255)
    BLUE = (0, 0, 255)  # rgb(0, 0, 255)
    YELLOW = (255, 255, 0)  # rgb(255, 255, 0)
    RED = (255, 0, 0)  # rgb(255, 0, 0)
    LEGO_BLUE = (0, 50, 150)  # rgb(0, 50, 150)
    LEGO_ORANGE = (255, 150, 40)  # rgb(255, 150, 40)
    VIOLET = (181, 126, 220)  # rgb(181, 126, 220)
    ORANGE = (255, 165, 0)  # rgb(255, 165, 0)
    GREEN = (0, 128, 0)  # rgb(0, 128, 0)
    GRAY = (128, 128, 128)  # rgb(128, 128, 128)
    # Extended Colors
    IVORY = (255, 255, 240)  # rgb(255, 255, 240)
    BEIGE = (245, 245, 220)  # rgb(245, 245, 220)
    WHEAT = (245, 222, 179)  # rgb(245, 222, 179)
    TAN = (210, 180, 140)  # rgb(210, 180, 140)
    KHAKI = (195, 176, 145)  # rgb(195, 176, 145)
    SILVER = (192, 192, 192)  # rgb(192, 192, 192)
    CHARCOAL = (70, 70, 70)  # rgb(70, 70, 70)
    NAVYBLUE = (0, 0, 128)  # rgb(0, 0, 128)
    ROYALBLUE = (8, 76, 158)  # rgb(8, 76, 158)
    MEDIUMBLUE = (0, 0, 205)  # rgb(0, 0, 205)
    AZURE = (0, 127, 255)  # rgb(0, 127, 255)
    CYAN = (0, 255, 255)  # rgb(0, 255, 255)
    AQUAMARINE = (127, 255, 212)  # rgb(127, 255, 212)
    TEAL = (0, 128, 128)  # rgb(0, 128, 128)
    FORESTGREEN = (34, 139, 34)  # rgb(34, 139, 34)
    OLIVE = (128, 128, 0)  # rgb(128, 128, 0)
    LIME = (191, 255, 0)  # rgb(191, 255, 0)
    GOLD = (255, 215, 0)  # rgb(255, 215, 0)
    SALMON = (250, 128, 114)  # rgb(250, 128, 114)
    HOTPINK = (252, 15, 192)  # rgb(252, 15, 192)
    FUCHSIA = (255, 119, 255)  # rgb(255, 119, 255)
    PUCE = (204, 136, 153)  # rgb(204, 136, 153)
    PLUM = (132, 49, 121)  # rgb(132, 49, 121)
    INDIGO = (75, 0, 130)  # rgb(75, 0, 130)
    MAROON = (128, 0, 0)  # rgb(128, 0, 0)
    CRIMSON = (220, 20, 60)  # rgb(220, 20, 60)
    LIGHTGRAY = (211, 211, 211)  # rgb(211, 211, 211)
    DEFAULT = (211, 211, 211)  # rgb(102, 102, 102)
    BACKGROUND = (211, 211, 211)  # rgb(102, 102, 102)
    # --------------------------------------------------------------

    colors = [
        BLACK,
        WHITE,
        BLUE,
        YELLOW,
        RED,
        VIOLET,
        ORANGE,
        GREEN,
        GRAY,
        IVORY,
        BEIGE,
        WHEAT,
        TAN,
        KHAKI,
        SILVER,
        CHARCOAL,
        NAVYBLUE,
        ROYALBLUE,
        MEDIUMBLUE,
        AZURE,
        CYAN,
        AQUAMARINE,
        TEAL,
        FORESTGREEN,
        OLIVE,
        LIME,
        GOLD,
        SALMON,
        HOTPINK,
        FUCHSIA,
        PUCE,
        PLUM,
        INDIGO,
        MAROON,
        CRIMSON,
        LIGHTGRAY,
        DEFAULT,
    ]

    # Colors 변환 https://www.rapidtables.com/convert/color/hex-to-rgb.html
    colour_codes = {
        "indianred": "#CD5C5C",  # rgb(205, 92, 92)
        "lightcoral": "#F08080",  # rgb(240, 128, 128)
        "salmon": "#FA8072",  # rgb(250, 128, 114)
        "darksalmon": "#E9967A",  # rgb(233, 150, 122)
        "lightsalmon": "#FFA07A",  # rgb(255, 160, 122)
        "crimson": "#DC143C",  # rgb(220, 20, 60)
        "red": "#FF0000",  # rgb(255, 0, 0)
        "firebrick": "#B22222",  # rgb(178, 34, 34)
        "darkred": "#8B0000",  # rgb(139, 0, 0)
        "pink": "#FFC0CB",  # rgb(255, 192, 203)
        "lightpink": "#FFB6C1",  # rgb(255, 182, 193)
        "hotpink": "#FF69B4",  # rgb(255, 105, 180)
        "deeppink": "#FF1493",  # rgb(255, 20, 147)
        "mediumvioletred": "#C71585",  # rgb(199, 21, 133)
        "palevioletred": "#DB7093",  # rgb(219, 112, 147)
        "lightsalmon": "#FFA07A",  # rgb(255, 160, 122)
        "coral": "#FF7F50",  # rgb(255, 127, 80)
        "tomato": "#FF6347",  # rgb(255, 99, 71)
        "orangered": "#FF4500",  # rgb(255, 69, 0)
        "darkorange": "#FF8C00",  # rgb(255, 140, 0)
        "orange": "#FFA500",  # rgb(255, 165, 0)
        "gold": "#FFD700",  # rgb(255, 215, 0)
        "yellow": "#FFFF00",  # rgb(255, 255, 0)
        "lightyellow": "#FFFFE0",  # rgb(255, 255, 224)
        "lemonchiffon": "#FFFACD",  # rgb(255, 250, 205)
        "lightgoldenrodyellow": "#FAFAD2",  # rgb(250, 250, 210)
        "papayawhip": "#FFEFD5",  # rgb(255, 250, 205)
        "moccasin": "#FFE4B5",  # rgb(255, 228, 181)
        "peachpuff": "#FFDAB9",  # rgb(255, 218, 185)
        "palegoldenrod": "#EEE8AA",  # rgb(238, 232, 170)
        "khaki": "#F0E68C",  # rgb(240, 230, 140)
        "darkkhaki": "#BDB76B",  # rgb(189, 183, 107)
        "lavender": "#E6E6FA",  # rgb(230, 230, 250)
        "thistle": "#D8BFD8",  # rgb(216, 191, 216)
        "plum": "#DDA0DD",  # rgb(221, 160, 221)
        "violet": "#EE82EE",  # rgb(238, 130, 238)
        "orchid": "#DA70D6",  # rgb(218, 112, 214)
        "fuchsia": "#FF00FF",  # rgb(255, 0, 255)
        "magenta": "#FF00FF",  # rgb(255, 0, 255)
        "mediumorchid": "#BA55D3",  # rgb(186, 85, 211)
        "mediumpurple": "#9370DB",  # rgb(147, 112, 219)
        "rebeccapurple": "#663399",  # rgb(102, 51, 153)
        "blueviolet": "#8A2BE2",  # rgb(138, 43, 226)
        "darkviolet": "#9400D3",  # rgb(148, 0, 211)
        "darkorchid": "#9932CC",  # rgb(153, 50, 204)
        "darkmagenta": "#8B008B",  # rgb(139, 0, 139)
        "purple": "#800080",  # rgb(128, 0, 128)
        "indigo": "#4B0082",  # rgb(75, 0, 130)
        "slateblue": "#6A5ACD",  # rgb(106, 90, 205)
        "darkslateblue": "#483D8B",  # rgb(72, 61, 139)
        "mediumslateblue": "#7B68EE",  # rgb(123, 104, 238)
        "greenyellow": "#ADFF2F",  # rgb(173, 255, 47)
        "chartreuse": "#7FFF00",  # rgb(127, 255, 0)
        "lawngreen": "#7CFC00",  # rgb(127, 255, 0)
        "lime": "#00FF00",  # rgb(0, 255, 0)
        "limegreen": "#32CD32",  # rgb(50, 205, 50)
        "palegreen": "#98FB98",  # rgb(152, 251, 152)
        "lightgreen": "#90EE90",  # rgb(144, 238, 144)
        "mediumspringgreen": "#00FA9A",  # rgb(0, 250, 154)
        "springgreen": "#00FF7F",  # rgb(0, 255, 127)
        "mediumseagreen": "#3CB371",  # rgb(60, 179, 113)
        "seagreen": "#2E8B57",  # rgb(46, 139, 87)
        "forestgreen": "#228B22",  # rgb(34, 139, 34)
        "green": "#008000",  # rgb(0, 128, 0)
        "darkgreen": "#006400",  # rgb(0, 100, 0)
        "yellowgreen": "#9ACD32",  # rgb(154, 205, 50)
        "olivedrab": "#6B8E23",  # rgb(107, 142, 35)
        "olive": "#808000",  # rgb(128, 128, 0)
        "darkolivegreen": "#556B2F",  # rgb(85, 107, 47)
        "mediumaquamarine": "#66CDAA",  # rgb(102, 205, 170)
        "darkseagreen": "#8FBC8B",  # rgb(143, 188, 139)
        "lightseagreen": "#20B2AA",  # rgb(32, 178, 170)
        "darkcyan": "#008B8B",  # rgb(0, 139, 139)
        "teal": "#008080",  # rgb(0, 128, 128)
        "aqua": "#00FFFF",  # rgb(0, 255, 255)
        "cyan": "#00FFFF",  # rgb(0, 255, 255)
        "lightcyan": "#E0FFFF",  # rgb(224, 255, 255)
        "paleturquoise": "#AFEEEE",  # rgb(175, 238, 238)
        "aquamarine": "#7FFFD4",  # rgb(127, 255, 212)
        "turquoise": "#40E0D0",  # rgb(64, 224, 208)
        "mediumturquoise": "#48D1CC",  # rgb(72, 209, 204)
        "darkturquoise": "#00CED1",  # rgb(0, 206, 209)
        "cadetblue": "#5F9EA0",  # rgb(95, 158, 160)
        "steelblue": "#4682B4",  # rgb(70, 130, 180)
        "lightsteelblue": "#B0C4DE",  # rgb(176, 196, 222)
        "powderblue": "#B0E0E6",  # rgb(176, 224, 230)
        "lightblue": "#ADD8E6",  # rgb(173, 216, 230)
        "skyblue": "#87CEEB",  # rgb(135, 206, 235)
        "lightskyblue": "#87CEFA",  # rgb(135, 206, 250)
        "deepskyblue": "#00BFFF",  # rgb(0, 191, 255)
        "dodgerblue": "#1E90FF",  # rgb(30, 144, 255)
        "cornflowerblue": "#6495ED",  # rgb(100, 149, 237)
        "mediumslateblue": "#7B68EE",  # rgb(123, 104, 238)
        "royalblue": "#4169E1",  # rgb(65, 105, 225)
        "blue": "#0000FF",  # rgb(0, 0, 255)
        "mediumblue": "#0000CD",  # rgb(0, 0, 205)
        "darkblue": "#00008B",  # rgb(0, 0, 139)
        "navy": "#000080",  # rgb(0, 0, 128)
        "midnightblue": "#191970",  # rgb(25, 25, 112)
        "cornsilk": "#FFF8DC",  # rgb(255, 248, 220)
        "blanchedalmond": "#FFEBCD",  # rgb(255, 235, 205)
        "bisque": "#FFE4C4",  # rgb(255, 228, 196)
        "navajowhite": "#FFDEAD",  # rgb(255, 222, 173)
        "wheat": "#F5DEB3",  # rgb(245, 222, 179)
        "burlywood": "#DEB887",  # rgb(222, 184, 135)
        "tan": "#D2B48C",  # rgb(210, 180, 140)
        "rosybrown": "#BC8F8F",  # rgb(188, 143, 143)
        "sandybrown": "#F4A460",  # rgb(244, 164, 96)
        "goldenrod": "#DAA520",  # rgb(218, 165, 32)
        "darkgoldenrod": "#B8860B",  # rgb(184, 134, 11)
        "peru": "#CD853F",  # rgb(205, 133, 63)
        "chocolate": "#D2691E",  # rgb(210, 105, 30)
        "saddlebrown": "#8B4513",  # rgb(139, 69, 19)
        "sienna": "#A0522D",  # rgb(160, 82, 45)
        "brown": "#A52A2A",  # rgb(165, 42, 42)
        "maroon": "#800000",  # rgb(128, 0, 0)
        "white": "#FFFFFF",  # rgb(255, 255, 255)
        "snow": "#FFFAFA",  # rgb(255, 250, 250)
        "honeydew": "#F0FFF0",  # rgb(240, 255, 240)
        "mintcream": "#F5FFFA",  # rgb(245, 255, 250)
        "azure": "#F0FFFF",  # rgb(240, 255, 255)
        "aliceblue": "#F0F8FF",  # rgb(240, 248, 255)
        "ghostwhite": "#F8F8FF",  # rgb(248, 248, 255)
        "whitesmoke": "#F5F5F5",  # rgb(245, 245, 245)
        "seashell": "#FFF5EE",  # rgb(255, 245, 238)
        "beige": "#F5F5DC",  # rgb(245, 245, 220)
        "oldlace": "#FDF5E6",  # rgb(253, 245, 230)
        "floralwhite": "#FFFAF0",  # rgb(255, 250, 240)
        "ivory": "#FFFFF0",  # rgb(255, 255, 240)
        "antiquewhite": "#FAEBD7",  # rgb(250, 235, 215)
        "linen": "#FAF0E6",  # rgb(250, 240, 230)
        "lavenderblush": "#FFF0F5",  # rgb(255, 240, 245)
        "mistyrose": "#FFE4E1",  # rgb(255, 228, 225)
        "gainsboro": "#DCDCDC",  # rgb(220, 220, 220)
        "lightgray": "#D3D3D3",  # rgb(211, 211, 211)
        "silver": "#C0C0C0",  # rgb(192, 192, 192)
        "darkgray": "#A9A9A9",  # rgb(169, 169, 169)
        "gray": "#808080",  # rgb(128, 128, 128)
        "dimgray": "#696969",  # rgb(105, 105, 105)
        "lightslategray": "#778899",  # rgb(119, 136, 153)
        "slategray": "#708090",  # rgb(112, 128, 144)
        "darkslategray": "#2F4F4F",  # rgb(47, 79, 79)
        "black": "#000000",  # rgb(0, 0, 0)
    }

    @classmethod
    def random(cls):
        r = random.randint(1, (len(cls.colors) - 1))
        return cls.colors[r]

    @classmethod
    def rgb_to_bgr(cls, tpl):
        return (tpl[2], tpl[1], tpl[0])

    @classmethod
    def bgr_to_rgb(cls, tpl):
        return (tpl[2], tpl[1], tpl[0])

    @classmethod
    def hsv(cls, tpl):
        hsv_float = colorsys.rgb_to_hsv(*tpl)
        return (hsv_float[0] * 180, hsv_float[1] * 255, hsv_float[2])

    @classmethod
    def hsv_to_rgb(cls, HSV):
        """Converts an integer HSV tuple (value range from 0 to 255) to an RGB tuple"""

        # Unpack the HSV tuple for readability
        H, S, V = HSV

        # Check if the color is Grayscale
        if S == 0:
            R = V
            G = V
            B = V
            return (R, G, B)

        # Make hue 0-5
        region = H // 43

        # Find remainder part, make it from 0-255
        remainder = (H - (region * 43)) * 6

        # Calculate temp vars, doing integer multiplication
        P = (V * (255 - S)) >> 8
        Q = (V * (255 - ((S * remainder) >> 8))) >> 8
        T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8

        # Assign temp vars based on color cone region
        if region == 0:
            R = V
            G = T
            B = P

        elif region == 1:
            R = Q
            G = V
            B = P

        elif region == 2:
            R = P
            G = V
            B = T

        elif region == 3:
            R = P
            G = Q
            B = V

        elif region == 4:
            R = T
            G = P
            B = V

        else:
            R = V
            G = P
            B = Q
        return (R, G, B)

    def RGB_2_HSV(RGB):
        """Converts an integer RGB tuple (value range from 0 to 255) to an HSV tuple"""

        # Unpack the tuple for readability
        R, G, B = RGB

        # Compute the H value by finding the maximum of the RGB values
        RGB_Max = max(RGB)
        RGB_Min = min(RGB)

        # Compute the value
        V = RGB_Max
        if V == 0:
            H = S = 0
            return (H, S, V)

        # Compute the saturation value
        S = 255 * (RGB_Max - RGB_Min) // V

        if S == 0:
            H = 0
            return (H, S, V)

        # Compute the Hue
        if RGB_Max == R:
            H = 0 + 43 * (G - B) // (RGB_Max - RGB_Min)
        elif RGB_Max == G:
            H = 85 + 43 * (B - R) // (RGB_Max - RGB_Min)
        else:  # RGB_MAX == B
            H = 171 + 43 * (R - G) // (RGB_Max - RGB_Min)

        return (H, S, V)
