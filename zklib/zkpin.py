def zkpinwidth(self):
    try:
        test = self.pinwidthtrynumber
    except:
        self.pinwidthtrynumber = 1
        
    data_seq=[ self.data_recv.encode("hex")[4:6], self.data_recv.encode("hex")[6:8] ]
    print data_seq
    if self.pinwidthtrynumber == 1:
        self.data_seq1 = hex( abs( int( data_seq[0], 16 ) - int( '5', 16 ) ) ).lstrip("0x")
        self.data_seq2 = hex( int( data_seq[1], 16 ) + int( '1c', 16 ) ).lstrip("0x")
        desc = ": -5, +1c"
    else:
        self.data_seq1 = hex( abs( int( data_seq[0], 16 ) - int( 'd', 16 ) ) ).lstrip("0x")
        self.data_seq2 = hex( abs( int( data_seq[1], 16 ) - int( '9e', 16 ) ) ).lstrip("0x")
        desc = ": -d, -9e"
        
        
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
    data = "0b00"+self.data_seq1+self.data_seq2+self.id_com+counter+"007e50494e32576964746800"
    #0b001b01f33b0f007e50494e32576964746800
    self.zkclient.sendto(data.decode("hex"), self.address)
    print data
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
    except:
        if self.pinwidthtrynumber == 1:
            self.pinwidthtrynumber = 2
            zkpinwidth(self)
    
    self.id_com = self.data_recv.encode("hex")[8:12]
    self.counter = self.counter + 1
    print self.data_recv.encode("hex")
    return self.data_recv[8:]
    
