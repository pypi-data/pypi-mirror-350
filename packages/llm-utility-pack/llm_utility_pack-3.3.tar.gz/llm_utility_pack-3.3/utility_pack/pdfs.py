from utility_pack.ocr_util import is_photo, ocr_page
import fitz, uuid, os, io
from enum import Enum
from PIL import Image

def perform_caption(img: Image):
    return "Dummy Caption"

def subtitle_images_from_pdf(pdf_path: str, caption_fn) -> str:
    """
    Extracts images from each page of a PDF, obtains captions via caption_fn(image),
    and inserts them as invisible text below each image.

    "caption_fn" should be a function that takes a Pillow Image and returns the caption as string.
    """
    pdf = fitz.open(pdf_path)
    for page_index, page in enumerate(pdf):
        infos = page.get_image_info()
        imgs  = page.get_images(full=True)
        for idx, info in enumerate(infos, start=1):
            bbox = fitz.Rect(info['bbox'])
            # Find matching xref by bbox containment
            xref = None
            for img in imgs:
                for rect in page.get_image_rects(img):
                    if rect.contains(bbox):
                        xref = img[0]
                        break
                if xref:
                    break
            if not xref:
                continue
            try:
                data = pdf.extract_image(xref)["image"]
                if not data:
                    continue
                img = Image.open(io.BytesIO(data))
                if img.mode != "RGB":
                    img = img.convert("RGB")
                try:
                    caption = caption_fn(img)
                except Exception:
                    caption = ""
                # Calculate textbox
                y0 = bbox.y1 + 5
                y1 = min(page.rect.y1 - 5, y0 + 30)
                rect = fitz.Rect(bbox.x0, y0, bbox.x1, y1)
                page.insert_textbox(rect, caption,
                                    fontsize=11,
                                    fontname="helv",
                                    render_mode=3)
            except Exception:
                continue

    out_path = f"/tmp/modified_{uuid.uuid4().hex}_{os.path.basename(pdf_path)}"
    pdf.save(out_path)
    pdf.close()
    return out_path

def get_pdf_page_as_image(pdf_path, page_num, zoom_factor=3.5):
    # 1 - Read PDF
    pdf_document = fitz.open(pdf_path)

    # 2 - Convert page to image
    page = pdf_document.load_page(page_num)

    # Define the zoom factor for the image resolution. Higher values mean more pixels.
    mat = fitz.Matrix(zoom_factor, zoom_factor)

    # Render the page to an image (pixmap)
    pix_image = page.get_pixmap(matrix=mat)

    return pix_image

class OcrStrategy(str, Enum):
    Always = "always"
    Never = "never"
    Auto = "auto"

def pdf_to_text(filepath, strategy_ocr: OcrStrategy, zoom_factor=3.5):
    pdf_document = fitz.open(filepath)

    page_texts = []

    for page_number in range(pdf_document.page_count):
        print(f'Processando página {page_number + 1}', flush=True)

        page = pdf_document.load_page(page_number)
        page_text = page.get_text("text")

        if strategy_ocr == OcrStrategy.Never:
            pass
        elif strategy_ocr == OcrStrategy.Always:
            pix_image = get_pdf_page_as_image(filepath, page_number, zoom_factor)
            page_text = ocr_page(pix_image)
        else:
            pix_image = get_pdf_page_as_image(filepath, page_number, zoom_factor)
            if len(page_text.split(' ')) < 10 or is_photo(pix_image) or strategy_ocr == OcrStrategy.Always:
                page_text = ocr_page(pix_image)

        while '\n\n' in page_text:
            page_text = page_text.replace('\n\n', '\n')

        page_texts.append(page_text)

    return {
        "full_text": "\n".join(page_texts),
        "text_per_page": [{
            "page": idx + 1,
            "text": text
        } for idx, text in enumerate(page_texts)]
    }
