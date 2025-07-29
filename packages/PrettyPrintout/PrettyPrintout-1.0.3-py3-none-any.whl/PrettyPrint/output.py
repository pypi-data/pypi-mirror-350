import sys
import os
import PrettyPrint.format as format
import time


class Printer:
    def __init__(self, log_type=None, timestamps=False, log_prefix='', location=''):
        '''
        Initialize the Outputter. On call takes a text and prints it to console with the specified formatting
        Also logs everything to a file if log_type is {html, txt}
        :param log_type: the type of logfile created, if None, no file is created. if 'html' formatted html, if 'txt' plain text txt
        :param timestamps: controls whether to print timestamps before each output
        '''
        if location != '':
            if os.path.exists(location):
                if os.path.isdir(location):
                    pass
                else:
                    raise ValueError(f'Got log location path {location} but the path is a file. Needs to be a directory')
            else:
                os.mkdir(location)
        if log_type in ['html', 'txt']:
            self.log_type = log_type
            filename = f"""{location}/{time.strftime("%Y%m%d-%H%M")}_{log_prefix}_PrettyPrint_Autolog.{self.log_type}"""
            self.log = open(filename, 'w')
            if log_type == 'html':
                html_init_str = '<!DOCTYPE html>\n<html>\n  <head>\n        <title>'+filename+'</title>\n   </head>\n   <body>\n'
                self.log.write(html_init_str)
        else:
            self.log = None

        self.timestamps = timestamps

    def __call__(self, msg, fmt=None):
        '''
        Prints a formatted message to the console and logs it to a file if log_type is {html, txt}
        :param msg: String The text to be printed
        :param fmt: String The format to print with, constructed using Builder.Compose() with the ansi_util callables.
        :return:
        '''
        if isinstance(fmt, format.PPFormat):
            formatter = str(fmt)
        elif fmt is None:
            formatter = "\033[0m"
        else:
            raise ValueError(
                f"fmt is not a suppoerted datastructure, expected format.PPFormat or None, got {str(type(fmt))} instead")

        if self.timestamps:
            sys.stdout.write(f"""{time.strftime("%Y-%m-%d-%H:%M:%S - ")}{formatter}{msg}\033[0m\n""")
        else:
            sys.stdout.write(f"{formatter}{msg}\033[0m\n")

        if self.log is not None:
            if self.log_type == 'html':
                #self.log.write("""      <p style="color: {}; font-family: 'Liberation Sans',sans-serif">{}</p>\n""".format(colour, msg))
                self.log.write(msg + '\n')

            elif self.log_type == 'txt':
                self.log.write(msg+'\n')


    def __del__(self):
        '''
        Called on delete to close the file and finish html if log_type is html
        :return:
        '''
        if self.log is not None:
            if self.log_type == 'html':
                html_closing_str = '    </body>\n</html>'
                self.log.write(html_closing_str)
            self.log.close()


    def tagged_print(self, tag, msg, tag_fmt, msg_fmt=format.Default()):
        if isinstance(tag_fmt, format.PPFormat):
            tag_fmt = str(tag_fmt)
        else:
            raise TypeError(f"Unbrecognized type for tag format: {type(tag_fmt)}")
        if isinstance(msg_fmt, format.PPFormat):
            msg_fmt = str(msg_fmt)
        else:
            raise TypeError(f"Unbrecognized type for message format: {type(msg_fmt)}")

        if self.timestamps: #
            self.__call__(f"""{time.strftime("%Y-%m-%d-%H:%M:%S - ")}{tag_fmt}{tag}\033[0m:{msg_fmt} {msg}\033[0m""")
        else:
            self.__call__(f"{tag_fmt}{tag}\033[0m:{msg_fmt} {msg}\033[0m")


    def warning(self, msg):
        self.tagged_print('WARNING', msg, format.Warning(), format.Default())

    def error(self, msg):
        self.tagged_print('ERROR', msg, format.Error(), format.Default())

    def success(self, msg):
        self.tagged_print('SUCCESS', msg, format.Success(), format.Default())

    def fail(self, msg):
        self.tagged_print('FAIL', msg, format.Error(), format.Default())

