class Height:
    def height(x,y,z):
       M= (x + y + z) / 3 # Mean M # Program can be used when we have more sensor readings
       calibration = 1000
       Range = 65535
       #print(M)
       M= ( M * calibration ) / Range # Height in meter
       print("height_in_meters")
       print(M)
       print("height_in_centi_meters")
       print(M*100)
       return(M*100)# Height in centimetres
       
