from pyfiglet import figlet_format
from typing import Any as Unknown

def recolor_horizontal(text: Unknown, start_color: tuple, end_color: tuple) -> Unknown:
    
    lines = text.split('\n')
    colored_lines = []
    
    for line in lines:

        if not line.strip():

            colored_lines.append("")

            continue
            
        colored_line = []
        line_length = len(line)
        
        for i, char in enumerate(line):

            ratio = i / max(line_length - 1, 1)
            
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            color_code = f"\033[38;2;{r};{g};{b}m"
            colored_line.append(f"{color_code}{char}")
        
        colored_lines.append("".join(colored_line))
    
    return "\n".join(colored_lines)

#agl ____usage____
if __name__ == "__name__":

    banner = figlet_format("Python Banner", font = "cosmic")

    gradient_banner = recolor_horizontal(

        banner,
        start_color = (0, 0, 255),
        end_color = (255, 165, 0)
    )

    print(gradient_banner)
