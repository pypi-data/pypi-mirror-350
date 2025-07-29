import os

from esi.clients import EsiClientProvider

from allianceauth import __version__, __title__, __url__

SWAGGER_SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

"""
Swagger spec operations:
get_killmails_killmail_id_killmail_hash
get_universe_types_type_id
"""

esi = EsiClientProvider(
    ua_appname=__title__,
    ua_version=__version__,
    ua_url=__url__,
)
