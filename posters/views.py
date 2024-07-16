import traceback
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
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

def generate_poster_two(request):
    bg_image_url = request.GET.get('bg_image_url')
    overlay_img_url = request.GET.get('overlay_img_url')
    text_color = request.GET.get('text_color')
    text1 = request.GET.get('text1')
    text2 = request.GET.get('text2')
    text3 = request.GET.get('text3')
    text4 = request.GET.get('text4')
    text = "                        Smaller text\nwith custom styling"

    try:
        response_bg = requests.get(bg_image_url)
        response_bg.raise_for_status()
        bg_image = Image.open(io.BytesIO(response_bg.content)).convert('RGBA')

        response_overlay = requests.get(overlay_img_url)
        response_overlay.raise_for_status()
        overlay_image = Image.open(io.BytesIO(response_overlay.content)).convert('RGBA')

        # overlay_image = overlay_image.resize(bg_image.size) # Resize to match the background without aspect ratio
        # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.LANCZOS) # BEST QUALITY
        # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.BICUBIC)
        # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.HAMMING)
        overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.BILINEAR) # CHOSEN FOR SPEED/QUALITY BALANCE
        # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.BOX) # POOR QUALITY
        # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.NEAREST) # POOREST QUALITY

        transparency = 0.9
        alpha = overlay_image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
        overlay_image.putalpha(alpha)

        # # when not resized... ensuring same mode and size before blending
        # if bg_image.size != overlay_image.size:
        #     # handlling mismatched sizes, e.g., by pasting overlay onto bg_image at a certain position
        #     bg_image.paste(overlay_image, (10, 10), overlay_image)

        blended_image = Image.alpha_composite(bg_image, overlay_image)

        font_path = os.path.join(os.path.dirname(__file__), '../static/assets/fonts/varela_round/VarelaRound-regular.ttf')
        if not os.path.exists(font_path):
            return HttpResponse("Font file not found.", status=500)

        font_size_big = 24
        font_size_small = 18
        font_big = ImageFont.truetype(font_path, font_size_big)
        font_small = ImageFont.truetype(font_path, font_size_small)

        draw = ImageDraw.Draw(blended_image)

        text1_position = (280, 250)
        text2_position = (280, 280)
        text3_position = (280, 310)
        text4_position = (280, 340)
        text_position = (280, 380)

        draw.text(text1_position, text1, fill=f"#{text_color}", font=font_big)
        draw.text(text2_position, text2, fill=f"#{text_color}", font=font_small)
        draw.text(text3_position, text3, fill=f"#{text_color}", font=font_small)
        draw.text(text4_position, text4, fill=f"#{text_color}", font=font_small)
        draw.text(text_position, text, fill=f"#{text_color}", font=font_small)

        buffer = io.BytesIO()
        blended_image.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error fetching image: {e}", status=500)
    except Exception as e:
        print(f"Error generating poster: {traceback.format_exc()}")
        return HttpResponse("Error generating poster", status=500)