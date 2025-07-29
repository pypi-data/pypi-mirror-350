from simple_term_menu import TerminalMenu
from termcolor import colored
from typing import Union, List, Tuple
import argparse
import base64
import getpass
import hashlib
import os
import platform
import re
import requests
import subprocess
import sys
import traceback
import urllib.parse
from packaging.version import Version

#-------------------------------------------------------------------------------
s_version = "0.7.4"
s_license_version = "1.1"
s_prefix = "nec"
s_urls = [
	'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/core/',
	'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/license/',
	'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/x86/',
	'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/ve/',
	'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/nvidia/',
	'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/dev/',
	'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/adv-dev/',
]
s_available_frameworks	= ['tensorflow', 'numpy', 'onnx', 'torch']
s_available_features	= ['adv-sdk', 'deployment', 'docs', 'sdk', 'tests']
s_available_devices		= ['x86', 've', 'nvidia']

#-------------------------------------------------------------------------------
emph	= lambda x: colored(x,				attrs=['bold'])
red		= lambda x: colored(x, 'red', 		attrs=['bold'])
green	= lambda x: colored(x, 'green',		attrs=['bold'])
yellow	= lambda x: colored(x, 'yellow',	attrs=['bold'])

s_installed			= None
s_dependencies		= None
s_python_packages	= None

#-------------------------------------------------------------------------------
def fingerprint():
	files = [
		'/sys/devices/virtual/dmi/id/board_version',
		'/sys/devices/virtual/dmi/id/board_vendor',
		'/sys/devices/virtual/dmi/id/board_name',
		'/sys/devices/virtual/dmi/id/product_version',
		'/sys/devices/virtual/dmi/id/product_name',
		'/sys/devices/virtual/dmi/id/sys_vendor'
	]

	x = hashlib.sha256()
	def update(y):
		y = y.strip()
		x.update(y.encode('utf-8'))

	for file in files:
		try:
			with open(file, 'r') as f:
				update(f.read())
		except Exception as e:
			raise e

	with open('/proc/cpuinfo', 'r') as f:
		for line in f:
			if line.startswith('model name'):
				update(line
					.split(':',1)[-1]	# split 'model name:', '...'
					.split('@',1)[0]	# remove trailing 'Intel ... @ 123GHz'
					.strip()
				)
				break

	p = subprocess.run(['lsblk', '-dno', 'serial'], capture_output=True, text=True)
	for line in p.stdout.strip().split("\n"):
		update(line)

	p = subprocess.run(['lshw', '-class', 'network'], capture_output=True, text=True)
	for line in p.stdout.split("\n"):
		if(
			'vendor' in line or
			'serial' in line or
			'product' in line
		):
			update(line.split(':', 1)[-1])

	return base64.b64encode(x.digest()).decode()

