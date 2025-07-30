from ipykernel.kernelbase import Kernel
from wollok_kernel.wollok_bridge.library import execute_repl
import json
import ast

class WollokKernel(Kernel):
    implementation = "Wollok"
    implementation_version = "1.2"
    language = "wollok"
    language_version = "3.3.1"
    language_info = {
        "name": "wollok",
        "mimetype": "text/plain",
        "file_extension": ".wlk",
    }
    banner = "Wollok >>> kernel"

    def do_execute(
        self,
        code: str,
        silent: bool,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        if not silent:
            result = execute_repl(code)
            stream_content = {"name": "stdout", "text": result, "data": result}
            self.send_response(self.iopub_socket, "stream", stream_content)

        return {
            "status": "ok",
            # The base class increments the execution count
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

    def do_apply(self, content: str, bufs, msg_id: str, reply_metadata):
        return {"status": "ok", "started": True}
