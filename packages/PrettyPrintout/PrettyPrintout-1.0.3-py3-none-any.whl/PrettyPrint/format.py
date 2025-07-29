from PrettyPrint import ansi


class ColourText:
    def __init__(self, colour='default', option='default'):
        if isinstance(colour, str):
            if colour in ansi._COLOURS:
                if option == 'default':
                    self.fmt = f"\033[3{ansi._COLOURS[colour]}m"
                elif option == 'bright':
                    self.fmt = f"\033[9{ansi._COLOURS[colour]}m"
                else:
                    raise ValueError(f"Selected option doesnt exist, must be default or bright, got {option}")
            else:
                raise ValueError(f"Selected colour is not supported: {colour}")
        elif isinstance(colour, list) and all(isinstance(elem, int) for elem in colour) and isinstance(option, str):
            if option == 'default':
                self.fmt = f"\033[38;2;{colour[0]};{colour[1]};{colour[2]}m"
            elif option == 'bright':
                self.fmt = f"\033[98;2;{colour[0]};{colour[1]};{colour[2]}m"
            else:
                raise ValueError(f"Selected option doesnt exist, must be default or bright, got {option}")

            #self.fmt = f"\033[38;2;{colour[0]};{colour[1]};{colour[2]}m"
        else:
            raise TypeError('Passed colour is not a supported type! Supported types are string and list of int, got {} instead'.format(type(colour)))

    def __call__(self):
        return self.fmt


class ColourBackground:
    def __init__(self, colour='default', option='default'):
        if isinstance(colour, str):
            if colour in ansi._COLOURS:
                if option == 'default':
                    self.fmt = f"\033[4{ansi._COLOURS[colour]}m"
                elif option == 'bright':
                    self.fmt = f"\033[10{ansi._COLOURS[colour]}m"
                else:
                    raise ValueError(f"Selected option doesnt exist, must be default or bright, got {option}")
            else:
                raise ValueError(f"Selected colour is not supported: {colour}")
        elif isinstance(colour, list) and all(isinstance(elem, int) for elem in colour) and isinstance(option, str):
            if option == 'default':
                self.fmt = f"\033[48;2;{colour[0]};{colour[1]};{colour[2]}m"
            elif option == 'bright':
                self.fmt = f"\033[108;2;{colour[0]};{colour[1]};{colour[2]}m"
            else:
                raise ValueError(f"Selected option doesnt exist, must be default or bright, got {option}")

        else:
            raise TypeError(
                'Passed colour is not a supported type! Supported types are string and list of int, got {} instead'.format(
                    type(colour)))

    def __call__(self):
        return self.fmt

class Effect:
    def __init__(self, effect):
        if isinstance(effect, str):
            if effect in ansi._EFFECTS:
                self.fmt = ansi._EFFECTS[effect]
            else:
                raise ValueError(f"Selected effect is not supported")
        else:
            raise TypeError(f"Passed effect is not a supported type, must be String but got {type(effect)}")

    def __call__(self):
        return self.fmt

class Font:
    def __init__(self, font):
        if isinstance(font, str):
            if font in ansi._FONTS:
                self.fmt = ansi._FONTS[font]
            else:
                raise ValueError(f"Selected font is not supported")
        else:
            raise TypeError(f"Passed font is not a supported type, must be String but got {type(font)}")

    def __call__(self):
        return self.fmt

class PPFormat:
    def __init__(self, options='default'):
        if options == 'default':
            self.format = ''
        else:
            self.compose(options)

    def compose(self, structure):
        '''
        Concatenates all the subsequences to make a big combined sequence for formatting
        :param structure: a list of callables with objects from ansi_util
        :return:
        '''
        if self._is_list_of_callables(structure):
            fmt = ''
            for element in structure:
                fmt += element()
            self.format = fmt
        else:
            self.format = ''
            raise TypeError('The passed variable is not a list of callables.')


    def _is_list_of_callables(self, variable) -> bool:
        '''
        Checks if the passed argument is a list of callables
        :param variable: the argument to check
        :return: bool
        '''
        if isinstance(variable, list) and all(callable(item) for item in variable):
            return True
        return False

    def __str__(self):
        return self.format

class Warning(PPFormat):
    def __init__(self):
        super().__init__([ColourText('yellow'),Effect('underlined'),Effect('bold')])

class Default(PPFormat):
    def __init__(self):
        super().__init__([Effect('reset')])

class Error(PPFormat):
    def __init__(self):
        super().__init__([ColourText('red'),Effect('underlined'),Effect('bold')])

class Success(PPFormat):
    def __init__(self):
        super().__init__([ColourText('green'),Effect('underlined'),Effect('bold')])