#-------------------------------------------------------------------------------
# taken from: https://stackoverflow.com/questions/1871549/determine-if-python-is-running-inside-virtualenv
def is_virtualenv():
	return (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

#-------------------------------------------------------------------------------
def run(cmd):
	ret = subprocess.run(cmd)
	if ret.returncode != 0:
		raise Exception("PIP error detected")

#-------------------------------------------------------------------------------
def run_output(cmd: Union[List[str], Tuple[str]]) -> str:
	ret = subprocess.run(cmd, stdout=subprocess.PIPE)
	if ret.returncode != 0:
		raise Exception("PIP error detected")
	return ret.stdout.decode('utf-8')

#-------------------------------------------------------------------------------
def initialize():
	global s_python_packages, s_installed, s_dependencies

	# Init Available Modules ---------------------------------------------------
	output				= run_output([sys.executable, '-m', 'pip', 'list', 'installed'])
	s_python_packages	= output.split('\n')[2:]
	s_installed			= dict()
	prog				= re.compile(r'^({}-sol[a-z0-9-_]+)\s+([0-9\.a-z]+)'.format(s_prefix))
	for x in s_python_packages:
		match = prog.match(x)
		if match:
			s_installed[match[1]] = match[2]

	# Init Dependencies --------------------------------------------------------
	s_dependencies = dict()

	# Init Available Hardware --------------------------------------------------
	if args.devices == ['all']:
		def add_device(name, func):
			global s_dependencies
			s_dependencies[name] = None
	else:
		def add_device(name, func):
			global s_dependencies
			try:
				if func() if len(args.devices) == 0 else args.devices.index(name) >= 0:
					s_dependencies[name] = None
			except ValueError:
				pass

	add_device('x86',		lambda: platform.machine() == 'x86_64')
	add_device('ve',		lambda: os.path.exists('/sys/class/ve'))
	add_device('nvidia',	lambda: os.path.exists('/proc/driver/nvidia/version'))

	dev_cnt = len(s_dependencies)
	if dev_cnt == 0:
		raise Exception('No devices detected or selected via --devices!')
	 
	# Init Features ------------------------------------------------------------
	if args.features == ['all']:
		for k in s_available_features:
			s_dependencies[k] = s_version
	else:
		for f in args.features:
			if f in s_available_features:	s_dependencies[f] = s_version
			else:							raise Exception(f'Unknown feature: {f}')

	# Init Available Frameworks ------------------------------------------------
	if len(args.frameworks) == 0: # auto
		args.frameworks = s_available_frameworks
	else:
		if args.frameworks == ['all']:
			args.frameworks = s_available_frameworks

		regex = re.compile(r'([a-zA-Z0-9\-]+)\s*(==|<=|>=|~=)?\s*([0-9\.]+(\.post[0-9]+)?)?')

		for d in args.frameworks:
			match = regex.search(d)

			if match is None:
				raise Exception(f'Unsupported framework: {d}')

			name, operator, version = match[1], match[2], match[3]

			if name not in s_available_frameworks:
				raise Exception(f'Unsupported framework: {d}')

			s_dependencies[name] = None if operator is None and version is None else f'{operator}{version}'

	# Determine Framework versions
	for x in s_python_packages:
		x = x.split(' ')
		name, v = x[0], x[-1]
		if name in args.frameworks:
			v = v.split('+',     1)[0]	# #1564
			v = v.split('.post', 1)[0]	# #1564
			v = f'~={v}.0'				# padding to enforce >=1.2.3.0, <1.2.3, which only allows .post!
			s_dependencies[name] = v

	# Framework compatibility --------------------------------------------------
	def check_version(framework, min_version, max_version):
		if framework in s_dependencies:
			version = s_dependencies[framework]
			if version is None:
				if min_version is not None:
					version = f'>={min_version}'
					if max_version is not None:
						version += f',<{max_version}'
				elif max_version is not None:
					version = '<{max_version}'
				s_dependencies[framework] = version
			else:
				ver = re.search(r'[0-9\.]*[0-9]', version)
				assert ver, f'Invalid version string {version}'
				version = ver[0]
				assert version[-1] != '.'
				if min_version is not None and Version(version) <  Version(min_version):
					raise Exception(f'SOL is incompatible to {framework} < {min_version}. Please install a newer version!')
				if max_version is not None and Version(version) >= Version(max_version):
					raise Exception(f'SOL is incompatible to {framework} >= {max_version}. Please install a older version!')

	check_version('tensorflow', '2.5.0', '2.16.0')	# TensorFlow >= 2.5.0 and < 2.16.0 #1392

	# --------------------------------------------------------------------------
	if args.mode != 'debug' and (len(s_dependencies) - dev_cnt) == 0:
		raise Exception('No frameworks detected or selected via --frameworks!')

#-------------------------------------------------------------------------------
# Callbacks
#-------------------------------------------------------------------------------
def install(args, plugins = None):
	# Run PIP installation -----------------------------------------------------
	is_install	= args.mode != 'download'
	is_local	= args.folder is not None

	credentials, user_access = None, None
	if not is_local:
		credentials, user_access = check_license(args)

	def pip_install(plugins, is_sol):
		cmd = [sys.executable, '-m', 'pip', 'install' if is_install else 'wheel']

		if is_install and not is_virtualenv() and args.user:
			cmd.append('--user')

		cmd += plugins

		if is_local:
			if args.no_index:
				cmd.append('--no-index')
			cmd.append('-f')
			cmd.append(args.folder)
		elif is_sol:
			assert isinstance(credentials, tuple) and len(credentials) == 2

			if args.trust:
				cmd.append('--trusted-host')
				cmd.append('sol.neclab.eu')

			# https://pip.pypa.io/en/stable/topics/authentication/#percent-encoding-special-characters
			username = credentials[0]
			password = urllib.parse.quote(credentials[1].encode('utf8'))

			def urls():
				for url in user_access:
					if 'license' in url:
						yield f'{url}index.php/pip-license-index'
					elif any(dev in url for dev in ['core', 'x86', 've', 'nvidia']):
						yield f'{url}v{s_version}'
						yield f'{url}dist'
					elif 'dev' in url:
						yield f'{url}v{s_version}'
					else:
						yield url

			for u in urls():
				cmd.append('-f')
				cmd.append(u.replace('{USERNAME}', username).replace('{PASSWORD}', password))
		run(cmd)
	
	# Get list of plugins to be installed --------------------------------------
	if plugins is None:
		# uninstall all previous packages --------------------------------------
		if is_install and len(s_installed) > 0:
			uninstall(args)

		# #1565 ----------------------------------------------------------------
		for framework in s_available_frameworks:
			if framework in s_dependencies:
				pip_install([f'{framework}{s_dependencies.get(framework, None) or ""}'], False)
		initialize() # reinitialize, e.g., we might have installed a torch version already
		# /#1565 ---------------------------------------------------------------
		plugins = available_plugins(args, user_access)

	pip_install(plugins, True)

#-------------------------------------------------------------------------------
def uninstall(args):
	if len(s_installed) == 0:
		print('SOL is not installed on this machine')
	else:
		run([sys.executable, '-m', 'pip', 'uninstall', '-y'] + list(s_installed.keys()))
		print('SOL has been uninstalled from this machine')
	print()

#-------------------------------------------------------------------------------
def check_access(args):
	credentials = None

	def check_login():
		return requests.get('https://sol.neclab.eu/license/', auth=credentials, verify=not args.trust).status_code == 200

	# Fetch License Agreement for this user ------------------------------------
	if args.username is None or args.password is None: # interactive
		while credentials is None:
			print('Please authenticate using your SOL login for verifying your license status:')
			if args.username is None:
				print('User for sol.neclab.eu: ', end='')
				username = input()
			else:
				username = args.username

			password = args.password or getpass.getpass()
			credentials = (username, password)
			print()

			if not check_login():
				print(red('Login failed!'))
				credentials = None
	else: # non-interactive
		credentials = (args.username, args.password)

		if not check_login():
			raise Exception('Login failed!')

	user_access	= set()
	cache		= dict()

	def add_access(url: str) -> bool:
		code = cache.get(url, None)
		if isinstance(code, int):
			return code == 200

		auth = None
		if '{USERNAME}:{PASSWORD}@' in url:
			url		= url.replace('{USERNAME}:{PASSWORD}@', '')
			auth	= credentials

		r			= requests.get(url, auth=auth, verify=not args.trust)
		cache[url]	= r.status_code
		return r.status_code == 200

	for url in s_urls:
		if add_access(url):
			user_access.add(url)

	return credentials, user_access, cache

#-------------------------------------------------------------------------------
def fetch_license(credentials, args):
	r = requests.get('https://sol.neclab.eu/license/index.php/fetch-license', auth=credentials, verify=not args.trust)
	try:					r.raise_for_status()
	except Exception as e:	return e

	try:					return r.json()
	except Exception:		return Exception(r.content.decode('utf-8'))

#-------------------------------------------------------------------------------
def check_license(args):
	# Helper Functions ---------------------------------------------------------		
	def less(text, step = 40):
		assert isinstance(text, list)
		cnt = len(text)
		for i in range(0, (cnt + step - 1) // step):
			start	= i * step
			end		= min(cnt, start + step)
			for n in range(start, end):
				print(text[n])

			if end < cnt:
				print('')
				input('Press <Enter> for more')
		print('')

	def convert(markdown):
		out	= []
		for l in markdown.split('\n'):
			l = l.replace('<br/>', ' ')
			l = re.sub(r'<[^>]+>', '', l) # removes HTML tags

			def find():
				i = 0
				for i in range(0, len(l)):
					if l[i] != '#' and l[i] != ' ' and l[i] != '*':
						return i
				return i

			r = l[:find()]
			if		r == '# ':	l = "\033[47m\033[1;30m"	+ l[2:] + "\033[0m"
			elif	r == '## ':	l = "\033[1;37m\033[4;37m"	+ l[3:] + "\033[0m"
			elif	r == '**':	l = "\033[1;37m"			+ l[2:-2] + "\033[0m"

			out.append(l)
		return out

	credentials, user_access, _ = check_access(args)

	if len(user_access) == 0:
		raise Exception('You don\'t have access to any SOL packages. Please contact the SOL team to set your permissions correctly!')

	# Check if license is installed and with correct version -------------------
	v = s_installed.get(f'{s_prefix}-sol-license')
	if v != s_license_version:
		# If wrong version is installed, uninstall it before continuing --------
		if v:
			run([sys.executable, '-m', 'pip', 'uninstall', '-y', f'{s_prefix}-sol-license'])

		# Process license request ----------------------------------------------
		msg = fetch_license(credentials, args)
		if isinstance(msg, Exception):
			raise msg

		license_text			= msg.get('license')
		license_authorization	= msg.get('license_authorization')
		license_acceptance		= msg.get('license_acceptance')
		license_error			= msg.get('license_error')

		if license_text is None or license_authorization is None or license_acceptance is None:
			raise Exception(license_error if license_error else 'invalid msg received from server')

		# Show license text ----------------------------------------------------
		license_text = convert(license_text)

		if args.accept_license:
			license_text			= '\n'.join(license_text)
			license_authorization	= license_authorization.replace('\n', '')
			license_acceptance		= license_acceptance.replace('\n', '')
			print(license_text)
			print()
			print(f'{license_authorization}:', emph('yes, I am [user accepted through --accept-license flag]'))
			print()
			print(f'{license_acceptance}:', emph('accept license [user accepted through --accept-license flag]'))
			print()
		else:
			less(license_text)

			options			= ['no, I am not', 'yes, I am']
			terminal_menu	= TerminalMenu(options, title=license_authorization)
			choice			= terminal_menu.show()
			if choice != 1:	raise Exception('License declined!')

			options			= ['decline license', 'accept license']
			terminal_menu	= TerminalMenu(options, title=license_acceptance)
			choice			= terminal_menu.show()
			if choice != 1:	raise Exception('License declined!')
	
	return credentials, user_access

#-------------------------------------------------------------------------------
def available_plugins(args, user_access) -> List[str]:
	plugins, extras = [], []

	if args.folder:
		def has_access(x: str) -> bool:
			return True
	else:
		def has_access(x: str) -> bool:
			url = 'https://{USERNAME}:{PASSWORD}@sol.neclab.eu/' + x + '/'
			return url in user_access

	for framework in s_available_frameworks:
		if framework in s_dependencies:
			extras.append(framework)

	for device in ['nvidia', 've', 'x86']:
		if device in s_dependencies and has_access(device):
			extras.append(device)

	if 'docs'		in s_dependencies: extras.append('docs')
	if 'deployment' in s_dependencies: extras.append('deployment')

	if has_access('dev'):
		if 'sdk' in s_dependencies:
			extras.append('sdk')

	if has_access('adv-dev'):
		if 'tests' in s_dependencies:
			for framework in s_available_frameworks:
				if framework in extras:
					extras.append(f'tests-{framework}')

		if 'adv-sdk' in s_dependencies:
			extras.append('adv-sdk')

	if 've' in extras and 'torch' in extras:
		plugins.append(f'veda-pytorch{s_dependencies.get("torch", None) or ""}')

	if args.mode == 'download':
		plugins.append(f'nec-sol=={s_version}')

	plugins.append(f'{s_prefix}-sol-core[{",".join(extras)}]=={s_version}')
	

	return sorted(plugins)

#-------------------------------------------------------------------------------
def renew_license(args):
	if f'{s_prefix}-sol-license' in s_installed:
		run([sys.executable, '-m', 'pip', 'uninstall', '-y', f'{s_prefix}-sol-license'])
	install(args, [f'{s_prefix}-sol-license=={s_license_version}'])

#-------------------------------------------------------------------------------
def debug(args):
	credentials, user_access, cache = check_access(args)
	
	msg = fetch_license(credentials, args)

	print(emph('User Information:'))
	print(f'Username: {credentials[0]}')
	license = red("failed") if isinstance(msg, Exception) else msg['license_type']
	print(f'License: {license}')
	print(f'Fingerprint: {fingerprint()}')
	print()
	
	print(emph('User Permissions:'))
	for k, v in sorted(cache.items()):
		print(f'{k.replace("{USERNAME}:{PASSWORD}@", "")}:{green("granted") if v == 200 else red("denied")}')
	print()

	print(emph('Packages to be installed:'))
	for p in available_plugins(args, user_access):
		print(f'- {p}')
	print()

	if args.verbose:
		print(emph('Installed Packages:'))
		for line in s_python_packages:
			print(line)

#-------------------------------------------------------------------------------
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=f'NEC-SOL Package Manager v{s_version}')
	parser.add_argument('mode', choices=[
		'download',
		'install',
		'uninstall',
		'debug',
		'renew-license',
	], default=None, nargs='?', help='installation mode')
	parser.add_argument('--accept-license', action='store_true', help='accept SOL license agreement')
	parser.add_argument('-u', '--username', default=None, type=str, help='SOL user name')
	parser.add_argument('-p', '--password', default=None, type=str, help='SOL user password')
	parser.add_argument('-f', '--folder', default=None, type=str, help='folder pointing to downloaded SOL packages')
	parser.add_argument('--trust', action='store_true', help='trust all SSL certificates (not recommended)')
	parser.add_argument('--devices', choices=['all'] + s_available_devices, nargs='*', type=str, default=[], help='manually list devices to download/install')
	parser.add_argument('--features', choices=['all'] + s_available_features, nargs='*', type=str, default=[], help='manually list features to download/install')
	parser.add_argument('--frameworks', choices=['all'] + s_available_frameworks, nargs='*', type=str, default=[], help='manually list frameworks to download/install')
	parser.add_argument('--user', action='store_true', help='install all packages using --user flag')
	parser.add_argument('--verbose', action='store_true', help='shows debug information')
	parser.add_argument('--version', action='store_true', help='shows version information')
	parser.add_argument('--no-index', action='store_true', help='disables PYPI in local installation mode')
	args = parser.parse_args()
	
	try:
		if sys.platform != 'linux':
			raise Exception(f'SOL only works on linux, but you are running: {sys.platform}')

		print(emph(f'## NEC-SOL Package Manager v{s_version}'))

		if not args.version:
			initialize()
			if		args.mode == 'install':			install			(args)
			elif	args.mode == 'download':		install			(args)
			elif	args.mode == 'uninstall':		uninstall		(args)
			elif	args.mode == 'debug':			debug			(args)
			elif	args.mode == 'renew-license':	renew_license	(args)
			else:	raise Exception(f'unsupported installer mode: {args.mode}')
	except Exception as e:
		print()
		print(red(str(e)))
		print()
		if args.verbose:
			for line in traceback.format_tb(e.__traceback__):
				print(line)
