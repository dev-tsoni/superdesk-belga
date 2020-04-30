import logging
from uuid import uuid4

from superdesk.metadata.item import GUID_FIELD
from superdesk.signals import item_create, item_update


logger = logging.getLogger(__name__)


def set_belga_url_ids(item):
    # URL in a context of belga360 system is a standalone news item with it's own id
    # URL's id (`Duid` in the NewsML output) is reused between updates/translations
    for url in [i for i in item.get('extra', {}).get('belga-url', []) if not i.get(GUID_FIELD)]:
        url[GUID_FIELD] = str(uuid4())


def handle_create(sender, item):
    set_belga_url_ids(item)


def handle_update(sender, updates, original):
    set_belga_url_ids(updates)


def init_app(_app):
    item_create.connect(handle_create)
    item_update.connect(handle_update)
