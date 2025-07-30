This project is a branch of [term-image](https://pypi.org/project/term-image/) on [QPython](https://www.qpython.org).

## Quick Start

### Creating an instance

1. Initialize with a file path:
   ```python
   from term_image.image import from_file
   
   image = from_file("path/to/image.png")
   ```

2. Initialize with a URL:
   ```python
   from term_image.image import from_url
   
   image = from_url("https://www.example.com/image.png")
   ```

3. Initialize with a PIL (Pillow) image instance:
   ```python
   from PIL import Image
   from term_image.image import AutoImage
   
   img = Image.open("path/to/image.png")
   image = AutoImage(img)
   ```

### Drawing/Displaying an Image

There are two basic ways to draw an image to the terminal screen:

1. Using the `draw()` method:
   ```python
   image.draw()
   ```
   **NOTE:** `draw()` has various parameters for render formatting.

2. Using `print()` with an image render output:
   ```python
   print(image)  # without formatting
   # OR
   print(f"{image:>200.^100#ffffff}")  # with formatting
   ```

For animated images, only the former animates the output, the latter only draws the current frame.

See the [tutorial](https://term-image.readthedocs.io/en/stable/start/tutorial.html) for a more detailed introduction.


## Usage

<p align="center"><b>
   🚧 Under Construction - There will most likely be incompatible changes between minor versions of
   <a href='https://semver.org/spec/v2.0.0.html#spec-item-4'>version zero</a>!
</b></p>

**If you want to use this library in a project while it's still on version zero, ensure you pin the dependency to a specific minor version e.g `>=0.4,<0.5`.**

See the [docs](https://term-image.readthedocs.io) for the User Guide and API Reference.
