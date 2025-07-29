from feng_tools.base.re.re_tools import get_match_first_group


def parse_event(msg):
    return get_match_first_group(r'<Event><!\[CDATA\[(.*?)\]\]></Event>', msg)


def parse_event_key(msg):
    return get_match_first_group(r'<EventKey><!\[CDATA\[(.*?)\]\]></EventKey>', msg)


def parse_ticket(msg):
    return get_match_first_group(r'<Ticket><!\[CDATA\[(.*?)\]\]></Ticket>', msg)


def parse_location_x(msg):
    return get_match_first_group(r'<Longitude>(.*?)</Longitude>', msg)


def parse_location_y(msg):
    return get_match_first_group(r'<Latitude>(.*?)</Latitude>', msg)


def parse_location_precision(msg):
    return get_match_first_group(r'<Precision>(.*?)</Precision>', msg)
