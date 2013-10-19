def zkconnect(self):
    data = "e80317fc00000000"
    self.zkclient.sendto(data.decode("hex"), self.address)
    print data.decode("hex")
    self.data_recv, addr = self.zkclient.recvfrom(1024)
    if len(self.data_recv) > 0:
        self.id_com = self.data_recv.encode("hex")[8:12]
        self.counter = self.counter+1
        print self.data_recv.encode("hex")
    return self.data_recv

def zkspace1(self):
    try:
        test = self.spacetrynumber
    except:
        self.spacetrynumber = 1
        
    data_seq=[ self.data_recv.encode("hex")[4:6], self.data_recv.encode("hex")[6:8] ]
    print data_seq
    if self.spacetrynumber == 1:
        self.data_seq1 = hex( abs( int( data_seq[0], 16 ) - int( '4f', 16 ) ) ).lstrip("0x")
        self.data_seq2 = hex( int( data_seq[1], 16 ) + int( '4e', 16 ) ).lstrip("0x")
        data_footer = "00782b"
        desc = ": -4f, +4e"
    else:
        self.data_seq1 = hex( abs( int( data_seq[0], 16 ) - int( '2f', 16 ) ) ).lstrip("0x")
        self.data_seq2 = hex( int( data_seq[1], 16 ) + int( '50', 16 ) ).lstrip("0x")
        data_footer = "005829"
        desc = ": -2f, +50"
        
        
    if len(self.data_seq1) >= 3:
        self.data_seq2 = hex( int( self.data_seq2, 16 ) + int( self.data_seq1[:1], 16) ).lstrip("0x")
        self.data_seq1 = self.data_seq1[-2:]
        
    if len(self.data_seq2) >= 3:
        self.data_seq1 = hex( int( self.data_seq1, 16 ) + int( self.data_seq2[:1], 16) ).lstrip("0x")
        self.data_seq2 = self.data_seq2[-2:]
        
        
    if len(self.data_seq1) <= 1:
        self.data_seq1 = "0"+self.data_seq1
        
    if len(self.data_seq2) <= 1:
        self.data_seq2 = "0"+self.data_seq2
    
    counter = hex( self.counter ).lstrip("0x")
    if len(counter):
        counter = "0" + counter
    print self.data_seq1+" "+self.data_seq2+desc
    data = "4500"+self.data_seq1+self.data_seq2+self.id_com+counter+data_footer
    #4500999e9e350b00782b
    self.zkclient.sendto(data.decode("hex"), self.address)
    print data
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
    except:
        if self.spacetrynumber == 1:
            self.spacetrynumber = 2
            zkspace1(self)
    
    self.id_com = self.data_recv.encode("hex")[8:12]
    self.counter = self.counter + 1
    print self.data_recv.encode("hex")
    return self.data_recv[8:]
    

def zkspace2(self):
    try:
        test = self.spacetrynumber2
    except:
        self.spacetrynumber2 = 1
        
    data_seq=[ self.data_recv.encode("hex")[4:6], self.data_recv.encode("hex")[6:8] ]
    print data_seq
    if self.spacetrynumber2 == 1:
        self.data_seq1 = hex( int( data_seq[0], 16 ) + int( '8a', 16 ) ).lstrip("0x")
        self.data_seq2 = hex( abs( int( data_seq[1], 16 ) - int( '1a', 16 ) ) ).lstrip("0x")
        data_footer = "00782b"
        desc = ": +8a, +4e"
    else:
        self.data_seq1 = hex( abs( int( data_seq[0], 16 ) - int( '2f', 16 ) ) ).lstrip("0x")
        self.data_seq2 = hex( int( data_seq[1], 16 ) + int( '50', 16 ) ).lstrip("0x")
        data_footer = "005829"
        desc = ": -2f, +50"
        
        
    if len(self.data_seq1) >= 3:
        self.data_seq2 = hex( int( self.data_seq2, 16 ) + int( self.data_seq1[:1], 16) ).lstrip("0x")
        self.data_seq1 = self.data_seq1[-2:]
        
    if len(self.data_seq2) >= 3:
        self.data_seq1 = hex( int( self.data_seq1, 16 ) + int( self.data_seq2[:1], 16) ).lstrip("0x")
        self.data_seq2 = self.data_seq2[-2:]
        
        
    if len(self.data_seq1) <= 1:
        self.data_seq1 = "0"+self.data_seq1
        
    if len(self.data_seq2) <= 1:
        self.data_seq2 = "0"+self.data_seq2
    
    counter = hex( self.counter ).lstrip("0x")
    if len(counter):
        counter = "0" + counter
    print self.data_seq1+" "+self.data_seq2+desc
    data = "f401"+self.data_seq1+self.data_seq2+self.id_com+counter+"00ffff0000"
    #f4010bc2f33b0d00ffff0000
    self.zkclient.sendto(data.decode("hex"), self.address)
    print data
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
    except:
        if self.spacetrynumber2 == 1:
            self.spacetrynumber2 = 2
            zkspace2(self)
    
    self.id_com = self.data_recv.encode("hex")[8:12]
    self.counter = self.counter + 1
    print self.data_recv.encode("hex")
    return self.data_recv[8:]
    
    
def zkdiconnect(self):
    data_seq=[ self.data_recv.encode("hex")[4:6], self.data_recv.encode("hex")[6:8] ]
    
    self.data_seq1 = hex( int( data_seq[0], 16 ) + int( '83', 16 ) ).lstrip("0x")
    self.data_seq2 = hex( int( data_seq[1], 16 ) + int( '3', 16 ) ).lstrip("0x")
    
    if len(self.data_seq1) >= 3:
        self.data_seq2 = hex( int( self.data_seq2, 16 ) + int( self.data_seq1[:1], 16) ).lstrip("0x")
        self.data_seq1 = self.data_seq1[-2:]
        
    if len(self.data_seq2) >= 3:
        self.data_seq1 = hex( int( self.data_seq1, 16 ) + int( self.data_seq2[:1], 16) ).lstrip("0x")
        self.data_seq2 = self.data_seq2[-2:]
    
    
    if len(self.data_seq1) <= 1:
        self.data_seq1 = "0"+self.data_seq1
        
    if len(self.data_seq2) <= 1:
        self.data_seq2 = "0"+self.data_seq2
    
    counter = hex( self.counter ).lstrip("0x")
    if len(counter):
        counter = "0" + counter
        
    data = "e903"+self.data_seq1+self.data_seq2+self.id_com+self.counter+"00"
    self.zkclient.sendto(data.decode("hex"), self.address)
    
    self.data_recv, addr = self.zkclient.recvfrom(1024)
    self.id_com = self.data_recv.encode("hex")[8:12]
    self.counter = 0
    #print self.data_recv.encode("hex")
    return self.data_recv
    
