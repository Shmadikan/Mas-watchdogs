## Формат Json от Координатора к анализатору
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
  

}