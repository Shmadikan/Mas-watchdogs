#from .AbstractScannerStrategy import AbstractScannerStrategy
from AbstractScannerStrategy import AbstractScannerStrategy
import nmap


class NmapScannerStrategy(AbstractScannerStrategy):

    def _parse(self):
        return self.scanner

    def execute(self):
        ip_address, arguments = self.instructions
        ports_and_scripts:dict[str, dict[str, list]] = arguments["ports"]
        ping = ""
        global_scripts = ""
        scan_speed = ""
        intensity = ""
        if arguments["ping"] == False:
           ping = "-Pn"

        scan_speed = self.scan_speed(arguments["scan_speed"])
        intensity = "--version-intensity" + " " + self.intensity_depth(arguments["intensity"])
        global_scripts = [self._script_interpreter(scr) for scr in global_scripts]

        for port in ports_and_scripts:
            scanner = nmap.PortScanner()
            all_scripts = [self._script_interpreter(i) for i in ports_and_scripts[port]["scripts"]]+global_scripts
            all_scripts = "--script" + " " + ",".join(all_scripts)
            result_args = all_scripts+ " " + scan_speed + " " + intensity + " " + ping
            scanner.scan(ip_address, ports=port, arguments=result_args)

    def scan_speed(self, scan_speed) -> str:
        if "scan_speed" == "panic":
           return "-T0"
        elif "scan_speed" == "slow":
           return "-T1"
        elif "scan_speed" == "normal":
           return "-T2"
        elif "scan_speed" == "fast":
           return "-T3"
        elif "scan_speed" == "aggressive":
           return "-T4"
        elif "scan_speed" == "hyper_aggressive":
           return "-T5"
        else:
           return "-T2"

    def intensity_depth(self, intensity) -> str:
        if intensity == "low":
           return "0"
        elif intensity == "medium":
           return "4"
        elif intensity == "high":
           return "9"
        else:
           return "2"








    def _script_interpreter(self, script: str):
            if script == "vuln":
                return "vuln"
            if script == "check_anonymous_login":
                return "ftp-anon"
            if script == "check_bounce_attack":
                return "ftp-bounce"
            if script == "check_brute_force":
                return "brute"
            if script == "check_weak_algorithms":
                return "ssh2-enum-algos"
            if script == "check_unencrypted_auth":
                return "telnet-encryption"
            if script == "check_open_relay":
                return "smtp-open-relay"
            if script == "check_user_enumeration":
                return "smtp-enum-users"
            if script == "check_sql_injection":
                return "http-sql-injection"
            if script == "check_xss":
                return "http-stored-xss"
            if script == "check_open_dirs":
                return "http-enum"
            if script == "check_default_credentials":
                return "default-accounts"
            if script == "check_rpc_info":
                return "rpcinfo"
            if script == "check_nfs_exports":
                return "nfs-showmount"
            if script == "check_null_session":
                return "smb-enum-shares"
            if script == "check_eternalblue":
                return "smb-vuln-ms17-010"
            if script == "check_smb_signing":
                return "smb-security-mode"
            if script == "check_rsh_access":
                return "rsh-brute"
            if script == "check_empty_password":
                return "mysql-empty-password"

            return ""

test = {
            "172.17.0.3": {
                "ports": {
                    "80,90": {"scripts": ["vuln"]}
                    #"3306": {"scripts": ["check_empty_password"]},
                    #"21": {"scripts": ["check_default_credentials"]}
                },
                "global_scripts": ["check_bounce_attack"],
                "scanner": "nmap",
                "ping": False,
                "scan_speed": "fast",
                "intensity": "low"
            }
        }

Nm = NmapScannerStrategy(("172.17.0.3",test["172.17.0.3"]))
Nm.execute()