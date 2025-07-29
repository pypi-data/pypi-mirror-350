# vis.py

import asyncio
import time
import cv2
from threading import Thread
from sil_sdk.client.vis_async_client import VISAsyncClient

class VISModule:
    def __init__(self, server_uri="ws://localhost:4201", start_server=True):
        # Start an asyncio loop in a background thread
        self.loop = asyncio.new_event_loop()
        Thread(target=self._start_loop, daemon=True).start()

        # Skip any built-in server when used as a remote client
        if start_server:
            pass

        # Underlying async WebSocket client
        self.client = VISAsyncClient(server_uri)
        # Ensure connection + listener are running
        self._run(self.client.connect())

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run(self, coro):
        # Helper to run coroutines on our background loop
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result()

    def load(self, module):
        self._run(self.client.load_module(module))

    def _start_module(self, module):
        self.load(module)
        self._run(self.client.run_module(module))

    def stop(self, module):
        self._run(self.client.stop_module(module))

    def close(self):
        self._run(self.client.close())
        # Stop our asyncio loop
        self.loop.call_soon_threadsafe(self.loop.stop)

    def get_latest(self, module):
        """Fetch the most recent result dict for `module`, or None."""
        return self.client.results.get(module)

    def single(self,
               module: str,
               window_name: str = "OneShot",
               timeout: float = 5.0,
               poll: float = 0.02):
        """
        Run exactly one inference pass:
         - loads & starts `module`
         - waits until the first result arrives (or timeout)
         - prints the detection log
         - shows the image in a window (press any key to close)
         - stops the module
        """
        self._start_module(module)
        start = time.time()
        while True:
            r = self.get_latest(module)
            if r:
                # Restore the log print
                print("Detection Result:", r["result"])
                self.stop(module)

                img = r["image"]
                # Draw detections on the image (if any)
                for d in r["result"].get("detections", []):
                    x1, y1, x2, y2 = d["bbox"]
                    label = f"{d['label']} {d['confidence']:.2f}"
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                cv2.imshow(window_name, img)
                cv2.waitKey(0)
                cv2.destroyWindow(window_name)
                return

            if time.time() - start > timeout:
                self.stop(module)
                cv2.destroyAllWindows()
                raise TimeoutError(f"{module} did not respond within {timeout}s")
            time.sleep(poll)

    def live(self,
             module: str,
             window_name: str = "Live",
             fps: float = 20.0):
        """
        Continuous live inference:
         - loads & starts `module`
         - opens a named window
         - on each new frame, prints the detection log, draws boxes, and displays
         - blocks until you press 'q'
         - stops the module and closes the window
        """
        self._start_module(module)
        delay = int(1000 / fps)
        last_id = None

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        while True:
            r = self.get_latest(module)
            if r:
                # Print every time we get a new frame's result
                print("Detection Result:", r["result"])

                # Only update the display when frame_id changes
                info = r["result"].get("frame_info", {})
                fid = info.get("frame_id")
                if fid is not None and fid != last_id:
                    last_id = fid
                    img = r["image"]
                    # Draw detections
                    for d in r["result"].get("detections", []):
                        x1, y1, x2, y2 = d["bbox"]
                        label = f"{d['label']} {d['confidence']:.2f}"
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    cv2.imshow(window_name, img)

            # Quit on 'q'
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        cv2.destroyWindow(window_name)
        self.stop(module)
