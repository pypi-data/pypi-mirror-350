from pyhik.hikvision import *
import requests
_LOGGING = logging.getLogger(__name__)

# Hide nuisance requests logging
logging.getLogger('urllib3').setLevel(logging.ERROR)


class HikCamera(HikCamera):
    def __init__(self, host=None, port=80,
                 usr=None, pwd=None, verify_ssl=True):
        if not host.startswith('http'):
            host = 'http://' + host
        super().__init__(host=host, port=port, usr=usr, pwd=pwd,
                         verify_ssl=verify_ssl)

    def alert_stream(self, reset_event, kill_event):
        """Open event stream."""
        _LOGGING.debug('Stream Thread Started: %s, %s', self.name, self.cam_id)
        start_event = False
        parse_string = ""
        fail_count = 0

        url = '%s/ISAPI/Event/notification/alertStream' % self.root_url

        # pylint: disable=too-many-nested-blocks
        while True:

            try:
                stream = self.hik_request.get(url, stream=True,
                                              timeout=(CONNECT_TIMEOUT,
                                                       READ_TIMEOUT))
                if stream.status_code == requests.codes.not_found:
                    # Try alternate URL for stream
                    url = '%s/Event/notification/alertStream' % self.root_url
                    stream = self.hik_request.get(url, stream=True)

                if stream.status_code != requests.codes.ok:
                    raise ValueError('Connection unsucessful.')
                else:
                    _LOGGING.debug('%s Connection Successful.', self.name)
                    fail_count = 0
                    self.watchdog.start()

                for line in stream.iter_lines():
                    # _LOGGING.debug('Processing line from %s', self.name)
                    # filter out keep-alive new lines
                    if line:
                        str_line = line.decode("utf-8", "ignore")
                        # New events start with --boundry
                        if str_line.find('<EventNotificationAlert') != -1:
                            # Start of event message
                            start_event = True
                            parse_string = str_line
                        elif str_line.find('</EventNotificationAlert>') != -1:
                            # Message end found found
                            parse_string += str_line
                            start_event = False
                            if parse_string:
                                try:
                                    tree = ET.fromstring(parse_string)
                                    self.process_stream(tree)
                                    self.update_stale()
                                except ET.ParseError as err:
                                    _LOGGING.warning(
                                        'XML parse error in stream.')
                                parse_string = ""
                        else:
                            if start_event:
                                parse_string += str_line

                    if kill_event.is_set():
                        # We were asked to stop the thread so lets do so.
                        break
                    elif reset_event.is_set():
                        # We need to reset the connection.
                        raise ValueError('Watchdog failed.')

                if kill_event.is_set():
                    # We were asked to stop the thread so lets do so.
                    _LOGGING.debug('Stopping event stream thread for %s',
                                   self.name)
                    self.watchdog.stop()
                    self.hik_request.close()
                    return
                elif reset_event.is_set():
                    # We need to reset the connection.
                    raise ValueError('Watchdog failed.')

            except (ValueError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError) as err:
                fail_count += 1
                reset_event.clear()
                _LOGGING.warning(
                    '%s Connection Failed (count=%d). Waiting %ss. Err: %s',
                    self.name, fail_count, (fail_count * 1) + 1, err)
                parse_string = ""
                self.watchdog.stop()
                self.hik_request.close()
                time.sleep(1)
                if self.event_states:
                    self.update_stale()
                time.sleep(fail_count * 1)
                continue

    def process_stream(self, tree):
        """Process incoming event stream packets."""
        if not self.namespace[CONTEXT_ALERT]:
            self.fetch_namespace(tree, CONTEXT_ALERT)

        try:
            etype = SENSOR_MAP[tree.find(
                self.element_query('eventType', CONTEXT_ALERT)).text.lower()]

            # Since this pasing is different and not really usefull for now, just return without error.
            if len(etype) > 0 and etype == 'Ongoing Events':
                return

            estate = tree.find(
                self.element_query('eventState', CONTEXT_ALERT)).text

            for idtype in ID_TYPES:
                echid = tree.find(self.element_query(idtype, CONTEXT_ALERT))
                if echid is not None:
                    try:
                        # Need to make sure this is actually a number
                        echid = int(echid.text)
                        break
                    except (ValueError, TypeError) as err:
                        # Field must not be an integer or is blank
                        pass

            ecount = tree.find(
                self.element_query('activePostCount', CONTEXT_ALERT)).text
        except (AttributeError, KeyError, IndexError) as err:
            if 'videoloss' in str(err):
                return
            _LOGGING.error('Problem finding attribute: %s', err)
            return