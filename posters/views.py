import traceback
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import io
import requests # to fetch the image from the URL
import os

from django.template.loader import render_to_string
from django.conf import settings
import convertapi


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

    if len(title) == 0 and len(description) == 0 and len(date) == 0 and len(time) == 0 and len(venue) == 0:
        return HttpResponse("Fields are required.", status=400)
    
    if len(title) < 10:
        font_size = 15
    elif len(title) > 10 and len(title) < 15:
        font_size = 10
    else:
        font_size = 4


    context = {
        'title': title,
        'description': description,
        'date': date,
        'time': time,
        'venue': venue,

        "font_size": font_size
    }

    request.session['context_data'] = context

    return render(request, 'simple_quick.html' , context)


def generate_poster(request):
    html_file = request.GET.get('file')
    context_data = request.session.get('context_data', {})

    if not html_file or not html_file.startswith('i_divs/') or not html_file.endswith('.html'):
        return HttpResponse("Invalid template file.", status=400)
    else:
        pass

    try:
        rendered_html = render_to_string(html_file, context_data)

        quick_temps_dir = os.path.join(settings.BASE_DIR, 'quick_temps')
        if not os.path.exists(quick_temps_dir):
            os.makedirs(quick_temps_dir)

        # base_name, ext = os.path.splitext(html_file)
        # temp_html_file_name = f"{base_name}_temp{ext}"
        base_name, ext = os.path.splitext(os.path.basename(html_file))
        temp_html_file_name = f"{base_name}_temp{ext}"
        temp_html_path = os.path.join(quick_temps_dir, temp_html_file_name)

        with open(temp_html_path, 'w') as temp_html_file:
            temp_html_file.write(rendered_html)

        convertapi.api_secret = 'FTgSGuFdVbvWNEfF'
        result = convertapi.convert('jpg', {
            'File': temp_html_path
        }, from_format='html').save_files(str(quick_temps_dir))

        # os.remove(temp_html_path) # temp file removal (later)

        # moved to download view
        # file_to_remove = quick_temps_dir / 'quick_temp.jpg'
        # if file_to_remove.exists():
        #     os.remove(file_to_remove)

        try:
            # # :::::::::::::::::::::  DEBUGGING BY OPENING THE HTML FILE   ::::::::::::::::::::

            # # Path to the local HTML file
            # file_path = os.path.join(quick_temps_dir, temp_html_file_name)
            
            # if not os.path.exists(file_path):
            #     return HttpResponse("File not found.", status=404)
            
            # # with open(file_path, 'r', encoding='utf-8') as file:
            # #     file_content = file.read()

            # import chardet
            # # Detect the encoding
            # with open(file_path, 'rb') as rawdata:
            #     result = chardet.detect(rawdata.read(10000))

            # # Read the file with the detected encoding
            # encoding = result['encoding']
            # with open(file_path, 'r', encoding=encoding) as file:
            #     file_content = file.read()

            # return HttpResponse(file_content, content_type='text/html')

            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            # :::::::::::::::: DOWNLOADING THE GENERATED POSTER ::::::::::::::::
            temp_jpg_file_name = f"{base_name}_temp.jpg"
            image_file_path = os.path.join(quick_temps_dir, temp_jpg_file_name)
            if os.path.exists(image_file_path):
                response = FileResponse(open(image_file_path, 'rb'), content_type='image/jpeg')
                response['Content-Disposition'] = 'attachment; filename="my_created_poster.jpg"'
                return response
            else:
                raise Http404("File not found")
        
        except Exception as e:
            print(f"Error generating poster: {traceback.format_exc()}")
            return HttpResponse("Error generating poster", status=500)

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error fetching context data: {e}", status=500)
    except Exception as e:
        print(f"Error generating poster!: {traceback.format_exc()}")
        return HttpResponse("Error generating poster!", status=500)
    
