import re

import argparse

import logging

from datetime import datetime, timedelta

from pathlib import Path

from typing import Any


class RecordData:
    """
    Зберігає інфу про гонщика, часові мітки старту та фінішу.
    """

    # винесений патерн для парсингу abbreviation.txt
    ABBREVIATION_PATTERN = re.compile(r"^([A-Z]{3})_(.*?)_(.*?)$")

    # винесений патерн для парсингу start.log, end.log
    TIMESTAMP_PATTERN = re.compile(
        r"^([A-Z]{3})(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\.\d{3})$"
    )

    def __init__(
        self,
        abbr: str = None,
        driver: str = None,
        team: str = None,
        start: datetime = None,
        stop: datetime = None,
    ):
        self.abbr = abbr
        self.driver = driver
        self.team = team
        self.start = start
        self.stop = stop
        self.errors: list[str] = []

    def __str__(self):
        # форматуємо вивід - і без помилки
        duration = self.duration
        formatted_time = (
            f"{int(duration.total_seconds() // 60)}:{duration.total_seconds() % 60:.3f}"
            if duration
            else "N/A"
        )
        errors = f" | Errors: {', '.join(self.errors)}" if self.errors else ""
        return f"{self.driver:20} | {self.team:25} | {formatted_time}{errors}"

    @property
    def duration(self) -> timedelta | None:
        # валідація на відсутність start або stop/ або start >= stop ---> self.errors
        if not (self.start and self.stop):
            self.errors.append("Missing start or stop time.")
            return None
        if self.start >= self.stop:
            self.errors.append("Start time is later than or equal to stop time.")
            return None
        return self.stop - self.start

    @classmethod
    def _read_abbreviation(
        cls,
        file: Path,
    ) -> dict[str, "RecordData"]:
        # перевірити наявність папки
        # перевірити наявність файлу
        # прочитати файл
        # валідувати рядки (формат)
        # зберегти в словник

        if not file.is_file():
            raise FileNotFoundError(f"File not found: {file}")

        records = {}

        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                match = cls.ABBREVIATION_PATTERN.match(line)
                if match:
                    abbr, driver, team = match.groups()
                    records[abbr] = cls(abbr, driver, team)
                else:
                    error_record = cls(driver="Unknown", team="Unknown")
                    error_record.errors.append(f"Incorrect format: {line}")
                    records[f"ERROR_{len(records)}"] = error_record
        return records

    @staticmethod
    def _read_start_stop(
        records_dict: dict[str, "RecordData"],
        file: Path,
        start: bool = True,
    ) -> dict[str, "RecordData"]:
        # перевірити наявність файлу
        # прочитати файл
        # валідувати рядки (формат)
        # можливі помилки: відсутня abbr
        # додати дані для відповідного запису (abbr) у відповідне поле (start or stop)
        if not file.is_file():
            raise FileNotFoundError(f"File not found: {file}")

        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                match = RecordData.TIMESTAMP_PATTERN.match(line)
                abbr = line[:3]

                if abbr not in records_dict:
                    records_dict[abbr] = RecordData(abbr=abbr)

                if match:
                    _, timestamp = match.groups()

                    try:
                        time = datetime.strptime(timestamp, "%Y-%m-%d_%H:%M:%S.%f")

                        if start:
                            records_dict[abbr].start = time
                        else:
                            records_dict[abbr].stop = time
                    except ValueError:
                        raise ValueError(
                            f"Incorrect timestamp: {timestamp}"
                        )
                else:
                    # logging.warning(f"Incorrect format: {line}")
                    print(f"Incorrect format: {line}")

        return records_dict

    def build_report(
        self,
        file: Path,
        start_file: Path,
        stop_file: Path,
        asc: bool = True,
        driver: str | None = None,
    ) -> tuple[list["RecordData"], list["RecordData"]]:
        # читаємо abbreviation.txt
        records_dict: dict[str, RecordData] = self._read_abbreviation(file)
        # читаємо стартові дані
        records_dict = self._read_start_stop(
            records_dict, start_file, start=True
        )
        # читаємо фінішні дані
        records_dict = self._read_start_stop(
            records_dict, stop_file, start=False
        )

        valid_records = [r for r in records_dict.values() if not r.errors and r.duration is not None]
        invalid_records = [r for r in records_dict.values() if r.errors or r.duration is None]

        valid_records.sort(key=lambda r: r.duration, reverse=not asc)

        if driver:
            # фільтруємо good_records по driver
            valid_records = [r for r in valid_records if r.driver == driver]

        return valid_records, invalid_records

    @staticmethod
    def print_report(
        valid_results: list["RecordData"],
        invalid_results: list["RecordData"] | None,
        underline: int = 15,
    ) -> str:
        if not valid_results and not invalid_results:
            return "No data to display."
        # форматуємо вивід good_records
        # якщо bad_records не None, форматуємо вивід bad_records
        # повертаємо вивід

        report_output = [
            "\nVALID RESULTS",
            *(
                f"{idx:2}. {racer}" + ("\n" + "-" * 70 if idx == underline else "")
                for idx, racer in enumerate(valid_results, start=1)
            ),
        ]

        if invalid_results:
            report_output.append("\nINVALID RECORDS")
            for error_racer in invalid_results:
                report_output.append(str(error_racer))

        report_text = "\n".join(report_output)
        print(report_text)

    @staticmethod
    def cli() -> dict[str, Any]:
        parser = argparse.ArgumentParser(
            description="F1 Qualification Report Generator"
        )

        base_dir = Path(__file__).resolve().parent
        data_dir = base_dir / "data"

        parser.add_argument(
            "--files",
            nargs=3,
            metavar=("ABBR", "START", "STOP"),
            type=Path,
            default=[
                data_dir / "abbreviations.txt",
                data_dir / "start.log",
                data_dir / "end.log",
            ],
            help="Paths to files (abbreviations.txt, start.log, end.log)."
            "Defaults: <package_path>/data/abbreviations.txt etc.",
        )

        parser.add_argument(
            "--asc", action="store_true", help="Sort in ascending order (default)."
        )
        parser.add_argument(
            "--desc", action="store_true", help="Sort in order of descent."
        )
        parser.add_argument(
            "--driver", type=str, help="Filter Report by the Name of the driver."
        )

        args = parser.parse_args()

        if args.asc and args.desc:
            parser.error("Cannot be used at the same time --asc, --desc.")

        return {
            "abbreviations": args.files[0],
            "start_log": args.files[1],
            "stop_log": args.files[2],
            "asc": args.asc or not args.desc,
            "driver": args.driver,
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        cli_args = RecordData.cli()
        record = RecordData()
        good_records, bad_records = record.build_report(
            file=cli_args["abbreviations"],
            start_file=cli_args["start_log"],
            stop_file=cli_args["stop_log"],
            asc=cli_args["asc"],
            driver=cli_args["driver"],
        )

        print(RecordData.print_report(good_records, bad_records))

    except FileNotFoundError as e:
        logging.error(f"Critical error: {e}")
