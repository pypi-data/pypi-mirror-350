import asyncio
import time
import cv2
from threading import Thread
from sil_sdk.client.vis_async_client import VISAsyncClient

class VISModule:
    def __init__(self, server_uri="ws://localhost:4201", start_server=True):
        self.loop = asyncio.new_event_loop()
        self.background = Thread(target=self._start_loop, daemon=True)
        self.background.start()

        # Skip the bundled server when used as a remote client
        if start_server:
            pass

        self.client = VISAsyncClient(server_uri)
        # ensure WS+listener started
        self._run(self.client.connect())

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result()

    def load(self, module):
        self._run(self.client.load_module(module))

    def _start_module(self, module):
        self.load(module)
        self._run(self.client.run_module(module))

    def stop(self, module):
        self._run(self.client.stop_module(module))

    def close(self):
        # stop everything
        self._run(self.client.close())
        self.loop.call_soon_threadsafe(self.loop.stop)

    def get_latest(self, module):
        """Internal: grab whatever’s currently in the client results dict."""
        return self.client.results.get(module)

    def single(self, module, timeout=5.0, poll=0.02):
        """
        Block until the *first* result arrives, then return (image, result_dict).
        """
        self._start_module(module)
        start = time.time()
        while True:
            r = self.get_latest(module)
            if r:
                self.stop(module)
                return r["image"], r["result"]
            if time.time() - start > timeout:
                self.stop(module)
                raise TimeoutError(f"{module} didn’t respond in {timeout}s")
            time.sleep(poll)

    def live(self, module, window_name="Live", fps=20.0):
        """
        Block and show a window with live detections.
        Press 'q' in the window to quit.
        """
        self._start_module(module)
        delay = int(1000 / fps)
        last_id = None

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        while True:
            r = self.get_latest(module)
            if r:
                info = r["result"].get("frame_info", {})
                fid = info.get("frame_id")
                if fid is not None and fid != last_id:
                    last_id = fid
                    img = r["image"]
                    # draw detections if they exist
                    for d in r["result"].get("detections", []):
                        x1, y1, x2, y2 = d["bbox"]
                        label = f"{d['label']} {d['confidence']:.2f}"
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
                        cv2.putText(img, label, (x1, y1-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                    cv2.imshow(window_name, img)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        cv2.destroyWindow(window_name)
        self.stop(module)
