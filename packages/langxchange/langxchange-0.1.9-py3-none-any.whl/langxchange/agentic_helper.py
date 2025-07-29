# langxchange/agentic_helper.py

import yaml
import time
from datetime import datetime
from typing import Any, Dict, List
from langxchange.mysql_helper import MySQLHelper
from langxchange.data_format_cleanup_helper import DataFormatCleanupHelper
from langxchange.chroma_helper import ChromaHelper
from langxchange.openai_helper import OpenAIHelper
from langxchange.file_helper import FileHelper

class AgenticHelper:
    """
    A lightweight agent runner that:
     - Loads a YAML config of named steps
     - Executes each action in sequence
     - Optionally loops at a fixed interval
    """

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.cfg = yaml.safe_load(f)
        self.context: Dict[str, Any] = {}
        # Instantiate helpers up-front
        self.helpers = {
            "mysql": MySQLHelper(),
            "cleanup": DataFormatCleanupHelper(llm_helper=OpenAIHelper()),
            "chroma": ChromaHelper(llm_helper=OpenAIHelper()),
            "llm": OpenAIHelper(),
            "file": FileHelper(),
        }

    def _run_action(self, action: Dict[str, Any]):
        t = action["type"]
        p = action.get("params", {})
        name = action.get("name")

        if t == "mysql_query":
            df = self.helpers["mysql"].query(p["query"])
            self.context[name or "last_df"] = df

        elif t == "cleanup":
            df = self.context.get("last_df")
            df_clean, records = self.helpers["cleanup"].clean(
                df, output_format=p.get("output_format", "json")
            )
            self.context[name or "cleaned"] = df_clean

        elif t == "chroma_ingest":
            df = self.context.get("cleaned")
            coll = p["collection_name"]
            count = self.helpers["chroma"].ingest_to_chroma(
                df, coll, text_column=p.get("text_column")
            )
            self.context[name or "ingested_count"] = count

        elif t == "llm_chat":
            prompt = p["prompt_template"].format(
                **{k: self.context.get(k, "") for k in p.get("format_keys", [])}
            )
            resp = self.helpers["llm"].chat([{"role":"user","content":prompt}])
            self.context[p.get("output_key", "llm_output")] = resp

        elif t == "file_write":
            content = self.context[p["content_key"]]
            path = p["path"].format(timestamp=datetime.utcnow().strftime("%Y%m%d%H%M"))
            self.helpers["file"]._write_text(path, content)
            self.context[name or "last_file"] = path

        else:
            raise ValueError(f"Unknown action type: {t}")

    def run(self):
        mode     = self.cfg.get("run_mode", "once")
        interval = self.cfg.get("interval", 0)

        def single_run():
            for action in self.cfg["actions"]:
                self._run_action(action)

        if mode == "once":
            single_run()
        elif mode == "loop":
            while True:
                single_run()
                time.sleep(interval)
        else:
            raise ValueError(f"Unsupported run_mode: {mode}")
