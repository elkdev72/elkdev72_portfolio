from cairosvg import svg2png
from PIL import Image
import io

# Read the SVG file
with open('main/static/main/images/favicon.svg', 'rb') as svg_file:
    svg_data = svg_file.read()

# Convert SVG to PNG in memory
png_data = svg2png(bytestring=svg_data, output_width=256, output_height=256)

# Create PIL Image from PNG data
img = Image.open(io.BytesIO(png_data))

# Convert to ICO and save
img.save('main/static/main/images/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (256, 256)]) 