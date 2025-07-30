#!python
from dataclasses import dataclass, field
from wowool.sdk import Pipeline
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from PIL import Image  # optional, for getting image dimensions

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTCollection
from pathlib import Path
from wowool.io.pdf.pdfcore import extract_results, ParseOptions
from wowool.io.pdf.objects import (
    TextBlock,
    TextBlockGroup,
    RectGroup,
    ImageBlock,
    FigureGroup,
    VisualLineSeparator,
)
from wowool.sdk import Pipeline
import traceback
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
from collections import OrderedDict
from pdfminer.layout import (
    LTTextLineVertical,
)
from wowool.io.pdf.pdfcore import is_text_bold
from wowool.document import DocumentInterface
from wowool.sdk import Pipeline
from wowool.anonymizer.core.anonymizer import Anonymizer, DefaultWriter
from sys import stderr
from pathlib import Path
from wowool.tools.anonymizer.writer_config import WriterConfig
from wowool.anonymizer.core.defines import (
    KW_URI,
    KW_ANONYMIZED,
    KW_TEXT,
    KW_BEGIN_OFFSET,
    KW_END_OFFSET,
    KW_BYTE_BEGIN_OFFSET,
    KW_BYTE_END_OFFSET,
)


# c.linkURL("https://www.example.com", (100, 700, 100, 15), relative=1)

split_font_name_pattern = re.compile(r"[,\- ]")


font_rename_map = OrderedDict(
    {
        "timesnewromanpsmt": "timesnewroman",
        "timesnewromanps-boldmt": "timesnewromanbold",
        "timesnewromanpsboldmt": "timesnewromanbold",
        "timesnewromanps-italicmt": "timesnewromanitalic",
        "timesnewromanps-bolditalicmt": "timesnewromanbolditalic",
        "helveticaneue": "helvetica",
        "helveticaneue-bold": "helvetica-bold",
    }
)
reverse_font_rename_map = OrderedDict({"ebgaramond": "garamond"})

font_locations = [
    "/System/Library/Fonts/Supplemental",
    "/System/Library/Fonts/",
    "~/Library/Fonts/",
]
font_locations = [Path(loc).expanduser() for loc in font_locations]
already_registered_fonts = set(pdfmetrics.getRegisteredFontNames())

pdf_font_mapping = OrderedDict()


def clean_font_name(fontname):
    """
    Cleans the font name by removing unwanted characters.
    """
    # Remove unwanted characters and split the font name
    font_parts = split_font_name_pattern.split(fontname)
    # Join the cleaned parts back together
    cleaned_fontname = "".join(font_parts)
    return cleaned_fontname


@dataclass
class FontInfoObject:
    filename: Path
    font_type: str = "ttf"
    ttc_font: TTFont | None = None


def load_fonts_mapping_table(locations: list[Path]):
    font_folder = Path("fonts").absolute()
    font_folder.mkdir(exist_ok=True)
    for folder in locations:
        for fn in Path(folder).glob("**/*.tt[fc]"):

            if fn.suffix == ".ttc":
                ttc = TTCollection(fn)
                for ttc_font in ttc:
                    # Try to get a meaningful name from the font
                    try:
                        font_name = ttc_font["name"].getDebugName(4)
                    except:
                        # Fallback to a generic name with index
                        continue
                    fontname = clean_font_name(font_name.lower())
                    # Create output path
                    output_path = font_folder / f"{font_name}.ttf"
                    pdf_font_mapping[fontname] = FontInfoObject(
                        font_type="ttc", filename=output_path, ttc_font=ttc_font
                    )
            else:
                fontname = fn.stem.lower()

                fparts = fontname.split("-")
                if len(fparts) == 2:
                    fparts[0] = reverse_font_rename_map.get(fparts[0], fparts[0])
                    fontname = "-".join(fparts)
                    if fparts[1] == "regular":
                        pdf_font_mapping[fparts[0]] = FontInfoObject(filename=fn)
                fontname = reverse_font_rename_map.get(fontname, fontname)
                fontname = clean_font_name(fontname)
                pdf_font_mapping[fontname] = FontInfoObject(filename=fn)


load_fonts_mapping_table(font_locations)

# for font in pdf_font_mapping.items():
#     print(font[0], font[1].stem)

# print("--------------------")


# clean_font_name_pattern = re.compile(r"^(*.)ms$")


def check_image_rotation(block):
    try:
        img = Image.open(block.filename)

        # Check for EXIF rotation data
        if hasattr(img, "_getexif") and img._getexif():
            exif = dict(img._getexif().items())
            orientation = exif.get(274, 1)  # 274 is the orientation tag
            if orientation != 1:
                return True, orientation

        # Check aspect ratio against block dimensions
        img_ratio = img.width / img.height
        block_ratio = (block.x1 - block.x0) / (block.y0 - block.y1)

        # If ratios differ significantly, image may be rotated
        if abs(img_ratio - block_ratio) > 0.1:
            return True, "aspect_ratio_mismatch"

        return False, None
    except Exception as e:
        print(f"Error checking image rotation: {e}")
        return False, None


