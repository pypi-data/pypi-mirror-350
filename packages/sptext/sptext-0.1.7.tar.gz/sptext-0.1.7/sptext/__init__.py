import os, ast

class reader:
	def __init__(self):
		self.path = "."
		self.data = {}
		self.default_section = None

	def config(self, path=None, default_section=None):
		if path:
			self.path = path
		else:
			self.path = "."
		if default_section:
			self.default_section = self._normalize_section(default_section)

	def load(self, folder=None):
		if folder:
			self.path = folder
		for filename in os.listdir(self.path):
			if filename.endswith(".txt"):
				self._load_file(filename)

	def reload(self, section):
		filename = section if section.endswith(".txt") else f"{section}.txt"
		self._load_file(filename, force=True)

	def get(self, key, section=None):
		section = self._normalize_section(section or self.default_section)
		if section is None:
			raise ValueError("Default section not set. Please provide a section.")

		if section not in self.data:
			self._load_file(f"{section}.txt")

		value = self.data.get(section, {}).get(key)
		if value is None and self.default_section and self.default_section != section:
			value = self.data.get(self.default_section, {}).get(key)

		return value if value is not None else f"{key}_notFound"

	def _normalize_section(self, name):
		return name.rsplit(".", 1)[0] if name else None

	def _load_file(self, filename, force=False):
		full_path = os.path.join(self.path, filename)
		if not os.path.isfile(full_path):
			return

		section = self._normalize_section(filename)
		if section in self.data and not force:
			return

		texts = {}
		with open(full_path, encoding="utf-8") as f:
			for line in f:
				if '=' in line:
					line = '"' + line.strip().replace('"', '\\"') + '"'
					line = ast.literal_eval(line)
					key, value = line.strip().split("=", 1)
					texts[key.strip()] = value.strip()
		self.data[section] = texts