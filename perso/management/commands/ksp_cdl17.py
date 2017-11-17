from datetime import date

from django.core.management.base import BaseCommand

from pgp_tables.models import KeySigningParty


class Command(BaseCommand):
    help = 'Importe les clefs du Capitole du Libre 2017'

    def handle(self, *args, **options):
        url = 'https://2017.capitoledulibre.org/key-signing-party/'
        keys = ['00018C22381A7594', '00758A3D27F4C016', '03F03E6F83D97FFC', '10589E8283DDA9A7', '16CB93EB68290509',
                '18B897CC465DC339', '207C80B44CF41375', '280A3AB7E360782B', '2C7C3146C1A00121', '3517A6F8E13D17D2',
                '3679E81D48A9D950', '427EA0F091F35303', '44975278B8612B5D', '4B71F3D418018128', '4BD410C39FCD3160',
                '66FB7073264C4323', '6AC0F18E0642FA40', '6BC7FAA8D1A7E93C', '6F563E6A4DD5DCEF', '708B5F3EF3B2CEDE',
                '72BDF1A17E0C775F', '77DCC04755921A10', '7813F66B8E303172', '79B5048AF8F5F173', '7D2ACDAF4653CF28',
                '7D9DC64EC1FBEC2C', '806539FA8D18CA37', '8092859142DBD9F4', '83E7EA669A19CB94', '854D5A8433D09FB5',
                '895D3214CB0371BA', '8E3C4EDF370C8750', '8F7295985A8940A2', '92BA3F1756C27D99', 'A6EF584AF4AAF006',
                'A7C1EDDE70ACE288', 'AD9B98859D0EECA7', 'BF3D19D2970714E2', 'C71F43692D871569', 'CBA4710116D85D33',
                'DDB27EF4BD273294', 'E8E137F154AC263D', 'E98DE6D2F8840DBD', 'E9A45DC0B30F44BE', 'F0FEAEF0093AA2CB']
        ksp, created = KeySigningParty.objects.get_or_create(slug='CdL17')
        if created:
            ksp.name = 'Capitole du Libre 2017'
            ksp.detail = '<a href="%s">Capitôle du Libre 2017</a>, à Toulouse' % url
            ksp.date = date(2017, 11, 19)
            ksp.save()
        ksp.add_keys(keys)
