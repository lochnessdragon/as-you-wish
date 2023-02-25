import configparser

def get_type_str(type):
    if type == str:
        return "string"
    elif type == int:
        return "int"
    elif type == list:
        return "list"
    elif type == dict:
        return "dict"
    elif type == float:
        return "float"
    elif type == tuple:
        return "tuple"
    else:
        return "<unknown-type>"


class ConfigValue:
    """Represents the value stored in a certain key. Keeps track of the type of the data, the data itself and the comment associated with the key.
    It also checks the data to make sure it fits the datatype.

    :param data_type: The data type of data
    :type data_type: type

    :param data: The data stored by this ConfigValue
    :type data: Any

    :param comment: The documentation for this value
    :type comment: str
    """
    def __init__(self, data_type, data, comment: str):
        if not isinstance(data, data_type):
            raise RuntimeError("The data doesn't match the type")
        self.data_type = data_type
        self._data = data
        self.comment = comment

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, input):
        if not isinstance(input, self.data_type):
            raise TypeError(f"Wrong type provided: {type(input)}. Expected: {self.data_type}")
        self._data = input

    def __repr__(self):
        return f"ConfigVal[type={repr(self.data_type)}, data={repr(self.data)}, comment={repr(self.comment)}]"

    def __str__(self):
        formatted_str = f'{repr(self.data)} ({get_type_str(self.data_type)})'
        if self.comment != '':
            formatted_str += f' # {self.comment}'
        return formatted_str


