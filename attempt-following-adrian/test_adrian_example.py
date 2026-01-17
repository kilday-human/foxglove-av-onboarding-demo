import foxglove as fg
from foxglove.schemas import Pose, PoseInFrame, Quaternion, Timestamp, Vector3

fg.start_server()

with fg.open_mcap("foo.mcap"):
   fg.log("/example", PoseInFrame(
       timestamp=Timestamp(sec=0),
       frame_id="ego",
       pose=Pose(
           position=Vector3(x=1.0, y=2.0, z=3.0),
           orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0),
       ),
   ))