from django import template
from django.utils.http import urlquote
from django.utils.safestring import mark_safe

register = template.Library()

EXIF_DATA = [
    ('Image Make', 'Constructeur'),
    ('Image Model', 'Appareil Photo'),
    ('EXIF BrightnessValue', 'Luminosité'),
    ('EXIF ExposureTime', 'Temps d’exposition'),
    ('EXIF FocalLength', 'Longueur Focale'),
    ('EXIF ShutterSpeedValue', 'Vitesse d’obturateur'),
    ('EXIF ISOSpeedRatings', 'Vitesse ISO'),
    ('EXIF SceneCaptureType', 'Type de scène'),
    ('EXIF WhiteBalance', 'Balance des blancs'),
    ('EXIF MeteringMode', 'Metering'),
]


@register.simple_tag
def url_get(request, key=None, value=None):
    get = request.GET.copy()
    if key:
        get[key] = value
    return "?%s" % get.urlencode()


@register.filter
def email(email, request):
    if request.user.is_authenticated():
        content = '<a href="mailto:%s">%s</a>' % (email, email)
    else:
        at, dot = ('<span class="%s"></span>' % i for i in ['at', 'dot'])
        content = email.replace('@', at).replace('.', dot)
    return mark_safe('<span class="mail">%s</span>' % content)

@register.simple_tag
def exif(photo):
    tags = photo.EXIF()
    ret = ['<dl class="dl-horizontal">']
    for key, val in EXIF_DATA:
        if key in tags:
            ret.append('<dt>%s:</dt>' % val)
            ret.append('<dd>%s</dd>' % tags[key])
    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        lat = '''%i°%i'%i"''' % tuple(i.num / i.den for i in tags['GPS GPSLatitude'].values)
        lat += tags['GPS GPSLatitudeRef'].values
        lon = '''%i°%i'%i"''' % tuple(i.num / i.den for i in tags['GPS GPSLongitude'].values)
        lon += tags['GPS GPSLongitudeRef'].values
        url = 'www.google.fr/maps/place/%s, %s' % (lat, lon)
        ret.append('<dt>Coordonnées approximatives:</dt>')
        ret.append('<dd><a href="https://%s">%s, %s</a></dd>' % (urlquote(url), lat, lon))
    ret.append('<dl>')
    return mark_safe('\n'.join(ret))
