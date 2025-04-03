from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image():
    # Create directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Create a placeholder image
    img = Image.new('RGB', (400, 300), color=(240, 240, 240))
    d = ImageDraw.Draw(img)
    
    # Try to use a font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # Add text
    d.text((150, 150), "No Image", fill=(100, 100, 100), font=font)
    
    # Save the image
    img.save('static/images/placeholder.png')
    print("Placeholder image created at static/images/placeholder.png")

if __name__ == "__main__":
    create_placeholder_image()
