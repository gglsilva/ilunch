from django.shortcuts import render

# Create your views here.
def memory_game(request):
    template_name = 'core/memory_game.html'
    return render(request, template_name)