def check_and_register_fonts(locations: list[Path], name):
    """
    Register fonts from a given folder.
    """

    # if name.startswith("timesnewroman"):
    #     print("Garamond bold")

    fontname = font_rename_map.get(name, name)
    if fontname in already_registered_fonts:
        return fontname

    if fontname in pdf_font_mapping:
        font_info = pdf_font_mapping[fontname]
        if font_info.font_type == "ttc":
            # Register the font from the TTC collection
            if not font_info.filename.exists():
                font_info.ttc_font.save(font_info.filename)
            pdfmetrics.registerFont(TTFont(fontname, font_info.filename))
        else:
            pdfmetrics.registerFont(
                TTFont(fontname, pdf_font_mapping[fontname].filename)
            )
        already_registered_fonts.add(fontname)

    return fontname


def is_url_link(text):
    if (
        text.startswith("www")
        or text.startswith("http://")
        or text.startswith("https://")
    ):
        return True


class PDFWriter:
    def __init__(self, filename, pagesize):
        self.filename = filename
        self.canvas = canvas.Canvas(filename, pagesize=A4)
        self.pagesize = pagesize
        self.text = ""
        self.font_name = "Helvetica"
        self.font_size = 12

    def draw_text(self, block):
        fontname_parts = block.fontname.split("+")
        if len(fontname_parts) > 1:
            fontname = fontname_parts[1].lower()
        else:
            fontname = block.fontname.lower()
        # print(f"fontname: {fontname}")
        try:
            fontname = clean_font_name(fontname)
            fontname = check_and_register_fonts(locations=font_locations, name=fontname)
            self.font_size = block.obj.height
            self.canvas.setFont(fontname, block.obj.height)
            self.font_name = fontname
        except Exception as e:
            print(
                f"Warning: could not set font {fontname}: {e}, {self.font_name},{self.font_size} {block.text}"
            )
            self.canvas.setFont(self.font_name, self.font_size)
            # self.canvas.setFont("OpenSans", block.obj.height)

        if isinstance(block.obj, LTTextLineVertical) and block.vertical:
            # Save the current graphics state
            self.canvas.saveState()

            # Move to the point where text should be positioned
            self.canvas.translate(block.x0, block.y1)

            # Rotate the canvas (90 degrees for true vertical)
            self.canvas.rotate(90)

            # Set font properties
            self.font_size = block.x1 - block.x0
            self.canvas.setFont(self.font_name, self.font_size)

            # Draw at origin (0,0) since we've already translated to the desired position
            self.canvas.drawString(0, 0, block.text)

            # Restore to the saved state (undoes rotation and translation)
            self.canvas.restoreState()
        else:
            # if "1. det är" in block.text:
            #     self.canvas.setFillColorRGB(1, 0, 0)
            #     self.canvas.setStrokeColorRGB(1, 0, 0)
            # else:
            #     self.canvas.setFillColorRGB(0, 0, 0)
            #     self.canvas.setStrokeColorRGB(0, 0, 0)
            if isinstance(block.obj, LTTextLineVertical):
                # print(f"Vertical text: {block.text}")
                self.canvas.setFont(self.font_name, block.obj._objs[0].height)

            if is_url_link(block.text):
                self.canvas.saveState()
                self.canvas.setStrokeColorRGB(1, 0, 2)
                self.canvas.drawString(block.x0, block.yl, block.text)
                self.canvas.restoreState()
            else:
                self.canvas.drawString(block.x0, block.yl, block.text)

            # if is_url_link(block.text):
            #     # print(f"WWW: {block.obj._objs[0]}")
            #     from reportlab.lib.colors import blue, Color

            #     custom_color = Color(0.8, 0.1, 0.3)  # pinkish red

            # self.canvas.linkURL(
            #     block.text,
            #     (block.x0, block.y1, block.x1, block.y0),
            #     relative=1,
            #     color=custom_color,
            #     thickness=1,
            # )

    def draw_blocks(self, blocks):
        for block in blocks:
            if isinstance(block, TextBlock):
                # print(f"Block: {block}")
                self.draw_text(block)
                self.text += block.text
            elif isinstance(block, TextBlockGroup):
                # print(f"Block: {block}")
                self.draw_blocks(block.text_blocks)
            elif isinstance(block, RectGroup):
                # print(f"Block: {block}")
                self.draw_blocks(block.text_blocks)
            elif isinstance(block, FigureGroup):
                self.draw_blocks(block.text_blocks)
            elif isinstance(block, ImageBlock):
                self.draw_image(block)
            elif isinstance(block, VisualLineSeparator):
            else:
                print(f"Unknown block type: {type(block)}")

    def draw_images(self, blocks):
        for block in blocks:
            if isinstance(block, TextBlock):
                # print(f"Block: {block}")
                # self.draw_text(block)
                # self.text += block.text
                pass
            elif isinstance(block, TextBlockGroup):
                # print(f"Block: {block}")
                self.draw_images(block.text_blocks)
            elif isinstance(block, RectGroup):
                # print(f"Block: {block}")
                self.draw_images(block.text_blocks)
            elif isinstance(block, FigureGroup):
                self.draw_images(block.text_blocks)
            elif isinstance(block, ImageBlock):
                self.draw_image(block)
            else:
                print(f"Unknown block type: {type(block)}")

    def draw_text_blocks(self, blocks):
        for block in blocks:
            if isinstance(block, TextBlock):
                # print(f"Block: {block}")
                self.draw_text(block)
                self.text += block.text
            elif isinstance(block, TextBlockGroup):
                # print(f"Block: {block}")
                self.draw_text_blocks(block.text_blocks)
            elif isinstance(block, RectGroup):
                # print(f"Block: {block}")
                self.draw_text_blocks(block.text_blocks)
            elif isinstance(block, FigureGroup):
                self.draw_text_blocks(block.text_blocks)
            elif isinstance(block, ImageBlock):
                # self.draw_image(block)
                pass
            else:
                print(f"Unknown block type: {type(block)}")

    def draw_image(self, block):
        try:
            img = Image.open(block.filename)
            is_rotated, rotation_value = check_image_rotation(block)

            if is_rotated:
                # Save current state
                self.canvas.saveState()

                # Calculate dimensions - important to swap width/height for 90/270 rotations
                width = block.x1 - block.x0
                height = block.y0 - block.y1

                # For 90 or 270 degree rotations, swap dimensions
                if isinstance(rotation_value, int):
                    rotation_degrees = {3: 180, 6: 90, 8: 270}.get(rotation_value, 90)
                else:
                    rotation_degrees = 90

                # For 90 or 270 degree rotations, swap width and height
                if rotation_degrees in (90, 270):
                    # Need to recalculate position to maintain alignment
                    center_x = block.x0 + width / 2
                    center_y = block.y1 + height / 2

                    # Properly center the image around its midpoint
                    self.canvas.translate(center_x, center_y)
                    self.canvas.rotate(rotation_degrees)

                    # Important: Note the negative coordinates to maintain proper positioning
                    # and swapped dimensions for proper scaling
                    self.canvas.drawImage(
                        block.filename,
                        -height / 2,
                        -width / 2,  # Centered coordinates
                        width=height,  # Swap width/height
                        height=width,  # Swap width/height
                        mask="auto",
                    )
                else:
                    # Handle 180 degree rotation
                    self.canvas.translate(block.x0 + width / 2, block.y1 + height / 2)
                    self.canvas.rotate(rotation_degrees)
                    self.canvas.drawImage(
                        block.filename,
                        -width / 2,
                        -height / 2,  # Center coordinates
                        width=width,
                        height=height,
                        mask="auto",
                    )

                # Restore state
                self.canvas.restoreState()
            else:
                # Unrotated image - original code
                self.canvas.drawImage(
                    block.filename,
                    block.x0,
                    block.y1,
                    width=block.x1 - block.x0,
                    height=block.y0 - block.y1,
                    mask="auto",
                )
        except Exception as e:
            print(f"Error drawing image {block.filename}: {e}")

    def new_page(self):
        self.canvas.showPage()

    def save(self):
        self.canvas.save()


