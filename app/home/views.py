import logging
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import InstanceForm
from .tasks import create_instance, delete_instance
from .vultr import Vultr

logger = logging.getLogger('app')


def home_view(request, **kwargs):
    # View /
    logger.debug(request.session['instance'] if 'instance' in request.session else None)
    if 'instance' in request.session:
        return redirect('home:manage')

    available = cache.get('vultr-available')
    if not available:
        vultr = Vultr()
        plans = vultr.list_plans()
        regions = vultr.list_regions()
        available = vultr.filter_regions(regions, plans[0]['locations'])
        cache.set('vultr-available', available, 900)
    context = {'available': available}
    return render(request, 'home.html', context)


def about_view(request, **kwargs):
    # View /about/
    return render(request, 'about.html')


def manage_view(request, **kwargs):
    # View /manage/
    logger.debug(request.session['token'] if 'token' in request.session else None)
    logger.debug(request.session['instance'] if 'instance' in request.session else None)
    if 'instance' not in request.session:
        return redirect('home:index')

    context = {'instance': request.session['instance']}
    return render(request, 'manage.html', context)


@require_http_methods(['POST'])
def create_view(request, **kwargs):
    # View /create/
    if 'instance' in request.session:
        logger.debug('INSTANCE FOUND IN SESSION - DUPLICATE CREATE DETECTED')
        error = {'location': '/'}
        return JsonResponse(error, status=400)

    logger.info(request.POST)
    form = InstanceForm(request.POST)
    if not form.is_valid():
        logger.debug(form.errors)
        return JsonResponse(form.errors, status=400)

    logger.debug(form.cleaned_data['token'])
    logger.debug(form.cleaned_data['location'])
    try:
        instance = create_instance(form.cleaned_data['token'], form.cleaned_data['location'])
    except Exception as error:
        logger.exception(error)
        return JsonResponse({'err_msg': str(error)}, status=400)

    request.session['token'] = form.cleaned_data['token']
    request.session['instance'] = instance
    messages.success(request, 'Success. Your VPN is installing now; however, I can not make the .ovpn file right now.')
    return JsonResponse(instance)


@require_http_methods(['POST'])
def delete_view(request, **kwargs):
    # View /delete/
    if 'instance' not in request.session:
        logger.debug('INSTANCE NOT FOUND IN SESSION - CAN NOT DELETE')
        return redirect('home:index')

    try:
        delete_instance(request.session['token'], request.session['instance']['id'])
    except Exception as error:
        logger.exception(error)
        messages.error(request, f'Error deleting instance: {str(error)}')
        return redirect('home:manage')

    del request.session['instance']
    return redirect('home:index')


@csrf_exempt
@require_http_methods(['POST'])
def callback_view(request, **kwargs):
    # View /callback/
    logger.info(request.POST)
    ip_address = request.POST['ip_address']
    password = request.POST['password']
    ca_cert = request.POST['ca_cert']
    logger.debug('ip_address: %s', ip_address)
    logger.debug('password: %s', password)
    logger.debug('ca_cert: %s', ca_cert)
    return HttpResponse()
