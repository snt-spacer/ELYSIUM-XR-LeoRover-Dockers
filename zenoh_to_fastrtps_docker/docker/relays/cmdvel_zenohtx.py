#!/usr/bin/env python3
import argparse, json, socket
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelZenohTx(Node):
    def __init__(self, host: str, port: int, topic: str):
        super().__init__("cmdvel_zenoh_tx")
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sub = self.create_subscription(Twist, topic, self.cb, 10)
        self.get_logger().info(f"Zenoh -> UDP relay on {host}:{port} for {topic}")

    def cb(self, msg: Twist):
        # minimal JSON payload for /cmd_vel
        payload = {
            "lx": msg.linear.x,  "ly": msg.linear.y,  "lz": msg.linear.z,
            "ax": msg.angular.x, "ay": msg.angular.y, "az": msg.angular.z
        }
        data = json.dumps(payload).encode("utf-8")
        try:
            self.sock.sendto(data, self.addr)
        except Exception as e:
            self.get_logger().error(f"UDP send failed: {e}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=20001)
    ap.add_argument("--topic", default="/leo04/cmd_vel")
    args = ap.parse_args()

    rclpy.init()
    node = CmdVelZenohTx(args.host, args.port, args.topic)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