class Config:
    """
    The config class represents a set of options and values and can be used to load settings from files.
    """
    def __init__(self):
        """Constructs a new Config"""
        self.values = {}

    def define(self, key, default_value, comment=""):
        """Creates a new option

        This is used to set a new k,v pair for an option.
        You can also chain these methods like so:

        .. code-block:: python
        
            config.define('westley.actor', 'Cary Elwes').define('westley.ressurect_count', 1)

        :param key: A unique identifier that refers to the value, used to retrieve the value in the get() method
        :type key: str

        :param default_value: The default value for this setting. Used to get the type that the option should be and it is used to create a setting in the options file when there isn't one.
        :type default_value: Any

        :param comment: A descriptive message to help users figure out what each setting does, defaults to ''
        :type comment: str, optional

        :raises TypeError: If the key provided is a subsection of a previously set key, a type error will be raised

        :return: self
        :rtype: :class:`as_you_wish.Config`
        """
        default_value_type = type(default_value)

        sections = key.split(".")
        head = self.values
        for i in range(len(sections)):
            if i < len(sections) - 1:
                # it isn't the end node, so it should be another table
                if not sections[i] in head:
                    # the table doesn't exist yet, create it
                    head[sections[i]] = {}
                elif not type(head[sections[i]]) is dict:
                    raise TypeError("The key provided points to a key instead of a table")

                head = head[sections[i]]
            else:
                # this is the end, so create a config value and set that.
                head[sections[i]] = ConfigValue(default_value_type,
                                                default_value, comment)

        return self

    def load(self, filename: str):
        """Attempts to load a configuration from a specified file.

        This function will also create the file if it doesn't exists already and it will update the file with any options that may not be defined.

        :param filename: The filename to load the config from.
        :type filename: str
        """
        try:
            parser = configparser.ConfigParser()
            with open(filename, 'r') as fp:
                parser.read_file(fp)

            missing_section = False
            missing_value = False
            wrong_type = False

            for section in self.get_sections(self.values):
                if not section in parser.sections():
                    print(f"We are missing section: {section}")
                    missing_section = True
                    continue

                for key in self.get_keys(section):
                    if not parser.has_option(section, key):
                        print(f"We are missing key: {key}")
                        missing_value = True
                        continue
                    # grab ConfigValue
                    section_parts = section.split('.')
                    head = self.values
                    for part in section_parts:
                        head = head[part]
                    config_val = head[key]

                    value_str = parser[section][key]
                    if config_val.data_type == str:
                        config_val.data = value_str
                    else:
                        try:
                            converted_value = eval(value_str, {"__builtins__":None})
                            config_val.data = converted_value
                        except:
                            wrong_type = True
                            print(f"Wrong type found when parsing {key} in {section}. Found: {type(coverted_value)} Expected: {config_val.data_type}")

                    # set ConfigValue
                    head = self.values
                    for i in range(len(section_parts)):
                        head = head[section_parts[i]]
                        if i >= len(section_parts) - 1:
                            head[key] = config_val

            if missing_section == True:
                print("We are missing a required section, attempting to fix.")
                raise RuntimeError("Missing section when reading config file.")
            elif missing_value == True:
                print("We are missing a required value, attempting to fix.")
                raise RuntimeError("Missing value when reading config file.")
            elif wrong_type == True:
                print("One of the setting values is of the wrong type, attempting to fix.")
                raise RuntimeError("Type mismatch when reading config file")
        except:
            print("Failed to read config file:", filename,
                  "Attempting to fix!")
            self.save(filename)

    def get_sections(self, table, base=[]):
        # returns a list of all the flattened sections that have config values
        sections = []
        is_section = False
        for key in table:
            if isinstance(table[key], ConfigValue):
                is_section = True
            elif isinstance(table[key], dict):
                base.append(key)
                sections.extend(self.get_sections(table[key], base))
                base.pop(-1)
        if is_section:
            sections.append('.'.join(base))
        return sections

    def get_keys(self, section):
        head = self.values
        for part in section.split('.'):
            head = head[part]

        keys = []
        for key in head:
            if isinstance(head[key], ConfigValue):
                keys.append(key)

        return keys

    def save(self, filename):
        """Saves the configuration to a specific file. Mostly used internally to fix broken configs, but can be used externally to allow users to update settings either through a file or another interface.

        :param filename: The file to save the config to.
        :type filename: str
        """
        parser = configparser.ConfigParser(allow_no_value=True)
        # alphabetical sections
        added_sections = self.get_sections(self.values)
        added_sections.sort()
        print(added_sections)
        for section in added_sections:
            parser.add_section(section)
            parts = section.split('.')
            head = self.values
            for part in parts:
                head = head[part]

            for key in head:
                if isinstance(head[key], ConfigValue):
                    config_val = head[key]
                    if config_val.comment != '':
                        parser.set(section, f"# {config_val.comment}")
                    parser.set(section, key, str(config_val.data))
        # write file
        with open(filename, 'w') as fp:
            parser.write(fp)

    def get(self, key):
        """Returns the value specificied by a key.

        :param key: The lookup key (unique identifier)
        :type key: str

        :return: The value associated with the key. Please remember which keys are associated with which data types.
        :rtype: Any
        """
        sections = key.split('.')
        head = self.values
        for i in range(len(sections)):
            # check if the next key exists
            if not sections[i] in head:
                raise KeyError(
                    f"Key: {key} not found in the configuration. Did you forget to define() it?"
                )
            if i < len(sections) - 1:
                # if we aren't at the end yet, then we should be at another table
                if not type(head[sections[i]]) is dict:
                    raise TypeError(
                        f"One of the table of the way to key: {key} is not actually a table."
                    )
                head = head[sections[i]]  # set reference to the next table
            else:
                # we are at the last value, return it
                if not type(head[sections[i]]) is ConfigValue:
                    raise TypeError(
                        f"Key: {key} doesn't lead to an actual value. Are you sure you are using the full key?"
                    )
                return head[sections[i]].data

    def __repr__(self):
        return f"Config: {repr(self.values)}"

    def recursive_str(self, table, indent_level=0) -> str:
        formatted_str = ''

        current_idx = 0
        for key in table:
            formatted_str += ('\t' * indent_level)
            formatted_str += repr(key) + ': '
            if type(table[key]) is dict:
                # new dict, add str
                formatted_str += ('\t' * indent_level)
                formatted_str += '{\n' + self.recursive_str(
                    table[key], indent_level=indent_level + 1) + '\n}'
            else:
                # ConfigValue
                formatted_str += str(table[key])
            if current_idx < len(table.keys()) - 1:
                formatted_str += ",\n"
            current_idx += 1
        return formatted_str

    def __str__(self):
        formatted_str = "Config:\n" + self.recursive_str(self.values)
        return formatted_str