# for use when download button leads to an intermidiate page first,
# example if you are to introduce some fee per download.
def download(request, temp_jpg_file_name):
    quick_temps_dir = os.path.join(settings.BASE_DIR, 'quick_temps')
    file_path = os.path.join(quick_temps_dir, temp_jpg_file_name)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="my_created_poster.jpg"'
        return response
    else:
        raise Http404("File not found")
    
# # Pillow library example (I ditched pillow because I had to manually define elements positions and deadline for this project was fast appoaching)
# def generate_poster(request):
#     bg_image_url = request.GET.get('bg_image_url')
#     overlay_img_url = request.GET.get('overlay_img_url')
#     text_color = request.GET.get('text_color')
#     title = request.GET.get('title')
#     date = request.GET.get('date')
#     time = request.GET.get('time')
#     description = request.GET.get('description')
#     # Replace newline characters with \n
#     # description = description.replace('\n', '\\n')
#     # description = description.replace('\r\n', '\\n').replace('\r', '\\n')
#     venue = request.GET.get('venue')
#     text0 = "                        Smaller text\nwith custom styling"

#     try:
#         response_bg = requests.get(bg_image_url)
#         response_bg.raise_for_status()
#         bg_image = Image.open(io.BytesIO(response_bg.content)).convert('RGBA')

#         response_overlay = requests.get(overlay_img_url)
#         response_overlay.raise_for_status()
#         overlay_image = Image.open(io.BytesIO(response_overlay.content)).convert('RGBA')

#         # overlay_image = overlay_image.resize(bg_image.size) # Resize to match the background without aspect ratio
#         # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.LANCZOS) # BEST QUALITY
#         # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.BICUBIC)
#         # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.HAMMING)
#         overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.BILINEAR) # CHOSEN FOR SPEED/QUALITY BALANCE
#         # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.BOX) # POOR QUALITY
#         # overlay_image = ImageOps.fit(overlay_image, bg_image.size, method=Image.NEAREST) # POOREST QUALITY

#         transparency = 0.9
#         alpha = overlay_image.split()[3]
#         alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
#         overlay_image.putalpha(alpha)

#         # # when not resized... ensuring same mode and size before blending
#         # if bg_image.size != overlay_image.size:
#         #     # handlling mismatched sizes, e.g., by pasting overlay onto bg_image at a certain position
#         #     bg_image.paste(overlay_image, (10, 10), overlay_image)

#         blended_image = Image.alpha_composite(bg_image, overlay_image)

#         font_path = os.path.join(os.path.dirname(__file__), '../static/assets/fonts/varela_round/VarelaRound-regular.ttf')
#         if not os.path.exists(font_path):
#             return HttpResponse("Font file not found.", status=500)

#         font_size_big = 24
#         font_size_small = 18
#         font_big = ImageFont.truetype(font_path, font_size_big)
#         font_small = ImageFont.truetype(font_path, font_size_small)

#         draw = ImageDraw.Draw(blended_image)

#         title_position = (280, 250)
#         date_position = (280, 280)
#         time_position = (280, 300)
#         description_position = (280, 340)
#         venue_position = (280, 380)
#         text0_position = (280, 420)

#         draw.text(title_position, title, fill=f"#{text_color}", font=font_big)
#         draw.text(date_position, date, fill=f"#{text_color}", font=font_small)
#         draw.text(time_position, time, fill=f"#{text_color}", font=font_small)
#         draw.text(description_position, description, fill=f"#{text_color}", font=font_small)
#         draw.text(venue_position, venue, fill=f"#{text_color}", font=font_small)
#         draw.text(text0_position, text0, fill=f"#{text_color}", font=font_small)

#         buffer = io.BytesIO()
#         blended_image.save(buffer, format='PNG')
#         buffer.seek(0)

#         return HttpResponse(buffer, content_type='image/png')

#     except requests.exceptions.RequestException as e:
#         return HttpResponse(f"Error fetching image: {e}", status=500)
#     except Exception as e:
#         print(f"Error generating poster: {traceback.format_exc()}")
#         return HttpResponse("Error generating poster", status=500)


