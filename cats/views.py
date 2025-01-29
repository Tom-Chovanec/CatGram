from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import CatImage
from .forms import CatImageForm
from django.contrib.auth.decorators import login_required


def home(request):
    cats = CatImage.objects.all().order_by('-uploaded_at')
    for cat in cats:
        cat.user_liked = cat.liked(request.user)
    return render(request, 'cats/home.html', {'cats': cats})


@login_required
def upload_cat(request):
    if request.method == 'POST':
        form = CatImageForm(request.POST, request.FILES)
        if form.is_valid():
            cat_image = form.save(commit=False)
            cat_image.uploaded_by = request.user
            cat_image.save()
            return redirect('home')
    else:
        form = CatImageForm()
    return render(request, 'cats/upload.html', {'form': form})


@login_required
def like_cat(request, cat_id):
    cat = get_object_or_404(CatImage, id=cat_id)
    if cat.likes.filter(id=request.user.id).exists():
        cat.likes.remove(request.user)
        liked = False
    else:
        cat.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': cat.like_count()})


@login_required
def favorite_cat(request, cat_id):
    cat = get_object_or_404(CatImage, id=cat_id)
    if cat.favorites.filter(id=request.user.id).exists():
        cat.favorites.remove(request.user)
    else:
        cat.favorites.add(request.user)
    return redirect('home')


@login_required
def profile(request):
    user_cats = CatImage.objects.filter(
        uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'cats/profile.html', {'user_cats': user_cats})


@login_required
def delete_cat(request, cat_id):
    cat = get_object_or_404(CatImage, id=cat_id, uploaded_by=request.user)
    cat.delete()
    return redirect('profile')
