# coding: utf-8

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import subprocess

from scrapy import Spider

class Crawler:
    @classmethod
    def execute(cls, spider: Spider) -> List[Dict]:
        now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_file = f"/tmp/articles_{now}.json"
        logs_file = f"/tmp/articles_logs_{now}.json"
        subprocess.run(
            [
                "scrapy", "runspider", "app/spiders.py",
                "-a", f"NAME={spider.__name__}",
                "--output", output_file,
                "--logfile", logs_file
            ]
        )
        return json.loads(Path(output_file).read_text())