# coding: utf-8

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import subprocess

from scrapy import Spider

class Crawler:
    """ Class providing a Scrapy Spider executor. """

    _output_file = "/tmp/articles_{now}.json"
    _logs_file = "/tmp/articles_logs_{now}.json"

    def __init__(self, spider: Spider):
        self._spider = spider

    def _perform_execution(self, output_file: str, log_file: str):
        """Launch the crawl process for the associated Spider.

        Args:
            output_file (str): output file path.
            log_file (str): log file path.
        """
        subprocess.run(
            [
                "scrapy", "runspider", "app/spiders.py",
                "-a", f"NAME={self._spider.__name__}",
                "--output", output_file,
                "--logfile", log_file
            ]
        )

    def execute(self) -> List[Dict]:
        """Executes the crawl process and return the crawl result.

        Returns:
            List[Dict]: the list of elements crawled by the spider.
        """
        now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_file = self._output_file.format(now=now)
        log_file = self._logs_file.format(now=now)
        self._perform_execution(output_file=output_file, log_file=log_file)
        return json.loads(Path(output_file).read_text())