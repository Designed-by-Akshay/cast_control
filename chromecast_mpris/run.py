from typing import Optional
from time import sleep
import logging
import sys

from mpris_server.server import Server

from .base import get_chromecast, Seconds, get_chromecast_via_host, \
  NoChromecastFoundException, RC_NO_CHROMECAST
from .adapter import ChromecastAdapter
from .listeners import register_mpris_adapter


DEFAULT_WAIT: Seconds = 30


def create_adapters_and_server(
  chromecast_name: Optional[str],
  host: Optional[str],
) -> Optional[Server]:
  if host:
    chromecast = get_chromecast_via_host(host)

  elif chromecast_name:
    chromecast = get_chromecast(chromecast_name)

  else:
    chromecast = get_chromecast()

  if not chromecast:
    return

  chromecast_adapter = ChromecastAdapter(chromecast)
  mpris = Server(name=chromecast.name, adapter=chromecast_adapter)
  mpris.publish()

  register_mpris_adapter(chromecast, mpris, chromecast_adapter)

  return mpris


def retry_until_found(
  name: Optional[str],
  host: Optional[str],
  wait: Optional[Seconds] = DEFAULT_WAIT,
  log_level: int = logging.DEBUG,
) -> Optional[Server]:
  """
    If the Chromecast isn't found, keep trying to find it.

    If `wait` is None, then retrying is disabled.
  """

  while True:
    mpris = create_adapters_and_server(name, host)

    if mpris or wait is None:
      return mpris

    logging.info(f"{name} not found. Waiting {wait} seconds before retrying.")
    sleep(wait)


def run_server(
  name: Optional[str],
  host: Optional[str],
  wait: Optional[Seconds] = DEFAULT_WAIT,
  log_level: int = logging.WARN,
):
  logging.basicConfig(level=log_level)
  mpris = retry_until_found(name, host, wait, log_level)

  if not mpris:
    raise NoChromecastFoundException(name)

  mpris.loop()

