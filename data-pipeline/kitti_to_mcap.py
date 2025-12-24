#!/usr/bin/env python3
"""
KITTI to MCAP Converter
Converts KITTI dataset (LiDAR + Camera) to MCAP format for Foxglove Studio.

Usage:
    python kitti_to_mcap.py --kitti_dir /path/to/kitti --output output.mcap
"""

import argparse
import os
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from mcap.writer import Writer
from foxglove_schemas_protobuf.PointCloud_pb2 import PointCloud
from foxglove_schemas_protobuf.CompressedImage_pb2 import CompressedImage
from foxglove_schemas_protobuf.FrameTransforms_pb2 import FrameTransforms
from google.protobuf import descriptor_pb2


def _build_file_descriptor_set_bytes(message_descriptor) -> bytes:
    """
    Build a FileDescriptorSet (serialized) containing the given message's .proto file
    and all transitive dependencies.

    MCAP's protobuf schema encoding expects a serialized FileDescriptorSet, not a single
    FileDescriptorProto.
    """

    fds = descriptor_pb2.FileDescriptorSet()
    seen = set()

    def add_file(fd):
        # fd is a google.protobuf.descriptor.FileDescriptor (or upb equivalent)
        name = getattr(fd, "name", None)
        if not name or name in seen:
            return
        seen.add(name)

        fd_proto = descriptor_pb2.FileDescriptorProto()
        fd.CopyToProto(fd_proto)
        fds.file.append(fd_proto)

        for dep in getattr(fd, "dependencies", []) or []:
            add_file(dep)

    add_file(message_descriptor.file)
    return fds.SerializeToString()


def _set_enum_field_by_preferred_names(msg, field_name: str, preferred_names: list[str]) -> None:
    """
    Set an enum-typed field on a protobuf message by trying enum value names (case-insensitive).
    This avoids hardcoding numeric enum values across schema versions.
    """
    field_desc = msg.DESCRIPTOR.fields_by_name.get(field_name)
    if field_desc is None or field_desc.enum_type is None:
        raise ValueError(f"Field {field_name} is not an enum field on {msg.DESCRIPTOR.full_name}")

    name_to_number = {v.name.lower(): v.number for v in field_desc.enum_type.values}
    for candidate in preferred_names:
        key = candidate.lower()
        if key in name_to_number:
            setattr(msg, field_name, name_to_number[key])
            return
    raise ValueError(
        f"Enum field {field_name} on {msg.DESCRIPTOR.full_name} has values {list(name_to_number.keys())}, "
        f"none of which match {preferred_names}"
    )


def _rotation_matrix_to_quaternion_xyzw(R: np.ndarray) -> tuple[float, float, float, float]:
    """
    Convert 3x3 rotation matrix to quaternion (x, y, z, w).
    """
    R = np.asarray(R, dtype=np.float64).reshape(3, 3)
    trace = float(np.trace(R))

    if trace > 0.0:
        s = np.sqrt(trace + 1.0) * 2.0
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s
    else:
        # Find the major diagonal element
        if R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
            s = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2.0
            w = (R[2, 1] - R[1, 2]) / s
            x = 0.25 * s
            y = (R[0, 1] + R[1, 0]) / s
            z = (R[0, 2] + R[2, 0]) / s
        elif R[1, 1] > R[2, 2]:
            s = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2.0
            w = (R[0, 2] - R[2, 0]) / s
            x = (R[0, 1] + R[1, 0]) / s
            y = 0.25 * s
            z = (R[1, 2] + R[2, 1]) / s
        else:
            s = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2.0
            w = (R[1, 0] - R[0, 1]) / s
            x = (R[0, 2] + R[2, 0]) / s
            y = (R[1, 2] + R[2, 1]) / s
            z = 0.25 * s

    # Normalize
    q = np.array([x, y, z, w], dtype=np.float64)
    q /= np.linalg.norm(q) + 1e-12
    return float(q[0]), float(q[1]), float(q[2]), float(q[3])


