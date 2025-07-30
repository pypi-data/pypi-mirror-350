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

        The test creates a map with multiple pipelines similar to those in the prompt engineering
        map to test realistic pipeline usage patterns.
        """

        map_definition = """
        title Map with Pipelines
        component User Interface [0.88, 0.53]
        component Pipeline Development [0.83, 0.55]
        component Techniques [0.75, 0.54]
        component Vector DB [0.26, 0.52]
        component Embedding [0.45, 0.59]
        component Compute [0.08, 0.76]
        
        pipeline User Interface [0.5, 0.8]
        pipeline Pipeline Development [0.22, 0.85]
        pipeline Techniques [0.1, 0.6]
        pipeline Vector DB [0.40, 0.8]
        pipeline Embedding [0.30, 0.8]
        pipeline Compute [0.6, 0.90]
        
        User Interface -> Pipeline Development
        Techniques -> Pipeline Development
        """
        wm, map_plot = create_wardley_map_plot(map_definition)

        # Generate SVG and check it was created successfully
        svg_content = create_svg_map(map_plot)
        self.assertIsNotNone(svg_content)

        # Verify the components are correctly parsed
        component = wm.nodes.get("User Interface")
        self.assertIsNotNone(component)
        self.assertEqual(component.get("type"), "component")

        # Verify multiple pipelines are correctly parsed
        pipeline_names = ["User Interface", "Pipeline Development", "Techniques", "Vector DB", "Embedding", "Compute"]
        for name in pipeline_names:
            pipeline = wm.pipelines.get(name)
            self.assertIsNotNone(pipeline, f"Pipeline {name} should exist")
            self.assertIn("start_evo", pipeline)
            self.assertIn("end_evo", pipeline)
            
        # Verify specific pipeline values
        ui_pipeline = wm.pipelines.get("User Interface")
        self.assertEqual(ui_pipeline.get("start_evo"), 0.5)
        self.assertEqual(ui_pipeline.get("end_evo"), 0.8)
        
        compute_pipeline = wm.pipelines.get("Compute")
        self.assertEqual(compute_pipeline.get("start_evo"), 0.6)
        self.assertEqual(compute_pipeline.get("end_evo"), 0.90)


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

    def test_prompt_engineering_map_a4_landscape(self):
        """
        Test visualization of the comprehensive prompt engineering Wardley Map in A4 landscape format.

        This test loads the prompt_engineering.owm file and generates a PNG visualization
        using A4 landscape format to ensure the package can handle complex, real-world maps 
        with many components, relationships, pipelines, markets, and annotations.
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

        # Save as PNG with A4 landscape format
        output_path = os.path.join(output_dir, "prompt_engineering_map_a4_landscape.png")
        map_plot.savefig(
            output_path,
            dpi=300,
            bbox_inches='tight'
        )

        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        print(f"Saved prompt engineering A4 landscape map to: {output_path}")

        # Verify the map has expected content
        self.assertIsNotNone(wm.title)
        self.assertEqual(wm.title, "Prompt Engineering (Public)")

        # Verify it has components, relationships, and other elements
        self.assertGreater(len(wm.nodes), 50)  # Should have many components
        self.assertGreater(len(wm.edges), 50)  # Should have many relationships
        self.assertGreater(len(wm.pipelines), 5)  # Should have several pipelines
        self.assertGreater(len(wm.notes), 10)  # Should have many notes

    def test_prompt_engineering_map_a3_landscape(self):
        """
        Test visualization of the comprehensive prompt engineering Wardley Map in A3 landscape format.

        This test loads the prompt_engineering.owm file and generates a PNG visualization
        using A3 landscape dimensions (16.54" x 11.69") to provide more space for the
        complex map with many components, relationships, pipelines, markets, and annotations.
        """
        import os

        # Read the prompt engineering map file
        owm_file_path = os.path.join(os.path.dirname(__file__), "prompt_engineering.owm")

        # Verify the file exists
        self.assertTrue(os.path.exists(owm_file_path), f"prompt_engineering.owm not found at {owm_file_path}")

        # Read the map definition
        with open(owm_file_path, 'r', encoding='utf-8') as f:
            map_definition = f.read()

        # Create the map visualization with A3 landscape format
        # A3 landscape: 16.54" x 11.69" (420mm x 297mm)
        wm, map_plot = create_wardley_map_plot(map_definition, figsize=(16.54, 11.69))

        # Verify the map was created successfully
        self.assertIsNotNone(wm)
        self.assertIsNotNone(map_plot)

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "..", "test_output")
        os.makedirs(output_dir, exist_ok=True)

        # Save as PNG with A3 landscape format
        output_path = os.path.join(output_dir, "prompt_engineering_map_a3_landscape.png")
        map_plot.savefig(
            output_path,
            dpi=300,
            bbox_inches='tight'
        )

        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        print(f"Saved prompt engineering A3 landscape map to: {output_path}")

        # Verify the map has expected content
        self.assertIsNotNone(wm.title)
        self.assertEqual(wm.title, "Prompt Engineering (Public)")

        # Verify it has components, relationships, and other elements
        self.assertGreater(len(wm.nodes), 50)  # Should have many components
        self.assertGreater(len(wm.edges), 50)  # Should have many relationships
        self.assertGreater(len(wm.pipelines), 5)  # Should have several pipelines
        self.assertGreater(len(wm.notes), 10)  # Should have many notes

    def test_prompt_engineering_map_linkedin(self):
        """
        Test visualization of the comprehensive prompt engineering Wardley Map in LinkedIn post format.

        This test loads the prompt_engineering.owm file and generates a PNG visualization
        using LinkedIn post dimensions (1200 x 630 pixels) optimized for social media sharing.
        """
        import os

        # Read the prompt engineering map file
        owm_file_path = os.path.join(os.path.dirname(__file__), "prompt_engineering.owm")

        # Verify the file exists
        self.assertTrue(os.path.exists(owm_file_path), f"prompt_engineering.owm not found at {owm_file_path}")

        # Read the map definition
        with open(owm_file_path, 'r', encoding='utf-8') as f:
            map_definition = f.read()

        # Create the map visualization with LinkedIn post format
        # LinkedIn post: 1200 x 630 pixels (aspect ratio ~1.9:1)
        # Convert to inches at 300 DPI: 4" x 2.1"
        wm, map_plot = create_wardley_map_plot(map_definition, figsize=(4.0, 2.1))

        # Verify the map was created successfully
        self.assertIsNotNone(wm)
        self.assertIsNotNone(map_plot)

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "..", "test_output")
        os.makedirs(output_dir, exist_ok=True)

        # Save as PNG with LinkedIn format
        output_path = os.path.join(output_dir, "prompt_engineering_map_linkedin.png")
        map_plot.savefig(
            output_path,
            dpi=300,
            bbox_inches='tight'
        )

        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        print(f"Saved prompt engineering LinkedIn map to: {output_path}")

        # Verify the map has expected content
        self.assertIsNotNone(wm.title)
        self.assertEqual(wm.title, "Prompt Engineering (Public)")

    def test_prompt_engineering_map_twitter(self):
        """
        Test visualization of the comprehensive prompt engineering Wardley Map in Twitter/X post format.

        This test loads the prompt_engineering.owm file and generates a PNG visualization
        using Twitter/X post dimensions (1024 x 512 pixels) optimized for social media sharing.
        """
        import os

        # Read the prompt engineering map file
        owm_file_path = os.path.join(os.path.dirname(__file__), "prompt_engineering.owm")

        # Verify the file exists
        self.assertTrue(os.path.exists(owm_file_path), f"prompt_engineering.owm not found at {owm_file_path}")

        # Read the map definition
        with open(owm_file_path, 'r', encoding='utf-8') as f:
            map_definition = f.read()

        # Create the map visualization with Twitter/X post format
        # Twitter/X post: 1024 x 512 pixels (aspect ratio 2:1)
        # Convert to inches at 300 DPI: 3.41" x 1.71"
        wm, map_plot = create_wardley_map_plot(map_definition, figsize=(3.41, 1.71))

        # Verify the map was created successfully
        self.assertIsNotNone(wm)
        self.assertIsNotNone(map_plot)

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "..", "test_output")
        os.makedirs(output_dir, exist_ok=True)

        # Save as PNG with Twitter/X format
        output_path = os.path.join(output_dir, "prompt_engineering_map_twitter.png")
        map_plot.savefig(
            output_path,
            dpi=300,
            bbox_inches='tight'
        )

        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        print(f"Saved prompt engineering Twitter/X map to: {output_path}")

        # Verify the map has expected content
        self.assertIsNotNone(wm.title)
        self.assertEqual(wm.title, "Prompt Engineering (Public)")

    def test_prompt_engineering_map_a2_landscape(self):
        """
        Test visualization of the comprehensive prompt engineering Wardley Map in A2 landscape format.

        This test loads the prompt_engineering.owm file and generates a PNG visualization
        using A2 landscape dimensions (23.39" x 16.54") to provide maximum space for the
        complex map with many components, relationships, pipelines, markets, and annotations.
        """
        import os

        # Read the prompt engineering map file
        owm_file_path = os.path.join(os.path.dirname(__file__), "prompt_engineering.owm")

        # Verify the file exists
        self.assertTrue(os.path.exists(owm_file_path), f"prompt_engineering.owm not found at {owm_file_path}")

        # Read the map definition
        with open(owm_file_path, 'r', encoding='utf-8') as f:
            map_definition = f.read()

        # Create the map visualization with A2 landscape format
        # A2 landscape: 23.39" x 16.54" (594mm x 420mm)
        wm, map_plot = create_wardley_map_plot(map_definition, figsize=(23.39, 16.54))

        # Verify the map was created successfully
        self.assertIsNotNone(wm)
        self.assertIsNotNone(map_plot)

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "..", "test_output")
        os.makedirs(output_dir, exist_ok=True)

        # Save as PNG with A2 landscape format
        output_path = os.path.join(output_dir, "prompt_engineering_map_a2_landscape.png")
        map_plot.savefig(
            output_path,
            dpi=300,
            bbox_inches='tight'
        )

        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        print(f"Saved prompt engineering A2 landscape map to: {output_path}")

        # Verify the map has expected content
        self.assertIsNotNone(wm.title)
        self.assertEqual(wm.title, "Prompt Engineering (Public)")

        # Verify it has components, relationships, and other elements
        self.assertGreater(len(wm.nodes), 50)  # Should have many components
        self.assertGreater(len(wm.edges), 50)  # Should have many relationships
        self.assertGreater(len(wm.pipelines), 5)  # Should have several pipelines
        self.assertGreater(len(wm.notes), 10)  # Should have many notes

    def test_text_visibility_red_test(self):
        """
        Test text visibility with overlapping components using red text for verification.

        This test creates a map with overlapping components and forces all text to be red
        to verify that component labels appear in front of all visual elements (circles, lines).
        This helps ensure text zorder values are properly set.
        """
        import os
        import matplotlib.pyplot as plt

        # Create test map with overlapping components
        map_definition = """
        title Text Visibility Test
        component Background Component [0.5, 0.5]
        component Overlapping Component [0.52, 0.52]
        component Third Component [0.48, 0.48]
        component Fourth Component [0.49, 0.51]
        Background Component -> Overlapping Component
        Overlapping Component -> Third Component
        Third Component -> Fourth Component
        """

        # Temporarily monkey patch the annotate function to add red color
        original_annotate = plt.Axes.annotate
        def red_annotate(self, *args, **kwargs):
            if 'color' not in kwargs:
                kwargs['color'] = 'red'
            return original_annotate(self, *args, **kwargs)

        plt.Axes.annotate = red_annotate

        try:
            # Create the map visualization
            wm, map_plot = create_wardley_map_plot(map_definition)

            # Verify the map was created successfully
            self.assertIsNotNone(wm)
            self.assertIsNotNone(map_plot)

            # Create output directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(__file__), "..", "test_output")
            os.makedirs(output_dir, exist_ok=True)

            # Save as PNG for visual verification
            output_path = os.path.join(output_dir, "text_visibility_test_red.png")
            map_plot.savefig(
                output_path,
                dpi=300,
                bbox_inches='tight'
            )

            # Verify file was created
            self.assertTrue(os.path.exists(output_path))
            print(f"Saved red text visibility test to: {output_path}")

            # Verify the map has expected content
            self.assertIsNotNone(wm.title)
            self.assertEqual(wm.title, "Text Visibility Test")
            self.assertEqual(len(wm.nodes), 4)  # Should have 4 components
            self.assertEqual(len(wm.edges), 3)  # Should have 3 relationships

        finally:
            # Always restore the original function
            plt.Axes.annotate = original_annotate

    def test_visualisation_annotations_and_notes(self):
        """
        Test the visualization of both annotations and notes in a Wardley Map.

        This method tests the ability of the package to correctly visualize both:
        1. Notes: Simple text annotations at specific coordinates (using 'note' keyword)
        2. Annotations: Numbered annotations with legend positioning (using 'annotation' and 'annotations' keywords)
        
        Both provide additional context, explanations, or insights about the map.
        """

        map_definition = """
        title Map with Annotations and Notes
        component Component A [0.3, 0.4]
        component Component B [0.6, 0.6]
        market Customer Market [0.9, 0.8]
        
        note Example note [0.2, 0.7]
        note Multi-word note text [0.7, 0.3]
        note Short note [0.5, 0.9]
        note Bottom note [0.4, 0.1]
        
        annotations [0.05, 0.95]
        annotation 1,[0.8, 0.2] This is annotation 1 explaining Component A
        annotation 2,[0.65, 0.65] This is annotation 2 about Component B
        annotation 3,[0.85, 0.85] This is annotation 3 describing the market
        
        Component A -> Component B
        Component B -> Customer Market
        """
        wm, map_plot = create_wardley_map_plot(map_definition)

        # Generate SVG and check it was created successfully
        svg_content = create_svg_map(map_plot)
        self.assertIsNotNone(svg_content)
        
        # Verify we have the expected number of notes
        self.assertEqual(len(wm.notes), 4)
        
        # Verify the notes were parsed correctly by checking the note texts
        note_texts = [note.get("text") for note in wm.notes]
        self.assertIn("Example note", note_texts)
        self.assertIn("Multi-word note text", note_texts)
        self.assertIn("Short note", note_texts)
        self.assertIn("Bottom note", note_texts)
        
        # Verify note coordinates for specific notes
        example_note = next((note for note in wm.notes if note.get("text") == "Example note"), None)
        self.assertIsNotNone(example_note)
        self.assertEqual(example_note.get("vis"), 0.2)
        self.assertEqual(example_note.get("evo"), 0.7)
        
        multiword_note = next((note for note in wm.notes if note.get("text") == "Multi-word note text"), None)
        self.assertIsNotNone(multiword_note)
        self.assertEqual(multiword_note.get("vis"), 0.7)
        self.assertEqual(multiword_note.get("evo"), 0.3)
        
        # Verify we have the expected number of annotations
        self.assertEqual(len(wm.annotations), 3)
        
        # Verify annotations legend position
        self.assertIsNotNone(wm.annotation)
        self.assertEqual(wm.annotation.get("vis"), 0.05)
        self.assertEqual(wm.annotation.get("evo"), 0.95)
        
        # Verify the annotations were parsed correctly
        annotation_texts = [ann.get("text") for ann in wm.annotations]
        self.assertIn("This is annotation 1 explaining Component A", annotation_texts)
        self.assertIn("This is annotation 2 about Component B", annotation_texts)
        self.assertIn("This is annotation 3 describing the market", annotation_texts)
        
        # Verify annotation numbers and coordinates
        ann1 = next((ann for ann in wm.annotations if ann.get("number") == 1), None)
        self.assertIsNotNone(ann1)
        self.assertEqual(ann1.get("vis"), 0.8)
        self.assertEqual(ann1.get("evo"), 0.2)
        self.assertEqual(ann1.get("text"), "This is annotation 1 explaining Component A")
        
        ann2 = next((ann for ann in wm.annotations if ann.get("number") == 2), None)
        self.assertIsNotNone(ann2)
        self.assertEqual(ann2.get("vis"), 0.65)
        self.assertEqual(ann2.get("evo"), 0.65)
        self.assertEqual(ann2.get("text"), "This is annotation 2 about Component B")

        # Create output directory and save for visual inspection
        import os
        output_dir = os.path.join(os.path.dirname(__file__), "..", "test_output")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "test_map_annotations_and_notes.png")
        map_plot.savefig(output_path, dpi=300, bbox_inches='tight')
        
        self.assertTrue(os.path.exists(output_path))
        print(f"Saved annotations and notes test map to: {output_path}")


# Allow running the tests from the command line
if __name__ == "__main__":
    unittest.main()
