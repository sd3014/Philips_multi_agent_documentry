import fitz
import os


def extract_visuals(file_path, file_type, output_folder="extracted_visuals"):
    os.makedirs(output_folder, exist_ok=True)
    visual_paths = []

    if file_type == "pdf":
        doc = fitz.open(file_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # 1) extract embedded images
            images = page.get_images(full=True)

            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)

                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                img_path = os.path.join(
                    output_folder,
                    f"page_{page_num+1}_img_{img_index+1}.{image_ext}"
                )

                with open(img_path, "wb") as f:
                    f.write(image_bytes)

                visual_paths.append(img_path)

            # 2) fallback: detect possible wide chart/table areas
            blocks = page.get_text("blocks")

            for idx, block in enumerate(blocks):
                x0, y0, x1, y1, text, *_ = block

                width = x1 - x0
                height = y1 - y0

                # avoid text-heavy blocks
                if len(text.split()) < 20 and width > 300 and height > 120:
                    rect = fitz.Rect(x0, y0, x1, y1)

                    pix = page.get_pixmap(
                        clip=rect,
                        matrix=fitz.Matrix(2, 2)
                    )

                    block_path = os.path.join(
                        output_folder,
                        f"page_{page_num+1}_visual_{idx+1}.png"
                    )

                    pix.save(block_path)
                    visual_paths.append(block_path)

    return visual_paths