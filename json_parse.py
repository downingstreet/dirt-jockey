from json import JSONDecoder
from functools import partial


def json_parse(fileobj, delimiter=None, decoder=JSONDecoder(), buffersize=2048):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
        buffer += chunk
        while buffer:
            try:
                stripped = buffer.strip(delimiter)
                result, index = decoder.raw_decode(stripped)
                yield result
                buffer = stripped[index:]
            except ValueError:
                # Not enough data to decode, read more
                break
