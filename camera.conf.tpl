{
  "global" : {
    "video_dir" : "/storage/camera/",
    "log_dir"   : "/var/log/camera/",
    "log_level" : 24
  },
  "cameras" : {
    "cam01" : {
      "host"            : "192.168.0.100",
      "rtsp_port"       : 10554,
      "rtsp_uri"        : "/udp/av0_0",
      "frame_rate"      : 15,
      "write_intervals" : "5m",
      "login"           : "admin",
      "pass"            : "admin"
    }
  }

}