def _parse_kitti_r_t_calib(calib_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """
    Parse KITTI calibration files like `calib_velo_to_cam.txt` / `calib_imu_to_velo.txt`
    which contain:
      R: r11 r12 ... r33
      T: t1 t2 t3
    Returns (R 3x3, T 3,).
    """
    R = None
    T = None
    with open(calib_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or ":" not in line:
                continue
            key, rest = line.split(":", 1)
            key = key.strip()
            vals = rest.strip().split()
            if key == "R":
                if len(vals) != 9:
                    raise ValueError(f"{calib_path} R: expected 9 floats, got {len(vals)}")
                R = np.array([float(x) for x in vals], dtype=np.float64).reshape(3, 3)
            elif key == "T":
                if len(vals) != 3:
                    raise ValueError(f"{calib_path} T: expected 3 floats, got {len(vals)}")
                T = np.array([float(x) for x in vals], dtype=np.float64).reshape(3)

    if R is None or T is None:
        raise ValueError(f"Failed to parse R/T from {calib_path}")
    return R, T

def read_lidar_bin(bin_path: Path) -> np.ndarray:
    """
    Read KITTI LiDAR .bin file.
    Format: 4 floats per point (x, y, z, intensity)
    """
    points = np.fromfile(str(bin_path), dtype=np.float32).reshape(-1, 4)
    return points


def read_camera_image(image_path: Path) -> np.ndarray:
    """Read KITTI camera image."""
    return cv2.imread(str(image_path))


def convert_pointcloud_to_proto(points: np.ndarray, timestamp_ns: int) -> PointCloud:
    """
    Convert numpy point cloud to Foxglove PointCloud protobuf.
    """
    pointcloud = PointCloud()
    
    # Set timestamp (field exists in foxglove schemas)
    if hasattr(pointcloud, "timestamp"):
        pointcloud.timestamp.FromNanoseconds(timestamp_ns)
    if hasattr(pointcloud, "frame_id"):
        pointcloud.frame_id = "velodyne"

    # Prefer the PointCloud2-style layout: fields + point_stride + data bytes
    if hasattr(pointcloud, "fields") and hasattr(pointcloud, "data"):
        pts = np.asarray(points, dtype=np.float32)
        if pts.ndim != 2 or pts.shape[1] < 3:
            raise ValueError(f"Expected Nx3(+), got shape {pts.shape}")

        # Ensure we have x,y,z,intensity (KITTI provides 4 floats)
        if pts.shape[1] >= 4:
            pts4 = pts[:, :4]
            field_defs = [("x", 0), ("y", 4), ("z", 8), ("intensity", 12)]
            stride = 16
        else:
            pts4 = pts[:, :3]
            field_defs = [("x", 0), ("y", 4), ("z", 8)]
            stride = 12

        # Populate fields
        del pointcloud.fields[:]
        for name, offset in field_defs:
            f = pointcloud.fields.add()
            if hasattr(f, "name"):
                f.name = name
            if hasattr(f, "offset"):
                f.offset = int(offset)
            if hasattr(f, "count"):
                f.count = 1
            # Foxglove schema uses an enum for type/datatype
            if hasattr(f, "type"):
                _set_enum_field_by_preferred_names(f, "type", ["FLOAT32", "float32"])
            elif hasattr(f, "datatype"):
                _set_enum_field_by_preferred_names(f, "datatype", ["FLOAT32", "float32"])

        # Populate stride/size fields (schema naming varies slightly across versions)
        if hasattr(pointcloud, "point_stride"):
            pointcloud.point_stride = int(stride)
        elif hasattr(pointcloud, "point_step"):
            pointcloud.point_step = int(stride)

        if hasattr(pointcloud, "point_count"):
            pointcloud.point_count = int(pts4.shape[0])
        elif hasattr(pointcloud, "width") and hasattr(pointcloud, "height"):
            # Some pointcloud schemas mirror PointCloud2's width/height
            pointcloud.width = int(pts4.shape[0])
            pointcloud.height = 1

        # Raw bytes (little-endian float32)
        pointcloud.data = np.ascontiguousarray(pts4).tobytes()
        return pointcloud

    raise RuntimeError(
        "Unsupported foxglove PointCloud schema layout. "
        f"Available fields: {[f.name for f in pointcloud.DESCRIPTOR.fields]}"
    )
    
    return pointcloud


def convert_image_to_proto(image: np.ndarray, timestamp_ns: int) -> CompressedImage:
    """
    Convert OpenCV image to Foxglove CompressedImage protobuf.
    """
    compressed_image = CompressedImage()
    
    # Set timestamp
    if hasattr(compressed_image, "timestamp"):
        compressed_image.timestamp.FromNanoseconds(timestamp_ns)
    if hasattr(compressed_image, "frame_id"):
        compressed_image.frame_id = "camera"
    
    # Compress image to JPEG
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    ok, img_data = cv2.imencode(".jpg", image, encode_param)
    if not ok:
        raise RuntimeError("cv2.imencode(.jpg) failed")
    
    compressed_image.format = "jpeg"
    compressed_image.data = img_data.tobytes()
    
    return compressed_image


def find_kitti_files(kitti_dir: Path):
    """
    Find KITTI LiDAR and camera files.
    Expected structure:
        kitti_dir/
            velodyne_points/data/  (LiDAR .bin files)
            image_02/data/         (Camera .png files)
    """
    velodyne_dir = kitti_dir / "velodyne_points" / "data"
    image_dir = kitti_dir / "image_02" / "data"
    
    if not velodyne_dir.exists():
        raise ValueError(f"LiDAR directory not found: {velodyne_dir}")
    if not image_dir.exists():
        raise ValueError(f"Camera directory not found: {image_dir}")
    
    # Get all frame indices
    lidar_files = sorted(velodyne_dir.glob("*.bin"))
    image_files = sorted(image_dir.glob("*.png"))
    
    # Match by frame number
    frames = []
    for lidar_file in lidar_files:
        frame_id = lidar_file.stem
        image_file = image_dir / f"{frame_id}.png"
        
        if image_file.exists():
            frames.append((frame_id, lidar_file, image_file))
    
    return frames


def convert_kitti_to_mcap(
    kitti_dir: Path,
    output_path: Path,
    start_time_ns: Optional[int] = None,
    frame_rate: float = 10.0,
    debug: bool = False,
    calib_dir: Optional[Path] = None,
):
    """
    Convert KITTI dataset to MCAP format.
    
    Args:
        kitti_dir: Path to KITTI dataset directory
        output_path: Path to output MCAP file
        start_time_ns: Starting timestamp in nanoseconds (default: current time)
        frame_rate: Frame rate for playback (default: 10 Hz)
    """
    import time
    
    if start_time_ns is None:
        start_time_ns = int(time.time() * 1e9)
    
    frames = find_kitti_files(kitti_dir)
    
    if len(frames) == 0:
        raise ValueError("No matching LiDAR and camera frames found!")
    
    print(f"Found {len(frames)} frames to convert")
    
    # Calculate time step per frame
    time_step_ns = int(1e9 / frame_rate)
    
    # Open MCAP writer
    with open(output_path, "wb") as f:
        writer = Writer(f)
        writer.start()
        
        # Register schemas (use descriptor-derived names + a FileDescriptorSet payload)
        pointcloud_schema = writer.register_schema(
            name=PointCloud.DESCRIPTOR.full_name,
            encoding="protobuf",
            data=_build_file_descriptor_set_bytes(PointCloud.DESCRIPTOR),
        )
        
        image_schema = writer.register_schema(
            name=CompressedImage.DESCRIPTOR.full_name,
            encoding="protobuf",
            data=_build_file_descriptor_set_bytes(CompressedImage.DESCRIPTOR),
        )
        
        # Register channels
        lidar_channel = writer.register_channel(
            schema_id=pointcloud_schema,
            topic="/velodyne_points",
            message_encoding="protobuf",
        )
        
        camera_channel = writer.register_channel(
            schema_id=image_schema,
            topic="/camera/image_raw",
            message_encoding="protobuf",
        )

        # TF / transforms
        tf_schema = writer.register_schema(
            name=FrameTransforms.DESCRIPTOR.full_name,
            encoding="protobuf",
            data=_build_file_descriptor_set_bytes(FrameTransforms.DESCRIPTOR),
        )
        tf_channel = writer.register_channel(
            schema_id=tf_schema,
            topic="/tf",
            message_encoding="protobuf",
        )

        # Publish static transforms (once at start)
        tf_msg = FrameTransforms()

        # map -> camera (identity) so Studio has a stable root frame
        t_map_cam = tf_msg.transforms.add()
        t_map_cam.timestamp.FromNanoseconds(start_time_ns)
        t_map_cam.parent_frame_id = "map"
        t_map_cam.child_frame_id = "camera"
        t_map_cam.translation.x = 0.0
        t_map_cam.translation.y = 0.0
        t_map_cam.translation.z = 0.0
        t_map_cam.rotation.x = 0.0
        t_map_cam.rotation.y = 0.0
        t_map_cam.rotation.z = 0.0
        t_map_cam.rotation.w = 1.0

        # camera -> velodyne from KITTI calibration (optional but recommended)
        if calib_dir is not None:
            velo_to_cam_path = calib_dir / "calib_velo_to_cam.txt"
            if velo_to_cam_path.exists():
                R, T = _parse_kitti_r_t_calib(velo_to_cam_path)
                qx, qy, qz, qw = _rotation_matrix_to_quaternion_xyzw(R)

                # KITTI gives: p_cam = R * p_velo + T
                # This matches a TF transform with parent=camera, child=velodyne.
                t_cam_velo = tf_msg.transforms.add()
                t_cam_velo.timestamp.FromNanoseconds(start_time_ns)
                t_cam_velo.parent_frame_id = "camera"
                t_cam_velo.child_frame_id = "velodyne"
                t_cam_velo.translation.x = float(T[0])
                t_cam_velo.translation.y = float(T[1])
                t_cam_velo.translation.z = float(T[2])
                t_cam_velo.rotation.x = qx
                t_cam_velo.rotation.y = qy
                t_cam_velo.rotation.z = qz
                t_cam_velo.rotation.w = qw
            else:
                print(f"Warning: calib_velo_to_cam.txt not found in calib_dir: {calib_dir}")

        tf_payload = tf_msg.SerializeToString()
        if debug:
            print(f"[debug] TF transforms={len(tf_msg.transforms)} serialized_bytes={len(tf_payload)}")

        writer.add_message(
            channel_id=tf_channel,
            log_time=start_time_ns,
            data=tf_payload,
            publish_time=start_time_ns,
        )
        
        # Write messages
        lidar_ok = 0
        camera_ok = 0
        lidar_fail = 0
        camera_fail = 0

        for idx, (frame_id, lidar_file, image_file) in enumerate(frames):
            timestamp_ns = start_time_ns + (idx * time_step_ns)
            
            # Convert and write LiDAR
            try:
                points = read_lidar_bin(lidar_file)
                pointcloud = convert_pointcloud_to_proto(points, timestamp_ns)
                payload = pointcloud.SerializeToString()
                if debug and idx < 3:
                    print(
                        f"[debug] LiDAR frame={frame_id} points={points.shape[0]} "
                        f"bin={lidar_file.name} serialized_bytes={len(payload)}"
                    )
                writer.add_message(
                    channel_id=lidar_channel,
                    log_time=timestamp_ns,
                    data=payload,
                    publish_time=timestamp_ns,
                )
                lidar_ok += 1
            except Exception as e:
                lidar_fail += 1
                print(f"Warning: Failed to process LiDAR frame {frame_id}: {type(e).__name__}: {e}")
                if debug:
                    import traceback

                    traceback.print_exc()
            
            # Convert and write camera
            try:
                image = read_camera_image(image_file)
                if image is None:
                    print(f"Warning: Failed to read image {image_file}")
                    camera_fail += 1
                    continue
                
                compressed_image = convert_image_to_proto(image, timestamp_ns)
                payload = compressed_image.SerializeToString()
                if debug and idx < 3:
                    print(
                        f"[debug] Camera frame={frame_id} shape={image.shape} "
                        f"png={image_file.name} jpeg_bytes={len(compressed_image.data)} serialized_bytes={len(payload)}"
                    )
                writer.add_message(
                    channel_id=camera_channel,
                    log_time=timestamp_ns,
                    data=payload,
                    publish_time=timestamp_ns,
                )
                camera_ok += 1
            except Exception as e:
                camera_fail += 1
                print(f"Warning: Failed to process camera frame {frame_id}: {type(e).__name__}: {e}")
                if debug:
                    import traceback

                    traceback.print_exc()
            
            if (idx + 1) % 10 == 0:
                print(f"Processed {idx + 1}/{len(frames)} frames...")
        
        writer.finish()
        # Ensure bytes are flushed to disk
        f.flush()
        os.fsync(f.fileno())

        print(
            f"Write summary: lidar_ok={lidar_ok} lidar_fail={lidar_fail} "
            f"camera_ok={camera_ok} camera_fail={camera_fail}"
        )

        if lidar_ok == 0 and camera_ok == 0:
            raise RuntimeError(
                "Wrote 0 messages. See warnings above; run with --debug for tracebacks."
            )

        print(f"Successfully wrote MCAP to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert KITTI dataset to MCAP format for Foxglove Studio"
    )
    parser.add_argument(
        "--kitti_dir",
        type=str,
        required=True,
        help="Path to KITTI dataset directory (should contain velodyne_points/data/ and image_02/data/ subdirectories)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="kitti_data.mcap",
        help="Output MCAP file path (default: kitti_data.mcap)",
    )
    parser.add_argument(
        "--frame_rate",
        type=float,
        default=10.0,
        help="Frame rate for playback in Hz (default: 10.0)",
    )
    parser.add_argument(
        "--calib_dir",
        type=str,
        default=None,
        help="Path to KITTI calibration directory (e.g., .../2011_09_26/ containing calib_velo_to_cam.txt, etc.)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose debug output and print tracebacks on per-frame failures",
    )
    
    args = parser.parse_args()
    
    kitti_dir = Path(args.kitti_dir)
    output_path = Path(args.output)
    calib_dir = Path(args.calib_dir) if args.calib_dir else None
    
    if not kitti_dir.exists():
        print(f"Error: KITTI directory not found: {kitti_dir}")
        return 1
    
    try:
        convert_kitti_to_mcap(
            kitti_dir=kitti_dir,
            output_path=output_path,
            frame_rate=args.frame_rate,
            debug=args.debug,
            calib_dir=calib_dir,
        )
        print(f"\n✓ Conversion complete! Open {output_path} in Foxglove Studio")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

