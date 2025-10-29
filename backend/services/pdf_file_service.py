import fitz
import re 
import json
import string

from pdf2image import convert_from_path
from pdfminer.high_level import extract_text
from collections import Counter

from core.config import POPPLER_PATH

def convert_pdf_to_image(file_path):
    images = convert_from_path(
        file_path, 
        dpi=300, 
        fmt="png",
        poppler_path = POPPLER_PATH
        )
    return images

def get_embedded_pdf_text(file_path):
    embedded_text = extract_text(file_path)
    return embedded_text

def get_content_streams(file_path):
    file = fitz.open(file_path)
    raw_streams = []
    structured_streams = []

    for page_num, page in enumerate(file, start=1):
        xref = page.get_contents()
        content_bytes = b""

        if isinstance(xref, list):
            for x in xref:
                content_bytes += file.xref_stream(x)
        else:
            content_bytes = file.xref_stream(xref)
        
        #Done to make the bytes readable by AI
        content_text = content_bytes.decode('latin-1', errors="ignore")

        raw_streams.append({
            "page": page_num,
            "stream": content_text
        })

        simplified_blocks = simplify_pdf_content_stream(content_text)
        null_cleaned_simplified_stream = remove_null_from_simplified_stream(simplified_blocks)
        readable_cleaned_simplified_stream = [b for b in null_cleaned_simplified_stream if is_readable(b["text"])]

        structured_data = add_structure_metadata(page_num, readable_cleaned_simplified_stream)
        structured_streams.append(structured_data)

    ai_inputs = prepare_streams_for_ai(structured_streams)
    return ai_inputs

def simplify_pdf_content_stream(raw_stream):
    blocks = re.findall(r"BT(.*?)ET", raw_stream, re.DOTALL)
    simplified_blocks = []

    if not blocks:
        printf(f"WARNING: No BT/ET blocks found in stream")
        return simplified_blocks

    for block in blocks:
        font_match = re.search(r"/F(\d+)", block)
        font = f"F{font_match.group(1)}" if font_match else None

        size_match = re.search(r"/F\d+\s+([\d.]+)\s+Tf", block)
        font_size = float(size_match.group(1)) if size_match else None

        color_match = re.search(r"([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+rg", block)
        if color_match:
            color = tuple(map(float, color_match.groups()))
        else:
            gray_match = re.search(r"([\d.]+)\s+g\b", block)
            if gray_match:
                gray = float(gray_match.group(1))
                color = (gray, gray, gray)
            else:
                color = (0, 0, 0)

        text_parts = []
        
        tj_matches = re.findall(r"\((.*?)\)\s*Tj", block)
        text_parts.extend(tj_matches)
   
        tj_array_matches = re.findall(r"\[(.*?)\]\s*TJ", block, re.DOTALL)
        for array_content in tj_array_matches:
            strings_in_array = re.findall(r"\((.*?)\)", array_content)
            text_parts.extend(strings_in_array)
        
        quote_matches = re.findall(r"\((.*?)\)\s*'", block)
        text_parts.extend(quote_matches)
        
        doublequote_matches = re.findall(r"\((.*?)\)\s*\"", block)
        text_parts.extend(doublequote_matches)
        
        hex_matches = re.findall(r"<([0-9A-Fa-f]+)>\s*(?:Tj|TJ|'|\")", block)
        for hex_str in hex_matches:
            try:
                decoded = bytes.fromhex(hex_str).decode('latin-1', errors='ignore')
                text_parts.append(decoded)
            except:
                pass

        text = " ".join(text_parts).strip()

        if text:  
            simplified_blocks.append({
                "font": font,
                "font_size": font_size,
                "color": color,
                "text": text
            })

    return simplified_blocks
   
def add_structure_metadata(page_number: int, simplified_blocks: list):
    num_objects = len(simplified_blocks)
    all_fonts = [b["font"] for b in simplified_blocks if b["font"]]
    all_colors = [tuple(b["color"]) for b in simplified_blocks if b["color"]]
    all_font_sizes = [b["font_size"] for b in simplified_blocks if b["font_size"]]

    unique_fonts = list(set(all_fonts))
    unique_colors = list(set(all_colors))
    unique_sizes = list(set(all_font_sizes))

    total_chars = sum(len(b["text"]) for b in simplified_blocks)
    fragmentation_ratio = round(num_objects / total_chars, 3) if total_chars > 0 else 0

    font_switches = sum(1 for i in range(1, len(all_fonts)) if all_fonts[i] != all_fonts[i - 1])

    color_switches = sum(1 for i in range(1, len(all_colors)) if all_colors[i] != all_colors[i - 1])

    structured = {
        "page": page_number,
        "metadata": {
            "num_objects": num_objects,
            "unique_fonts": unique_fonts,
            "unique_colors": unique_colors,
            "unique_font_sizes": unique_sizes,
            "fragmentation_ratio": fragmentation_ratio,
            "font_switches": font_switches,
            "color_switches": color_switches
        },
        "objects": simplified_blocks
    }

    return structured

def prepare_streams_for_ai(streams):
    ai_inputs = []
    
    for structured_data in streams:
        page_num = structured_data["page"]
        metadata = structured_data["metadata"]
        objects = structured_data["objects"]
            
        limited_objects = objects[:50]
            
        objects_summary = json.dumps(limited_objects, indent=2)
        metadata_summary = json.dumps(metadata, indent=2)
            
        prompt = f"""Analyze this structured PDF content stream data for page {page_num}.
        Metadata:
        {metadata_summary}

        Text Objects (showing first {len(limited_objects)} of {len(objects)}):
        {objects_summary}

        Detection Guidelines:
        1. Check fragmentation_ratio: Values > 0.15 suggest excessive text splitting (possible tampering)
        2. Check font_switches: Unusual number of font changes may indicate inserted text
        3. Check color_switches: Unexpected color changes can signal modifications
        4. Look for font/color/size inconsistencies that don't match document style

        Legitimate patterns to ignore:**
        - Headers/footers often use different fonts
        - Hyperlinks naturally use different colors
        - Some PDF generators split text more than others
        - Legitimate PDFs often split text into multiple BT/ET sections
        - Color or font changes mid-line can occur naturally
        - Treat these only as suspicious if new or inconsistent text appears
        - Many PDFs use embedded fonts that make extracted text appear garbled or "encoded."
        - This is **normal**, and not encryption or deliberate obfuscation.
        - Caesar cipher–like patterns, uniform character shifts, or unreadable text caused by font subsets 
        should be treated as **standard PDF encoding behavior**, not tampering.
        - Only mark "modified": true if
        • A localized region shows replaced or inserted text with inconsistent styling, color, or spacing.
        • Metadata or structure (not just glyphs) shows anomalous insertion.

        Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks):
        {{
            "page": {page_num},
            "modified": "true or false or unsure",
            "confidence": 85,
            "summary": "brief explanation of findings based on structured data",
            "notable_differences": ["difference 1", "difference 2"],
            "suspicious_metrics": {{
                "fragmentation": "high/normal/low",
                "font_consistency": "consistent/inconsistent",
                "color_consistency": "consistent/inconsistent"
            }}
        }}
        """
            
        ai_inputs.append({
            "prompt": prompt,
            "page": page_num
        }) 
    return ai_inputs 

def remove_null_from_simplified_stream(content_stream):
    for b in content_stream:
        b["text"] = b["text"].replace("\u0000", "")
        
    return content_stream

def is_readable(text):
    allowed = string.ascii_letters + string.digits + string.punctuation + ' '
    readable_chars = sum(c in allowed for c in text)
    return readable_chars / len(text) > 0.5 if text else False
