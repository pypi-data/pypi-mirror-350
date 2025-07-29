import json
import os
from pathlib import Path
import subprocess
import threading
import traceback
from typing import IO, Callable, Any, Dict, List, Literal, NewType, Union
from unittest import TextTestRunner, registerResult, TestSuite, TestCase, TextTestResult
import random
import warnings
from dataclasses import dataclass, asdict
import requests
from .absDriver import AbstractDriver
from functools import wraps
from time import sleep
from .adbUtils import push_file
from .logWatcher import LogWatcher
from .utils import TimeStamp, getProjectRoot, getLogger
from .u2Driver import StaticU2UiObject
import uiautomator2 as u2
import types
PRECONDITIONS_MARKER = "preconds"
PROP_MARKER = "prop"


logger = getLogger(__name__)


# Class Typing
PropName = NewType("PropName", str)
PropertyStore = NewType("PropertyStore", Dict[PropName, TestCase])

TIME_STAMP = TimeStamp().getTimeStamp()
LOGFILE = f"fastbot_{TIME_STAMP}.log"
RESFILE = f"result_{TIME_STAMP}.json"

def precondition(precond: Callable[[Any], bool]) -> Callable:
    """the decorator @precondition

    The precondition specifies when the property could be executed.
    A property could have multiple preconditions, each of which is specified by @precondition.
    """
    def accept(f):
        @wraps(f)
        def precondition_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        preconds = getattr(f, PRECONDITIONS_MARKER, tuple())

        setattr(precondition_wrapper, PRECONDITIONS_MARKER, preconds + (precond,))

        return precondition_wrapper

    return accept

def prob(p: float):
    """the decorator @prob

    The prob specify the propbability of execution when a property is satisfied.
    """
    p = float(p)
    if not 0 < p <= 1.0:
        raise ValueError("The propbability should between 0 and 1")
    def accept(f):
        @wraps(f)
        def precondition_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        setattr(precondition_wrapper, PROP_MARKER, p)

        return precondition_wrapper

    return accept


@dataclass
class Options:
    """
    Kea and Fastbot configurations
    """
    # the driver_name in script (if self.d, then d.) 
    driverName: str
    # the driver (only U2Driver available now)
    Driver: AbstractDriver
    # list of package names. Specify the apps under test
    packageNames: List[str]
    # target device
    serial: str = None
    # test agent. "native" for stage 1 and "u2" for stage 1~3
    agent: Literal["u2", "native"] = "u2"
    # max step in exploration (availble in stage 2~3)
    maxStep: Union[str, float] = float("inf")
    # time(mins) for exploration
    running_mins: int = 10
    # time(ms) to wait when exploring the app
    throttle: int = 200
    # the output_dir for saving logs and results
    output_dir: str = "output"

    def __post_init__(self):
        if self.serial and self.Driver:
            self.Driver.setDeviceSerial(self.serial)


@dataclass
class PropStatistic:
    precond_satisfied: int = 0
    executed: int = 0
    fail: int = 0
    error: int = 0

class PBTTestResult(dict):
    def __getitem__(self, key) -> PropStatistic:
        return super().__getitem__(key)


def getFullPropName(testCase: TestCase):
    return ".".join([
        testCase.__module__,
        testCase.__class__.__name__,
        testCase._testMethodName
    ])

class JsonResult(TextTestResult):
    res: PBTTestResult

    @classmethod
    def setProperties(cls, allProperties: Dict):
        cls.res = dict()
        for testCase in allProperties.values():
            cls.res[getFullPropName(testCase)] = PropStatistic()

    def flushResult(self, outfile):
        json_res = dict()
        for propName, propStatitic in self.res.items():
            json_res[propName] = asdict(propStatitic)
        with open(outfile, "w", encoding="utf-8") as fp:
            json.dump(json_res, fp, indent=4)

    def addExcuted(self, test: TestCase):
        self.res[getFullPropName(test)].executed += 1

    def addPrecondSatisfied(self, test: TestCase):
        self.res[getFullPropName(test)].precond_satisfied += 1

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.res[getFullPropName(test)].fail += 1

    def addError(self, test, err):
        super().addError(test, err)
        self.res[getFullPropName(test)].error += 1


