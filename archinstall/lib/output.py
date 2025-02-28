import logging
import os
import sys
from enum import Enum

from pathlib import Path
from typing import Dict, Union, List, Any, Callable, Optional
from dataclasses import asdict, is_dataclass

from .storage import storage


class FormattedOutput:
	@classmethod
	def values(
		cls,
		o: Any,
		class_formatter: Optional[Union[str, Callable]] = None,
		filter_list: List[str] = []
	) -> Dict[str, Any]:
		""" the original values returned a dataclass as dict thru the call to some specific methods
		this version allows thru the parameter class_formatter to call a dynamicly selected formatting method.
		Can transmit a filter list to the class_formatter,
		"""
		if class_formatter:
			# if invoked per reference it has to be a standard function or a classmethod.
			# A method of an instance does not make sense
			if callable(class_formatter):
				return class_formatter(o, filter_list)
			# if is invoked by name we restrict it to a method of the class. No need to mess more
			elif hasattr(o, class_formatter) and callable(getattr(o, class_formatter)):
				func = getattr(o, class_formatter)
				return func(filter_list)

			raise ValueError('Unsupported formatting call')
		elif hasattr(o, 'as_json'):
			return o.as_json()
		elif hasattr(o, 'json'):
			return o.json()
		elif is_dataclass(o):
			return asdict(o)
		else:
			return o.__dict__

	@classmethod
	def as_table(
		cls,
		obj: List[Any],
		class_formatter: Optional[Union[str, Callable]] = None,
		filter_list: List[str] = [],
		capitalize: bool = False
	) -> str:
		""" variant of as_table (subtly different code) which has two additional parameters
		filter which is a list of fields which will be shon
		class_formatter a special method to format the outgoing data

		A general comment, the format selected for the output (a string where every data record is separated by newline)
		is for compatibility with a print statement
		As_table_filter can be a drop in replacement for as_table
		"""
		raw_data = [cls.values(o, class_formatter, filter_list) for o in obj]

		# determine the maximum column size
		column_width: Dict[str, int] = {}
		for o in raw_data:
			for k, v in o.items():
				if not filter_list or k in filter_list:
					column_width.setdefault(k, 0)
					column_width[k] = max([column_width[k], len(str(v)), len(k)])

		if not filter_list:
			filter_list = list(column_width.keys())

		# create the header lines
		output = ''
		key_list = []
		for key in filter_list:
			width = column_width[key]
			key = key.replace('!', '').replace('_', ' ')

			if capitalize:
				key = key.capitalize()

			key_list.append(key.ljust(width))

		output += ' | '.join(key_list) + '\n'
		output += '-' * len(output) + '\n'

		# create the data lines
		for record in raw_data:
			obj_data = []
			for key in filter_list:
				width = column_width.get(key, len(key))
				value = record.get(key, '')
				if '!' in key:
					value = '*' * width
				if isinstance(value,(int, float)) or (isinstance(value, str) and value.isnumeric()):
					obj_data.append(str(value).rjust(width))
				else:
					obj_data.append(str(value).ljust(width))
			output += ' | '.join(obj_data) + '\n'

		return output

	@classmethod
	def as_columns(cls, entries: List[str], cols: int) -> str:
		chunks = []
		output = ''

		for i in range(0, len(entries), cols):
			chunks.append(entries[i:i + cols])

		for row in chunks:
			out_fmt = '{: <30} ' * len(row)
			output += out_fmt.format(*row) + '\n'

		return output


class Journald:
	@staticmethod
	def log(message: str, level: int = logging.DEBUG) -> None:
		try:
			import systemd.journal  # type: ignore
		except ModuleNotFoundError:
			return None

		log_adapter = logging.getLogger('archinstall')
		log_fmt = logging.Formatter("[%(levelname)s]: %(message)s")
		log_ch = systemd.journal.JournalHandler()
		log_ch.setFormatter(log_fmt)
		log_adapter.addHandler(log_ch)
		log_adapter.setLevel(logging.DEBUG)

		log_adapter.log(level, message)


def check_log_permissions():
	filename = storage.get('LOG_FILE', None)

	if not filename:
		return

	log_dir = storage.get('LOG_PATH', Path('./'))
	absolute_logfile = log_dir / filename

	try:
		log_dir.mkdir(exist_ok=True, parents=True)
		with absolute_logfile.open('a') as fp:
			fp.write('')
	except PermissionError:
		# Fallback to creating the log file in the current folder
		fallback_log_file = Path('./').absolute() / filename
		absolute_logfile = fallback_log_file
		absolute_logfile.mkdir(exist_ok=True, parents=True)
		storage['LOG_PATH'] = Path('./').absolute()

		err_string = f"Not enough permission to place log file at {absolute_logfile}, creating it in {fallback_log_file} instead."
		warn(err_string)


