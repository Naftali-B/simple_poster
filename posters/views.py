from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
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
    font_path = os.path.join(os.path.dirname(__file__), '../static/assets/fonts/varela_round/VarelaRound-regular.ttf')
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

def generate_poster_two(request, bg_image_url, overlay_img_url, text_color, text1, text2, text3, text4):
    # Fetch the background image from the URL
    response = requests.get(bg_image_url)
    bg_image = Image.open(io.BytesIO(response.content))

    # Fetch the overlay image from the URL
    overlay_response = requests.get(overlay_img_url)
    overlay_image = Image.open(io.BytesIO(overlay_response.content))

    # # Resize overlay image to match background image size
    # overlay_image = overlay_image.resize(bg_image.size)

    # Apply transparency to the overlay image (0.4 to 0.6 transparency)
    transparency = 0.5  # Adjust value between 0.0 (fully transparent) and 1.0 (fully opaque)
    overlay_image = ImageEnhance.Brightness(overlay_image).enhance(transparency)

    # Blend the overlay image with the background image
    blended_image = Image.alpha_composite(bg_image.convert('RGBA'), overlay_image.convert('RGBA'))

    # Load a font
    font_path = os.path.join(os.path.dirname(__file__), '../static/assets/fonts/varela_round/VarelaRound-regular.ttf')
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
    draw = ImageDraw.Draw(blended_image)

    # Define text position and color
    text1_position = (280, 250)
    text2_position = (280, 280)
    text3_position = (280, 310)
    text4_position = (280, 340)

    # Draw text on the image
    draw.text(text1_position, text1, fill=f"#{text_color}", font=font_big)
    draw.text(text2_position, text2, fill=f"#{text_color}", font=font_small)
    draw.text(text3_position, text3, fill=f"#{text_color}", font=font_small)
    draw.text(text4_position, text4, fill=f"#{text_color}", font=font_small)

    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    blended_image.save(buffer, format='PNG')
    buffer.seek(0)

    # Return the image as a response
    return HttpResponse(buffer, content_type='image/png')