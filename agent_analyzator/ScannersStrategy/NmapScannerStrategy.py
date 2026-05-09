from .AbstractScannerStrategy import AbstractScannerStrategy
#from AbstractScannerStrategy import AbstractScannerStrategy
import nmap
import re

class NmapScannerStrategy(AbstractScannerStrategy):

    def _parse(self, scan_result) -> list[dict]:
        cve_pattern = re.compile(r'(CVE-\d{4}-\d{4,})', re.IGNORECASE)
        results = []

        for host_ip, host_data in scan_result.get('scan', {}).items():
            for port, port_data in host_data.get('tcp', {}).items():
                cves_found = []
                for script_name, script_output in port_data.get('script', {}).items():
                    cves_found.extend(cve_pattern.findall(script_output))

                if cves_found:
                    results.append({
                        'host': host_ip,
                        'port': port,
                        'cves': list(set(cves_found))
                    })
                else:
                    results.append({
                        'host': host_ip,
                        'port': port,
                        'cves': [],
                        'info': 'no CVE found'
                    })

        return results

    def execute(self) -> list[dict]:
        print("start execute")
        ip_address, arguments = self.instructions
        ports_and_scripts:dict[str, dict[str, list]] = arguments.get("ports")
        ping = ""
        global_scripts = ""
        scan_speed = ""
        intensity = ""
        if arguments["ping"] == False:
           ping = "-Pn"

        scan_speed = self.scan_speed(arguments["scan_speed"])
        intensity = "--version-intensity" + " " + self.intensity_depth(arguments["intensity"])
        global_scripts = [self._script_interpreter(scr) for scr in arguments["global_scripts"]]


        result_for_return = []
        if ports_and_scripts != None:
            for port in ports_and_scripts:
                scanner = nmap.PortScanner()
                all_scripts = [self._script_interpreter(i) for i in ports_and_scripts[port]["scripts"]]+global_scripts
                all_scripts = "--script" + " " + ",".join(all_scripts)
                result_args = all_scripts+ " " + scan_speed + " " + intensity + " " + ping

                scanner.scan(ip_address, ports=port, arguments=result_args)
                print(scanner.command_line())
                result_scanner = self._parse(scanner._scan_result)

                result_for_return.extend(result_scanner)
        else:
            scanner = nmap.PortScanner()
            result_args = "--script" +" "+ ",".join(global_scripts) + " " + scan_speed + " " + intensity + " " + ping

            scanner.scan(ip_address, arguments=result_args, sudo=True)
            result_scanner = self._parse(scanner._scan_result)
            result_for_return.extend(result_scanner)

        return result_for_return

    def scan_speed(self, scan_speed) -> str:
        if scan_speed == "panic":
           return "-T0"
        elif scan_speed == "slow":
           return "-T4"
        elif scan_speed == "normal":
           return "-T4"
        elif scan_speed == "fast":
           return "-T3"
        elif scan_speed == "aggressive":
           return "-T4"
        elif scan_speed == "hyper_aggressive":
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

        if script == "ssl_check_heartbleed":
            return "ssl-heartbleed"
        if script == "ssl_check_ccs_injection":
            return "ssl-ccs-injection"
        if script == "ssl_check_poodle":
            return "ssl-poodle"
        if script == "ssl_check_drown":
            return "ssl-drown"
        if script == "ftp_vsftpd_backdoor":
            return "ftp-vsftpd-backdoor"
        if script == "ssl_weak_dh":
            return "ssl-dh-params"
        if script == "http_slowloris":
            return "http-slowloris-check"
        if script == "smb_check_eternal_blue":
            return "smb-vuln-ms17-010"
        if script == "smb_check_smbghost":
            return "smb-vuln-cve-2020-0796"
        if script == "smb_check_ms08_067":
            return "smb-vuln-ms08-067"
        if script == "smb_check_ms10_054":
            return "smb-vuln-ms10-054"
        if script == "smb_check_ms10_061":
            return "smb-vuln-ms10-061"

        if script == "http_check_log4shell":
            return "http-log4shell"
        if script == "http_check_spring4shell":
            return "http-vuln-spring4shell"
        if script == "http_check_cve2017_5638":
            return "http-vuln-cve2017-5638"
        if script == "http_check_cve2021_40444":
            return "http-vuln-cve2021-40444"
        if script == "http_check_cve2021_34473":
            return "http-vuln-cve2021-34473"
        if script == "http_check_cve2022_1388":
            return "http-vuln-cve2022-1388"

        if script == "smtp_check_proxylogon":
            return "smtp-vuln-cve2023-23397"

        if script == "mysql_check_cve2012_2122":
            return "mysql-vuln-cve2012-2122"


        return ""
"""
test = {
            "172.17.0.4": {
                "ports": {
                    "21":   {"scripts": ["ftp_vsftpd_backdoor"]},
                    "25":   {"scripts": ["ssl_weak_dh", "ssl_check_poodle"]},
                    "5432": {"scripts": ["ssl_check_ccs_injection"]},
                    "8180": {"scripts": ["http_slowloris"]}
                },
                "global_scripts": ["check_bounce_attack"],
                "scanner": "nmap",
                "ping": False,
                "scan_speed": "aggressive",
                "intensity": "high"
            }
        }

test2 = {
            "172.17.0.4": {
                "global_scripts": ["vuln"],
                "scanner": "nmap",
                "ping": False,
                "scan_speed": "aggressive",
                "intensity": "high"
            }
        }

Nm = NmapScannerStrategy(("172.17.0.4",test["172.17.0.4"]))
print(Nm.execute())
"""