from playwright.sync_api import sync_playwright
from django.template.loader import render_to_string
import markdown as md
from django.utils.safestring import mark_safe


def generate_pdf(order) -> bytes:
    document_html = mark_safe(md.markdown(
        order.generated_document,
        extensions=["tables", "nl2br"]
    ))

    html = render_to_string("pdf_template.html", {
        "order": order,
        "document_html": document_html,
    })

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        pdf_bytes = page.pdf(
            format="A4",
            margin={"top": "2cm", "bottom": "2cm", "left": "2.5cm", "right": "2.5cm"},
            print_background=True,
        )
        browser.close()

    return pdf_bytes
