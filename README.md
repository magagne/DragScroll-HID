# Corne-Ploopy-Bridge

A small host-side bridge connecting a **Corne / ZMK keyboard** to a **Ploopy pointing device**.

Its primary purpose is to carry custom pointing-related events, such as **DRAG_SCROLL**, from the keyboard to the Ploopy.

## Architecture

```text
Corne / ZMK
     │
     ▼
Raw HID event
     │
     ▼
Corne-Ploopy-Bridge
     │
     ▼
Ploopy
