#!/usr/bin/env python3
"""
Color Palette Extractor
Extracts the dominant colors from an image and generates a color palette.
Outputs the palette as a visual HTML file with hex codes.
"""

from PIL import Image
import sys
from collections import Counter
import colorsys


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def get_dominant_colors(image_path, num_colors=5, quality=1):
    """
    Extract dominant colors from an image.
    
    Args:
        image_path: Path to the image file
        num_colors: Number of dominant colors to extract
        quality: Quality setting (1-10, lower is faster but less accurate)
    
    Returns:
        List of RGB tuples representing dominant colors
    """
    try:
        img = Image.open(image_path)
        
        # Resize image for faster processing
        img = img.resize((150, 150))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get all pixels
        pixels = list(img.getdata())
        
        # Sample pixels based on quality
        pixels = pixels[::quality]
        
        # Count color frequency
        color_counts = Counter(pixels)
        
        # Get most common colors
        dominant_colors = [color for color, count in color_counts.most_common(num_colors)]
        
        return dominant_colors
    
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)


def get_color_name(rgb):
    """Get a descriptive name for the color based on HSV values."""
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    h = h * 360
    
    # Determine color name based on hue
    if s < 0.1:
        if v > 0.9:
            return "White"
        elif v < 0.1:
            return "Black"
        else:
            return "Gray"
    
    if h < 15 or h >= 345:
        return "Red"
    elif h < 45:
        return "Orange"
    elif h < 75:
        return "Yellow"
    elif h < 150:
        return "Green"
    elif h < 210:
        return "Cyan"
    elif h < 270:
        return "Blue"
    elif h < 330:
        return "Magenta"
    else:
        return "Red"


def generate_html_palette(colors, output_file='palette.html'):
    """Generate an HTML file displaying the color palette."""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Color Palette</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        
        .palette {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .color-card {
            display: flex;
            align-items: center;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .color-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }
        
        .color-swatch {
            width: 150px;
            height: 100px;
            flex-shrink: 0;
        }
        
        .color-info {
            padding: 20px;
            flex-grow: 1;
            background: #f8f9fa;
        }
        
        .color-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }
        
        .color-hex {
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .color-rgb {
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #999;
        }
        
        .copy-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            margin-top: 10px;
            transition: background 0.3s ease;
        }
        
        .copy-btn:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Color Palette</h1>
        <div class="palette">
"""
    
    for i, color in enumerate(colors, 1):
        hex_code = rgb_to_hex(color)
        color_name = get_color_name(color)
        
        html_content += f"""
            <div class="color-card">
                <div class="color-swatch" style="background-color: {hex_code};"></div>
                <div class="color-info">
                    <div class="color-name">{color_name} #{i}</div>
                    <div class="color-hex">{hex_code}</div>
                    <div class="color-rgb">RGB({color[0]}, {color[1]}, {color[2]})</div>
                    <button class="copy-btn" onclick="copyToClipboard('{hex_code}')">Copy Hex</button>
                </div>
            </div>
"""
    
    html_content += """
        </div>
    </div>
    
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied ' + text + ' to clipboard!');
            });
        }
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Palette saved to {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python color_palette_extractor.py <image_path> [num_colors]")
        print("Example: python color_palette_extractor.py photo.jpg 5")
        sys.exit(1)
    
    image_path = sys.argv[1]
    num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"🎨 Extracting {num_colors} dominant colors from {image_path}...")
    
    colors = get_dominant_colors(image_path, num_colors)
    
    print("\n📊 Dominant Colors:")
    for i, color in enumerate(colors, 1):
        hex_code = rgb_to_hex(color)
        color_name = get_color_name(color)
        print(f"  {i}. {color_name}: {hex_code} - RGB{color}")
    
    output_file = 'palette.html'
    generate_html_palette(colors, output_file)
    
    print(f"\n🌐 Open {output_file} in your browser to view the palette!")


if __name__ == "__main__":
    main()
