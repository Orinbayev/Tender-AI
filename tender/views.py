from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import markdown as md
from .models import TenderOrder
from .ai_service import fetch_tender_info, generate_tender_document
from .pdf_generator import generate_pdf


def to_html(text):
    return mark_safe(md.markdown(text, extensions=["tables", "nl2br"]))


def home(request):
    return render(request, "home.html")


def create_order(request):
    if request.method == "POST":
        order = TenderOrder.objects.create(
            company_name=request.POST["company_name"],
            company_inn=request.POST["company_inn"],
            company_activity=request.POST["company_activity"],
            company_experience=request.POST["company_experience"],
            tender_url=request.POST["tender_url"],
            price_offer=request.POST["price_offer"],
            status="processing",
        )

        tender_info = fetch_tender_info(order.tender_url)
        order.tender_title = tender_info["title"]
        order.tender_description = tender_info["description"]
        order.save()

        try:
            document = generate_tender_document(order)
            order.generated_document = document
            order.status = "done"
        except Exception as e:
            order.generated_document = f"Xatolik yuz berdi: {str(e)}"
            order.status = "error"

        order.save()
        return redirect("result", order_id=order.id)

    return render(request, "create.html")


def result(request, order_id):
    order = get_object_or_404(TenderOrder, id=order_id)
    return render(request, "result.html", {
        "order": order,
        "document_html": to_html(order.generated_document),
    })


def download_pdf(request, order_id):
    order = get_object_or_404(TenderOrder, id=order_id)
    pdf = generate_pdf(order)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="tender_{order.id}.pdf"'
    return response
