"""
Generates a visual representation of a Wardley Map using Matplotlib.

This function takes a Wardley Map object as input and utilises Matplotlib to generate
a visual representation of the map. It supports various styles for the map, such as 'wardley',
'handwritten', 'default', and 'plain', among others available in Matplotlib. The function
configures the plot's appearance, including font, title, axes, and grid lines. It then adds
the Wardley Map components like nodes, edges, annotations, and special features such as
evolve markers and pipeline representations to the plot. The output is a Matplotlib figure
object, which can be displayed in a Jupyter notebook or saved as an image file.

Parameters:
    map (WardleyMap): An instance of the WardleyMap class containing the elements and
    properties of the map to be visualised, including components, relationships, and annotations.

Returns:
    matplotlib.figure.Figure: A Matplotlib figure object representing the Wardley Map. This object
    can be used to display the map within a Jupyter notebook or saved to a file in formats supported
    by Matplotlib, such as PNG or SVG.

Raises:
    ValueError: If an unrecognised style is specified in the WardleyMap object.
    KeyError: If a node referenced in edges, bluelines, evolves, or pipelines is not defined in the map.

Notes:
    The function automatically adjusts the plot settings based on the specified style in the WardleyMap object.
    It supports advanced customisation through the WardleyMap object, allowing users to define specific aspects
        of the map, such as evolution stages, visibility levels, and custom annotations.
    Warnings are generated and appended to the WardleyMap object's warnings attribute for any inconsistencies or
        issues detected during the map generation process, such as missing components or unsupported styles.
"""

import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import copy
from io import BytesIO
from .wardley_maps import WardleyMap


def initialize_plot(figsize=None):
    """
    Initializes a Matplotlib figure and axes tailored for Wardley Map plotting.

    Sets up a figure with specified dimensions and configures the axes with predefined limits suitable for
    Wardley Maps, ensuring a consistent foundation for subsequent plotting. The function also resets Matplotlib's
    configuration to its default settings to avoid unintended styling side effects from previous plots, maintaining
    a clean visual slate for each Wardley Map visualisation.

    Parameters:
        figsize (tuple, optional): The dimensions of the figure in inches, given as a tuple (width, height).
            If None, defaults to A4 landscape dimensions (11.69" x 8.27").

    Returns:
        tuple: A tuple containing:
            - fig (matplotlib.figure.Figure): The Matplotlib figure object.
            - ax (matplotlib.axes.Axes): The axes object.
            - plot_aspect_ratio (float): The calculated height/width aspect ratio of the plot area.
    """
    if figsize is None:
        # A4 landscape dimensions in inches (297mm x 210mm)
        fig_width_inches = 297 / 25.4
        fig_height_inches = 210 / 25.4
        figsize = (fig_width_inches, fig_height_inches)
    else:
        fig_width_inches, fig_height_inches = figsize

    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    fig, ax = plt.subplots(figsize=figsize)

    # Calculate the aspect ratio based on the actual figsize used for the figure
    plot_aspect_ratio = fig_height_inches / fig_width_inches

    ax.set_xlim(0, 1)
    ax.set_ylim(0, plot_aspect_ratio)  # Dynamically set Y-limit based on figure aspect
    ax.set_aspect('equal') # Crucial for making circles round

    return fig, ax, plot_aspect_ratio


