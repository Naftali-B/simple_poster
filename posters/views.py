from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import io
import requests # to fetch the image from the URL
import os


def quick_create(request):
    return render(request, 'quick_create.html')

def simple_quick(request):
    return render(request, 'simple_quick.html')


def generate_poster(request, bg_image_url, text_color, text1, text2, text3, text4):
    # generate_poster(request, bg_color, text_color, text1, text2, text3):
    # Create an image with the specified background color
    # image = Image.new('RGB', (300, 400), color=f"#{bg_color}")

    # Fetch the background image from the URL
    response = requests.get(bg_image_url)
    bg_image = Image.open(io.BytesIO(response.content))

    # Resize the background image to the desired size if necessary
    # bg_image = bg_image.resize((300, 400))


    # Load a font
    font_path = os.path.join(os.path.dirname(__file__), '../staticfiles/assets/fonts/varela_round/VarelaRound-regular.ttf')
    if not os.path.exists(font_path):
        return HttpResponse("Font file not found.", status=500)
    
    try:
        font_size_big = 24
        font_size_small = 18
        font_big = ImageFont.truetype(font_path, font_size_big)
        font_small = ImageFont.truetype(font_path, font_size_small)
    except IOError:
        return HttpResponse("Cannot load font file.", status=500)

    # Initialize ImageDraw
    # draw = ImageDraw.Draw(image)

    draw = ImageDraw.Draw(bg_image)

    # Define text position and color
    text1_position = (280, 250)
    text2_position = (280, 280)
    text3_position = (280, 310)
    text4_position = (280, 340)

    # Draw text on the image
    # draw.text(text1_position, text1, fill=f"#{text_color}", font=font)
    # draw.text(text2_position, text2, fill=f"#{text_color}", font=font)
    # draw.text(text3_position, text3, fill=f"#{text_color}", font=font)

    draw.text(text1_position, text1, fill=f"#{text_color}", font=font_big)
    draw.text(text2_position, text2, fill=f"#{text_color}", font=font_small)
    draw.text(text3_position, text3, fill=f"#{text_color}", font=font_small)
    draw.text(text4_position, text4, fill=f"#{text_color}", font=font_small)

    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    # image.save(buffer, format='PNG')
    bg_image.save(buffer, format='PNG')
    buffer.seek(0)

    # Return the image as a response
    return HttpResponse(buffer, content_type='image/png')