@dataclass
class WTextBlock:
    begin_offset: int
    end_offset: int
    block: any
    page: any

    def __repr__(self):
        return (
            f"WTextBlock({self.begin_offset}, {self.end_offset}, '{self.block.text}' )"
        )


@dataclass
class RwTextBlock:
    rw_block: TextBlock
    locations: list = field(default_factory=list)


@dataclass
class WDocument:
    text: str = ""
    blocks: list = field(default_factory=list)
    prev_bold_status: bool = False
    cur_bold_status: bool = False

    def add(self, block, page):
        if isinstance(block, TextBlock):
            self.cur_bold_status = is_text_bold(block)
            if not self.cur_bold_status and self.prev_bold_status:
                self.text += "\n"

            start_offset = len(self.text)
            # Check if the block is empty
            tb = WTextBlock(
                start_offset, start_offset + len(block.text), block=block, page=page
            )

            # print("WB", block)
            if is_text_bold(block):
                self.prev_bold_status = True
            else:
                self.prev_bold_status = False

            self.blocks.append(tb)

            self.text += block.text
            self.text += "\n"
            self.prev_bold_status = self.cur_bold_status

            # self.input_text_blocks.append(block)
        elif isinstance(block, TextBlockGroup):
            for b in block.text_blocks:
                self.add(b, page)
            self.text += "\n"
        elif isinstance(block, RectGroup):
            for b in block.text_blocks:
                self.add(b, page)
                self.text += "\n"
        elif isinstance(block, FigureGroup):
            for b in block.text_blocks:
                self.add(b, page)
                self.text += "\n"


