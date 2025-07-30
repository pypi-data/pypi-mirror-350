import builtins
import logging
import os
import shutil
import sys
import time
import traceback
from contextlib import contextmanager
from functools import partial


def log_init():
    logger = logging.getLogger(__name__)
    return logger
    
class ABFormatter(logging.Formatter):
    attr_tup = [('process', 3), ('asctime', 23), ('levelname', 4), ('funcName', 8), ('pathname', 4), ('lineno', 2)]
    max_lengths = {key:val for key, val in attr_tup}
    def __init__(self, log_file):
        self.log_file = log_file
        super().__init__()
    def pad(self, string, length, idx):
        return string.ljust(length) if idx != 4 else string.rjust(length)
    def rewrite_log(self):
        bak_path = f"{self.log_file}.bak"
        with open (bak_path, mode='w', encoding='utf-8') as file_backup:
            bak_path = file_backup.name
            with open (self.log_file, 'r', encoding='utf-8') as file_log:
                for idx, line in enumerate(file_log):
                    line = line.strip()
                    if line.startswith("----"):
                        hor_line = self.draw_horizontal_line()
                        file_backup.write(f"{hor_line}\n")
                    else:
                        attr_list =line.split("|")
                        newline_arr = []
                        for attr_idx, attr in enumerate(attr_list[:-1]):
                            if attr_idx == 4:
                                lo_li_arr = attr.strip().split(":")
                                new_li = lo_li_arr[0].rjust(self.max_lengths[self.attr_tup[4][0]])
                                new_lo = lo_li_arr[1].ljust(self.max_lengths[self.attr_tup[5][0]])
                                newline_arr.append(f"{new_li}:{new_lo}")
                            else:
                                attr = attr.strip()
                                attr = attr.ljust(self.max_lengths[self.attr_tup[attr_idx][0]] + (1 if idx == 0 and attr_idx == 2 else 0))
                                newline_arr.append(attr)
                        newline_arr.append(attr_list[-1].strip())
                        file_backup.write(f"{' | '.join(newline_arr)}\n")
        try:
            shutil.copyfile(bak_path, self.log_file)
            os.remove(bak_path)
        except Exception as e:
            pass
    
    @classmethod
    def draw_horizontal_line(cls, placement="+"):
        length = sum(cls.max_lengths.values()) + 3*6 + 7
        hor_arr = ['-'*(cls.max_lengths[item[0]] + (1 if item[0] == 'levelname' else 0)) for item in cls.attr_tup]
        hor_arr[4] = hor_arr[4] + hor_arr[5] + '-'
        hor_arr.pop()
        hor_arr.append('-'*40)
        hor_line = f'-{placement}-'.join(hor_arr)
        return hor_line
        
        
        
        
    def format(self, record):
        rewrite = False
        
        if hasattr(record, 'func_id'):
            record.pathname = record.file_id
            record.funcName = record.func_id
            record.lineno = record.line_id
        lib_name = "logab"
        if record.module != "log_utils" or hasattr(record, 'func_id'):
            abs_path = record.pathname
            record.pathname = os.path.relpath(abs_path, start=os.getcwd())
        else:
            record.pathname = lib_name
        record.lineno = record.lineno if record.pathname != lib_name else 0
        
        # Level emoji
        level_emoji = {
            "DEBUG":    "🟢",
            "INFO":     "🔵",
            "WARNING":  "🟡",
            "ERROR":    "🔴",
            "CRITICAL": "🟣"
        }
        record.levelname = f"{level_emoji[record.levelname]} {record.levelname.lower()}"
        # Calculating max length
        for field in self.max_lengths:
            newlen = len(str(getattr(record, field, ''))) 
            # + (1 if field == 'levelname' else 0)
            if self.max_lengths[field] < newlen:
                rewrite = True
                self.max_lengths[field] = max(self.max_lengths[field], newlen)
        if rewrite:
            self.rewrite_log()
        
        self._style._fmt = (
            f'%(process){self.max_lengths["process"]}d | '
            f'%(asctime){self.max_lengths["asctime"]}s | '
            f'%(levelname)-{self.max_lengths["levelname"]}s | '
            f'%(funcName)-{self.max_lengths["funcName"]}s | '
            f'%(pathname){self.max_lengths["pathname"]}s:%(lineno)-{self.max_lengths["lineno"]}d | '
            f'%(message)s'
        )
        
        return super().format(record)


def format_seconds(seconds):
    if seconds <= 0:
        return "0 seconds"
    
    units = [
        ("day", 86400),    # 24 * 60 * 60
        ("hour", 3600),    # 60 * 60
        ("minute", 60),
        ("second", 1)
    ]
    
    result = []
    remaining = float(seconds)
    
    for unit_name, unit_seconds in units[:-1]:
        if remaining >= unit_seconds:
            value = int(remaining // unit_seconds)
            remaining = remaining % unit_seconds
            result.append(f"{value} {unit_name}{'s' if value > 1 else ''}")
    
    if remaining > 0 or not result: 
        if remaining.is_integer():
            result.append(f"{int(remaining)} second{'s' if remaining != 1 else ''}")
        else:
            result.append(f"{remaining:.4f} seconds".rstrip('0').rstrip('.'))
    
    return " ".join(result)

def logab_custom_print(print_level, *args, **kwargs):
    # Combine arguments into a single message
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '')
    message = sep.join(str(arg) for arg in args) + end
    frame = traceback.extract_stack()[-2]
    filename = frame.filename
    funcname = frame.name
    lineno = frame.lineno
    # Log the message at the specified print_level
    logging.log(print_level, message, extra={
            'file_id': filename,
            'func_id': funcname,
            'line_id': lineno
        })

@contextmanager
def log_wrap(log_file='./app.log', log_level="info", print_level="info"):
    # Set up log configuration
    log_level=getattr(logging, log_level.upper(), logging.info)
    handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    formatter = ABFormatter(log_file)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    
    # Set up print configuration
    print_level=getattr(logging, print_level.upper(), logging.info)
    builtins.print = partial(logab_custom_print, print_level)
    
    # Print table header
    with open (log_file, 'w', encoding='utf-8') as file:
        newstr = """PID | Time | Level | Function | File:No | Message\n----+------+-------+----------+---------+--------"""
        file.write(newstr)
    
    start_time = time.time()
    try:
        yield
    except Exception as e:
        # Catch and write error message
        tb = traceback.format_exc()
        root_logger.error(e)
        with open(log_file, 'a', encoding='utf-8') as file:
            hor_line = formatter.draw_horizontal_line(placement='+')
            file.write(f"{hor_line}\n")
            file.write(tb)
        exit()
    finally:
        # Write execution time
        end_time = time.time()
        hor_line = formatter.draw_horizontal_line(placement='+')
        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(f"{hor_line}\n")
        root_logger.info(f"Execution time {format_seconds(end_time-start_time)}")

