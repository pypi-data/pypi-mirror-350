import asyncio
import time
import cv2
import numpy as np
from threading import Thread
from sil_sdk.client.vis_async_client import VISAsyncClient

class VISModule:
    def __init__(self, server_uri="ws://localhost:4201", start_server=True):
        self.loop = asyncio.new_event_loop()
        Thread(target=self._start_loop, daemon=True).start()
        if start_server:
            pass
        self.client = VISAsyncClient(server_uri)
        self._run(self.client.connect())

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result()

    def load(self, modules):
        if isinstance(modules, str):
            modules = [modules]
        for m in modules:
            self._run(self.client.load_module(m))

    def single(self, module, window_name="OneShot", timeout=5.0):
        data = self._run(self.client.run_module(module))
        self._run(self.client.stop_module(module))
        print("Detection Result:", data["result"])
        img = data["image"]
        for d in data["result"].get("detections", []):
            if "bbox" in d:
                x1,y1,x2,y2 = map(int, d["bbox"])
                label = f"{d['label']} {d.get('confidence',0):.2f}"
                cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(img, label, (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            if "mask" in d:
                pts = np.array(d["mask"], np.int32)
                cv2.polylines(img, [pts], True, (0,255,0), 2)
                overlay = img.copy()
                cv2.fillPoly(overlay, [pts], (0,255,0))
                cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
            if "track_id" in d:
                pts = np.array(d.get("mask",[]), np.int32)
                if pts.size:
                    M = cv2.moments(pts)
                    if M["m00"]>0:
                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])
                    else:
                        cx,cy = pts[0]
                else:
                    cx,cy = 10,30
                cv2.putText(img, f"ID:{d['track_id']}", (cx,cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyWindow(window_name)

    def live(self, module, window_name="Live", fps=20.0):
        self._run(self.client.run_module(module))
        delay = int(1000/fps)
        last_id = None
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        while True:
            r = self.client.results.get(module)
            if r:
                print("Detection Result:", r["result"])
                fid = r["result"].get("frame_info",{}).get("frame_id")
                if fid is not None and fid != last_id:
                    last_id = fid
                    img = r["image"].copy()
                    for d in r["result"].get("detections", []):
                        if "bbox" in d:
                            x1,y1,x2,y2 = map(int, d["bbox"])
                            label = f"{d['label']} {d.get('confidence',0):.2f}"
                            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
                            cv2.putText(img, label, (x1,y1-10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                        if "mask" in d:
                            pts = np.array(d["mask"], np.int32)
                            cv2.polylines(img, [pts], True, (0,255,0), 2)
                            overlay = img.copy()
                            cv2.fillPoly(overlay, [pts], (0,255,0))
                            cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
                        if "track_id" in d:
                            pts = np.array(d.get("mask",[]), np.int32)
                            if pts.size:
                                M = cv2.moments(pts)
                                if M["m00"]>0:
                                    cx = int(M["m10"]/M["m00"])
                                    cy = int(M["m01"]/M["m00"])
                                else:
                                    cx,cy = pts[0]
                            else:
                                cx,cy = 10,30
                            cv2.putText(img, f"ID:{d['track_id']}", (cx,cy),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
                    cv2.imshow(window_name, img)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        cv2.destroyWindow(window_name)
        self._run(self.client.stop_module(module))

    def unload(self, module):
        """
        Completely unload this module on the server (frees GPU/model memory).
        """
        self.client.results.pop(module, None)
        self._run(self.client.unload_module(module))

    def close(self):
        self._run(self.client.close())
        self.loop.call_soon_threadsafe(self.loop.stop)
