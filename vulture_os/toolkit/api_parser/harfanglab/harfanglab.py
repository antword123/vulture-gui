#!/home/vlt-os/env/bin/python
"""This file is part of Vulture OS.

Vulture OS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Vulture OS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Vulture OS.  If not, see http://www.gnu.org/licenses/.
"""
__author__ = "Kevin GUILLEMOT"
__credits__ = []
__license__ = "GPLv3"
__version__ = "4.0.0"
__maintainer__ = "Vulture OS"
__email__ = "contact@vultureproject.org"
__doc__ = 'HarfangLab EDR API Parser'


import logging
import requests

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from toolkit.api_parser.api_parser import ApiParser

from datetime import datetime, timedelta
import json

logging.config.dictConfig(settings.LOG_SETTINGS)
logger = logging.getLogger('crontab')


class HarfangLabAPIError(Exception):
    pass



class HarfangLabParser(ApiParser):
    VERSION = "api/version/"
    STATUS = "api/status/"
    CONFIG = "api/config/"
    ALERTS = "api/data/alert/alert/Alert/"
    ALERT_DETAILS = "api/data/alert/alert/Alert/{id}/details/"
    AGENT = "api/data/endpoint/Agent/"
    AGENT_STATS = "api/data/endpoint/Agent/dashboard_stats/"
    POLICY = "api/data/endpoint/Policy/"


    HEADERS = {
        "Content-Type": "application/json",
        'Accept': 'application/json'
    }

    def __init__(self, data):
        super().__init__(data)

        self.harfanglab_host = data["harfanglab_host"].rstrip("/")
        if not self.harfanglab_host.startswith('https://'):
            self.harfanglab_host = f"https://{self.harfanglab_host}"

        self.harfanglab_apikey = data["harfanglab_apikey"]

        self.session = None


    def _connect(self):
        try:
            if self.session is None:
                self.session = requests.Session()

                headers = self.HEADERS
                headers.update({'Authorization': f"Token {self.harfanglab_apikey}"})

                self.session.headers.update(headers)

                response = self.session.get(
                    f'{self.harfanglab_host}/{self.VERSION}',
                    timeout=10,
                    proxies=self.proxies
                )
                assert response.status_code == 200

            return True

        except Exception as err:
            raise HarfangLabAPIError(err)


    def __execute_query(self, method, url, query, timeout=10):
        '''
        raw request dosent handle the pagination natively
        '''
        self._connect()

        if (method == "GET"):
            response = self.session.get(url, params=query, headers=self.HEADERS, timeout=timeout, proxies=self.proxies)
        elif (method == "POST"):
            response = self.session.post(url, data=json.dumps(query), headers=self.HEADERS, timeout=timeout, proxies=self.proxies)
        else:
            raise HarfangLabAPIError(f"Error at HarfangLab request, unknown method : {method}")

        # response.raise_for_status()
        if response.status_code != 200:
            raise HarfangLabAPIError(f"Error at HarfangLab API Call URL: {url} Code: {response.status_code} Content: {response.content}")

        return response.json()


    def test(self):
        try:
            result = self.get_logs(timezone.now()-timedelta(hours=24), timezone.now())

            return {
                "status": True,
                "data": result
            }
        except Exception as e:
            logger.exception(e)
            return {
                "status": False,
                "error": str(e)
            }


    def get_logs(self, since=None, to=None, index=0):
        alert_url = f"{self.harfanglab_host}/{self.ALERTS}"
        # Remove miliseconds - format not supported
        since_utc = since.isoformat().split('.')[0] + "+00:00"
        to_utc = to.isoformat().split('.')[0] + "+00:00"
        payload = {
            'offset': index,
            'limit': 100, # Mandatory
            'from': since_utc,
            'to': to_utc,
            'ordering': '-last_seen',
            'status': 'new,investigating,probable_false_positive'
        }
        return self.__execute_query("GET", alert_url, payload)

    def format_log(self, log):
        log['url'] = f"{self.harfanglab_host}"
        return json.dumps(log)


    def execute(self):

        since = self.last_api_call or (timezone.now() - timedelta(days=7))
        to = timezone.now()
        logger.info(f"HarfangLab API parser starting from {since} to {to}.")

        index = 0
        total = 1
        while index < total:

            response = self.get_logs(since, to, index)

            # Downloading may take some while, so refresh token in Redis
            self.update_lock()

            logs = response['results']

            total = int(response['count'])
            logger.debug(f"HarfangLab API parser: got {total} lines available")

            if total == 0:
                # Means that there are no logs available. It may be for two
                # reasons: no log during this period or logs not available at
                # request time.
                # If there are no logs, no need to write them and we should not
                # set the last_api_call.
                break

            index += len(logs)
            logger.debug(f"HarfangLab API parser: retrieved {index} lines")

            self.write_to_file([self.format_log(l) for l in logs])

            # Writting may take some while, so refresh token in Redis
            self.update_lock()

            # increment by 1ms to avoid repeating a line if its timestamp happens to be the exact timestamp 'to'
            self.frontend.last_api_call = datetime.fromtimestamp(logs[0]['last_seen']) + timedelta(microseconds=1000)
            self.frontend.save()

        logger.info("HarfangLab API parser ending.")