def create_wardley_map_plot(wardley_map, figsize=None):
    """
    Generates and visualizes a Wardley Map using Matplotlib, based on the provided WardleyMap object.

    This function interprets the structure and elements defined in a WardleyMap object to create a visual representation
    of the map using Matplotlib. It accommodates various visual styles by leveraging Matplotlib's styling capabilities
    and custom settings to represent nodes, edges, annotations, and other components of a Wardley Map. The function
    ensures the map's elements are accurately positioned and styled according to their respective attributes within
    the WardleyMap object, supporting a range of customization options for personalized map visualization.

    Parameters:
        wardley_map (WardleyMap): An instance of the WardleyMap class, encapsulating the structure, components,
            and configuration of the Wardley Map to be visualized.

    Returns:
        tuple: A tuple containing two elements:
            - wm (WardleyMap): The WardleyMap object, potentially augmented with warnings about any issues encountered during plotting.
            - fig (matplotlib.figure.Figure): The Matplotlib figure object representing the visualized Wardley Map.

    Raises:
        ValueError: If the style specified in the WardleyMap object is unrecognized or unsupported by the function.
        KeyError: If elements referenced in edges, pipelines, or annotations are undefined in the WardleyMap object.

    Notes:
        - The function dynamically adjusts plot settings based on the style attribute of the WardleyMap object,
          enabling a variety of visual themes for the map representation.
        - It is capable of handling advanced customization through the WardleyMap object, allowing for detailed
          specification of evolution stages, visibility levels, and custom annotations.
        - Potential inconsistencies or issues detected during the plotting process, such as missing components or
          unsupported styles, are recorded as warnings in the WardleyMap object for user review.
    """

    CIRCLESIZE = 5

    # Parse the OWM syntax:
    wm = WardleyMap(wardley_map)

    # Initialise the plot and get the dynamic aspect ratio
    fig, ax, plot_aspect_ratio = initialize_plot(figsize) # <--- Correctly capture plot_aspect_ratio

    # Create a temporary scaled copy for rendering without modifying original data
    wm_render = copy.deepcopy(wm)

    # Scale all visibility values in the copy for rendering
    for node_title, node in wm_render.nodes.items():
        node["vis"] = node["vis"] * plot_aspect_ratio

    for note in wm_render.notes:
        note["vis"] = note["vis"] * plot_aspect_ratio

    for annotation in wm_render.annotations:
        annotation["vis"] = annotation["vis"] * plot_aspect_ratio

    if hasattr(wm_render, 'annotation') and wm_render.annotation:
        if "vis" in wm_render.annotation: # Check if 'vis' key exists for safety
            wm_render.annotation["vis"] = wm_render.annotation["vis"] * plot_aspect_ratio

    # Set Matplotlib style based on wm.style
    if wm.style is None:
        wm.style = "wardley"

    if wm.style == "wardley":
        # Use a monospaced font:
        matplotlib.rcParams["font.family"] = "monospace"
        matplotlib.rcParams["font.size"] = 6

        # Add the gradient background
        norm = matplotlib.colors.Normalize(0, 1)
        colors = [[norm(0.0), "white"], [norm(0.5), "white"], [norm(1.0), "#f6f6f6"]]
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)

        # Extent of imshow needs to match the axes limits (0-1 for x, 0-plot_aspect_ratio for y)
        plot_extent = [0, 1, 0, plot_aspect_ratio]
        ax.imshow(
            [[1, 0, 1], [1, 0, 1]],
            cmap=cmap,
            interpolation="bicubic",
            extent=plot_extent,
            aspect="auto", # "auto" lets it fill the current axes dimensions
        )
    elif wm.style in ["handwritten"]:
        matplotlib.rcParams["font.family"] = "Gloria Hallelujah"
    elif wm.style in ["default", "plain"]:
        pass  # Use the figure from initialize_plot()
    elif wm.style in plt.style.available:
        plt.style.use(wm.style)
    elif wm.style is not None:
        wm.warnings.append(f"Map style '{wm.style}' not recognised or supported.")

    # Set up basic properties:
    if wm.title:
        plt.title(wm.title)

    # Plot the lines
    l = []
    for edge in wm_render.edges:
        if edge[0] in wm_render.nodes and edge[1] in wm_render.nodes:
            n_from = wm_render.nodes[edge[0]]
            n_to = wm_render.nodes[edge[1]]
            l.append([(n_from["evo"], n_from["vis"]), (n_to["evo"], n_to["vis"])])
        else:
            for n_edge_comp in edge:
                if n_edge_comp not in wm.nodes: # Use original wm for warning reference
                    wm.warnings.append(f"Could not find component called {n_edge_comp}")
    if len(l) > 0:
        lc = LineCollection(l, color=matplotlib.rcParams["axes.edgecolor"], lw=0.5)
        ax.add_collection(lc)

    # Plot blue lines
    b = []
    for blueline in wm_render.bluelines:
        if blueline[0] in wm_render.nodes and blueline[1] in wm_render.nodes:
            n_from = wm_render.nodes[blueline[0]]
            n_to = wm_render.nodes[blueline[1]]
            b.append([(n_from["evo"], n_from["vis"]), (n_to["evo"], n_to["vis"])])
        else:
            for n_blueline_comp in blueline:
                if n_blueline_comp not in wm.nodes: # Use original wm for warning reference
                    wm.warnings.append(f"Could not find blueline component called {n_blueline_comp}")
    if len(b) > 0:
        lc = LineCollection(b, color="blue", lw=1)
        ax.add_collection(lc)

    # Plot Evolve
    e = []
    for evolve_title, evolve in wm_render.evolves.items():
        if evolve_title in wm_render.nodes:
            n_from = wm_render.nodes[evolve_title]
            e.append([(n_from["evo"], n_from["vis"]), (evolve["evo"], n_from["vis"])])
        else:
            wm.warnings.append(
                f"Could not find evolve component called {evolve_title}"
            )
    if len(e) > 0:
        lc = LineCollection(e, color="red", lw=0.5, linestyles="dotted")
        ax.add_collection(lc)

    for node_title, n in wm_render.nodes.items():
        if n["type"] == "market":
            # Implement market symbol exactly like the original React component

            # Market symbol with proper geometric proportions
            OUTER_RADIUS = 0.012  # Outer circle radius
            INNER_RADIUS = OUTER_RADIUS / 3.6  # Inner circle radius with proper proportion

            # Distance from center to inner circle centers (circumradius of equilateral triangle)
            distance_centers = INNER_RADIUS * 1.8

            # Calculate positions of three inner circles forming equilateral triangle
            # Angles: top (90°), bottom-left (210°), bottom-right (330° / -30°)
            angles_deg = [90, 210, 330]
            inner_centers = []

            for angle_deg in angles_deg:
                angle_rad = np.deg2rad(angle_deg)
                x = n["evo"] + distance_centers * np.cos(angle_rad)
                y = n["vis"] + distance_centers * np.sin(angle_rad)
                inner_centers.append((x, y))

            # 1. Draw outer circle first
            outer_circle = patches.Circle(
                (n["evo"], n["vis"]),
                radius=OUTER_RADIUS,
                fill=True,
                facecolor='white',
                edgecolor='black',
                linewidth=1.0,
                zorder=3
            )
            ax.add_patch(outer_circle)

            # 2. Draw connecting lines between inner circle centers (triangle)
            for i in range(3):
                start_center = inner_centers[i]
                end_center = inner_centers[(i + 1) % 3]  # Loop back to first for last line
                ax.plot(
                    [start_center[0], end_center[0]],
                    [start_center[1], end_center[1]],
                    color='black',
                    linewidth=1.5,
                    zorder=4
                )

            # 3. Draw the three inner circles
            for center in inner_centers:
                inner_circle = patches.Circle(
                    center,
                    radius=INNER_RADIUS,
                    fill=True,
                    facecolor='white',
                    edgecolor='black',
                    linewidth=1.3,
                    zorder=5
                )
                ax.add_patch(inner_circle)

            # Add label outside the market symbol - up and to the right
            # Position label to the upper right of the outer circle
            label_offset_x = OUTER_RADIUS * 1.7 * 1000  # Convert to pixels (approximate)
            label_offset_y = OUTER_RADIUS * 1.7 * 1000  # Convert to pixels (approximate)
            ax.annotate(
                node_title,
                fontsize=matplotlib.rcParams["font.size"],
                fontfamily=matplotlib.rcParams["font.family"],
                xy=(n["evo"], n["vis"]),
                xycoords="data",
                xytext=(label_offset_x, label_offset_y),  # Offset to the upper right of circle
                textcoords="offset pixels",
                horizontalalignment="left",
                verticalalignment="bottom",
                zorder=20
            )

        elif n["type"] == "component":
            plt.plot(
                n["evo"],  # Evolution (previously "mat")
                n["vis"],
                marker="o",
                color="green",
                markeredgecolor="green",
                markersize=CIRCLESIZE,
                lw=1,
            )

            # Add inertia symbol if component has inertia
            if n.get("inertia", False):
                # Add vertical line (wall) slightly to the right of component's position
                offset = 0.03
                height = 0.008
                plt.plot(
                    [n["evo"] + offset, n["evo"] + offset],  # Same x for vertical line, with offset
                    [n["vis"] - height, n["vis"] + height],  # Shorter vertical extension
                    color="black",
                    linewidth=3,  # Thick line
                    solid_capstyle="butt"  # Flat ends
                )
            # Add label with default offset
            ax.annotate(
                node_title,
                fontsize=matplotlib.rcParams["font.size"],
                fontfamily=matplotlib.rcParams["font.family"],
                xy=(n["evo"], n["vis"]),
                xycoords="data",
                xytext=(10, 10),  # Default offset: 10 right, 10 above
                textcoords="offset pixels",
                horizontalalignment="left",
                verticalalignment="bottom",
                zorder=20
            )

    # Add the anchors:
    for node_title, n in wm_render.nodes.items():
        if n["type"] == "anchor":
            plt.plot(
                n["evo"],  # Evolution (previously "mat")
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor="blue",
                markersize=CIRCLESIZE,
                lw=1,
            )
            # Add label with default offset
            ax.annotate(
                node_title,
                fontsize=matplotlib.rcParams["font.size"],
                fontfamily=matplotlib.rcParams["font.family"],
                xy=(n["evo"], n["vis"]),
                xycoords="data",
                xytext=(10, 10),  # Default offset: 10 right, 10 above
                textcoords="offset pixels",
                horizontalalignment="left",
                verticalalignment="bottom",
                zorder=20
            )

    # Add the evolve nodes:
    for evolve_title, evolve in wm_render.evolves.items():
        if evolve_title in wm_render.nodes:
            n = wm_render.nodes[evolve_title]
            plt.plot(
                evolve["evo"],  # Evolution (previously "mat")
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor="red",
                markersize=CIRCLESIZE,
                lw=1,
            )
            # Add label with default offset
            ax.annotate(
                evolve_title,
                fontsize=matplotlib.rcParams["font.size"],
                fontfamily=matplotlib.rcParams["font.family"],
                xy=(evolve["evo"], n["vis"]),
                xycoords="data",
                xytext=(10, 10),  # Default offset: 10 right, 10 above
                textcoords="offset pixels",
                horizontalalignment="left",
                verticalalignment="bottom",
                zorder=20
            )
        else:
            wm.warnings.append(f"Node '{evolve_title}' does not exist in the map.")

    # Add the pipeline nodes:
    for pipeline_title, _pipeline in wm_render.pipelines.items():
        if pipeline_title in wm_render.nodes:
            n = wm_render.nodes[pipeline_title] # Get the node data for the pipeline component

            # Plot the square marker at the pipeline component's position
            plt.plot(
                n["evo"],  # Evolution (x-coordinate)
                n["vis"],  # Visibility (y-coordinate)
                marker="s", # Square marker
                color='white', # White fill
                markeredgecolor='black', # Black edge
                markersize=CIRCLESIZE, # Use CIRCLESIZE for consistency, adjust if needed
                lw=1, # Line width for the marker edge
                zorder=6 # Ensure it's on top of the rectangle and lines
            )
        else:
            wm.warnings.append(f"Node '{pipeline_title}' does not exist in the map.")

    # Plot Pipelines (the rectangle and end circle)
    for pipeline_title, pipeline in wm_render.pipelines.items():
        if pipeline_title in wm_render.nodes:
            n_from = wm_render.nodes[pipeline_title]

            # Plot the horizontal rectangle representing the pipeline
            rectangle = patches.Rectangle(
                (pipeline["start_evo"], n_from["vis"] - 0.02),
                pipeline["end_evo"] - pipeline["start_evo"],
                0.02,
                fill=False,
                lw=0.5,
            )
            ax.add_patch(rectangle)

            # Add circle at the beginning of the pipeline (inside the box)
            circle_start_radius = 0.004  # Smaller to fit inside
            circle_start = patches.Circle(
                (pipeline["start_evo"] + 0.01, n_from["vis"] - 0.01),  # Offset inward and center vertically
                radius=circle_start_radius,
                fill=True,
                facecolor='white',
                edgecolor='black',
                linewidth=1.0,
                zorder=7
            )
            ax.add_patch(circle_start)

            # Add horizontal dotted line from start circle to end circle with arrow
            ax.annotate('',
                       xy=(pipeline["end_evo"] - 0.015, n_from["vis"] - 0.01),  # End point (arrow tip, shorter)
                       xytext=(pipeline["start_evo"] + 0.015, n_from["vis"] - 0.01),  # Start point (after first circle)
                       arrowprops=dict(arrowstyle='->',
                                     linestyle=':',
                                     color='black',
                                     linewidth=0.5),
                       zorder=5)

            # Add the circle marker at the end of the pipeline (inside the box)
            circle_end_radius = 0.004  # Smaller to fit inside
            circle_end = patches.Circle(
                (pipeline["end_evo"] - 0.01, n_from["vis"] - 0.01),  # Offset inward and center vertically
                radius=circle_end_radius,
                fill=True,
                facecolor='white',
                edgecolor='black',
                linewidth=1.0,
                zorder=7
            )
            ax.add_patch(circle_end)

        else:
            wm.warnings.append(
                f"Could not find pipeline component called {pipeline_title}"
            )

    # Add the notes:
    for note in wm_render.notes:
        plt.text(
            note["evo"],  # Evolution (previously "mat")
            note["vis"],
            note["text"],
            fontsize=matplotlib.rcParams["font.size"],
            fontfamily=matplotlib.rcParams["font.family"],
            fontweight='bold',
            fontname='monospace',
            zorder=20
        )

    # Add annotation markers:
    for annotation in wm_render.annotations:
        # Draw numbered marker at annotation position
        circle = plt.Circle(
            (annotation["evo"], annotation["vis"]),
            radius=0.008,  # Small circle
            color='blue',
            zorder=10
        )
        ax.add_patch(circle)

        # Add number text centered on circle
        plt.text(
            annotation["evo"],
            annotation["vis"],
            str(annotation["number"]),
            fontsize=6,
            fontweight='bold',
            color='white',
            horizontalalignment='center',
            verticalalignment='center',
            zorder=21
        )

    # Add annotation legend if position is specified:
    if hasattr(wm_render, 'annotation') and wm_render.annotation:
        legend_x = wm_render.annotation["evo"]
        legend_y = wm_render.annotation["vis"]

        # Create legend text
        legend_lines = []
        for annotation in sorted(wm_render.annotations, key=lambda x: x["number"]):
            legend_lines.append(f"{annotation['number']}: {annotation['text']}")

        if legend_lines:
            legend_text = "\n".join(legend_lines)
            plt.text(
                legend_x,
                legend_y,
                legend_text,
                fontsize=5,
                fontfamily=matplotlib.rcParams["font.family"],
                verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8),
                zorder=22
            )

    # Scale the yticks to match the plot_aspect_ratio
    # The original "Visible" position was 0.925 on a 0-1 scale. Scale it to the new Y-axis max.
    visible_tick_position = 0.925 * plot_aspect_ratio

    plt.yticks(
        [0.0, visible_tick_position], ["Invisible", "Visible"], rotation=90, verticalalignment="bottom"
    )
    plt.ylabel("Visibility", fontweight="bold")
    plt.xticks(
        [0.0, 0.17, 0.4, 0.70],
        ["Genesis", "Custom-Built", "Product\n(+rental)", "Commodity\n(+utility)"],
        ha="left",
    )
    plt.xlabel("Evolution", fontweight="bold")

    plt.tick_params(axis="x", direction="in", top=True, bottom=True, grid_linewidth=1)
    plt.grid(visible=True, axis="x", linestyle="--")
    plt.tick_params(axis="y", length=0)

    wm.warnings = list(set(wm.warnings))

    return wm, fig
