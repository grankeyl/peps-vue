from PIL import Image

import io

def photoBannerCreate(skin_id):
    '''
    New Skin Banner Generate
    '''
    
    background = Image.open("./bot/handlers/media/newSkinNull.png").convert("RGBA")
    overlay = Image.open(f"./../frontend/src/assets/skins/{skin_id}.png").convert("RGBA")

    new_width = 450
    new_height = 450

    bg_width, bg_height = background.size

    overlay = overlay.resize((new_width, new_height), Image.LANCZOS)
    overlay_width, overlay_height = overlay.size

    x = (bg_width - overlay_width) // 2
    y = (bg_height - overlay_height) // 2

    result = Image.new('RGBA', background.size)
    result.paste(background, (0, 0))
    result.paste(overlay, (x, y), overlay)

    byte_stream = io.BytesIO()
    result.save(byte_stream, format="PNG")
    
    byte_stream.seek(0)

    return byte_stream.getvalue()