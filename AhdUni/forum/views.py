from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator

from .models import Post


def post_list_view(request, *args, **kwargs):
	post_list = Post.objects.all()
	paginator = Paginator(post_list, 1)

	page = request.GET.get('page')
	page_data = paginator.get_page(page)

	context = {'page_data': page_data, 'last_page': paginator.num_pages}
	return render(request, 'forum/forum.html', context)

def post_detail_view(request, slug, *args, **kwargs):
	post = Post.objects.get(slug=slug)

	context = {'object': post}
	return render(request, 'forum/post_detail.html', context)