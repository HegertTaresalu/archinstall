from __future__ import annotations

import pathlib
from typing import List, Any, Optional, TYPE_CHECKING

from ..locale import list_timezones, list_keyboard_languages
from ..menu import MenuSelectionType, Menu, TextInput
from ..output import warn
from ..packages.packages import validate_package_list
from ..storage import storage
from ..translationhandler import Language

if TYPE_CHECKING:
	_: Any


def ask_ntp(preset: bool = True) -> bool:
	prompt = str(_('Would you like to use automatic time synchronization (NTP) with the default time servers?\n'))
	prompt += str(_('Hardware time and other post-configuration steps might be required in order for NTP to work.\nFor more information, please check the Arch wiki'))
	if preset:
		preset_val = Menu.yes()
	else:
		preset_val = Menu.no()
	choice = Menu(prompt, Menu.yes_no(), skip=False, preset_values=preset_val, default_option=Menu.yes()).run()

	return False if choice.value == Menu.no() else True


def ask_hostname(preset: str = '') -> str:
	while True:
		hostname = TextInput(
			str(_('Desired hostname for the installation: ')),
			preset
		).run().strip()

		if hostname:
			return hostname


def ask_for_a_timezone(preset: Optional[str] = None) -> Optional[str]:
	timezones = list_timezones()
	default = 'UTC'

	choice = Menu(
		_('Select a timezone'),
		list(timezones),
		preset_values=preset,
		default_option=default
	).run()

	match choice.type_:
		case MenuSelectionType.Skip: return preset
		case MenuSelectionType.Selection: return choice.single_value

	return None


def ask_for_audio_selection(desktop: bool = True, preset: Optional[str] = None) -> Optional[str]:
	no_audio = str(_('No audio server'))
	choices = ['pipewire', 'pulseaudio'] if desktop else ['pipewire', 'pulseaudio', no_audio]
	default = 'pipewire' if desktop else no_audio

	choice = Menu(_('Choose an audio server'), choices, preset_values=preset, default_option=default).run()

	match choice.type_:
		case MenuSelectionType.Skip: return preset
		case MenuSelectionType.Selection: return choice.single_value

	return None


def select_language(preset: Optional[str] = None) -> Optional[str]:
	"""
	Asks the user to select a language
	Usually this is combined with :ref:`archinstall.list_keyboard_languages`.

	:return: The language/dictionary key of the selected language
	:rtype: str
	"""
	kb_lang = list_keyboard_languages()
	# sort alphabetically and then by length
	sorted_kb_lang = sorted(sorted(list(kb_lang)), key=len)

	choice = Menu(
		_('Select keyboard layout'),
		sorted_kb_lang,
		preset_values=preset,
		sort=False
	).run()

	match choice.type_:
		case MenuSelectionType.Skip: return preset
		case MenuSelectionType.Selection: return choice.single_value

	return None


def select_archinstall_language(languages: List[Language], preset: Language) -> Language:
	# these are the displayed language names which can either be
	# the english name of a language or, if present, the
	# name of the language in its own language
	options = {lang.display_name: lang for lang in languages}

	title = 'NOTE: If a language can not displayed properly, a proper font must be set manually in the console.\n'
	title += 'All available fonts can be found in "/usr/share/kbd/consolefonts"\n'
	title += 'e.g. setfont LatGrkCyr-8x16 (to display latin/greek/cyrillic characters)\n'

	choice = Menu(
		title,
		list(options.keys()),
		default_option=preset.display_name,
		preview_size=0.5
	).run()

	match choice.type_:
		case MenuSelectionType.Skip: return preset
		case MenuSelectionType.Selection: return options[choice.single_value]

	raise ValueError('Language selection not handled')


def ask_additional_packages_to_install(preset: List[str] = []) -> List[str]:
	# Additional packages (with some light weight error handling for invalid package names)
	print(_('Only packages such as base, base-devel, linux, linux-firmware, efibootmgr and optional profile packages are installed.'))
	print(_('If you desire a web browser, such as firefox or chromium, you may specify it in the following prompt.'))

	def read_packages(p: List = []) -> list:
		display = ' '.join(p)
		input_packages = TextInput(_('Write additional packages to install (space separated, leave blank to skip): '), display).run().strip()
		return input_packages.split() if input_packages else []

	preset = preset if preset else []
	packages = read_packages(preset)

	if not storage['arguments']['offline'] and not storage['arguments']['no_pkg_lookups']:
		while True:
			if len(packages):
				# Verify packages that were given
				print(_("Verifying that additional packages exist (this might take a few seconds)"))
				valid, invalid = validate_package_list(packages)

				if invalid:
					warn(f"Some packages could not be found in the repository: {invalid}")
					packages = read_packages(valid)
					continue
			break

	return packages


def add_number_of_parrallel_downloads(input_number :Optional[int] = None) -> Optional[int]:
	max_downloads = 5
	print(_(f"This option enables the number of parallel downloads that can occur during installation"))
	print(_(f"Enter the number of parallel downloads to be enabled.\n (Enter a value between 1 to {max_downloads})\nNote:"))
	print(_(f" - Maximum value   : {max_downloads} ( Allows {max_downloads} parallel downloads, allows {max_downloads+1} downloads at a time )"))
	print(_(f" - Minimum value   : 1 ( Allows 1 parallel download, allows 2 downloads at a time )"))
	print(_(f" - Disable/Default : 0 ( Disables parallel downloading, allows only 1 download at a time )"))

	while True:
		try:
			input_number = int(TextInput(_("[Default value: 0] > ")).run().strip() or 0)
			if input_number <= 0:
				input_number = 0
			elif input_number > max_downloads:
				input_number = max_downloads
			break
		except:
			print(_(f"Invalid input! Try again with a valid input [1 to {max_downloads}, or 0 to disable]"))

	pacman_conf_path = pathlib.Path("/etc/pacman.conf")
	with pacman_conf_path.open() as f:
		pacman_conf = f.read().split("\n")

	with pacman_conf_path.open("w") as fwrite:
		for line in pacman_conf:
			if "ParallelDownloads" in line:
				fwrite.write(f"ParallelDownloads = {input_number+1}\n") if not input_number == 0 else fwrite.write("#ParallelDownloads = 0\n")
			else:
				fwrite.write(f"{line}\n")

	return input_number


def select_additional_repositories(preset: List[str]) -> List[str]:
	"""
	Allows the user to select additional repositories (multilib, and testing) if desired.

	:return: The string as a selected repository
	:rtype: string
	"""

	repositories = ["multilib", "testing"]

	choice = Menu(
		_('Choose which optional additional repositories to enable'),
		repositories,
		sort=False,
		multi=True,
		preset_values=preset,
		allow_reset=True
	).run()

	match choice.type_:
		case MenuSelectionType.Skip: return preset
		case MenuSelectionType.Reset: return []
		case MenuSelectionType.Selection: return choice.single_value

	return []
