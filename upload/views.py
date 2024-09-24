from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ProjectImage
from .models import Contact
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Contact
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.http import FileResponse
from django.views.generic import ListView,View
from .models import News
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core import serializers





def index(request):
    projects = Project.objects.all()
    return render(request, 'index.html', {'projects': projects})

def project_view(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def detail_view(request, slug):
    all_projects = Project.objects.all()
    project = get_object_or_404(Project, project_slug=slug)
    photos = ProjectImage.objects.filter(project=project)
    return render(request, 'project_detail.html', {
        'project': project,
        'photos': photos,
        'all_projects' : all_projects,
    })

@csrf_exempt  # Since the form is in a modal, CSRF exemption is needed
def contact_view(request):
    if request.method == 'POST':
        form = request.POST
        contact = Contact(
            name=form['name'],
            company=form['company'],
            email=form['email'],
            phone=form['phone'],
            message=form['message'],
            agree=form.get('agree')
        )
        contact.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    return render(request, 'index.html')  # Replace 'your_base_template.html' with your actual base template

class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news_list'
    ordering = '-date_uploaded'  # Default ordering
    paginate_by = 4  # Change this to the desired initial number of items per page
    
    def get_queryset(self):
        ordering = self.request.GET.get('ordering')
        if ordering == 'asc':
            return News.objects.order_by('date_uploaded')
        elif ordering == 'desc':
            return News.objects.order_by('-date_uploaded')
        else:
            return News.objects.all()  # Default ordering

# views.py
@csrf_exempt
def load_more(request):
    offset = int(request.POST['offset'])
    limit = int(request.POST['limit'])  # Fetch the limit value
    posts = News.objects.all()[offset:offset + limit]  # Slice the queryset correctly
    totalData = News.objects.count()
    posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': posts_json,
        'totalResult': totalData
    })

class NewsPDFView(View):
    def get(self, request, slug):
        news = get_object_or_404(News, slug=slug)
        response = HttpResponse(news.pdf_file, content_type='application/pdf')
        return response
    
def about_us(request):
    return render(request, 'about_us.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def vastukar_architects(request):
    all_projects = Project.objects.all()
    return render(request, 'vastukar_architects.html', {'all_projects': all_projects})

def certified_constructions(request):
    all_projects = Project.objects.all()
    return render(request, 'vastukar_constructions.html', {'all_projects': all_projects})

def vastukar_interiors(request):
    all_projects = Project.objects.all()
    return render(request, 'vastukar_interiors.html', {'all_projects': all_projects})

def swiper(request):
    all_projects = Project.objects.all()
    return render(request, 'swiper.html', {'all_projects': all_projects})
