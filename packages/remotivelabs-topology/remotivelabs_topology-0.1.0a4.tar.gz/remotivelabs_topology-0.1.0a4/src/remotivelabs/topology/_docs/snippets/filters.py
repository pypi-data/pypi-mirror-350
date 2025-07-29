from remotivelabs.topology.namespaces.filters import AllFrames, Frame

filters1 = [
    AllFrames(),
    Frame(frame_name="Frame1", include=False),
]
filters2 = [
    Frame(frame_name="Frame1", include=False),
    AllFrames(),
]
