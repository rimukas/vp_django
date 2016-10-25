from django.http import HttpResponse
from vart.printing import ReportPrint
from io import BytesIO


def print_users(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="My Users.pdf"'

    buffer = BytesIO()

    report = ReportPrint(buffer)
    pdf = report.print_users()

    response.write(pdf)
    return response
