class SystemInfoDisplay:
    def __init__(self, mac_label, ip_label, pc_name_label, system_info):
        self.mac_label = mac_label
        self.ip_label = ip_label
        self.pc_name_label = pc_name_label
        self.system_info = system_info

    def show_system_info(self):
        mac = self.system_info.get_mac_address()
        ip = self.system_info.get_ip_address()
        pc_name = self.system_info.get_pc_name()