from django.shortcuts import render


def home(request):
    return render(request, 'home/home_page.html')

def live_feed(request):
    return render(request, '../templates/live_feed.html')

def privacy_policy(request):
    return render(request, '../templates/privacy_policy.html')

def cookie_policy(request):
    return render(request, '../templates/cookies_policy.html')
