import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import Image
from typing import Optional, List
import os

def handle_figure_output(fig, output_file=None, return_fig=False, transparent=False):
    """
    Figure handler: save, return, or show.
    """
    if output_file and return_fig:
        raise ValueError("Cannot both save (output_file='myimage') and return the figure (return_fig=True). Choose one.")
    elif output_file:
        save_figure_png(output_file, bbox_inches='tight', transparent=transparent)
        plt.close()
    elif return_fig:
        return fig
    else:
        plt.show()

def save_figure_png(output_file, bbox_inches=None, transparent=False):
    """
    Save the current matplotlib figure as a PNG file.
    """
    # Ensure the extension is .png
    base, _ = os.path.splitext(output_file)
    output_file = f"{base}.png"
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(output_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Save the figure
    plt.savefig(output_file, format="png", dpi=300, bbox_inches=bbox_inches, transparent=transparent)

def get_color_palette(n_classes, palette=None, custom_palette=None):
    """
    Generate a color palette for plotting based on either a ColorBrewer palette or a custom palette file.
    """
    if custom_palette:
        palette_dict = {}
        with open(custom_palette, 'r') as file:
            lines = file.readlines()
            if len(lines) != n_classes:
                raise ValueError(f"Custom palette file has {len(lines)} lines, but {n_classes} classes are required.")
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2:
                    label, color = parts
                    palette_dict[label] = color
                else:
                    raise ValueError("Custom palette provided should have two elements maximum per line.")
        
        # Extract colors from the dictionary
        palette = [palette_dict[label] for label in palette_dict]

    else:
        if palette:
            palette = sns.color_palette(palette, n_colors=n_classes)
        else:
            if n_classes > 20:
                raise ValueError("A maximum of 20 classes is recommended. Use your own palette with custom_palette.")
            palette = sns.color_palette("tab20", n_colors=n_classes)
        palette_dict = None
    
    return palette, palette_dict

def make_dark_mode(fig, ax, legend_style=None, cbar=None, gridlines=None):
    """
    Apply dark mode styling to the given figure and axis.
    """
    dark_gray = '#1F1F1F'
    fig.patch.set_facecolor(dark_gray)
    ax.set_facecolor(dark_gray)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    if gridlines:
        gridlines.xlabel_style = {'color': 'white'}
        gridlines.ylabel_style = {'color': 'white'}
    
    if cbar:
        cbar.ax.xaxis.label.set_color('white')
        cbar.ax.tick_params(axis='x', colors='white')
        cbar.outline.set_edgecolor('white')
    
    legend = ax.get_legend()
    if legend and legend_style == 'default':
        for text in legend.get_texts():
            text.set_color('white')
    
    return fig, ax

def multiple_figs(fig_list: List[Figure], output_file: Optional[str] = None, 
                   ncols: Optional[int] = 2, dpi: Optional[int] = 300, dark_mode: Optional[bool] = False):
    """
    Arrange multiple figures into a single figure.

    Parameters
    ----------
    fig_list : list of matplotlib.Figure
        List of figure and axes pairs to combine into a single image.
    output_file : str, optional
        Path to save the combined image
    ncols : int, optional
        Number of columns in the grid
    dpi : int, optional
        Resolution for the output
    dark_mode : bool, optional
        If True, use dark gray background instead of white
    """
    none_indices = [i for i, fig in enumerate(fig_list) if fig is None]
    if none_indices:
        raise ValueError(f"Figures at indices {none_indices} are None. Please check your figure creation.")

    # Save each figure temporarily
    temp_files = []
    for i, fig in enumerate(fig_list):
        temp_file = f"temp_plot_{i}.png"
        fig.savefig(temp_file, dpi=dpi, bbox_inches='tight', edgecolor='none')
        temp_files.append(temp_file)
    
    # Load images and combine them
    images = [Image.open(tf) for tf in temp_files]
    
    # Calculate dimensions
    nplots = len(images)
    nrows = (nplots + ncols - 1) // ncols
    
    # Get max dimensions for consistent sizing
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # Create combined image with appropriate background color
    combined_width = ncols * max_width
    combined_height = nrows * max_height
    combined_image = Image.new('RGB', (combined_width, combined_height), '#1F1F1F' if dark_mode else 'white')
    
    # Paste individual images
    for idx, img in enumerate(images):
        row = idx // ncols
        col = idx % ncols
        x = col * max_width
        y = row * max_height
        
        # Center the image in its cell
        x_offset = (max_width - img.width) // 2
        y_offset = (max_height - img.height) // 2
        
        combined_image.paste(img, (x + x_offset, y + y_offset))
    
    # Save or show the result
    if output_file:
        combined_image.save(output_file, dpi=(dpi, dpi))
    else:
        combined_image.show()
    
    # Clean up temporary files
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except:
            pass
    
    return combined_image
