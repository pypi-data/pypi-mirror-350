"""
This test module contains unit tests for parsing functionality in the 'wardley_map' package.

The tests in this module are designed to verify the parsing capabilities of the 'wardley_map' package,
specifically ensuring that the parsing functions can accurately interpret and process different
elements of a Wardley Map definition, such as titles, components, edges, markets, and component attributes.

Functions:
    test_parse_title(): Tests the parsing of map titles from a definition string.
        It creates a map plot by parsing a definition that includes
        only a title and checks if the title is correctly interpreted.

    test_parse_component(): Tests the parsing of individual components from a definition string.
        It creates a map plot by parsing a definition that includes a single component with
        specified coordinates and checks if the component is correctly interpreted and placed on the map.

    test_parse_edge(): Tests the parsing of edges (dependencies) between components from a definition string.
        It creates a map plot by parsing a definition that includes two components and an edge between them,
        verifying if the components and their relationship (edge) are correctly interpreted and represented on the map.
        
    test_parse_inertia(): Tests the parsing of components with the inertia attribute.
        It creates a map plot by parsing a definition that includes a component with the inertia attribute
        and checks if the inertia flag is correctly set in the parsed component.
        
    test_parse_market(): Tests the parsing of market elements in a Wardley Map definition.
        It creates a map plot by parsing a definition that includes a market element and checks
        if the market is correctly identified and processed.

Each test function creates a Wardley Map plot by calling the `create_wardley_map_plot` function
with a map definition string as input, and implicitly checks for errors in the parsing process.
The actual validation of the map plot (e.g., checking if the title, components,
and edges are correctly represented) is not shown in the code snippet
but would typically involve assertions or visual inspection during the test run.
"""

import unittest
from wardley_map.create_wardley_map import create_wardley_map_plot


class TestParsing(unittest.TestCase):
    def test_parse_title(self):
        """
        Test the ability to parse the title from a Wardley Map definition string.
    
        This method tests if the `create_wardley_map_plot` function correctly interprets and handles 
        a map definition that includes only a title. The test passes if no errors occur during 
        the parsing and creation of the map plot, indicating successful title interpretation.
        """
    
        map_definition = "title Example Map"
        wm, map_plot = create_wardley_map_plot(map_definition)
        self.assertIsNotNone(map_plot)
        self.assertEqual(wm.title, "Example Map")



    def test_parse_component(self):
        """
        Test the parsing of individual components from a Wardley Map definition string.
    
        This test verifies that the `create_wardley_map_plot` function can accurately parse and incorporate 
        a single component, specified by its name and coordinates, into the map plot. Success is indicated 
        by the absence of errors during parsing and map plot creation, suggesting correct component 
        interpretation and placement.
        """
    
        map_definition = """
        component Component [0.5, 0.5]
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        self.assertIsNotNone(map_plot)
        self.assertIn("Component", wm.nodes)
        self.assertEqual(wm.nodes["Component"]["vis"], 0.5)
        self.assertEqual(wm.nodes["Component"]["evo"], 0.5)
    
    
    def test_parse_edge(self):
        """
        Test the parsing of edges (dependencies) between components from a Wardley Map definition string.
    
        This method assesses the ability of the `create_wardley_map_plot` function to parse a definition 
        that includes two components and an edge representing a dependency between them. The test is 
        considered successful if the parsing process completes without errors, implying that both components 
        and their relationship are correctly interpreted and depicted on the map plot.
        """
    
        map_definition = """
        component A [0.2, 0.2]
        component B [0.8, 0.8]
        A -> B
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        self.assertIsNotNone(map_plot)
        self.assertIn("A", wm.nodes)
        self.assertIn("B", wm.nodes)
        self.assertIn(["A", "B"], wm.edges)
    
    
    def test_parse_inertia(self):
        """
        Test the parsing of components with the inertia attribute from a Wardley Map definition string.
    
        This method tests if the `create_wardley_map_plot` function correctly recognizes and processes
        a component with the inertia attribute, which indicates resistance to evolution. The test verifies
        that the inertia flag is properly set and visualized in the final map plot.
        """
    
        map_definition = """
        component Component with Inertia [0.5, 0.5] inertia
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        
        # Check if the component was parsed correctly with the inertia attribute
        component = wm.nodes.get("Component with Inertia")
        self.assertIsNotNone(map_plot)
        self.assertIsNotNone(component)
        self.assertTrue(component.get("inertia", False))
    
    
    def test_parse_market(self):
        """
        Test the parsing of market elements from a Wardley Map definition string.
    
        This method tests if the `create_wardley_map_plot` function correctly interprets and processes
        a market element in the map definition. Markets represent user needs or groups that components serve
        and are visualized distinctly from regular components. The test passes if the market is correctly
        parsed as a node with the type "market" and is included in the map visualization.
        """
    
        map_definition = """
        market Test Market [0.9, 0.8]
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        
        # Check if the market was parsed correctly
        market = wm.nodes.get("Test Market")
        self.assertIsNotNone(map_plot)
        self.assertIsNotNone(market)
        self.assertEqual(market.get("type"), "market")


# Allow running the tests from the command line
if __name__ == "__main__":
    unittest.main()
