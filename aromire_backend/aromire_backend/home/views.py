from django.shortcuts import render


def about(request):
    return render(request, "home/about.html")


def gallery(request):
    return render(request, "home/gallery.html")


def contact(request):
    return render(request, "home/contact.html")
