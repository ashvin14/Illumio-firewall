def search(rule, term, search):
    return search >= rule[term][0] and \
                    search <= rule[term][1] \
                        if isinstance(rule[term], list) else search == rule[term]

def convertIPtoInt(ip_address):
        # ipv4 consist of 4 parts a.b.c.d each part ranging from [0-255]
        # lets convert that parts into respective values
        #  a.b.c.d => d + c*256 + b*65536 + a*16777216
        output = ip_address.split('.')
        output.reverse()
        return (int(output[0])+int(output[1])*256+int(output[2])*65536+int(output[3])*16777216)

def is_it_range(csvRow):
    return '-' in csvRow