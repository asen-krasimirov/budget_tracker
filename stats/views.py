from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .utils import get_grouped_statistics, get_most_and_least_bought, send_statistics_email
from accounts.models import UserProfile


@login_required
def stats_view(request):
    """
    Renders the statistics page with initial data.
    """
    return render(request, "stats/stats.html")


def stats_data(request):
    """
    Returns purchase statistics with numeric values (for Chart.js) and a separate currency symbol.
    """
    stats = get_grouped_statistics(request.user)
    most_least = get_most_and_least_bought(request.user)

    profile = UserProfile.objects.get(user=request.user)
    currency_symbol = profile.get_currency_display().split()[-1]

    formatted_stats = {
        "monthly": {k: v for k, v in stats["monthly"].items()} if stats else {},
        "weekly": {k: v for k, v in stats["weekly"].items()} if stats else {},
        "daily": {k: v for k, v in stats["daily"].items()} if stats else {},
        "category": {k: v for k, v in stats["category"].items()} if stats else {},
        "most_bought": most_least.get("most_bought", "N/A"),
        "least_bought": most_least.get("least_bought", "N/A"),
        "currency_symbol": currency_symbol
    }

    return JsonResponse(formatted_stats)


@login_required
def send_report_email(request):
    """
    Sends an email with user statistics when requested via AJAX.
    """
    if request.method == "POST":
        send_statistics_email(request.user)
        return JsonResponse({"message": "Report Sent Successfully!"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)