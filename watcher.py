"""
FileWatcher and Runner file for advent-of-code days and years
"""

import pathlib
import re
from typing import Optional
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import click


class PathNotFound(Exception):
    ...


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, module, klass, data_path):
        self.module = module
        self.klass = klass
        self.data = data_path
        super().__init__()

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")
        module = importlib.reload(self.module)
        obj = getattr(module, self.klass)()

        for indx, test in enumerate(obj.TESTS, start=1):
            try:
                obj.run_test(test)
                print(f"Test {indx}: Passed. Expected: {test.expects} Received: {obj.run_part(test.part, test.data)}")
            except AssertionError:
                print(f"Test {indx}: Failed. Expected: {test.expects} Received: {obj.run_part(test.part, test.data)}")

class Runner:
    """Main Challenge runner class"""

    def __init__(self, year, day, root_path_dir):
        self.year = year
        self.day = day
        self.root_path_dir = root_path_dir

    @property
    def code_path(self):
        """Property for fetching the module path that will be hot loaded"""
        return self.root_path_dir / "years" / f"{self.year}/d{self.day:02}.py"

    @property
    def data_path(self):
        """Property for fetching path to data used"""
        return self.root_path_dir / "data" / f"{self.year}/d{self.day:02}.py"

    @property
    def module_path(self):
        return f"years.{self.year}.d{self.day:02}"

    @property
    def module_class(self):
        """Property for building class name for module"""
        return f"D{self.day:02}"

    def run_test(self):
        """Runner method for running the tests cases only"""
        # TODO: How would I run just the tests
        return

    def live_solve(self):
        """Runner method to observe changes to file and rerun tests"""
        # Initial Import of Module and instantiation of Class
        module = importlib.import_module(self.module_path)
        obj = getattr(module, self.module_class)()

        for indx, test in enumerate(obj.TESTS, start=1):
            try:
                obj.run_test(test)
                print(f"Test {indx}: Passed. Expected: {test.expects} Received: {obj.run_part(test.part, test.data)}")
            except AssertionError:
                print(f"Test {indx}: Failed. Expected: {test.expects} Received: {obj.run_part(test.part, test.data)}")
        try:
            print(f"Watching Path {self.code_path}")
            event_handler = MyEventHandler(module, self.module_class, str(self.data_path))
            observer = Observer()
            observer.schedule(
                event_handler, path=self.code_path, recursive=True
            )  # '.' indicates the current directory
            observer.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
        except ModuleNotFoundError as exc:
            raise exc


@click.command()
@click.option("--date", "-d", type=str, required=False, help="YYYY/dd")
@click.option("--day", type=int, required=False, help="AoC day")
@click.option("--year", type=int, required=False, help="AoC year")
@click.option(
    "--live",
    "-l",
    is_flag=True,
    help="Solve advent-of-code for a single Day and Year watching for changes and running tests.",
)
@click.option(
    "--test", "-t", is_flag=True, help="Run Test for a specific Year and Day."
)
def main(
    date: Optional[str],
    day: Optional[int],
    year: Optional[int],
    live: bool,
    test: bool,
) -> None:
    """
    Main Method that kicks off either the Runner or the Watch and Run
    """
    if date and not (day and year):
        m = re.search(r"^(?P<year>\d{2}|\d{4})/(?P<day>\d{1,2})$", date)
        if not m:
            print("Unable to get year and date from date format.")
            return

        try:
            year = int(m.group("year"))
            day = int(m.group("day"))
        except ValueError:
            print("Unable to derive Year and Day from date input. Format: YYYY/DD")
            return
        if year < 2000:
            year += 2000

    root_path_dir = pathlib.Path(__file__).parent

    if live:
        return Runner(year, day, root_path_dir).live_solve()

    if test:
        return Runner(year, day, root_path_dir).run_test()


if __name__ == "__main__":
    main()
