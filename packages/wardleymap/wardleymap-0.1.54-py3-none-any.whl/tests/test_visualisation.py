# tests/test_visualisation.py
import unittest
from wardley_map.create_wardley_map import create_wardley_map_plot
from wardley_map.wardley_maps_utils import create_svg_map


class TestVisualisation(unittest.TestCase):
    def test_visualisation_elements(self):
        """
        Test the generation of a Wardley Map's visual representation from its definition.
    
        This method evaluates the visualisation capabilities of the 'wardley_map' package by creating 
        a map plot from a basic map definition and then generating its SVG content. The map definition 
        includes a title and a single component, providing a minimal but sufficient basis for testing 
        the visualisation process.
    
        The test involves two main steps:
        1. Creation of a Wardley Map plot using the `create_wardley_map_plot` function with the provided definition.
        2. Conversion of the map plot to SVG format using the `create_svg_map` function.
    
        The test is considered successful if the SVG content is generated and is not `None`.
        """
    
        map_definition = """
        title Example Map
        component A [0.2, 0.2]
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
    
        # Act: Generate the SVG content
        svg_content = create_svg_map(map_plot)
        self.assertIsNotNone(svg_content)
    
    
    def test_visualisation_inertia(self):
        """
        Test the visualization of components with inertia in a Wardley Map.
        
        This method tests the ability of the package to correctly visualize components
        with the inertia attribute. Inertia is represented as a vertical line ("wall") 
        at the component's position, indicating resistance to evolution.
        
        The test creates a map with a component that has inertia and verifies that
        the visualization pipeline handles this special attribute correctly.
        """
        
        map_definition = """
        title Map with Inertia
        component Component with Inertia [0.5, 0.5] inertia
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        
        # Generate SVG and check it was created successfully
        svg_content = create_svg_map(map_plot)
        self.assertIsNotNone(svg_content)
        # Verify the component has inertia flag set
        component = wm.nodes.get("Component with Inertia")
        self.assertTrue(component.get("inertia", False))
            
    
    def test_visualisation_market(self):
        """
        Test the visualization of market elements in a Wardley Map.
        
        This method tests the ability of the package to correctly visualize market elements,
        which are represented as a complex symbol with a circle, internal triangle, and dots.
        Markets represent user needs or groups that components serve.
        
        The test creates a map with a market element and verifies that the visualization
        pipeline handles this special element type correctly.
        """
        
        map_definition = """
        title Map with Market
        market Test Market [0.9, 0.8]
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        
        # Generate SVG and check it was created successfully
        svg_content = create_svg_map(map_plot)
        self.assertIsNotNone(svg_content)
        # Verify the market is correctly parsed
        market = wm.nodes.get("Test Market")
        self.assertEqual(market.get("type"), "market")
        
    def test_visualisation_pipeline(self):
        """
        Test the visualization of pipeline elements in a Wardley Map.
        
        This method tests the ability of the package to correctly visualize pipeline elements,
        which are represented as a rectangular bar with specified start and end points along
        the evolution axis. Pipelines represent value chains or processes that span multiple
        evolution stages.
        
        The test creates a map with a pipeline component and verifies that the visualization
        pipeline handles this special element type correctly.
        """
        
        map_definition = """
        title Map with Pipeline
        component Pipeline Component [0.6, 0.5]
        pipeline Pipeline Component [0.4, 0.8]
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        
        # Generate SVG and check it was created successfully
        svg_content = create_svg_map(map_plot)
        self.assertIsNotNone(svg_content)
        
        # Verify the component is correctly parsed
        component = wm.nodes.get("Pipeline Component")
        self.assertIsNotNone(component)
        self.assertEqual(component.get("type"), "component")
        
        # Verify the pipeline is correctly parsed
        pipeline = wm.pipelines.get("Pipeline Component")
        self.assertIsNotNone(pipeline)
        self.assertEqual(pipeline.get("start_evo"), 0.4)
        self.assertEqual(pipeline.get("end_evo"), 0.8)
    
    
    def test_visualisation_complex(self):
        """
        Test the visualization of a complex Wardley Map with multiple element types.
        
        This method tests the ability of the package to correctly visualize a more complex
        map that includes regular components, components with inertia, markets, and dependencies
        between elements. This tests the full visualization pipeline and the integration
        of different element types in a single map.
        """
        
        map_definition = """
        title Complex Map
        component Component A [0.3, 0.4]
        component Component B [0.6, 0.6] inertia
        market Market [0.9, 0.8]
        Component A -> Component B
        Component B -> Market
        """
        wm, map_plot = create_wardley_map_plot(map_definition)
        
        # Generate SVG and check it was created successfully
        svg_content = create_svg_map(map_plot)
        self.assertIsNotNone(svg_content)
        # Verify components were parsed correctly
        self.assertIn("Component A", wm.nodes)
        self.assertIn("Component B", wm.nodes)
        self.assertIn("Market", wm.nodes)
        # Verify inertia was parsed correctly
        self.assertTrue(wm.nodes["Component B"].get("inertia", False))
        # Verify market type was parsed correctly
        self.assertEqual(wm.nodes["Market"].get("type"), "market")


    def test_save_maps_for_inspection(self):
        """
        Save visual maps as PNG files for manual inspection.
        
        This test creates several map types (basic, with inertia, with market, complex)
        and saves them as PNG files in the project directory. This allows for manual
        visual inspection of the rendered maps to verify the visualization works correctly.
        """
        import os
        
        # Create test directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Test cases to generate
        test_cases = {
            "basic": """
            title Basic Map
            component Component A [0.3, 0.4]
            component Component B [0.7, 0.6]
            Component A -> Component B
            """,
            
            "inertia": """
            title Map with Inertia
            component Component A [0.3, 0.4]
            component Component B with Inertia [0.7, 0.6] inertia
            Component A -> Component B with Inertia
            """,
            
            "market": """
            title Map with Market
            component Component [0.5, 0.5]
            market Customer Market [0.9, 0.8]
            Component -> Customer Market
            """,
            
            "pipeline": """
            title Map with Pipeline
            component Pipeline Component [0.6, 0.5]
            pipeline Pipeline Component [0.4, 0.8]
            """,
            
            "complex": """
            title Complex Map
            component Component A [0.3, 0.4]
            component Component B [0.6, 0.6] inertia
            component Component C [0.7, 0.3]
            market Market [0.9, 0.8]
            component Pipeline Component [0.5, 0.7]
            pipeline Pipeline Component [0.3, 0.7]
            Component A -> Component B
            Component B -> Component C
            Component C -> Market
            """
        }
        
        # Generate and save each test case
        created_files = []
        for name, definition in test_cases.items():
            _, map_plot = create_wardley_map_plot(definition)
            
            # Save as PNG
            output_path = os.path.join(output_dir, f"test_map_{name}.png")
            map_plot.savefig(output_path, dpi=300, bbox_inches='tight')
            
            # Verify file was created
            self.assertTrue(os.path.exists(output_path))
            created_files.append(f"test_map_{name}.png")
            print(f"Saved test map to: {output_path}")
            
        # Test passed if all expected files were created
        for expected_file in created_files:
            expected_path = os.path.join(output_dir, expected_file)
            self.assertTrue(os.path.exists(expected_path))

    def test_prompt_engineering_map(self):
        """
        Test visualization of the comprehensive prompt engineering Wardley Map.
        
        This test loads the prompt_engineering.owm file and generates a PNG visualization
        to ensure the package can handle complex, real-world maps with many components,
        relationships, pipelines, markets, and annotations.
        """
        import os
        
        # Read the prompt engineering map file
        owm_file_path = os.path.join(os.path.dirname(__file__), "prompt_engineering.owm")
        
        # Verify the file exists
        self.assertTrue(os.path.exists(owm_file_path), f"prompt_engineering.owm not found at {owm_file_path}")
        
        # Read the map definition
        with open(owm_file_path, 'r', encoding='utf-8') as f:
            map_definition = f.read()
        
        # Create the map visualization
        wm, map_plot = create_wardley_map_plot(map_definition)
        
        # Verify the map was created successfully
        self.assertIsNotNone(wm)
        self.assertIsNotNone(map_plot)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "..", "test_output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as PNG
        output_path = os.path.join(output_dir, "prompt_engineering_map.png")
        map_plot.savefig(output_path, dpi=300, bbox_inches='tight')
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        print(f"Saved prompt engineering map to: {output_path}")
        
        # Verify the map has expected content
        self.assertIsNotNone(wm.title)
        self.assertEqual(wm.title, "Prompt Engineering (Public)")
        
        # Verify it has components, relationships, and other elements
        self.assertGreater(len(wm.nodes), 50)  # Should have many components
        self.assertGreater(len(wm.edges), 50)  # Should have many relationships
        self.assertGreater(len(wm.pipelines), 5)  # Should have several pipelines
        self.assertGreater(len(wm.notes), 10)  # Should have many notes


# Allow running the tests from the command line
if __name__ == "__main__":
    unittest.main()
