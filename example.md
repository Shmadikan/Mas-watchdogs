## Формат Json от Координатора к анализатору
{
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
    "ping":false/true
    "reverse_dns":false/true
}