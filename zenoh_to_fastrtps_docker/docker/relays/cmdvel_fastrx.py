#!/usr/bin/env python3
import argparse, json, socket, time, signal
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelFastDDSRx(Node):
    def __init__(self, host: str, port: int, topic: str, hz: float, deadman: float):
        super().__init__("cmdvel_fastdds_rx")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(False)

        self.pub = self.create_publisher(Twist, topic, 10)
        self.msg = Twist()                     # latest command (held)
        self.zero = Twist()                    # zero command
        self.last_rx = 0.0                     # monotonic time of last received packet
        self.deadman = float(deadman)
        self.timer = self.create_timer(1.0 / max(hz, 1.0), self.tick)
        self.get_logger().info(
            f"UDP -> FastDDS relay on {host}:{port} -> {topic} @ {hz} Hz, deadman={self.deadman}s"
        )

        # publish zero on Ctrl+C/kill
        signal.signal(signal.SIGINT, lambda *_: self._stop())
        signal.signal(signal.SIGTERM, lambda *_: self._stop())

    def _stop(self):
        try:
            self.pub.publish(self.zero)
        finally:
            rclpy.shutdown()

    def tick(self):
        # Drain socket; update msg and last_rx
        while True:
            try:
                data, _ = self.sock.recvfrom(4096)
            except BlockingIOError:
                break
            try:
                d = json.loads(data.decode("utf-8"))
                self.msg.linear.x  = float(d.get("lx", 0.0))
                self.msg.linear.y  = float(d.get("ly", 0.0))
                self.msg.linear.z  = float(d.get("lz", 0.0))
                self.msg.angular.x = float(d.get("ax", 0.0))
                self.msg.angular.y = float(d.get("ay", 0.0))
                self.msg.angular.z = float(d.get("az", 0.0))
                self.last_rx = time.monotonic()
            except Exception as e:
                self.get_logger().error(f"Bad payload: {e}")

        # Deadman: if stale, publish zero instead of last
        now = time.monotonic()
        if self.last_rx == 0.0 or (now - self.last_rx) > self.deadman:
            self.pub.publish(self.zero)
        else:
            self.pub.publish(self.msg)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=20001)
    ap.add_argument("--topic", default="/leo04/cmd_vel")
    ap.add_argument("--hz", type=float, default=10.0)
    ap.add_argument("--deadman", type=float, default=0.3, help="stop if no input for this many seconds")
    args = ap.parse_args()

    rclpy.init()
    node = CmdVelFastDDSRx(args.host, args.port, args.topic, args.hz, args.deadman)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

