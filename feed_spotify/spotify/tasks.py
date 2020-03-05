import csv
import requests
import datetime

from contextlib import closing
from dateutil.relativedelta import relativedelta
from time import sleep
from traceback import print_exc

from feed_spotify.settings import COUNTRIES, CELERY_ENABLED
from feed_spotify.celery import app as celery_app
from spotify.models import Hit, Track

END_DATE = datetime.date.today()
START_DATE = datetime.date(2016, 12, 30)
WEEK_DELTA = relativedelta(weeks=1)


@celery_app.task(bind=True)
def async_ingest_csv_for_week(country, week_of):
    _ingest_csv_for_week(country, week_of)


@celery_app.task(bind=True)
def async_set_metrics(track):
    track.set_metrics()


def feed_spotify_charts(start_date=START_DATE, end_date=END_DATE, use_async=CELERY_ENABLED):
    """
    For every combination of start date and country, update the db.
    Asynchronous has not been fully implemented yet. Need Google Cloud deployable redis or other broker
    """

    for country in COUNTRIES:
        week_of = start_date
        while week_of < end_date:
            try:
                if use_async:
                    async_ingest_csv_for_week.delay(country, week_of)
                else:
                    _ingest_csv_for_week(country, week_of)
            except Exception:
                print_exc()
            week_of += WEEK_DELTA


def _ingest_csv_for_week(country, week_of):

    week_range = "{}--{}".format((week_of - WEEK_DELTA).strftime("%Y-%m-%d"), week_of.strftime("%Y-%m-%d"))
    url = "https://spotifycharts.com/regional/{}/weekly/{}/download".format(country, week_range)
    for pos, name, artist, streams, uri in parse_by_hit(url):
        try:
            Hit.set(name, uri, artist, pos, streams, country, week_of)
        except Exception:
            print_exc()


def parse_by_hit(target_url):
    with closing(requests.get(target_url, stream=True)) as streaming:
        file_like = (line.decode('utf-8') for line in streaming.iter_lines())
        reader = csv.reader(file_like, delimiter=',', quotechar='"')
        for row in reader:
            if not row[0]:
                continue
            position, name, artist, streams, url = row
            uri = url.split('/')[-1]
            yield int(position), name, artist, int(streams), uri


def compute_track_metrics(use_async=CELERY_ENABLED):
    """
    Request metrics per each track in db. Bulk operations require talking to Spotify for api access
    Add sleep to not anger spotify lords until operations access is granted
    """

    # arbitrary field check to not update already loaded tracks
    for track in Track.objects.filter(duration__is_null=False):
        if use_async:
            async_set_metrics.delay(track)
        else:
            sleep(2)
            track.set_metrics()













