import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class RTSPMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        # GStreamer pipeline for capturing video from the camera
        # Adjust "v4l2src" to the correct camera source if necessary
        pipeline_str = (
            "v4l2src ! video/x-raw, width=640, height=480 ! videoconvert ! "
            "x264enc ! rtph264pay name=pay0 pt=96"
        )
        return Gst.parse_launch(pipeline_str)

class GstServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        self.server.attach(None)

        factory = RTSPMediaFactory()
        factory.set_shared(True)

        mount_points = self.server.get_mount_points()
        mount_points.add_factory("/camera", factory)

        print("RTSP server is live at rtsp://localhost:8554/camera")

        GObject.MainLoop().run()

if __name__ == '__main__':
    Gst.init(None)
    server = GstServer()
