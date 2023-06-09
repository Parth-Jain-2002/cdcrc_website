from django.shortcuts import render
from django.views.generic import ListView, DetailView
from info.models import News, Events, Resource, ResourceCategory, ResourceImage
from recruiter.models import Recruiter
from profiles.models import TeamMemberProfile
from django.db.models import Q
from config.utils import get_page_visibility_status
from info.forms import ResourceForm, ContactUsForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from utils.utils import render_message
from utils.mailer import Mailer
from utils.metadata import CDCRC_MEDIA_EMAIL, PRIMARY_ALERT_EMAILS, PRIMARY_PHONE
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .team_member import TeamMember
from django.conf import settings
import requests
from django.conf import settings
from functools import lru_cache


# Create your views here.
def home(request):
    news = News.objects.all()
    events = Events.objects.all()
    events = events.order_by('date').all().reverse() # sort events by date so that latest event is shown first
    for event in events:
        print(event.url)
    recruiters = Recruiter.objects.filter(visible=True)
    return render(request, 'info/home.html',{'news':news,'events':events, 'recruiters': recruiters})

def messages(request):
    MAX_NO_OF_WORDS = 100
    directors_message = ' '.join(get_message_from_google_sheet(settings.DIRECTORS_SHEET).split(' ')[:MAX_NO_OF_WORDS]) + '...'
    chairpersons_message = ' '.join(get_message_from_google_sheet(settings.CHAIRPERSONS_SHEET).split(' ')[:MAX_NO_OF_WORDS]) + '...'
    vicechairmans_message = ' '.join(get_message_from_google_sheet(settings.VICECHAIRMANS_SHEET).split(' ')[:MAX_NO_OF_WORDS]) + '...'
    print(directors_message, chairpersons_message, vicechairmans_message, sep='\n')
    context = {
        'directors_message': directors_message,
        'chairpersons_message': chairpersons_message,
        'vicechairmans_message': vicechairmans_message,
    }
    return render(request, 'info/messages.html', context=context)

def contacts(request):
    return render(request, 'info/contacts.html')

@login_required
def resources(request):
    resources = Resource.objects.filter(approved=True).order_by('-datetime')
    resource_remainder_4 = resources.count()
    context = {'resources': resources,  'resources_remainder_4': range(1, resource_remainder_4+1)}
    return render(request, 'info/resources.html', context=context)

@login_required
def resource_detail(request, pk):
    resource = Resource.objects.get(pk=pk)
    context = {'resource': resource}
    return render(request, 'info/resource_detail.html', context=context)

def create_resource(request): 
    if request.method=='POST':
        if not request.user.is_authenticated:
            return render_message(request,
                'Kindly authenticate',
                'We are glad to see that you want to add resouce on this forum. Unfortunately we need you to authenticate before you add any resource.'
            )
        form = ResourceForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid():
            with transaction.atomic():
                res = form.save(commit=True)
                res.author = request.user
                res.save()
                for file in files:
                    file = ResourceImage(image=file)
                    file.resource = res
                    file.save()
            mailer = Mailer()
            mailer._send_email(
                CDCRC_MEDIA_EMAIL,
                'Approval Request for New Resource {}'.format(res.title),
                '{} has added a resource titled {}. Please take a look.'.format(res.author.username, res.title)
            )
            return render_message(request, 'Approval Pending', 'Thanks for sharing the resource...it will be posted on the website after being approved by our team!')
        else:
            return render_message(request, 'Error', 'There was an error in creating the resource')
    else:
        form = ResourceForm()
        return render(request, 'info/resource_create.html', context={'form': form})

def news_detail(request, pk):    
    news = News.objects.get(pk=pk)    
    return render(request,'info/news_detail.html', {'news': news})

def events_detail(request, pk):
    events = Events.objects.get(pk=pk)
    return render(request,'info/events_detail.html',{'events':events})

def parse_sheet_url(sheet_url):
    """Returns the sheet_id and gid from the sheet_url"""
    sheet_id = sheet_url.split('/')[5]
    gid = sheet_url.split('/')[6].split('=')[1]
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=tsv&gid={gid}"

# @lru_cache(maxsize=None)
def get_team_data(sheet_url):
    """
    Returns a list of TeamMember objects
    Fetches data from Google Sheets
    """

    url = parse_sheet_url(sheet_url)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Error fetching data from Google Sheets')
    data = response.text
    members = []
    for line in data.split('\n')[1:]:
        line = line.strip()
        if not line:
            continue
        fname, lname, email, designation, phone, linkedin = (line.split('\t') + ['']*6)[:6]
        members.append(TeamMember(fname, lname, email, designation, phone, linkedin))
    return members

