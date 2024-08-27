from gi.repository import Gst, GstRtspServer
import sys

Gst.init(None)

class RTSPServer(GstRtspServer.RTSPServer):
    def __init__(self):
        super().__init__()
        self.set_service("8554")  # Port RTSP server
        self.get_mount_points().add_factory("/camera", self.create_pipeline())

    def create_pipeline(self):
        factory = GstRtspServer.RTSPMediaFactory()
        factory.set_launch(
            "v4l2src ! video/x-raw, width=640, height=480 ! videoconvert ! x264enc ! rtph264pay name=pay0"
        )
        factory.set_shared(True)
        return factory

def main():
    server = RTSPServer()
    server.attach(None)
    loop = GObject.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
