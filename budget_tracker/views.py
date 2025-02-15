from django.shortcuts import render


def home(request):
    """Renders base.html as the homepage."""
    return render(request, 'base.html')
