import logging
import sys

logger = logging.getLogger("kusto-mcp")


handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger.addHandler(handler)
