from __future__ import annotations

from typing import Protocol, override, runtime_checkable

from mpris_server import DbusObj, LoopStatus, Microseconds, Paths, PlayState, Rate, ValidMetadata, Volume
from pychromecast.controllers.media import MediaController, MediaStatus
from pychromecast.controllers.receiver import CastStatus
from pychromecast.socket_client import ConnectionStatus

from .base import DEFAULT_ICON, Device, NAME
from .device.base import CachedIcon, Controllers, Titles


@runtime_checkable
class CliIntegration(Protocol):
  def set_icon(self, lighter: bool = False): ...


@runtime_checkable
class ListenerIntegration(Protocol):
  def on_new_status(self, *args, **kwargs):
    """Callback for event listener"""


@runtime_checkable
class ModuleIntegration(Protocol):
  def get_duration(self) -> Microseconds: ...


@runtime_checkable
class Statuses(Protocol):
  @property
  def cast_status(self) -> CastStatus | None: ...

  @property
  def connection_status(self) -> ConnectionStatus | None: ...

  @property
  def media_controller(self) -> MediaController: ...

  @property
  def media_status(self) -> MediaStatus | None: ...


@runtime_checkable
class Properties(Protocol):
  device: Device
  controllers: Controllers

  cached_icon: CachedIcon | None = None
  light_icon: bool = DEFAULT_ICON

  @property
  def name(self) -> str:
    return self.device.name or NAME

  @property
  def is_youtube(self) -> bool: ...

  @property
  def titles(self) -> Titles: ...


@runtime_checkable
class AdapterIntegration(Protocol):
  def add_track(self, uri: str, after_track: DbusObj, set_as_current: bool): ...

  def can_control(self) -> bool: ...

  def can_edit_tracks(self) -> bool: ...

  def can_pause(self) -> bool: ...

  def can_play(self) -> bool: ...

  def can_play_next(self) -> bool: ...

  def can_play_prev(self) -> bool: ...

  def can_quit(self) -> bool: ...

  def can_seek(self) -> bool: ...

  def get_art_url(self, track: int | None = None) -> str: ...

  def get_desktop_entry(self) -> Paths: ...

  def get_playstate(self) -> PlayState: ...

  def get_rate(self) -> Rate: ...

  def get_shuffle(self) -> bool: ...

  def get_stream_title(self) -> str: ...

  def get_tracks(self) -> list[DbusObj]: ...

  def get_volume(self) -> Volume: ...

  def has_tracklist(self) -> bool: ...

  def has_current_time(self) -> bool: ...

  def is_mute(self) -> bool: ...

  def is_playlist(self) -> bool: ...

  def is_repeating(self) -> bool: ...

  def metadata(self) -> ValidMetadata: ...

  def next(self): ...

  def open_uri(self, uri: str): ...

  def pause(self): ...

  def play(self): ...

  def previous(self): ...

  def quit(self): ...

  def resume(self): ...

  def seek(self, time: Microseconds, track_id: DbusObj | None = None): ...

  def set_loop_status(self, value: LoopStatus): ...

  def set_mute(self, value: bool): ...

  def set_rate(self, value: Rate): ...

  def set_repeating(self, value: bool): ...

  def set_shuffle(self, value: bool): ...

  def set_volume(self, value: Volume): ...

  def stop(self): ...


@runtime_checkable
class Wrapper(
  AdapterIntegration,
  CliIntegration,
  ListenerIntegration,
  ModuleIntegration,
  Properties,
  Statuses,
  Protocol
):
  pass


@runtime_checkable
class DeviceIntegration[W: Wrapper](CliIntegration, ListenerIntegration, ModuleIntegration, Protocol):
  wrapper: W

  @override
  def get_duration(self) -> Microseconds:
    return self.wrapper.get_duration()

  @override
  def on_new_status(self, *args, **kwargs):
    self.wrapper.on_new_status(*args, **kwargs)

  @override
  def set_icon(self, lighter: bool = False):
    self.wrapper.set_icon(lighter)
