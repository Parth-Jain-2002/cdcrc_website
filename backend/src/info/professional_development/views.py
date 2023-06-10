"""
Views for the professional development section
"""

from django.shortcuts import render
from info.models import ProfessionalDevelopmentActivity, ProfessionalDevelopmentBook, ProfessionalDevelopmentVideo, ProfessionalDevelopmentInitiatives, Messages
from recruiter.models import Recruiter
from django.db.models import Q
from config.utils import get_page_visibility_status
from info.models import Events
from django.conf import settings
import requests

def about(request):
    if(get_page_visibility_status('pd_about')==False):
        return render(request, 'under_construction.html')
    context = {
        'title': 'About the Career Development Cell'
    }
    return render(request, 'info/professional_development/about.html', context=context)

def activities(request):
    if(get_page_visibility_status('pd_activities')==False):
        return render(request, 'under_construction.html')
    events = Events.objects.all()
    context = {
        'activities': ProfessionalDevelopmentActivity.objects.order_by('-date'),
        'title': 'Career Development Activities',
        'events':events,
    }
    return render(request, 'info/professional_development/activities.html', context=context)

def initiatives(request):
    if(get_page_visibility_status('pd_initiatives')==False):
        return render(request, 'under_construction.html')
    context = {
        'initiatives': ProfessionalDevelopmentInitiatives.objects.order_by('-date'),
        'title': 'Career Development Initiatives',
    }
    return render(request, 'info/professional_development/initiatives.html', context=context)

def activity_detail(request, pk):
    context = {
        'activity': ProfessionalDevelopmentActivity.objects.get(pk=pk),
        'title': 'Activity Detail',
    }
    return render(request, 'info/professional_development/activity_detail.html', context=context)

def initiative_detail(request, pk):
    context = {
        'initiative': ProfessionalDevelopmentInitiatives.objects.get(pk=pk),
        'title': 'Initiative Detail',
    }
    return render(request, 'info/professional_development/initiative_detail.html', context=context)

def books(request):
    if(get_page_visibility_status('pd_library')==False):
        return render(request, 'under_construction.html')
    context = {
        'title' : 'Library',
        'books': ProfessionalDevelopmentBook.objects.all()
    }
    return render(request, 'info/professional_development/books.html', context=context)

def videos(request):
    if(get_page_visibility_status('pd_videos')==False):
        return render(request, 'under_construction.html')
    context = {
        'title' : 'Video Resources for Students',
        'videos' : ProfessionalDevelopmentVideo.objects.all()
    }
    return render(request, 'info/professional_development/videos.html', context=context)


def parse_sheet_url(sheet_url):
    """Returns the sheet_id and gid from the sheet_url"""
    sheet_id = sheet_url.split('/')[5]
    gid = sheet_url.split('/')[6].split('=')[1]
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=tsv&gid={gid}"

def get_message_from_google_sheet(sheet_url):
    url = parse_sheet_url(sheet_url)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Error fetching data from Google Sheets')
    data = response.content.decode('utf-8')
    return data.replace('\n', '<br>').replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')

def hod_message(request):
    if(get_page_visibility_status('pd_hod_message')==False):
        return render(request, 'under_construction.html')
    # message = get_message_from_google_sheet(settings.VICECHAIRMANS_SHEET)
    # return render(request, 'info/professional_development/hod_message.html', {'message': message})
    vicechairperson = Messages.objects.filter(authorDesignation='Vice Chairperson')[0]
    return render(request, 'info/tnp_hod_message.html', {'chairperson': vicechairperson})

def pg_resources(request):
    context = {
        'title' : 'Resources for PG Students',
    }
    return render(request, 'info/professional_development/graduate_student_resources.html', context=context)