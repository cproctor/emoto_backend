from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from emoto_backend.models import Message, Profile, Emoto, generate_pair_code
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json
import logging

log = logging.getLogger('django')

def missing_props(props, expected_props):
    missing = []
    for prop in expected_props:
        if props.get(prop) is None:
            missing.append(prop)
    if missing:
        return missing

@csrf_exempt
def signup(request):
    try:
        log.info("IN SIGNUP")
        props = json.loads(request.body.decode("utf-8"))
        log.info(props)
    
        missing = missing_props(props, ["username", "latitude", "longitude"])
        if missing:
            return JsonResponse({"error": "missing properties: {}".format(", ".join(missing))}, status=400)
        if Profile.objects.filter(username=props.get('username')).count() != 0:
            return JsonResponse({"error": "username already exists"}, status=400)
    
        profile = Profile(**props)
        profile.clean()
        profile.save()
        return JsonResponse(profile.status_json())
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except ValueError:
        return JsonResponse({"error": "malformed json"}, status=400)
        

def status(request, username):
    try:
        profile = Profile.objects.get(username=username)
        return JsonResponse({
            "self": profile.status_json(),
            "partner": profile.partner.status_json() if profile.partner else None
        })
    except Profile.DoesNotExist:
        return JsonResponse({"error": "no such user"}, status=400)

def messages(request, username):
    try:
        profile = Profile.objects.get(username=username)
        if profile.partner:
            messages = Message.objects.filter(author__in=[profile, profile.partner]).all()
        else:
            messages = profile.message_set.all()
        return JsonResponse({"messages": [m.json() for m in messages]})
    except Profile.DoesNotExist:
        return JsonResponse({"error": "no such user"}, status=400)

@csrf_exempt
def new_message(request, username):
    try:
        profile = Profile.objects.get(username=username)
        props = json.loads(request.body.decode("utf-8"))
        log.info(props)
        if not props.get('text'):
            return JsonResponse({'error': 'missing properties: text'}, status=400)
        if props.get('emoto'):
            emoto =  Emoto.objects.get(name=props.get('emoto'))
        else:   
            emoto = None
        message = Message(text=props.get('text'), author=profile, emoto=emoto)
        message.save()
        return JsonResponse(message.json())
        
    except Profile.DoesNotExist:
        return JsonResponse({"error": "no such user"}, status=400)
    except Emoto.DoesNotExist:
        return JsonResponse({"error": "no such emoto"}, status=400)
    except ValueError:
        return JsonResponse({"error": "malformed json"}, status=400)

@csrf_exempt
def set_location(request, username):
    try:
        profile = Profile.objects.get(username=username)
        props = json.loads(request.body.decode("utf-8"))
        log.info(props)
    
        missing = missing_props(props, ["latitude", "longitude"])
        if missing: 
            return JsonResponse({"error": "missing properties: {}".format(", ".join(missing))}, status=400)
        profile.latitude = props['latitude']
        profile.longitude = props['longitude']
        profile.reload_cache()
        profile.clean()
        profile.save()
        return JsonResponse(profile.status_json())
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "no such user"}, status=400)
    except ValueError:
        return JsonResponse({"error": "malformed json"}, status=400)

@csrf_exempt
def pair(request, username, pair_code):
    try:
        profile = Profile.objects.get(username=username)
        partner = Profile.objects.get(pair_code=pair_code)
        if profile.partner or partner.partner:
            return JsonResponse({"error": "user already paired"}, status=400)
        profile.partner = partner
        partner.partner = profile
        profile.save()
        partner.save()
        return JsonResponse({
            "self": profile.status_json(),
            "partner": profile.partner.status_json() if profile.partner else None
        })
            
    except Profile.DoesNotExist:
        return JsonResponse({"error": "no such user"}, status=400)

@csrf_exempt
def unpair(request, username):
    try:
        profile = Profile.objects.get(username=username)
        if not profile.partner:
            return JsonResponse({"error": "user not paired"}, status=400)
        partner = profile.partner
        profile.partner = None
        profile.pair_code = generate_pair_code()
        profile.message_set.clear()
        partner.partner = None
        partner.pair_code = generate_pair_code()
        partner.message_set.clear()
        profile.save()
        partner.save()
        return JsonResponse({
            "self": profile.status_json(),
            "partner": profile.partner.status_json() if profile.partner else None
        })
    except Profile.DoesNotExist:
        return JsonResponse({"error": "no such user"}, status=400)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)

def emotos(request):
    emotos = Emoto.objects.filter(available=True).all()
    return JsonResponse({"emotos": [e.json() for e in emotos]})
