# SIL-SDK

**SIL Robotics SDK** for interacting with **SAR grippers**, **DAG dexterous hands**, and **VIS vision systems** over WebSockets.

Built and maintained by **Sastra Innovation Labs**.

---

## Features

- **VIS Module**:
  - Run inference on multiple vision models (e.g., object detection, segmentation).
  - Supports concurrent module execution.

- **SAR Gripper**:
  - Set grasp commands, velocity, stroke limits, and force thresholds.
  - Continuously fetch gripper status.

- **DAG Dexterous Hand**:
  - Configure joint positions, grasp modes, and forces.
  - Retrieve joint-level feedback like currents, forces, and strokes.

---

## Quick Start

```bash
pip install sil-sdk
```

```python
from sil_sdk.modules.vis import VISModule

vis = VISModule("ws://<server-ip>:8765")
vis.load(["obj_detection", "gdino"])
vis.run("obj_detection")
result = vis.get_result("obj_detection")
```

---

## License

**Proprietary - Sastra Innovation Labs**

This software is the property of **Sastra Innovation Labs**. Unauthorized copying, distribution, modification, or use is prohibited.

```
