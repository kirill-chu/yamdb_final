import logging
import sys
from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(filename)s/%(funcName)s %(message)s'
)
logger.addHandler(handler)
handler.setFormatter(formatter)

User = get_user_model()

DATAPATH = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    Title: 'static/data/titles.csv',
    Title.genre.through: 'static/data/genre_title.csv',
    User: 'static/data/users.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
}


class Command(BaseCommand):
    help = 'Use this command to fill the database'

    def handle(self, *args, **options):
        for model in DATAPATH:
            logger.debug(f'Start {model.__name__} data transfer')
            try:
                objs = [
                    model.objects.create(**obj)
                    for obj in DictReader(
                        open(DATAPATH[model], encoding='utf8')
                    )
                ]
                model.objects.bulk_create(objs=objs, ignore_conflicts=True)
                logger.debug(
                    f'Data successfully loaded into {model.__name__}\n'
                )
            except Exception:
                logger.error(
                    f'We have a problem with data or {model.__name__} model\n',
                    exc_info=True
                )
