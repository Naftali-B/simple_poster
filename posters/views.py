import traceback
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import io
import requests # to fetch the image from the URL
import os


def quick_create(request):
    return render(request, 'quick_create.html')

def details(request):
    return render(request, 'details.html')


def simple_quick(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    date = request.POST.get('date')
    time = request.POST.get('time')
    venue = request.POST.get('venue')

    context = {
        'title': title,
        'description': description,
        'date': date,
        'time': time,
        'venue': venue
    }
    return render(request, 'simple_quick.html' , context)


def generate_poster(request):
    bg_image_url = request.GET.get('bg_image_url')
    overlay_img_url = request.GET.get('overlay_img_url')
    text_color = request.GET.get('text_color')
    title = request.GET.get('title')
    date = request.GET.get('date')
    time = request.GET.get('time')
    description = request.GET.get('description')
    venue = request.GET.get('venue')
    text0 = "                        Smaller text\nwith custom styling"

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

        title_position = (280, 250)
        date_position = (280, 280)
        time_position = (280, 300)
        description_position = (280, 340)
        venue_position = (280, 380)
        text0_position = (280, 420)

        draw.text(title_position, title, fill=f"#{text_color}", font=font_big)
        draw.text(date_position, date, fill=f"#{text_color}", font=font_small)
        draw.text(time_position, time, fill=f"#{text_color}", font=font_small)
        draw.text(description_position, description, fill=f"#{text_color}", font=font_small)
        draw.text(venue_position, venue, fill=f"#{text_color}", font=font_small)
        draw.text(text0_position, text0, fill=f"#{text_color}", font=font_small)

        buffer = io.BytesIO()
        blended_image.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error fetching image: {e}", status=500)
    except Exception as e:
        print(f"Error generating poster: {traceback.format_exc()}")
        return HttpResponse("Error generating poster", status=500)