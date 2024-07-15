from django.shortcuts import render

def home(request):

    # sample_tacks = Tack.objects.filter(title__in=['Sample', 'What are Tacks?', 'Canva DIY'])
    # user_tacks = None
    # if request.user.is_authenticated:
    #     user = get_object_or_404(User, username=request.user.username)
    #     user_tacks = Tack.objects.filter(members=user)

    # context = {
    #     'sample': sample,
    #     'user': request.user,
    # }
    # return render(request, 'home.html', context)

    return render(request, 'home.html')
