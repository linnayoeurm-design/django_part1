from django.shortcuts import render

def wheel_timer(request):
    return render(request, 'wheel_timer/wheel_timer.html', {})
