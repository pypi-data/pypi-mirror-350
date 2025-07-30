"""
Wardley Map Parser and Visualiser

This module provides the wardley_map class, designed to parse, interpret,
and manage the data of Wardley Maps from their textual representation in Open Wardley Map (OWM) syntax.
It supports extracting components, anchors, pipelines, notes, and more from a given map syntax or map ID,
allowing for further analysis and visualization of the map's content.
Additionally, the class can fetch map data from a remote source using a map ID.

The wardley_map class offers methods to retrieve detailed information about the map's components,
including their evolution stages, visibility, and relationships.
It also includes functionality to identify and report potential issues or unsupported features in the map syntax.

Dependencies:
    - json: For parsing JSON data.
    - re: For regular expression operations.
    - requests: For making HTTP requests to fetch map data from remote sources.

Example usage:
    owm_syntax = "<Your OWM syntax here>"
    wardley_map = wardley_map(owm_syntax)
    components = wardley_map.getComponents()
    print(components)

Note:
    This module is intended for educational and informational purposes.
    Ensure you have the necessary permissions to fetch and use map data from remote sources.
"""

import re
import json
import requests


class WardleyMap:
    """
    Represents a Wardley Map parsed from a given Wardley Map Syntax (OWM) string or a map ID.

    This class provides functionalities to parse various components of a Wardley Map
    including nodes (components and anchors), edges, pipelines, evolutions,
    and notes from the OWM syntax. It also supports fetching map data
    from a remote source using a map ID.

    Attributes:
        title (str): The title of the Wardley Map.
        anchors (list): A list of anchors in the map.
        nodes (dict): A dictionary of nodes in the map, keyed by node title.
        edges (list): A list of edges (relationships) between nodes.
        bluelines (list): A list of blueline relationships between nodes.
        evolutions (dict): A dictionary containing evolution stages of components.
        evolves (dict): A dictionary containing evolve relationships between nodes.
        pipelines (dict): A dictionary of pipelines in the map.
        annotations (list): A list of annotations in the map.
        notes (list): A list of notes associated with the map.
        style (str): The visual style of the map.
        warnings (list): A list of warnings generated during parsing.
        components (list): A list of components parsed from the map.
        component (dict): Details of a single component when searched by name.
    """

    # Developed using https://regex101.com/
    _coords_regexs = "\\[\\s*([\\d\\.-]+)\\s*,\\s*([\\d\\.-]+)\\s*\\]"

    # _node_regex = re.compile(r"^(\w+) ([a-zA-Z0-9_.,/&' +)(?-]+)\s+{COORDS}(\s+label\s+{COORDS})*".format(COORDS=_coords_regexs))
    _node_regex = re.compile(
        r"^(\w+) (?:.*?//.*?)?([a-zA-Z0-9_.,/&' +)(?_!/-]+?)\s+{COORDS}(\s+label\s+{COORDS})*".format(
            COORDS=_coords_regexs
        )
    )

    # _evolve_regex = re.compile(r"^evolve ([\w \/',)(-]+)\s+([\d\.-]+)(\s+label\s+{COORDS})*".format(COORDS=_coords_regexs))
    _evolve_regex = re.compile(
        r"^evolve (?:.*?//.*?)?([\w \/',)(-]+?)\s+([\d\.-]+)(\s+label\s+{COORDS})*".format(
            COORDS=_coords_regexs
        )
    )

    # _pipeline_regex = re.compile(r"^pipeline ([a-zA-Z0-9_.,/&' )(?-]+)\s+\[\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\]$")
    _pipeline_regex = re.compile(
        r"^pipeline ([a-zA-Z0-9_.,/&' )(?-]+?)(?:\s*//.*)?\s+\[\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\]$"
    )

    # _note_regex = re.compile(r"^(\w+) ([\S ]+)\s+{COORDS}\s*".format(COORDS=_coords_regexs))
    _note_regex = re.compile(
        r"^(\w+) (?:.*?//.*?)?([\S ]+?)\s+{COORDS}\s*".format(COORDS=_coords_regexs)
    )

    def __init__(self, owm: str):
        """
        Initializes a WardleyMap object either from a map ID or OWM syntax string.

        If the provided string is recognized as a map ID,the map data is fetched from a remote source.
        Otherwise, the string is treated as the OWM syntax of the map and parsed accordingly.

        Parameters:
            owm (str): A string representing either the map ID or the OWM syntax of a Wardley Map.
        """

        # Defaults:
        self.title = None
        self.nodes = {}
        self.edges = []
        self.bluelines = []
        self.evolutions = {}
        self.evolves = {}
        self.pipelines = {}
        self.annotations = []
        self.annotation = {}
        self.notes = []
        self.style = None
        self.warnings = []
        self.components = []
        self.anchors = []
        self.component = None


        if self.is_map_id(owm):
            self.map_id = owm
            self.owm = self.fetch_map_text()
        else:
            self.map_id = None
            self.owm = owm

        # Validation completed

        if self.owm is None:
            self.warnings.append(f"Could not fetch map data for ID: {owm}")
            return

        # And load:
        for line in self.owm.splitlines():
            line = line.strip()
            if not line:
                continue

            elif line.startswith("#"):
                # Skip comments...
                continue

            elif line.startswith("//"):
                # Skip comments...
                continue

            elif line.startswith("annotation "):
                # Parse annotation: "annotation 1,[0.63,0.57] Memory is the capacity..."
                try:
                    # Extract number
                    number_match = re.search(r'annotation\s+(\d+)', line)
                    if not number_match:
                        continue
                    number = int(number_match.group(1))
                    
                    # Extract coordinates using existing regex
                    coords_match = re.search(self._coords_regexs, line)
                    if not coords_match:
                        continue
                    vis = float(coords_match.group(1))
                    evo = float(coords_match.group(2))
                    
                    # Extract text after coordinates
                    bracket_end = line.find(']')
                    if bracket_end == -1:
                        continue
                    text = line[bracket_end + 1:].strip()
                    
                    # Store annotation
                    annotation = {
                        "number": number,
                        "vis": vis,
                        "evo": evo,
                        "text": text
                    }
                    self.annotations.append(annotation)
                except (ValueError, AttributeError):
                    self.warnings.append(f"Could not parse annotation: {line}")
                continue

            elif line.startswith("annotations "):
                # Parse annotations legend position: "annotations [0.32, 0.01]"
                try:
                    coords_match = re.search(self._coords_regexs, line)
                    if coords_match:
                        self.annotation = {
                            "vis": float(coords_match.group(1)),
                            "evo": float(coords_match.group(2))
                        }
                except (ValueError, AttributeError):
                    self.warnings.append(f"Could not parse annotations position: {line}")
                continue

            elif line.startswith("market "):
                # Use RegEx to split into fields:
                match = self._node_regex.search(line)
                if match is not None:
                    matches = match.groups()
                    node = {
                        "type": "market",
                        "title": matches[1],
                        "vis": float(matches[2]),
                        "evo": float(matches[3]),  # Evolution (previously "mat")
                    }
                    # Handle label position adjustments:
                    if matches[4]:
                        node["label_x"] = float(matches[5])
                        node["label_y"] = float(matches[6])
                    # Store it:
                    self.nodes[node["title"]] = node
                    continue
                self.warnings.append(f"Could not parse market: {line}")

            elif line.startswith("pipeline "):
                match = self._pipeline_regex.search(line)
                if match is not None:
                    matches = match.groups()
                    pipeline = {
                        "title": matches[0],
                        "start_evo": float(matches[1]),  # Evolution start (previously "start_mat")
                        "end_evo": float(matches[2]),    # Evolution end (previously "end_mat")
                    }

                    # And store it:
                    self.pipelines[matches[0]] = pipeline
                    continue

                self.warnings.append(f"Could not parse pipeline: {line}")

            elif line.startswith("evolution "):
                warning_message = "Displaying evolution axis tags not currently supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                    continue

            elif line.startswith("title "):
                self.title = line.split(" ", maxsplit=1)[1]
                continue

            elif line.startswith("style "):
                self.style = line.split(" ", maxsplit=1)[1]
                continue

            elif line.startswith("anchor "):
                # Use RegEx to split into fields:
                match = self._node_regex.search(line)
                if match is not None:
                    matches = match.groups()
                    node = {
                        "type": matches[0],
                        "title": matches[1],
                        "vis": float(matches[2]),
                        "evo": float(matches[3]),  # Evolution (previously "mat")
                        "inertia": "inertia" in line,  # Check if component has inertia
                    }
                    # Handle label position adjustments:
                    if matches[4]:
                        node["label_x"] = float(matches[5])
                        node["label_y"] = float(matches[6])
                    #else:
                    #    # Default to a small additional offset:
                    #    node["label_x"] = 2
                    #    node["label_y"] = 2
                    # And store it:
                    self.nodes[node["title"]] = node
                    continue
                self.warnings.append(f"Could not parse anchor: {line}")

            elif line.startswith("component "):
                # Use RegEx to split into fields:
                match = self._node_regex.search(line)
                if match is not None:
                    matches = match.groups()
                    node = {
                        "type": matches[0],
                        "title": matches[1],
                        "vis": float(matches[2]),
                        "evo": float(matches[3]),  # Evolution (previously "mat")
                        "inertia": "inertia" in line,  # Check if component has inertia
                    }
                    # Handle label position adjustments:
                    if matches[4]:
                        node["label_x"] = float(matches[5])
                        node["label_y"] = float(matches[6])
                    #else:
                    #    # Default to a small additional offset:
                    #    node["label_x"] = None
                    #    node["label_y"] = None
                    # And store it:
                    self.nodes[node["title"]] = node
                    continue
                self.warnings.append(f"Could not parse component line: {line}")

            elif line.startswith("evolve "):
                match = self._evolve_regex.search(line)
                if match is not None:
                    matches = match.groups()
                    evolve = {"title": matches[0], "evo": float(matches[1])}  # Evolution (previously "mat")
                    # Handle label position adjustments:
                    if matches[3] is not None:
                        evolve["label_x"] = float(matches[3])
                    else:
                        evolve["label_x"] = 2

                    if matches[4] is not None:
                        evolve["label_y"] = float(matches[4])
                    #else:
                    #    evolve["label_y"] = 2

                    # And store it:
                    self.evolves[matches[0]] = evolve
                    continue
                self.warnings.append(f"Could not parse evolve line: {line}")

            elif "->" in line:
                edge_parts = line.split("->")
                if len(edge_parts) != 2:
                    self.warnings.append(
                        f"Unexpected format for edge definition: {line}. Skipping this edge."
                    )
                    continue
                n_from, n_to = edge_parts
                self.edges.append([n_from.strip(), n_to.strip()])

            elif "+<>" in line:
                edge_parts = line.split("+<>")
                if len(edge_parts) != 2:
                    self.warnings.append(
                        f"Unexpected format for blueline definition: {line}. Skipping this edge."
                    )
                    continue
                n_from, n_to = edge_parts
                self.bluelines.append([n_from.strip(), n_to.strip()])
                continue

            elif line.startswith("note"):
                match = self._note_regex.search(line)
                if match is not None:
                    matches = match.groups()
                    note = {
                        "text": matches[1],
                    }
                    # Handle text position adjustments:
                    if matches[2]:
                        note["vis"] = float(matches[2])
                        note["evo"] = float(matches[3])
                    else:
                        # Default to a small additional offset:
                        note["vis"] = 0.2
                        note["evo"] = 0.2
                    # And store it:
                    self.notes.append(note)
                    continue
                self.warnings.append(f"Could not parse note line: {line}")

            else:
                self.warnings.append(f"Could not parse line: {line}")

        self.warnings = list(set(self.warnings))


    def is_map_id(self, val):
        """
        Check if a value is a valid map ID based on its format.
        Map IDs should be 18-character alphanumeric strings.
        :param val: The value to check.
        :type val: str
        :return: True if the value is a valid map ID, False otherwise.
        """
        import re
        if not isinstance(val, str):
            return False
        # Check if it's exactly 18 characters of alphanumeric characters (including hyphens/underscores)
        return bool(re.match(r'^[a-zA-Z0-9_-]{18}$', val))


    def fetch_map_text(self, timeout=15):
        """
        Fetches the map data using the Wardley Mapping AI API.
        
        :param timeout: Request timeout in seconds (default: 15)
        :type timeout: int
        """
        # Sanitize map_id to prevent URL injection
        from urllib.parse import quote
        sanitized_map_id = quote(str(self.map_id), safe='')
        url = f"https://maps.wardleymaps.ai/v2/maps/fetch?id={sanitized_map_id}"
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

            try:
                mapdata = response.json()
                self.owm = mapdata.get("text", "")
                if not self.owm:
                    pass  # Empty text field
            except ValueError:
                self.owm = None

        except requests.exceptions.RequestException as e:
            self.owm = None

        return self.owm


    def get_warnings(self):
        """
        Parses the Wardley Map syntax to identify and return any warnings generated during parsing.

        Warnings may include unrecognized lines, unsupported features, or errors in the map syntax.

        Returns:
            list: A list of warning messages.
        """

        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )

        return self.warnings


    def get_notes(self):
        """
        Extracts and returns notes from the Wardley Map syntax.

        Returns:
            list: A list of dictionaries, each representing a note with its content and position.
        """
        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )

        self.notes = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("note"):
                note = line[line.find(" ") + 1 : line.find("[")].strip()
                pos_index = line.find("[")
                self.swap_xy(line) if pos_index != -1 else ""
                self.notes.append({"note": note})
        return self.notes


    def get_annotations(self):
        """
        Extracts and returns annotations from the Wardley Map syntax.

        Returns:
            list: A list of dictionaries,
            each representing an annotation with its number and content.
        """
        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )

        self.annotations = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("annotation"):
                self.swap_xy(line)
                number = re.findall(r"\d+", line)
                annotation = line[line.index("]") + 1 :].lstrip()
                self.annotations.append({"number": number[0], "annotation": annotation})
        self.annotations = [
            i
            for n, i in enumerate(self.annotations)
            if i not in self.annotations[n + 1 :]
        ]  # Remove duplicates
        return self.annotations


    def get_components(self):
        """
        Extracts and returns the components from the Wardley Map syntax.

        Returns:
            list: A list of dictionaries, each representing a component with its name,
            evolution stage, visibility, and description.
        """
        if self.owm is None:
            raise ValueError(
                "Map is not initialised. Please check if the map ID is correct."
            )

        self.components = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("component"):
                stage = ""
                pos_index = line.find("[")
                if pos_index != -1:
                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)

                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    elif 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    elif 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    elif 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    else:
                        stage = ""

                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    elif 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    elif 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    else:
                        visibility = ""

                else:
                    new_c_xy = ""
                name = line.split("[")[0].split(" ", 1)[1].strip()
                self.components.append(
                    {
                        "name": name,
                        "evolution": stage,
                        "visibility": visibility,
                        #"description": "",
                    }
                )
        return self.components


    def get_anchors(self):
        """
        Extracts and returns all the anchors from the Wardley Map syntax.

        Each anchor is represented as a dictionary containing its name, evolution stage, and visibility.

        Returns:
            list[dict]: A list of dictionaries, each representing an anchor with its details.
        """

        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )

        self.anchors = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("anchor"):
                stage = ""
                pos_index = line.find("[")
                if pos_index != -1:
                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)

                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    elif 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    elif 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    elif 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    else:
                        stage = ""

                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    elif 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    elif 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    else:
                        visibility = ""

                else:
                    new_c_xy = ""
                anchor = line.split("[")[0].split(" ", 1)[1].strip()
                self.anchors.append(
                    {
                        "name": anchor,
                        "evolution": stage,
                        "visibility": visibility
                    }
                )
        return self.anchors


    def get_pipelines(self):
        """
        Extracts and returns all the pipelines from the Wardley Map syntax.

        Each pipeline is represented as a dictionary containing its name, evolution stage, and visibility.

        Returns:
            list[dict]: A list of dictionaries, each representing a pipeline with its details.
        """

        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )

        self.pipelines = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("pipeline"):
                stage = ""
                pos_index = line.find("[")
                if pos_index != -1:
                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)

                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    elif 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    elif 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    elif 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    else:
                        stage = ""

                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    elif 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    elif 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    else:
                        visibility = ""

                else:
                    new_c_xy = ""
                pipeline = line.split("[")[0].split(" ", 1)[1].strip()
                self.pipelines.append(
                    {
                        "name": pipeline,
                        "evolution": stage,
                        "visibility": visibility
                    }
                )
        return self.pipelines


    def get_component(self, component_name):
        """
        Retrieves the details of a specific component by its name.

        Parameters:
            component_name (str): The name of the component to retrieve.

        Returns:
            dict: A dictionary containing the details of the specified component, including its name, evolution stage, visibility, and description. Returns None if the component is not found.
        """

        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )

        self.component = None
        lines = self.owm.strip().split("\n")
        for line in lines:
            # Use regex to match exact component name (not partial matches)
            import re
            # Match "component" followed by whitespace, then the exact component name, then end or whitespace or [
            pattern = rf"^component\s+{re.escape(component_name)}(?:\s|\[|$)"
            if re.search(pattern, line.strip()):
                stage = ""
                visibility = ""  # Initialize visibility variable
                pos_index = line.find("[")
                if pos_index != -1:
                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)

                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    elif 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    elif 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    elif 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    else:
                        stage = ""

                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    elif 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    elif 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    else:
                        visibility = ""
                else:
                    new_c_xy = ""
                # Extract the component name properly (everything between 'component ' and '[' or end of line)
                bracket_pos = line.find("[")
                if bracket_pos != -1:
                    # Extract name between 'component ' and '['
                    extracted_name = line[line.find(" ") + 1:bracket_pos].strip()
                else:
                    # Extract name after 'component ', handling potential attributes like 'inertia'
                    name_part = line[line.find(" ") + 1:].strip()
                    # If there are attributes like 'inertia', the component name is everything except the last word
                    words = name_part.split()
                    if words and words[-1] in ['inertia']:  # Known attributes
                        extracted_name = ' '.join(words[:-1])
                    else:
                        extracted_name = name_part
                
                self.component = {
                    "name": extracted_name,
                    "evolution": stage,
                    "visibility": visibility,
                    "description": "",
                }
                break  # Exit the loop as soon as we've found our component
        return self.component


    def swap_xy(self, xy):
        """
        Swaps the x and y coordinates in a string representation of a coordinate pair.

        Parameters:
            xy (str): A string containing the coordinate pair.

        Returns:
            str: The string with swapped coordinates, or "[0, 0]" if parsing fails.
        """
        # Import here to avoid circular imports
        from .wardley_maps_utils import swap_xy as utils_swap_xy
        return utils_swap_xy(xy)


    def get_map_text(self):
        """
        Returns the original Wardley Map syntax as a string.

        Returns:
            str: The OWM syntax of the Wardley Map.
        """
        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )
        return self.owm


    def search_component(self, search_term):
        """
        Search for components in the Wardley Map by a search term.

        :param search_term: The term to search for in component names
        :type search_term: str
        :return: A list of components that match the search term
        """
        if self.owm is None:
            raise ValueError(
                "Map is not initialized. Please check if the map ID is correct."
            )

        # Ensure components are parsed and up to date
        self.get_components()

        # Perform case-insensitive search
        search_term = search_term.lower()
        found_components = [
            component
            for component in self.components
            if search_term in component["name"].lower()
            or search_term in component.get("evolution", "").lower()
            or search_term in component.get("visibility", "").lower()
        ]
        return found_components
