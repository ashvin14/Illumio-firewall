import csv
from helper_methods import convertIPtoInt, search, is_it_range
from fw_rules_format import rule_format

class Firewall:
    def __init__(self, filename):
        # nested dictionaries in order to get constant access time
        self.rules = rule_format()
        with open(filename, "r") as csvFile:
            csv_reader = csv.reader(csvFile, delimiter = ',')
            for csvRow in csv_reader:
                # generating port and ip address ranges
                # port and ip address could be either value or range of values in firewall rules 
                # based on that we are setting values 
                # port = [x,y] or a where [x,y] denotes range of ports from x to y inclusive and a denotes single value
                rule_port, rule_ip = csvRow[2],csvRow[3]
                # ternary operator: val = executed_when_cond_true if condition else executed_when_condition_false
                port = [int(port_range) for port_range in rule_port.split('-')] if is_it_range(rule_port) else int(rule_port)
                ip = [convertIPtoInt(ip_range) for ip_range in rule_ip.split('-')] if is_it_range(rule_ip) else convertIPtoInt(rule_ip)
                # ip = [x,y] or a where [x,y] denotes range of ip addresses from x to y inclusive and a denotes single value
                self.rules[csvRow[1]][csvRow[0]].append({ "port": port ,"ip_address": ip })

    def accept_packet(self, direction, protocol, port , ip_address):
        # converting input ip address to integer
        ip_address = convertIPtoInt(ip_address)
        # based on protocol, direction, and ip address partition 
        # reducing the search area as much as possible
        rules = self.rules[protocol][direction]
        # if no such rule found 
        if not rules:
            return False
        
        # dividing the rules-set into chunks
        CHUNK_SIZE = 1000
        END_CHUNK = CHUNK_SIZE
        # if length of rule is less than chunk size
        if len(rules) < CHUNK_SIZE: 
            CHUNK_SIZE = len(rules)
        # considering one chunk at a time
        for chunk in range(0, len(rules), CHUNK_SIZE):
            BEGIN_CHUNK = chunk
            for rule in rules[BEGIN_CHUNK:END_CHUNK]:
                # comparing the input packet port and ip_address with existing rules
                # if the port/ip_address in rules is mentioned in range,
                # comparing that range with packet port/ip_address
                # if the port/ip_address in rules is single value,
                # comparing that value with i/p packet port/ip_address
                if search(rule,"port",port) and search(rule,"ip_address",ip_address):
                    return True
            END_CHUNK += CHUNK_SIZE
        return False
        
            



