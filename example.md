## Формат Json от Координатора к анализатору
[
    "scan_speed":
    ["panic", 
    "slow" , 
    "normal", 
    "fast", "aggresive", 
    "hyper_aggressive"],
    "targets_ip": {
        ("example_ip", [10,100,200],[""], "for_all"/"once"),
        ("example_ip", [20,40,60]),
    },
    "ping":false/true,
    "reverse_dns":false/true,
    


    {
  "192.168.1.1": {
    "ports": {
      "80":   {"scripts": ["check_sql_injection", "check_xss"]},
      "3306": {"scripts": ["check_mysql_empty_password"]},
      "443":  {"scripts": ["check_heartbleed"]}
    },
    "global_scripts": ["check_os"],
    "scanner": "nmap",
    "ping": false,
    "scan_speed": "normal",
    "intensity": "deep"
  }

]