def activateFastbot(options: Options, port=None) -> threading.Thread:
    """
    activate fastbot.
    :params: options: the running setting for fastbot
    :params: port: the listening port for script driver
    :return: the fastbot daemon thread
    """
    cur_dir = Path(__file__).parent
    push_file(
        Path.joinpath(cur_dir, "assets/monkeyq.jar"),
        "/sdcard/monkeyq.jar",
        device=options.serial
    )
    push_file(
        Path.joinpath(cur_dir, "assets/fastbot-thirdpart.jar"),
        "/sdcard/fastbot-thirdpart.jar",
        device=options.serial,
    )
    push_file(
        Path.joinpath(cur_dir, "assets/framework.jar"), 
        "/sdcard/framework.jar",
        device=options.serial
    )
    push_file(
        Path.joinpath(cur_dir, "assets/fastbot_libs/arm64-v8a"),
        "/data/local/tmp",
        device=options.serial
    )
    push_file(
        Path.joinpath(cur_dir, "assets/fastbot_libs/armeabi-v7a"),
        "/data/local/tmp",
        device=options.serial
    )
    push_file(
        Path.joinpath(cur_dir, "assets/fastbot_libs/x86"),
        "/data/local/tmp",
        device=options.serial
    )
    push_file(
        Path.joinpath(cur_dir, "assets/fastbot_libs/x86_64"),
        "/data/local/tmp",
        device=options.serial
    )

    t = startFastbotService(options)
    print("[INFO] Running Fastbot...", flush=True)

    return t


def check_alive(port):
    """
    check if the script driver and proxy server are alive.
    """
    for _ in range(10):
        sleep(2)
        try:
            requests.get(f"http://localhost:{port}/ping")
            return
        except requests.ConnectionError:
            print("[INFO] waiting for connection.", flush=True)
            pass
    raise RuntimeError("Failed to connect fastbot")


def startFastbotService(options: Options) -> threading.Thread:
    shell_command = [
        "CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar",
        "exec", "app_process",
        "/system/bin", "com.android.commands.monkey.Monkey",
        "-p", *options.packageNames,
        "--agent-u2" if options.agent == "u2" else "--agent", 
        "reuseq",
        "--running-minutes", f"{options.running_mins}",
        "--throttle", f"{options.throttle}",
        "--bugreport", "--output-directory", "/sdcard/fastbot_report"
        "-v", "-v", "-v"
    ]

    full_cmd = ["adb"] + (["-s", options.serial] if options.serial else []) + ["shell"] + shell_command

    outfile = open(LOGFILE, "w", encoding="utf-8", buffering=1)

    print("[INFO] Options info: {}".format(asdict(options)), flush=True)
    print("[INFO] Launching fastbot with shell command:\n{}".format(" ".join(full_cmd)), flush=True)
    print("[INFO] Fastbot log will be saved to {}".format(outfile.name), flush=True)

    # process handler
    proc = subprocess.Popen(full_cmd, stdout=outfile, stderr=outfile)
    t = threading.Thread(target=close_on_exit, args=(proc, outfile), daemon=True)
    t.start()

    return t


def close_on_exit(proc: subprocess.Popen, f: IO):
    proc.wait()
    f.close()
  