def _supports_color() -> bool:
	"""
	Found first reference here:
		https://stackoverflow.com/questions/7445658/how-to-detect-if-the-console-does-support-ansi-escape-codes-in-python
	And re-used this:
		https://github.com/django/django/blob/master/django/core/management/color.py#L12

	Return True if the running system's terminal supports color,
	and False otherwise.
	"""
	supported_platform = sys.platform != 'win32' or 'ANSICON' in os.environ

	# isatty is not always implemented, #6223.
	is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
	return supported_platform and is_a_tty


class Font(Enum):
	bold = '1'
	italic = '3'
	underscore = '4'
	blink = '5'
	reverse = '7'
	conceal = '8'


def _stylize_output(
	text: str,
	fg: str,
	bg: Optional[str],
	reset: bool,
	font: List[Font] = [],
) -> str:
	"""
	Heavily influenced by:
		https://github.com/django/django/blob/ae8338daf34fd746771e0678081999b656177bae/django/utils/termcolors.py#L13
	Color options here:
		https://askubuntu.com/questions/528928/how-to-do-underline-bold-italic-strikethrough-color-background-and-size-i

	Adds styling to a text given a set of color arguments.
	"""
	colors = {
		'black' : '0',
		'red' : '1',
		'green' : '2',
		'yellow' : '3',
		'blue' : '4',
		'magenta' : '5',
		'cyan' : '6',
		'white' : '7',
		'teal' : '8;5;109',      # Extended 256-bit colors (not always supported)
		'orange' : '8;5;208',    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#256-colors
		'darkorange' : '8;5;202',
		'gray' : '8;5;246',
		'grey' : '8;5;246',
		'darkgray' : '8;5;240',
		'lightgray' : '8;5;256'
	}

	foreground = {key: f'3{colors[key]}' for key in colors}
	background = {key: f'4{colors[key]}' for key in colors}
	code_list = []

	if text == '' and reset:
		return '\x1b[%sm' % '0'

	code_list.append(foreground[str(fg)])

	if bg:
		code_list.append(background[str(bg)])

	for o in font:
		code_list.append(o.value)

	ansi = ';'.join(code_list)

	return f'\033[{ansi}m{text}\033[0m'


def info(
	*msgs: str,
	level: int = logging.INFO,
	fg: str = 'white',
	bg: Optional[str] = None,
	reset: bool = False,
	font: List[Font] = []
):
	log(*msgs, level=level, fg=fg, bg=bg, reset=reset, font=font)

def debug(
	*msgs: str,
	level: int = logging.DEBUG,
	fg: str = 'white',
	bg: Optional[str] = None,
	reset: bool = False,
	font: List[Font] = []
):
	log(*msgs, level=level, fg=fg, bg=bg, reset=reset, font=font)

def error(
	*msgs: str,
	level: int = logging.ERROR,
	fg: str = 'red',
	bg: Optional[str] = None,
	reset: bool = False,
	font: List[Font] = []
):
	log(*msgs, level=level, fg=fg, bg=bg, reset=reset, font=font)


def warn(
	*msgs: str,
	level: int = logging.WARN,
	fg: str = 'yellow',
	bg: Optional[str] = None,
	reset: bool = False,
	font: List[Font] = []
):
	log(*msgs, level=level, fg=fg, bg=bg, reset=reset, font=font)


def log(
	*msgs: str,
	level: int = logging.INFO,
	fg: str = 'white',
	bg: Optional[str] = None,
	reset: bool = False,
	font: List[Font] = []
):
	text = orig_string = ' '.join([str(x) for x in msgs])

	# Attempt to colorize the output if supported
	# Insert default colors and override with **kwargs
	if _supports_color():
		text = _stylize_output(text, fg, bg, reset, font)

	# If a logfile is defined in storage,
	# we use that one to output everything
	if filename := storage.get('LOG_FILE', None):
		log_dir = storage.get('LOG_PATH', Path('./'))
		absolute_logfile = log_dir / filename

		with open(absolute_logfile, 'a') as fp:
			fp.write(f"{orig_string}\n")

	Journald.log(text, level=level)

	# Finally, print the log unless we skipped it based on level.
	# We use sys.stdout.write()+flush() instead of print() to try and
	# fix issue #94
	if level != logging.DEBUG or storage.get('arguments', {}).get('verbose', False):
		sys.stdout.write(f"{text}\n")
		sys.stdout.flush()
