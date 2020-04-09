from colored import fg, bg, attr


class ColorsPrint():
    def __init__(self, text, t):
        self.text = text
        self.type = t

    def do_colored(self):
        if self.type == 'suc':
            color = fg('#00D000')
        elif self.type == 'err':
            color = fg('#FFFFFF') + bg('#CE0000')
        elif self.type == 'att':
            color = fg('#312A16') + bg('#F9B800')
        elif self.type == 'inf':
            color = fg('#8440B0')
        else:
            print("Неверно указан идентификатор цветового решения")

        res = attr('reset')
        return color + self.text + res