def find_next_block(blocks, start_offset, offset):
    """
    Finds the next block in the list of blocks starting from the given offset.
    """
    len_blocks = len(blocks)
    for idx in range(start_offset, len_blocks):
        if blocks[idx].begin_offset <= offset < blocks[idx].end_offset:
            return idx, blocks[idx]
    return -1, None


def anonymize_pdf_document_results(results):
    input_info = WDocument()
    for page in results["document"].pages:
        input_info.text += (
            f"\n-------------------------{page.page_number}-------------------------\n"
        )
        for block in page.layout_blocks:
            input_info.add(block, page)
    return input_info


class Writer:
    def __init__(self, writer_config: WriterConfig):
        self.writer_config = writer_config
        self.suffix = "suffix" if writer_config.suffix is None else writer_config.suffix
        self.writer = DefaultWriter(
            writer_config.pseudonyms,
            writer_config.formatters,
        )
        self.anonymizer = Anonymizer(
            writer_config.annotations,
            self.writer,
        )

    def __call__(self, document: DocumentInterface, pipeline: Pipeline) -> Path:
        pdf_path = Path(document.id)
        output_filename = pdf_path.with_suffix(".anonymized.pdf")

        writer = PDFWriter(str(output_filename), pagesize=A4)
        # print(f"Creating PDF: {output_filename} {A4}")
        # get the parse tree
        parse_options = ParseOptions(remove_footer_header=False)
        document_tree = extract_results(pdf_path, options=parse_options)

        w_doc = anonymize_pdf_document_results(document_tree)
        pdf_path.with_suffix(".extracted.txt").write_text(w_doc.text)
        # print(f"Input text: {w_doc.text[:2000]}")

        doc = pipeline(w_doc.text)
        # for e in [e for e in doc.analysis.entities if e.uri in ["Person", "Company"]]:
        #     print(f"{e.begin_offset} {e.uri} {e.literal}")
        doc = self.anonymizer(doc)

        # print("doc", doc.analysis)
        results = doc.results("wowool_anonymizer")
        locations = results["locations"]
        # print("locations", *locations)
        idx = 0
        prev_w_block = None
        block_diff_offset = 0
        leftover = 0

        for loc in locations:
            bo = loc[KW_BYTE_BEGIN_OFFSET]
            idx, w_block = find_next_block(w_doc.blocks, idx, bo)

            if prev_w_block is not None and prev_w_block != w_block:
                block_diff_offset = 0

            if w_block:
                # print(w_block)
                cur_text = w_block.block.text
                cur_text_len = len(cur_text)
                # print(f"{len(cur_text)=} {cur_text=}")
                begin = loc[KW_BYTE_BEGIN_OFFSET]
                end = loc[KW_BYTE_END_OFFSET]
                pos_begin_in_text = (
                    begin - w_block.begin_offset + block_diff_offset - leftover
                )
                pos_end_in_text = (
                    end - w_block.begin_offset + block_diff_offset - leftover
                )
                if pos_end_in_text > cur_text_len:
                    leftover = pos_end_in_text - cur_text_len
                    pos_end_in_text = cur_text_len
                    if idx + 1 < len(w_doc.blocks):
                        next_block = w_doc.blocks[idx + 1]
                        # next_block.block.text = (
                        #     " " * leftover
                        # ) + next_block.block.text[leftover:]
                        next_block.block.text = next_block.block.text[leftover:]
                else:
                    leftover = 0

                new_text = cur_text[:pos_begin_in_text]
                replacement_text = loc[KW_ANONYMIZED]
                if loc[KW_URI] == "Person":
                    parts = replacement_text.split("-")
                    if len(parts) == 3:
                        if parts[1] == "None":
                            replacement_text = f"{parts[0]}-{parts[2]}"
                        else:
                            parts[1] = parts[1].capitalize()
                            replacement_text = "#" + "-".join(parts[1:])
                    else:
                        replacement_text = loc[KW_ANONYMIZED]

                new_text += replacement_text
                new_text += cur_text[pos_end_in_text:]
                # print(f"{len(new_text)=} {new_text=}")
                w_block.block.text = new_text
                block_diff_offset += len(replacement_text) - (end - begin)

            prev_w_block = w_block

        for page_number, page in enumerate(document_tree["document"].pages):
            writer.draw_text_blocks(page.layout_blocks)
            writer.draw_images(page.layout_blocks)
            writer.new_page()

        writer.save()
        return output_filename
