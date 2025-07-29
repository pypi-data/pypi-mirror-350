# langxchange/agent_memory_helper.py

import os
import sqlite3
import uuid
from datetime import datetime
from typing import List, Tuple

import pandas as pd
from chromadb import Client
from chromadb.config import Settings

class AgentMemoryHelper:
    """
    Manages per-agent conversational memory:
      - Stores every turn in SQLite (agent_id, timestamp, role, text)
      - Embeds and indexes each turn in ChromaDB for semantic search
    """

    def __init__(
        self,
        llm_helper,
        sqlite_path: str = "agent_memory.db",
        chroma_persist: str = None
    ):
        # LLM helper must provide get_embedding(text)->List[float]
        if not hasattr(llm_helper, "get_embedding"):
            raise ValueError("llm_helper must implement .get_embedding(text)")

        self.llm = llm_helper

        # --- SQLite setup ---
        self.conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        self._init_sqlite()

        # --- ChromaDB setup ---
        persist = chroma_persist or os.getenv("CHROMA_PERSIST_PATH", "./chroma_memory")
        self.chroma = Client(Settings(persist_directory=persist))

    def _init_sqlite(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            agent_id TEXT,
            timestamp TEXT,
            role      TEXT,
            text      TEXT
        )""")
        self.conn.commit()

    def add_memory(self, agent_id: str, role: str, text: str):
        """Add a new message turn to SQLite and ChromaDB for this agent."""
        timestamp = datetime.utcnow().isoformat()
        # 1) SQLite
        self.conn.execute(
            "INSERT INTO memory (agent_id,timestamp,role,text) VALUES (?,?,?,?)",
            (agent_id, timestamp, role, text)
        )
        self.conn.commit()

        # 2) Chroma: one collection per agent
        col_name = f"memory_{agent_id}"
        coll = self.chroma.get_or_create_collection(name=col_name)

        # embed
        emb = self.llm.get_embedding(text)
        # use uuid for id
        rec_id = str(uuid.uuid4())
        coll.add(
            ids=[rec_id],
            documents=[text],
            embeddings=[emb],
            metadatas=[{"role": role, "timestamp": timestamp}]
        )

    def get_recent(
        self,
        agent_id: str,
        n: int = 10
    ) -> List[Tuple[str, str, str]]:
        """
        Return the last n turns as a list of tuples:
          [(timestamp, role, text), ...], most recent last.
        """
        c = self.conn.cursor()
        c.execute("""
            SELECT timestamp, role, text 
              FROM memory 
             WHERE agent_id = ? 
          ORDER BY timestamp DESC 
             LIMIT ?
        """, (agent_id, n))
        rows = c.fetchall()
        # reverse to chronological order
        return list(reversed(rows))

    def search_memory(
        self,
        agent_id: str,
        query: str,
        top_k: int = 5
    ) -> List[Tuple[str, str, str]]:
        """
        Perform semantic search over this agent's memory.
        Returns top_k matching turns as (timestamp, role, text).
        """
        col_name = f"memory_{agent_id}"
        coll = self.chroma.get_or_create_collection(name=col_name)

        q_emb = self.llm.get_embedding(query)
        results = coll.query(
            query_embeddings=[q_emb],
            n_results=top_k,
            include=["metadatas", "documents"]
        )
        out = []
        for meta, doc in zip(results["metadatas"][0], results["documents"][0]):
            out.append((meta["timestamp"], meta["role"], doc))
        return out

    def clear_memory(self, agent_id: str):
        """Delete all history for the given agent."""
        # SQLite
        self.conn.execute("DELETE FROM memory WHERE agent_id = ?", (agent_id,))
        self.conn.commit()
        # Chroma
        col_name = f"memory_{agent_id}"
        try:
            self.chroma.delete_collection(name=col_name)
        except Exception:
            pass
