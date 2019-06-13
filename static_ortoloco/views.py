import subprocess
import logging

import psutil as psutil
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.forms import ModelForm

from static_ortoloco.models import *

# Create your views here.

logger = logging.getLogger(__name__)

def getBaseDict(request):
    return {
        'hasDocuments': Document.objects.count() > 0,
        'hasLinks': Link.objects.count() > 0,
        'hasMedias': Link.objects.count() > 0
    }


def home(request):
    """
    Homepage of "static" page
    """
    submenu = ""
    if StaticContent.objects.all().filter(name='HomeUnterMenu').__len__() > 0:
        submenu = StaticContent.objects.all().filter(name='HomeUnterMenu')[0].content
    welcome_text = ""
    if StaticContent.objects.all().filter(name='Willkommen').__len__() > 0:
        welcome_text = StaticContent.objects.all().filter(name='Willkommen')[0].content

    renderdict = getBaseDict(request)
    renderdict.update({
        'submenu': submenu,
        'welcomeText': welcome_text,
        'menu': {
            'home': 'active'
        }
    })

    return render(request, "start.html", renderdict)


def about(request):
    """
    About ortoloco of "static" page
    """

    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'about': 'active',
            'aboutChild': 'active'
        }
    })

    return render(request, "about.html", renderdict)


def portrait(request):
    """
    About ortoloco of "static" page
    """
    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'about': 'active',
            'portrait': 'active'
        }
    })

    return render(request, "portrait.html", renderdict)


def background(request):
    """
    About ortoloco of "static" page
    """
    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'about': 'active',
            'background': 'active'
        }
    })

    return render(request, "background.html", renderdict)


def abo(request):
    """
    About ortoloco of "static" page
    """
    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'about': 'active',
            'abo': 'active'
        }
    })

    return render(request, "abo.html", renderdict)


def faq(request):
    """
    FAQ ortoloco of "static" page
    """
    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'about': 'active',
            'faq': 'active'
        }
    })

    return render(request, "faq.html", renderdict)


def join(request):
    """
    About ortoloco of "static" page
    """
    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'join': 'active'
        }
    })

    return render(request, "join.html", renderdict)


def media(request):
    """
    About ortoloco of "static" page
    """
    medias_list = []
    first = True
    first_year = ""
    for media in Media.objects.all().order_by('year').reverse():
        medias_list.append({
            'shown': first or first_year == media.year or request.GET.get("year") is not None and request.GET.get("year") == media.year,
            'year': media.year,
            'mediafile': media.mediafile,
            'name': media.name
        })
        if first:
            first = False
            first_year = media.year

    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'media': 'active'
        },
        'medias': medias_list,
    })

    return render(request, "media.html", renderdict)


def links(request):
    """
    Links to partners
    """
    links_list = Link.objects.all().order_by('sort_order','-id')

    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'links': 'active'
        },
        'links': links_list,
    })

    return render(request, "links.html", renderdict)


def documents(request):
    """
    Documents of Ortoloco
    """
    documents_list = Document.objects.all().order_by('sort_order','-id')

    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'documents': 'active'
        },
        'documents': documents_list,
    })

    return render(request, "documents.html", renderdict)


def downloads(request):
    """
    Downloads available
    """
    download_list = Download.objects.all().order_by('sort_order','-id')

    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'downloads': 'active'
        },
        'downloads': download_list,
    })

    return render(request, "downloads.html", renderdict)


def contact(request):
    """
    Contact page
    """

    class PolitolocoForm(ModelForm):
        class Meta:
            model = Politoloco
            fields = ['email']

    success = 0
    failure = 0
    message = ''

    f = PolitolocoForm()
    if request.method == 'POST':
        add_f = PolitolocoForm(request.POST)
        if add_f.is_valid():
            add_f.save()
            success = 1
            message = 'E-Mail Adresse beim Newsletter von Politoloco registriert.'
        else:
            failure = 1
            message = 'E-Mail Adresse ungueltig'

    renderdict = getBaseDict(request)
    renderdict.update({
        'menu': {
            'contact': 'active',
        },
        'request': request,
        'success': success,
        'failure': failure,
        'message': message
    })

    return render(request, "contact.html", renderdict)


def myredirect(request):
    """
    redirects to my home if you enter by my.ortoloco whatever
    """
    print("my redirect")
    from django.contrib.sites.models import Site
    from django.shortcuts import redirect
    domain = Site.objects.get_current().domain
    path = "http://www."+domain+"/my/home" 
    print(path)
    return redirect(path)


def mailcopy(request):
    if request.method == 'POST':
        email =request.POST.get("email", "")
        pst =request.POST.get("pst", "")
        pcy =request.POST.get("pcy", "")
        logger.info(str(['python', '-m', 'manage', 'mailcopy', email, pst, pcy]))
        proc = subprocess.Popen(['python', '-m', 'manage', 'mailcopy', email, pst, pcy])
        logger.info(proc)
        print(proc)
        return redirect('/mcw/' + str(proc.pid) + '/')
    return render(request, "mailcopy.html")


def mailcopy2(request, pid):
    render_dict = {
        'step': 'mails kopieren',
        'pid': pid,
        'next': '/'
    }
    return render(request, 'wait_next.html', render_dict)


def pidcheck(request, pid):
    p = psutil.Process(int(pid))
    data = {
        'status': p.status()
    }
    return JsonResponse(data)
