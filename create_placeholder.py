from PIL import Image, ImageDraw
import os

# Ensure the directory exists
os.makedirs('static/images', exist_ok=True)

# Create a simple placeholder image
img = Image.new('RGB', (400, 300), color=(240, 240, 240))
draw = ImageDraw.Draw(img)

# Add a border
draw.rectangle([(0, 0), (399, 299)], outline=(200, 200, 200))

# Add some text
draw.text((150, 140), "No Image", fill=(100, 100, 100))

# Save the image
img.save('static/images/placeholder.png')
print("Created placeholder image at static/images/placeholder.png")
