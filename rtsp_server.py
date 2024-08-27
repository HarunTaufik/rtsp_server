import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class RTSPMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        pipeline_str = "( videotestsrc ! x264enc ! rtph264pay name=pay0 pt=96 )"
        return Gst.parse_launch(pipeline_str)

class GstServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        self.server.attach(None)

        factory = RTSPMediaFactory()
        factory.set_shared(True)

        mount_points = self.server.get_mount_points()
        mount_points.add_factory("/test", factory)

        print("RTSP server is live at rtsp://localhost:8554/test")

        GObject.MainLoop().run()

if __name__ == '__main__':
    Gst.init(None)
    server = GstServer()