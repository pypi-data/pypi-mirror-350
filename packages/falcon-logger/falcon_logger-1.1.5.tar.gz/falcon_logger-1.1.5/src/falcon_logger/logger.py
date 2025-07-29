import atexit
import copy
import json
import queue
import sys
import threading
import time
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta


# --------------------
## holds logging functions that replace common python logger functions
class FalconLogger:  # pylint: disable=too-many-public-methods
    ## logging format with elapsed time and prefixes
    log_format_elapsed = 1
    ## logging format with prefixes only
    log_format_prefix = 2
    ## logging format with no prefixes or elapsed time
    log_format_none = 3

    # --------------------
    ## constructor
    #
    # @param path         None for stdout, or full path to the logger file
    # @param max_entries  (optional) maximum number of entries before a flush is done; default 10
    # @param loop_delay   (optional) time between checking queue; default 0.250 seconds
    # @param mode         (optional) logging mode: default is None
    #                      None or "normal": log all lines as set by configuration, format, etc.
    #                      "ut" or "mock": for UT purposes, saves lines in ut_lines array
    #                      "null": do no logging; see verbosity for an alternative
    def __init__(self, path=None, max_entries=10, loop_delay=0.250, mode=None):
        ## the full path to the log file (if any)
        self._path = path
        ## file pointer to destination file or stdout
        self._fp = None
        ## holds the logging mode (None, normal, ut, etc.
        self._logging_mode = mode
        ## holds the function that handles the logging of the current mode and format
        self._log_it = None

        # === log formatting related

        ## verbosity; if True print all lines, if not print only errors, excp ad bug lines
        self._verbose = True
        ## the log display format to use; default: elapsed time + prefixes
        self._log_format = self.log_format_elapsed
        ## holds the last time a full DTS was written to the log;
        # printed at the beginning and once per hour
        self._start_time = 0.0
        ## current number of dots printed
        self._dots = 0
        ## max number of dots to display
        self._max_dots = 25

        # === runner() related

        ## configuration values used by runner()
        self._runner_cfg = None
        ## backup of runner_cfg
        self._backup_cfg = None
        ## the bg thread used to run
        self._thread = None
        ## the queue used
        self._queue = None
        ## flag to the thread to end the loop
        self._finished = False

        # === UT related

        ## holds lines during UTs; must be a public attribute
        self.ut_lines = []

        # === log_mode related
        self._init_cfg(max_entries, loop_delay)
        if mode is None or mode == 'normal':
            self._logging_mode = 'normal'
            self._log_it = self._log_it_normal

            # initialize destination file pointer
            if self._path is None:
                self._fp = sys.stdout
            else:
                self._fp = open(self._path, 'w', encoding='UTF-8')  # pylint: disable=consider-using-with

            self._init_thread()
        elif mode in ['ut', 'mock']:
            self._set_log_it_fn()
        elif mode == 'null':
            self._log_it = self._log_it_null
        else:
            raise Exception(f'Unknown mode: "{mode}", '  # pylint: disable=broad-exception-raised
                            'choose "normal", "ut", "mock" or "null"')

        # try ensure at least one save() and thread cleanup is done
        ## term(), see below
        atexit.register(self.term)

    # --------------------
    ## initialize the configuration variables for the loop
    #
    # @param max_entries   the max number of entries in the queue
    # @param loop_delay    how long to wait between checks of the queue
    # @return None
    def _init_cfg(self, max_entries, loop_delay):
        @dataclass
        class RunnerCfg:
            ## the maximum entries to hold in the queue before saving to the file
            max_entries: int
            ## the maximum number of loops before the queue is emptied
            max_count: int
            ## the delay between checking the queue for entries to save
            loop_delay: float

        self._runner_cfg = RunnerCfg(0, 0, 0.0)
        self.set_max_entries(max_entries)
        self.set_loop_delay(loop_delay)
        self._backup_cfg = copy.deepcopy(self._runner_cfg)

    # --------------------
    ## initialize and start the thread
    #
    # @return None
    def _init_thread(self):
        self._queue = queue.Queue()
        self._finished = False

        self._thread = threading.Thread(target=self._runner)
        self._thread.daemon = True
        self._thread.start()

        # wait for thread to start
        time.sleep(0.1)

    # --------------------
    ## backwards compatibility; clears ut_lines
    #
    # @return None
    def ut_clear(self):
        self.ut_lines = []

    # --------------------
    ## for UT only; set the start_time to the given value
    #
    # @param new_time  the time to set start_time to
    # @return None
    def ut_start_time(self, new_time):
        self._start_time = new_time

    ## set verbosity
    #
    # @param value  (bool) verbosity level
    # @return None
    def set_verbose(self, value):
        self._verbose = value

    # --------------------
    ## set log line format.
    #
    # @param form  (str) either "elapsed" or "prefix" or throws excp
    # @return None
    def set_format(self, form):
        if form == 'elapsed':
            self._log_format = self.log_format_elapsed
        elif form == 'prefix':
            self._log_format = self.log_format_prefix
        elif form == 'none':
            self._log_format = self.log_format_none
        else:
            raise Exception(f'Unknown format: "{form}", '  # pylint: disable=broad-exception-raised
                            'choose "elapsed", "prefix" or "none"')

        if self._logging_mode in ['ut', 'mock']:
            self._set_log_it_fn()

    # --------------------
    ## set the log_it function to call based on the current logging format
    #
    # @return None
    def _set_log_it_fn(self):
        if self._log_format == self.log_format_elapsed:
            self._log_it = self._log_it_ut_elapsed
        elif self._log_format == self.log_format_prefix:
            self._log_it = self._log_it_ut_prefix
        elif self._log_format == self.log_format_none:
            self._log_it = self._log_it_ut_none
        else:  # pragma: no cover
            print(f'BUG in _set_log_it_fn: unhandled log format {self._log_format}')

    # --------------------
    ## set max entries to allow in the queue before printing them
    #
    # @param value  (int) number of entries; default: 10
    # @return None
    def set_max_entries(self, value):
        self._runner_cfg.max_entries = value
        if self._runner_cfg.max_entries <= 0:
            raise Exception('max_entries must be greater than 0')  # pylint: disable=broad-exception-raised

    # --------------------
    ## set loop delay to check the queue
    #
    # @param loop_delay (float) number of seconds; default: 0.250
    # @return None
    def set_loop_delay(self, loop_delay):
        self._runner_cfg.loop_delay = loop_delay
        if self._runner_cfg.loop_delay < 0.001:
            raise Exception('loop_delay must be >= 0.001 seconds')  # pylint: disable=broad-exception-raised

        # print every loop_delay seconds even if less than max_entries are in the queue
        self._runner_cfg.max_count = int(round(1 / self._runner_cfg.loop_delay, 1))

    # --------------------
    ## set how many dots to print on one line before printing a newline
    #
    # @param value  (int) number of dots
    # @return None
    def set_max_dots(self, value):
        self._max_dots = value
        if self._max_dots <= 0:
            raise Exception('max_dots must be greater than 0')  # pylint: disable=broad-exception-raised

    # === cleanup functions

    # --------------------
    ## terminate
    # stop the thread, save any remaining line in the internal queue
    #
    # @return None
    def term(self):
        try:
            # since this will be called during atexit() handling,
            # stdout and/or file can be closed. Protect against this case.
            self._save()
        except Exception:  # pylint: disable=broad-exception-caught
            pass
        self._finished = True
        if self._thread is not None and self._thread.is_alive():  # pragma: no cover
            # coverage: always taken in tests
            self._thread.join(5)

    # --------------------
    ## do a save at this point
    #
    # @return None
    def save(self):
        self._save()

    # === log modes

    # --------------------
    ## since it's normal mode, put the logging info on the queue.
    #
    # @param info  the line info
    # @return None
    def _log_it_normal(self, info):
        self._queue.put(info)

    # --------------------
    ## since it's ut mode and no prefixes, add the line to ut_lines
    #
    # @param info  the line info
    # @return None
    def _log_it_ut_none(self, info):
        if not info[0] and not info[1]:  # !always_print and !verbose
            return

        if info[3] is None and info[4] == (None,):
            line = 'DTS'
        elif info[3] == '.' and info[4] == (None,):
            line = '.'
        else:
            line = ' '.join(map(str, info[4]))
        self.ut_lines.append(line)

    # --------------------
    ## since it's ut mode and prefix mode add the line with prefix to ut_lines
    #
    # @param info  the line info
    # @return None
    def _log_it_ut_prefix(self, info):
        if not info[0] and not info[1]:  # !always_print and !verbose
            return

        prefix = info[3]
        if prefix is None and info[4] == (None,):
            line = 'DTS'
            self.ut_lines.append(f'{" ": <4} {line}')
        elif info[3] == '.' and info[4] == (None,):
            self.ut_lines.append('.')
        elif prefix is None:
            line = ' '.join(map(str, info[4]))
            self.ut_lines.append(line)
        else:
            line = ' '.join(map(str, info[4]))
            self.ut_lines.append(f'{prefix: <4} {line}')

    # --------------------
    ## since it's ut mode and elapsed mode add the line with elapsed and prefix to ut_lines
    #
    # @param info  the line info
    # @return None
    def _log_it_ut_elapsed(self, info):
        if not info[0] and not info[1]:  # !always_print and !verbose
            return

        dts = info[2]
        elapsed = dts - self._start_time
        if elapsed >= 3600.0:
            self._start_time = dts
            elapsed = 0
        t_str = self._get_elapsed_str(elapsed)

        prefix = info[3]
        if prefix is None and info[4] == (None,):
            line = 'DTS'
            self.ut_lines.append(f'{" ": <4} {line}')
        elif info[3] == '.' and info[4] == (None,):
            self.ut_lines.append('.')
        elif prefix is None:  # raw line
            line = ' '.join(map(str, info[4]))
            self.ut_lines.append(f'{line}')
        else:
            line = ' '.join(map(str, info[4]))
            self.ut_lines.append(f'{t_str} {prefix: <4} {line}')

    # --------------------
    ## since it's null mode, ignore the line
    #
    # @param info  (ignored)
    # @return None
    def _log_it_null(self, info):
        # logging ignored
        pass

    # === log lines with prefixes and elapsed times

    # --------------------
    ## add an item to write the full date-time-stamp to the log
    #
    # @return None
    def full_dts(self):
        # the None args/line causes the full dts to display
        self._log_it((False, self._verbose, time.time(), None, (None,)))

    # --------------------
    ## indicate some activity is starting
    #
    # @param args  the message to log
    # @return None
    def start(self, *args):
        self._log_it((False, self._verbose, time.time(), '====', args))

    # --------------------
    ## write line with no prefix
    #
    # @param args  the message to log
    # @return None
    def line(self, *args):
        self._log_it((False, self._verbose, time.time(), '', args))

    # --------------------
    ## write a highlight line
    #
    # @param args  the message to log
    # @return None
    def highlight(self, *args):
        self._log_it((False, self._verbose, time.time(), '--->', args))

    # --------------------
    ## write an ok line
    #
    # @param args  the message to log
    # @return None
    def ok(self, *args):
        self._log_it((False, self._verbose, time.time(), 'OK', args))

    # --------------------
    ## write an error line
    #
    # @param args  the message to log
    # @return None
    def err(self, *args):
        self._log_it((True, self._verbose, time.time(), 'ERR', args))

    # --------------------
    ## write an warn line
    #
    # @param args  the message to log
    # @return None
    def warn(self, *args):
        self._log_it((False, self._verbose, time.time(), 'WARN', args))

    # --------------------
    ## write a debug line
    #
    # @param args  the message to log
    # @return None
    def bug(self, *args):
        self._log_it((True, self._verbose, time.time(), 'BUG', args))

    # --------------------
    ## write a debug line
    #
    # @param args  the message to log
    # @return None
    def dbg(self, *args):
        self._log_it((False, self._verbose, time.time(), 'DBG', args))

    # --------------------
    ## write a raw line (no prefix)
    #
    # @param args  the message to log
    # @return None
    def raw(self, *args):
        self._log_it((False, self._verbose, time.time(), None, args))

    # -------------------
    ## write an output line with the given message
    #
    # @param lineno  (optional) the current line number for each line printed
    # @param args    the message to write
    # @return None
    def output(self, lineno, *args):
        prefix = ' --'
        if lineno is None:
            new_args = ('    ',) + args
        else:
            new_args = (f'{lineno: >3}]',) + args

        self._log_it((False, self._verbose, time.time(), prefix, new_args))

    # -------------------
    ## write a list of lines using output()
    #
    # @param lines   the lines to write
    # @return None
    def num_output(self, lines):
        lineno = 0
        for line in lines:
            lineno += 1
            self.output(lineno, line)

    # --------------------
    ## if ok is True, write an OK line, otherwise an ERR line.
    #
    # @param ok   condition indicating ok or err
    # @param args  the message to log
    # @return None
    def check(self, ok, *args):
        if ok:
            self.ok(*args)
        else:
            self.err(*args)

    # --------------------
    ## log a series of messages. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param title   the line indicating what the check is about
    # @param lines   individual list of lines to print
    # @return None
    def check_all(self, ok, title, lines):
        self.check(ok, f'{title}: {ok}')
        for line in lines:
            self.check(ok, f'   - {line}')

    # -------------------
    ## add an item to write a 'line' message and a json object to the log
    #
    # @param j       the json object to write
    # @param args    the message to write
    # @return None
    def json(self, j, *args):
        now = time.time()
        self._log_it((False, self._verbose, now, ' ', args))

        if isinstance(j, str):
            j = json.loads(j)

        for line in json.dumps(j, indent=2).splitlines():
            self._log_it((False, self._verbose, now, ' >', (line,)))

    # -------------------
    ## add an item to write a 'line' message and a data buffer to the log in hex
    #
    # @param data    the data buffer to write; can be a string or a bytes array
    # @param args    the message to write
    # @return None
    def hex(self, data, *args):
        now = time.time()
        self._log_it((False, self._verbose, now, ' ', args))
        i = 0
        line = f'{i:>3} 0x{i:02X}:'
        if isinstance(data, str):
            data = bytes(data, 'utf-8')

        col = 0
        for i, ch in enumerate(data):
            if col >= 16:
                self._log_it((False, self._verbose, now, '', (' ', line)))
                col = 0
                line = f'{i:>3} 0x{i:02X}:'

            line += f' {ch:02X}'
            col += 1
            if col == 8:
                line += '  '
            # else:
            #     line += ' '

        # print if there's something left over
        self._log_it((False, self._verbose, now, ' ', (' ', line)))

    # --------------------
    ## write a dot to stdout
    #
    # @return None
    def dot(self):
        self._log_it((False, self._verbose, time.time(), '.', (None,)))

    # === (some) compatibility with python logger

    # --------------------
    ## log a debug line
    #
    # @param args the line to print; default empty
    # @return None
    def debug(self, *args):
        self._log_it((False, self._verbose, time.time(), 'DBG', args))

    # --------------------
    ## log an info line
    #
    # @param args the line to print; default empty
    # @return None
    def info(self, *args):
        self._log_it((False, self._verbose, time.time(), '', args))

    # --------------------
    ## log a warning line
    #
    # @param args the line to print; default empty
    # @return None
    def warning(self, *args):
        self._log_it((False, self._verbose, time.time(), 'WARN', args))

    # --------------------
    ## log an error line
    #
    # @param args the line to print; default empty
    # @return None
    def error(self, *args):
        self._log_it((True, self._verbose, time.time(), 'ERR', args))

    # --------------------
    ## log a critical line
    #
    # @param args the line to print; default empty
    # @return None
    def critical(self, *args):
        self._log_it((True, self._verbose, time.time(), 'CRIT', args))

    # --------------------
    ## log an exception
    #
    # @param excp       the exception to print
    # @param max_lines  (optional) max lines to print
    # @return None
    def exception(self, excp, max_lines=None):
        now = time.time()
        self._log_it((True, self._verbose, now, 'EXCP', (str(excp),)))
        lineno = 1
        done = False
        for line in traceback.format_exception(excp):
            for line2 in line.splitlines():
                if max_lines is not None and lineno >= max_lines:
                    done = True
                    break

                self._log_it((True, self._verbose, now, 'EXCP', (line2,)))
                lineno += 1
            if done:
                break

    # === logging functions

    # --------------------
    ## save any entries in the queue to the file
    #
    # @return None
    def _save(self):  # pylint: disable=too-many-branches, too-many-statements
        # if stdout or file is none/closed then nothing to do
        if self._fp is None:  # pragma: no cover
            # coverage: can not be replicated
            # probably redundant to finish but do it anyway
            self._finished = True
            return

        count = self._queue.qsize()
        while count > 0:
            # in some closing/race conditions, the file may be closed in the middle of a loop
            # note this can be applied to stdout as well.
            if self._fp.closed:
                break

            (always_print, verbose, dts, prefix, args) = self._queue.get_nowait()
            count -= 1

            if not verbose and not always_print:
                # not verbose and ok not to print
                continue

            # uncomment to debug
            # print(f'{always_print} {verbose} "{prefix}"  {dts}  "{line}"')

            if args[0] is None and prefix == '.':
                # dots just log a wait, so okay to call fn
                self._handle_dots()
                continue

            # at this point, not a dot

            # last call was a dot, so reset and print a newline ready for the new log line
            if self._dots != 0:
                self._dots = 0
                self._fp.write('\n')
                self._runner_cfg = copy.deepcopy(self._backup_cfg)

            # print the full DTS requested by the user
            if args[0] is None and prefix is None:
                # rare request, so okay to call fn
                self._handle_full_dts(dts)
                continue

            # print with the prefix, but no elapsed time
            if self._log_format == self.log_format_none:
                line = ' '.join(map(str, args))
                self._fp.write(line)
                self._fp.write('\n')
                continue

            # print with the prefix, but no elapsed time
            if self._log_format == self.log_format_prefix:
                line = ' '.join(map(str, args))
                if prefix is None:
                    msg = line
                else:
                    msg = f'{prefix:<4} {line}'
                self._fp.write(msg)
                self._fp.write('\n')
                continue

            # at this point, mode is self.LOG_MODE_ELAPSED

            # print prefix and elapsed time
            line = ' '.join(map(str, args))
            elapsed = dts - self._start_time

            # approximately once an hour, restart the time period
            if elapsed >= 3600.0:
                # rare, so okay to call fn
                # display the time at the moment the log line was saved
                self._handle_full_dts(dts)

                # recalc the elapsed time, should be 0
                elapsed = dts - self._start_time

            # log the line
            if prefix is None:
                msg = line
            else:
                t_str = self._get_elapsed_str(elapsed)
                msg = f'{t_str} {prefix:<4} {line}'

            self._fp.write(msg)
            self._fp.write('\n')

        # flush lines to stdout/file; protect with except in case
        try:
            if not self._fp.closed:
                self._fp.flush()
        except BrokenPipeError:  # pragma: no cover
            # coverage: rare case: if stdout/file is closed this will throw an exception
            pass

    # --------------------
    ## If past max_dots, print a newline. Then print a dot.
    #
    # @return none
    def _handle_dots(self):
        if self._dots == 0:
            # save delay and count
            self._backup_cfg = copy.deepcopy(self._runner_cfg)
            self._runner_cfg.loop_delay = 0.100
            self._runner_cfg.max_entries = 1
            self._runner_cfg.max_count = 1

        if self._dots >= self._max_dots:
            self._fp.write('\n')
            self._dots = 0

        self._fp.write('.')
        self._dots += 1

    # --------------------
    ## print full DTS stamp
    #
    # @param dts   the dts of the current log line
    # @return None
    def _handle_full_dts(self, dts):
        # restart the timer; user wants the full DTS and elapsed is since that absolute time
        self._start_time = dts

        t_str = datetime.fromtimestamp(self._start_time).strftime('%H:%M:%S.%f')[:12]
        dts_str = time.strftime("%Y/%m/%d", time.localtime(self._start_time))
        full_dts = f'{"DTS": <4} {dts_str} {t_str}'
        if self._log_format == self.log_format_elapsed:
            full_dts = f'{"": <6} {full_dts}'
        self._fp.write(full_dts)
        self._fp.write('\n')

    # --------------------
    ## generate the string of the given elapsed time
    #
    # @param elapsed   the elapsed time to format
    # @return the string ("MM.SS.nnn")
    def _get_elapsed_str(self, elapsed):
        t_str = timedelta(seconds=elapsed)
        # rare case: str(timedelta) makes the ".000000" optional if the number of microseconds is 0
        if t_str.microseconds == 0:  # pragma: no cover
            # bump the number of microseconds by 1 to make sure the full string is formatted
            t_str = timedelta(seconds=elapsed + 0.000001)
        return str(t_str)[2:11]

    # --------------------
    ## the thread runner
    # wakes periodically to check if the queue has max_entries or more in it
    # if so, the lines are written to the file
    # if not, it sleeps
    #
    # @return None
    def _runner(self):
        # wrap with try/except for catching ctrl-c
        # usually fails in sleep() so may not call finally clause
        try:
            count = 0
            while not self._finished:
                # sleep until:
                #  - there are enough entries in the queue
                #  - the max delay is reached
                if self._queue.qsize() < self._runner_cfg.max_entries and count < self._runner_cfg.max_count:
                    count += 1
                    time.sleep(self._runner_cfg.loop_delay)
                    continue

                # write out all the current entries
                count = 0
                self._save()
        finally:
            # save any remaining entries
            self._save()

            # close the file if necessary
            if self._path and self._fp is not None:  # pragma: no cover
                # coverage: can't be replicated in UTs
                self._fp.close()
                self._fp = None
