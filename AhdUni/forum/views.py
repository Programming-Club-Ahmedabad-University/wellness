from django.shortcuts import render
from django.views import View
from .models import Post


def post_list_view(request, *args, **kwargs):
	post_list = Post.objects.all()

	context = {'post_list': post_list}
	return render(request, 'forum/forum.html', context)

def post_detail_view(request, slug, *args, **kwargs):
	post = Post.objects.get(slug=slug)

	context = {'object': post}
	return render(request, 'forum/post_detail.html', context)