def faculty_team(request):
    # faculty_team_members = TeamMemberProfile.objects.filter((Q(category='faculty') | Q(category='staff')) & Q(visible=True)).order_by('-level')
    # members_remainder_4 = faculty_team_members.count()
    faculty_team_members = get_team_data(settings.FACULTY_MEMBERS_SHEET)
    members_remainder_4 = len(faculty_team_members)
    context = {'team_members': faculty_team_members, 'team_members_remainder_4': range(1, members_remainder_4+1), 'title': 'Faculty Team', 'show_email': True}
    return render(request, 'info/team.html', context=context)

def student_team(request):
    # return render(request, 'under_construction.html')
    # student_team_members = TeamMemberProfile.objects.filter((Q(category='ug') | Q(category='pg')) & Q(visible=True)).order_by('-level')
    # members_remainder_4 = student_team_members.count()
    student_team_members = get_team_data(settings.STUDENT_MEMBERS_SHEET)
    members_remainder_4 = len(student_team_members)
    context = {'team_members': student_team_members, 'team_members_remainder_4': range(1, members_remainder_4+1), 'title': 'Student Team', 'show_email': False}
    return render(request, 'info/team.html', context=context)

def under_construction(request):
    return render(request, 'under_construction.html')

# @lru_cache(maxsize=None)
def get_message_from_google_sheet(sheet_url):
    url = parse_sheet_url(sheet_url)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Error fetching data from Google Sheets')
    data = response.content.decode('utf-8')
    return data.replace('\n', '<br>').replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')

def directors_message(request):
    message = get_message_from_google_sheet(settings.DIRECTORS_SHEET)
    return render(request, 'info/directors_message.html', {'message': message})

def vision_statement(request):
    return render(request, 'info/vision_statement.html')

def corporate_relations_home(request):
    return render(request, 'under_construction.html')


def tnp_hod_message(request):
    if(get_page_visibility_status('tnp_hod_message')==False):
        return render(request, 'under_construction.html')
    message = get_message_from_google_sheet(settings.CHAIRPERSONS_SHEET)
    return render(request, 'info/tnp_hod_message.html', {'message': message})


def contact_us_form(request):
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact_us_obj = form.save(commit=True)
            mailer = Mailer()
            mailer._send_email(
                PRIMARY_ALERT_EMAILS,
                '[ALERT] New Registration on Website:  {}'.format(contact_us_obj.name), 
                'Please reach out to {} from {} who has registered on the CDCRC Website.\n Contact Info - {}, {}.\nMessage- {}'.format(contact_us_obj.name, contact_us_obj.organization, contact_us_obj.email, contact_us_obj.phone, contact_us_obj.message),
            )
            return render_message(request, 'Thanks!', 'Our team will reach out to you shortly. You can also call us at {} whenever you want!'.format(PRIMARY_PHONE))
        else:
            return render_message(request, 'Error', 'There was an error in filling the form..')
    else:
        title = 'Contact Us Form'
        form = ContactUsForm()
        return render(request, 'info/contact_us_form.html', context={'title': title, 'form':form})


def placement_stats(request):

    """
    Renders the placement stats page, using the data from the placements sheet
    """

    def parse_sheet_url(sheet_url):
        """Returns the sheet_id and gid from the sheet_url"""
        sheet_id = sheet_url.split('/')[5]
        gid = sheet_url.split('/')[6].split('=')[1]

        return sheet_id, gid

    sheet_url = settings.PLACEMENTS_SHEET
    sheet_id, gid = parse_sheet_url(sheet_url)

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=tsv&gid={gid}"

    req = requests.get(url).text


    allItems = []
    item = []
    for data_string in req.split('\n'):
        if(data_string.startswith('NEW')):
            if(item): # adding item to allItems if item is not empty
                allItems.append(item)
            item=[] # clearing item for new values
            continue

        # removing \r from the end of each data value
        data_values = [data.rstrip('\r') for data in data_string.split('\t')]
        item.append(data_values) # adding data_values to item

    # add the last item
    if(item):
        allItems.append(item)
    
    return render(request, 'info/placement_stats.html', {'allItems': allItems})