class KeaTestRunner(TextTestRunner):

    resultclass: JsonResult
    allProperties: PropertyStore
    options: Options = None
    _block_widgets_funcs = None

    @classmethod
    def setOptions(cls, options: Options):
        if not isinstance(options.packageNames, list) and len(options.packageNames) > 0:
            raise ValueError("packageNames should be given in a list.")
        if options.Driver is not None and options.agent == "native":
            print("[Warning] Can not use any Driver when runing native mode.", flush=True)
            options.Driver = None
        cls.options = options

    def _setOuputDir(self):
        output_dir = Path(self.options.output_dir).absolute()
        output_dir.mkdir(parents=True, exist_ok=True)
        global LOGFILE, RESFILE
        LOGFILE = output_dir / Path(LOGFILE)
        RESFILE = output_dir / Path(RESFILE)

    def run(self, test):

        self.allProperties = dict()
        self.collectAllProperties(test)

        if len(self.allProperties) == 0:
            print("[Warning] No property has been found.", flush=True)

        self._setOuputDir()

        JsonResult.setProperties(self.allProperties)
        self.resultclass = JsonResult

        result: JsonResult = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals

        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ["default", "always"]:
                    warnings.filterwarnings(
                        "module",
                        category=DeprecationWarning,
                        message=r"Please use assert\w+ instead.",
                    )

            t = activateFastbot(options=self.options)
            log_watcher = LogWatcher(LOGFILE)
            if self.options.agent == "native":
                t.join()
            else:
                # initialize the result.json file
                result.flushResult(outfile=RESFILE)
                # setUp for the u2 driver
                self.scriptDriver = self.options.Driver.getScriptDriver()
                check_alive(port=self.scriptDriver.lport)

                end_by_remote = False
                step = 0
                while step < self.options.maxStep:

                    step += 1
                    print("[INFO] Sending monkeyEvent {}".format(
                        f"({step} / {self.options.maxStep})" if self.options.maxStep != float("inf")
                        else f"({step})"
                        )
                    , flush=True)

                    try:
                        propsSatisfiedPrecond = self.getValidProperties()
                    except requests.ConnectionError:
                        print(
                            "[INFO] Exploration times up (--running-minutes)."
                        , flush=True)
                        end_by_remote = True
                        break

                    print(f"{len(propsSatisfiedPrecond)} precond satisfied.", flush=True)

                    # Go to the next round if no precond satisfied
                    if len(propsSatisfiedPrecond) == 0:
                        continue

                    # get the random probability p
                    p = random.random()
                    propsNameFilteredByP = []
                    # filter the properties according to the given p
                    for propName, test in propsSatisfiedPrecond.items():
                        result.addPrecondSatisfied(test)
                        if getattr(test, "p", 1) >= p:
                            propsNameFilteredByP.append(propName)

                    if len(propsNameFilteredByP) == 0:
                        print("Not executed any property due to probability.", flush=True)
                        continue

                    execPropName = random.choice(propsNameFilteredByP)
                    test = propsSatisfiedPrecond[execPropName]
                    # Dependency Injection. driver when doing scripts
                    self.scriptDriver = self.options.Driver.getScriptDriver()
                    setattr(test, self.options.driverName, self.scriptDriver)
                    print("execute property %s." % execPropName, flush=True)

                    result.addExcuted(test)
                    try:
                        test(result)
                    finally:
                        result.printErrors()

                    result.flushResult(outfile=RESFILE)

                if not end_by_remote:
                    self.stopMonkey()
                result.flushResult(outfile=RESFILE)

            print(f"Finish sending monkey events.", flush=True)
            log_watcher.close()
            self.tearDown()

        # Source code from unittest Runner
        # process the result
        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(
                len,
                (result.expectedFailures, result.unexpectedSuccesses, result.skipped),
            )
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        self.stream.flush()
        return result

    def stepMonkey(self) -> str:
        """
        send a step monkey request to the server and get the xml string.
        """
        block_widgets: List[str] = self._getBlockedWidgets()
        URL = f"http://localhost:{self.scriptDriver.lport}/stepMonkey"
        r = requests.post(
            url=URL,
            json={
                "block_widgets": block_widgets
            }
        )

        res = json.loads(r.content)
        xml_raw = res["result"]
        return xml_raw

    def stopMonkey(self) -> str:
        """
        send a stop monkey request to the server and get the xml string.
        """
        r = requests.get(f"http://localhost:{self.scriptDriver.lport}/stopMonkey")

        res = r.content.decode(encoding="utf-8")
        print(f"[Server INFO] {res}", flush=True)

    def getValidProperties(self) -> PropertyStore:

        xml_raw = self.stepMonkey()
        staticCheckerDriver = self.options.Driver.getStaticChecker(hierarchy=xml_raw)

        validProps: PropertyStore = dict()
        for propName, test in self.allProperties.items():
            valid = True
            prop = getattr(test, propName)
            # check if all preconds passed
            for precond in prop.preconds:
                # Dependency injection. Static driver checker for precond
                setattr(test, self.options.driverName, staticCheckerDriver)
                # excecute the precond
                try:
                    if not precond(test):
                        valid = False
                        break
                except Exception as e:
                    print(f"[ERROR] Error when checking precond: {getFullPropName(test)}", flush=True)
                    traceback.print_exc()
                    valid = False
                    break
            # if all the precond passed. make it the candidate prop.
            if valid:
                validProps[propName] = test
        return validProps

    def collectAllProperties(self, test: TestSuite):
        """collect all the properties to prepare for PBT
        """

        def remove_setUp(testCase: TestCase):
            """remove the setup function in PBT
            """
            def setUp(self): ...
            testCase.setUp = types.MethodType(setUp, testCase)

        def remove_tearDown(testCase: TestCase):
            """remove the tearDown function in PBT
            """
            def tearDown(self): ...
            testCase = types.MethodType(tearDown, testCase)
        
        def iter_tests(suite):
            for test in suite:
                if isinstance(test, TestSuite):
                    yield from iter_tests(test)
                else:
                    yield test

        # Traverse the TestCase to get all properties
        for t in iter_tests(test):
            testMethodName = t._testMethodName
            # get the test method name and check if it's a property
            testMethod = getattr(t, testMethodName)
            if hasattr(testMethod, PRECONDITIONS_MARKER):
                # remove the hook func in its TestCase
                remove_setUp(t)
                remove_tearDown(t)
                # save it into allProperties for PBT
                self.allProperties[testMethodName] = t
                print(f"[INFO] Load property: {getFullPropName(t)}", flush=True)
    
    @property
    def _blockWidgetFuncs(self):
        if self._block_widgets_funcs is None:
            self._block_widgets_funcs = list()
            root_dir = getProjectRoot()
            if root_dir is None or not os.path.exists(
                file_block_widgets := root_dir / "configs" / "widget.block.py"
            ):
                print(f"[WARNING] widget.block.py not find", flush=True)
            

            def __get_block_widgets_module():
                import importlib.util
                module_name = "block_widgets"
                spec = importlib.util.spec_from_file_location(module_name, file_block_widgets)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod

            mod = __get_block_widgets_module()

            import inspect
            for func_name, func in inspect.getmembers(mod, inspect.isfunction):
                if func_name.startswith("block_") or func_name == "global_block_widgets":
                    if getattr(func, PRECONDITIONS_MARKER, None) is None:
                        if func_name.startswith("block_"):
                            logger.warning(f"No precondition in block widget function: {func_name}. Default globally active.")
                        setattr(func, PRECONDITIONS_MARKER, (lambda d: True, ))
                    self._block_widgets_funcs.append(func)

        return self._block_widgets_funcs

    def _getBlockedWidgets(self):
        blocked_widgets = list()
        for func in self._blockWidgetFuncs:
            try:
                script_driver = self.options.Driver.getScriptDriver()
                preconds = getattr(func, PRECONDITIONS_MARKER)
                if all([precond(script_driver) for precond in preconds]):
                    _widgets = func(self.options.Driver.getStaticChecker())
                    if not isinstance(_widgets, list):
                        _widgets = [_widgets]
                    for w in _widgets:
                        if isinstance(w, StaticU2UiObject):
                            blocked_widgets.append(w._getXPath(w.selector))
                        elif isinstance(w, u2.xpath.XPathSelector):
                            def getXPathRepr(w):
                                return w._parent.xpath
                            blocked_widgets.append(getXPathRepr(w))
                        else:
                            logger.warning(f"{w} Not supported")
                    # blocked_widgets.extend([
                    #     w._getXPath(w.selector) for w in _widgets
                    # ])
            except Exception as e:
                logger.error(f"error when getting blocked widgets: {e}")
                import traceback
                traceback.print_exc()

        return blocked_widgets

    def tearDown(self):
        # TODO Add tearDown method (remove local port, etc.)
        pass
