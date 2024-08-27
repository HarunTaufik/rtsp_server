#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GstRtspServer

Gst.init(None)

class RTSPServer(GstRtspServer.RTSPServer):
    def __init__(self):
        super().__init__()
        self.set_address('0.0.0.0')  # Bind to all interfaces
        self.set_service('8554')     # Default RTSP port

        self.factory = GstRtspServer.RTSPMediaFactory()
        self.factory.set_launch("( v4l2src ! videoconvert ! x264enc ! rtph264pay name=pay0 )")
        self.factory.set_shared(True)

        self.get_mount_points().add_factory('/stream', self.factory)

        self.attach(None)

if __name__ == '__main__':
    server = RTSPServer()
    loop = GObject.MainLoop()
    loop.run()
