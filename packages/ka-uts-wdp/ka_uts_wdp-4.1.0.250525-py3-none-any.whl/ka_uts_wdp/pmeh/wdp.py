"""
This module provides task scheduling classes for the management of OmniTracker
SRR (NHRR) processing for Department UMH.
    SRR: Sustainability Risk Rating
    NHRR: Nachhaltigkeits Risiko Rating
"""
import os
import glob
import time

from ka_uts_log.log import LogEq
from ka_uts_log.log import Log
from ka_uts_dic.dic import Dic
from ka_uts_path.pathnm import PathNm
from ka_uts_path.path import Path, AoPath
from ka_uts_uts.utils.srv import Srv

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from typing import Any
TyArr = list[Any]
TyDic = dict[Any, Any]
TyStr = str
TyPath = str
TyAoPath = list[str]

TnPath = None | TyPath


class PmeHandler(PatternMatchingEventHandler):
    """
    WatchDog Event Handler for pattern matching of files paths
    """
    msg_evt: TyStr = "Watchdog received {E} - {P}"
    msg_exe: TyStr = "Watchdog executes script: {S}"

    def __init__(self, patterns, scripts):
        # Set the patterns for PatternMatchingEventHandler
        # self.kwargs = kwargs
        super().__init__(
                patterns=patterns,
                ignore_patterns=None,
                ignore_directories=True,
                case_sensitive=False)
        self.scripts = scripts

    def ex(self):
        """
        Process created or modified event
        """
        Log.debug(f"Watchdog executes scripts: {self.scripts}")
        for _script in self.scripts:
            Log.debug(f"Watchdog executes script: {_script}")
            os.system(_script)

    def on_created(self, event):
        """
        Process 'files paths are created' event
        """
        Log.debug(f"Watchdog received created event = {event} for path = {event.src_path}")
        self.ex()

    def on_modified(self, event):
        """
        Process 'files paths are modified' event
        """
        _path = event.src_path
        Log.debug(f"Watchdog received modified event = {event} for path = {_path}")
        self.ex()


class WdP:
    """
    Watch Dog Processor
    """
    @staticmethod
    def ex_last(kwargs: TyDic) -> None:
        """
        Execute Script of all files changed or created since last
        service shutdown
        """
        _scripts: TyArr = Dic.get_as_array(kwargs, 'scripts')
        LogEq.debug("_scripts", _scripts)

    @staticmethod
    def sh_scripts(kwargs: TyDic) -> TyArr:
        """
        WatchDog Task for pattern matching of files paths
        """
        _scripts: TyArr = Dic.get_as_array(kwargs, 'scripts')
        LogEq.debug("_scripts", _scripts)

        _scripts_new = []
        for _script in _scripts:
            LogEq.debug("_script", _script)
            _script = Path.sh_path_by_tpl(_script, kwargs)
            LogEq.debug("_script", _script)
            _scripts_new.append(_script)
        LogEq.debug("_scripts_new", _scripts_new)
        return _scripts_new

    @classmethod
    def pmeh(cls, kwargs: TyDic) -> None:
        """
        WatchDog Task for pattern matching of files paths
        """
        _in_dir = PathNm.sh_path('in_dir', kwargs)
        _in_patterns: TyArr = Dic.get_as_array(kwargs, 'in_patterns')
        _scripts: TyArr = cls.sh_scripts(kwargs)
        _sw_ex_gt_threshold = kwargs.get('sw_ex_gt_threshold', False)

        LogEq.debug("_in_dir", _in_dir)
        LogEq.debug("_in_patterns", _in_patterns)
        LogEq.debug("_scripts", _scripts)

        _pmehandler = PmeHandler(_in_patterns, _scripts)

        if _sw_ex_gt_threshold:
            _a_path: TyAoPath = []
            for _path in _in_patterns:
                _path = os.path.join(_in_dir, _path)
                _a_path = _a_path + glob.glob(_path)
            Log.debug(f"_a_path: {_a_path} for _in_dir: {_in_dir}, _in_patterns: {_in_patterns}")

            _service_name = kwargs.get('service_name', '')
            _start_timestamp = Srv.get_start_timestamp(_service_name)
            if _start_timestamp:
                _a_path = AoPath.sh_aopath_mtime_gt_threshold(_a_path, _start_timestamp)
            Log.debug(f"_a_path: {_a_path} after selection by threshhold: {_start_timestamp}")
            if len(_a_path) > 0:
                _pmehandler.ex()

        _observer = Observer()
        _observer.schedule(_pmehandler, path=_in_dir, recursive=False)
        _observer.start()

        _sleep: int = kwargs.get('sleep', 1)
        try:
            while True:
                time.sleep(_sleep)
        except KeyboardInterrupt:
            _observer.stop()
        _observer.join()
