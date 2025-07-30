from pyfiglet import figlet_format
from typing import Any as Unknown

def recolor_vertical(text: Unknown, start_color: tuple, end_color: tuple) -> Unknown:

    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    
    lines = text.split('\n')
    colored_lines = []
    total_lines = len(lines)
    
    for i, line in enumerate(lines):
        ratio = i / max(total_lines - 1, 1)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        color_code = f"\033[38;2;{r};{g};{b}m"
        colored_lines.append(f"{color_code}{line}")
    
    return '\n'.join(colored_lines)

#agl ____usage____
if __name__ == "__main__":

    banner = figlet_format("GD V3", font="cosmic")

    start_color = (255, 0, 0)
    end_color = (0, 0, 255)

    gradient_banner = recolor_vertical(banner, start_color, end_color)

    print(gradient_banner)