#Module Name: VorpalDataAnalysis
#Version: 2.4
#Author: Maninder Kaur and Sushil Kumar Sawant
#Date: Friday 13/02/2015
#Purpose : This module can be use to analyse Particle as well as Field data generated by VORPAL software.

import os
import tables
import sys
import numpy
import string
#import matplotlib
#matplotlib.use('AGG')
import matplotlib.pylab as plt
                
       omega = 1883651567308853.5          ### frequency of laser varies acc to simulation
       omegaP = 356797270747134.4          ### frequency of plasma
       rf = numpy.sqrt(1-((omegaP*omegaP)/(omega*omega)))   ### refractive index of plasma



class Ptcls :

    def get_Ptcls_Data_From_h5_File(self,filename,attr,ienergy,fenergy,idistance,fdistance,MAXPART):

        '''
          This method of class Ptcls reads partticle data from h5 file according to the total energy filter and distance filter ( currently having only 'x' filter ).  
          Arguments to the method are as follows :
          filename = string Name of the particle h5 file.
          attr = string attribute in the file e.g electrons.
          ienergy = float lower energy cut-off for kinetic energy.
          fenergy = float final energy cut-off for kinetic energy.
          idistance = float lower x cut-off.
          fdistance = float higher x cut-off.
          MAXPART = int maximum number of particles having highest energy. I think about 2,00,000 should be more than sufficient.
        '''
        self.x = []
        self.y = []
        self.z = []
        self.px = []
        self.py = []
        self.pz = []
        self.ke = []
        self.ydash = []
        self.zdash = [] 
        self.ypy = []
        self.zpz = []
        self.w = []
        self.tag = []
        
        self.filename = filename
        myFile = tables.openFile(filename)
        myData = myFile.root.__getattr__(attr)
       
        self.dim = myData.attrs.vsNumSpatialDims
        self.np2c = myData.attrs.numPtclsInMacro
        self.ec = myData.attrs.charge 
        self.m = myData.attrs.mass
        
        self.rm = self.m*c*c*6.24150974e9       ### Rest mass in GeV

        NX =len(myData)
        NY = len(myData[0])
     
        mindistance = idistance
        maxdistance = fdistance
        minenergy = ienergy*abs(self.ec)*1e9  ##converting to Joule
        maxenergy = fenergy*abs(self.ec)*1e9
 
        mingamavx = numpy.sqrt(minenergy*(minenergy + (2*self.m*c*c)))/(self.m*c) ##calculating gamav
        maxgamavx = numpy.sqrt(maxenergy*(maxenergy + (2*self.m*c*c)))/(self.m*c)

       # f = open (os.path.splitext(self.filename)[0]+'.out','w')

        if self.dim == 1: 

         for i in range(NX):
          soln = myData[i]
          if ( soln[1] >= mingamavx and soln[1] <= maxgamavx and soln[0] <= maxdistance and soln[0] >= mindistance )  :

              self.x.append(soln[0])

              self.px.append(soln[1]/c)


              self.ke.append(self.r(soln[1],0.0,0.0))
 

              if NY == 6 :
               self.w.append(soln[5])
               self.tag.append(long(soln[4]))
        #       f.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(long(soln[4]))+' '+str(soln[5])+'\n')
              else :
               self.w.append(soln[4])
         #      f.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(soln[4])+'\n')

        if self.dim == 2: 

         g = numpy.argsort(myData[:,2])  ### This holds the indices of sorted myData array with respect to gamavx column. 
         NXX = NX - MAXPART             #### This means we are selecting only MAXPART lakh particles out of NX particles and they will be in asending order with respect to gamavx.  
         if NXX < 0 :
            NXX = 0
         for i in range(NXX,NX):
          soln = myData[g[i]]
          if ( soln[2] >= mingamavx and soln[2] <= maxgamavx and soln[0] <= maxdistance and soln[0] >= mindistance )  :

              self.x.append(soln[0])
              self.y.append(soln[1])
              self.px.append(soln[2]/c)
              self.py.append(soln[3]/c)
              self.ydash.append(soln[3]/soln[2])
              self.ke.append(self.r(soln[2],soln[3],soln[4]))
              self.ypy.append((soln[3]*soln[1])/c)

              if NY == 7 :
               self.w.append(soln[6])
               self.tag.append(long(soln[5]))
           #    f.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(soln[4])+' '+str(long(soln[5]))+' '+str(soln[6])+'\n')
              else :
               self.w.append(soln[5])
           #    f.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(soln[4])+' '+str(soln[5])+'\n')

        if self.dim == 3: 
         g = numpy.argsort(myData[:,3])  ### This holds the indices of sorted myData array with respect to gamavx column. 
         NXX = NX - MAXPART            #### This means we are selecting only 2 lakh particles out of NX particles and they will be in asending order with respect to gamavx.  
         if NXX < 0 :
            NXX = 0
         for i in range(NXX,NX):
          soln = myData[g[i]]
          if ( soln[3] >= mingamavx and soln[3] <= maxgamavx and soln[0] <= maxdistance and soln[0] >= mindistance )  :

        
              self.x.append(soln[0])
              self.y.append(soln[1])
              self.z.append(soln[2])
              self.px.append(soln[3]/c)
              self.py.append(soln[4]/c)
              self.pz.append(soln[5]/c)
              self.ydash.append(soln[4]/soln[3])
              self.zdash.append(soln[5]/soln[3])
              self.ke.append(self.r(soln[3],soln[4],soln[5]))
              self.ypy.append((soln[1]*soln[4])/c)
              self.zpz.append((soln[2]*soln[5])/c)
              
              if NY == 8 :
               self.w.append(soln[7])
               self.tag.append(long(soln[6]))
           #    f.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(soln[4])+' '+str(soln[5])+' '+str(long(soln[6]))+' '+str(soln[7])+'\n')
              else :
           #    f.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(soln[4])+' '+str(soln[5])+' '+str(soln[6])+'\n')
               self.w.append(soln[6])

        myFile.close()
 #       f.close()



    def beamDiagno(self) :

        ''' This method of class Ptcls computes the various beam quality related quantities such as energy,energy spread etc.
            This method should be called after get_Ptcls_Data_From_h5_File() or after get_Ptcls_Data_From_txt_File().
            It does not take any arguments and returns following list.
            L = [number of macro particles,charge in pC,current in A,rms beamlength,rms size in y,rms size in z,rms divergence in y,rms divergence in z,Avg kinetic energy,%energy    
                 spread,Normalized emittance in y,Normalized emittance in z] .
        ''' 
        c=299792458.0 
        meany = numpy.average(self.y)
        meanz = numpy.average(self.z)
        meanypy = numpy.average(self.ypy)
        meanzpz = numpy.average(self.zpz)
        meanpy = numpy.average(self.py)
        meanpz = numpy.average(self.pz)
        meanke = numpy.average(self.ke)
        charge = numpy.sum(self.w)*self.ec*self.np2c
        stdx = numpy.std(self.x) 
        stdy = numpy.std(self.y) 
        stdz = numpy.std(self.z)
        current = (charge*c)/stdx
        stdpx = numpy.std(self.px) 
        stdpy = numpy.std(self.py) 
        stdpz = numpy.std(self.pz) 

        stdTE = numpy.std(self.ke)
        stdydash = numpy.std(self.ydash)
        stdzdash = numpy.std(self.zdash)

        Nemittancey = numpy.sqrt((stdy**2)*(stdpy**2)-(meanypy-(meany*meanpy))**2)
        Nemittancez = numpy.sqrt((stdz**2)*(stdpz**2)-(meanzpz-(meanz*meanpz))**2) 
        L=[len(self.w),abs(charge*1e12),abs(current),stdx,stdy,stdz,stdydash,stdzdash,meanke,(stdTE/meanke)*100,Nemittancey,Nemittancez]      
        return L  

    def r(self, m, n, s) :

         ''' This method of class Ptcls returns kinetic energy of the particle.
            Arguments to the method are as follows :
            m = float gama*vx
            n = float gama*vy
            s = float gama*vz 
            This returns Kinetic energy in GeV
         '''     
         f=numpy.sqrt((m*m)+(n*n)+(s*s))
         r=self.rm*numpy.sqrt(((f/2.99792458e8)*(f/2.99792458e8))+1) - self.rm  ## Kinetic energy in GeV
         return r


    def get_Ptcls_Data_From_txt_File(self,filename,ienergy,fenergy,idistance,fdistance,dim,np2c,ec,m):

        '''
          This method of class Ptcls reads partticle data from a txt file according to the energy filter and distance filter ( currently having only 'x' filter ). 
          Arguments to the method are as follows :
          filename = string Name of the particle h5 file.
          attr = string attribute in the file e.g electrons.
          ienergy = float lower energy cut-off for total energy.
          fenergy = float final energy cut-off for total energy.
          idistance = float lower x cut-off.
          fdistance = float higher x cut-off.
          dim = integer vorpal run dimension e.g 1 for 1d .
          np2c = float number of physicle particles in one macroparticle.
          ec = float charge of one physical particle.
          m = float mass of one physical particle.
        '''
            
           
        
        self.x = []
        self.y = []
        self.z = []
        self.px = []
        self.py = []
        self.pz = []
        self.ke = []
        self.ydash = []
        self.zdash = [] 
        self.ypy = []
        self.zpz = []
        self.w = []
        self.tag = []

        
        self.m = m
        self.ec = ec
        self.np2c = np2c
        self.dim = dim
        self.filename = filename 
        myFile = open(filename,'r')
        myData = myFile.readlines()


        NX =len(myData)
        NY = len(string.split(myData[0])) 
        
        c = 299792458.0   
        self.rm = self.m*c*c*6.24150974e9       ### Rest mass in GeV     
        mindistance = idistance
        maxdistance = fdistance
        minenergy = ienergy*abs(self.ec)*1e9  ##converting to Joule
        maxenergy = fenergy*abs(self.ec)*1e9
 
        mingamavx = numpy.sqrt(minenergy*(minenergy + (2*self.m*c*c)))/(self.m*c) ##calculating gamavx
        maxgamavx = numpy.sqrt(maxenergy*(maxenergy + (2*self.m*c*c)))/(self.m*c)

        if self.dim == 1: 
         for i in range(NX):
          soln = string.split(myData[i]) 
          
          if ( float(soln[1]) >= mingamavx and float(soln[1]) <= maxgamavx and float(soln[0]) <= maxdistance and float(soln[0]) >= mindistance )  :

              self.x.append(float(soln[0]))
         
              self.px.append(float(soln[1])/c)
              
              self.ke.append(self.r(float(soln[1]),0.0,0.0))
              
              
              if NY == 6 :
               self.w.append(float(soln[5]))
               self.tag.append(long(soln[4]))
              else :
               self.w.append(float(soln[4]))

        if self.dim == 2: 
         for i in range(NX):
          soln = string.split(myData[i]) 
          
          if ( float(soln[2]) >= mingamavx and float(soln[2]) <= maxgamavx and float(soln[0]) <= maxdistance and float(soln[0]) >= mindistance )  :

              self.x.append(float(soln[0]))
              self.y.append(float(soln[1]))
              self.px.append(float(soln[2])/c)
              self.py.append(float(soln[3])/c)
              self.ydash.append(float(soln[3])/float(soln[2]))
              self.ke.append(self.r(float(soln[2]),float(soln[3]),float(soln[4])))
              self.ypy.append((float(soln[3])*float(soln[1]))/c)
              
              if NY == 7 :
               self.w.append(float(soln[6]))
               self.tag.append(long(soln[5]))
              else :
               self.w.append(float(soln[5]))

        if self.dim == 3: 
         for i in range(NX):
          soln = string.split(myData[i]) 

          if ( float(soln[3]) >= mingamavx and float(soln[3]) <= maxgamavx and float(soln[0]) <= maxdistance and float(soln[0]) >= mindistance )  :

              self.x.append(float(soln[0]))
              self.y.append(float(soln[1]))
              self.z.append(float(soln[2]))
              self.px.append(float(soln[3])/c)
              self.py.append(float(soln[4])/c)
              self.pz.append(float(soln[5])/c)
              self.ydash.append(float(soln[4])/float(soln[3]))
              self.zdash.append(float(soln[5])/float(soln[3]))
              self.ke.append(self.r(float(soln[3]),float(soln[4]),float(soln[5])))
              self.ypy.append((float(soln[1])*float(soln[4]))/c)
              self.zpz.append((float(soln[2])*float(soln[5]))/c)
              
              if NY == 8 :
               self.w.append(float(soln[7]))
               self.tag.append(long(soln[6]))
              else :
               self.w.append(float(soln[6]))

        myFile.close()




    def getTAGs(self,tagfile):
       
        ''' This method of class Ptcls simply writes the TAGs of the particles to a file and also return list of tags.
           This method should be called after get_Ptcls_Data_From_h5_File() or after get_Ptcls_Data_From_txt_File().
           Arguments to the method are :
           tagfile = string name of the file in which you want to save the tags information.

        '''

        tf = open(tagfile,'w')

        for T in self.tag:

                tf.write(str(T)+'\n')

        tf.close()
        
        return self.tag 


    def checkforTAGs(self,filename,attribute,tagfile,outfile):
        
        ''' This method of class Ptcls simply checks for existance of given set of tags into a h5 file
            Arguments to the method are :
            filename = string h5 particle file name in which you want to check existance of tags.
            attribute = string particle attribute in the file e.g electrons.
            tagfile = string txt file containing tag information (one tag per line). 
            outfile = string output file name, where information of only matched tags will be stored.
        '''
        self.filename = filename
        myFile = tables.openFile(filename)
        myData = myFile.root.__getattr__(attribute)
      
        dim = myData.attrs.vsNumSpatialDims
	NX = len(myData)
	NX1 = int(NX/4)
	NX2 = 2*NX1
	NX3 = 3*NX1
	NX4 = 4*NX1
 	SUM = (NX2-NX1)+(NX3-NX2)+(NX-NX3)+(NX1-0)
	
	
        of = open(outfile,'w')
        tf = open(tagfile,'r')

        myTAGS = tf.readlines()
        
        if dim == 1: 
          for tag in myTAGS :
           try :
               Matched_tag_INDEX = numpy.where(myData[:,4].astype(long) == long(tag))
               soln = myData[Matched_tag_INDEX[0][0]]
               of.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(long(tag))+' '+str(soln[5])+'\n')
           except :   
               pass

        if dim == 2: 
          for tag in myTAGS :
           try :
               Matched_tag_INDEX = numpy.where(myData[:,5].astype(long) == long(tag))
               soln = myData[Matched_tag_INDEX[0][0]]
               of.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(soln[4])+' '+str(long(tag))+' '+str(soln[6])+'\n')
           except :   
               pass

        if dim == 3:        
          for tag in myTAGS :
            try :
               Matched_tag_INDEX = numpy.where(myData[:,6].astype(long) == long(tag))
               soln = myData[Matched_tag_INDEX[0][0]]
               of.write(str(soln[0])+' '+str(soln[1])+' '+str(soln[2])+' '+str(soln[3])+' '+str(soln[4])+' '+str(soln[5])+' '+str(long(tag))+' '+str(soln[7])+'\n')
            except :   
               pass
     

        myFile.close()
        tf.close()
        of.close()
        

    def make_2d_Ptcl_Plot(self,plot_type,outfile,xaxis,yaxis) :

        ''' This method of class Ptcls plots a simple xy plot on the screen or as png file.
            This method should be called after get_Ptcls_Data_From_h5_File() or after get_Ptcls_Data_From_txt_File().
            Arguments to the method are :
            plot_type = string png or x11 .
            outfile = name of png file will be used if plot_type is png .
            xaxis = string physical variable on x axis possible are x,y,z,px,py,pz,ke,tag,w .
            yaxis = string physical variable on y axis possible are x,y,z,px,py,pz,ke,tag,w  .
        ''' 

        xx = []
        yy = []

        if xaxis == 'x' :
           x_label = " x (mm) "
           xx = [a * 1000 for a in self.x] 
        elif xaxis == 'y' :
           x_label = " y (mm) "
           xx = [a * 1000 for a in self.y]
        elif xaxis == 'z' :
           x_label = " z (mm) "
           xx = [a * 1000 for a in self.z]
        elif xaxis == 'px' :
           x_label = " px/mc "
           xx.extend(self.px)
        elif xaxis == 'py' :
           x_label = " py/mc "
           xx.extend(self.py)
        elif xaxis == 'pz' :
           x_label = " pz/mc "
           xx.extend(self.pz)
        elif xaxis == 'ke' :
           x_label = " ke (GeV) "
           xx.extend(self.ke)
        elif xaxis == 'tag' :
           x_label = " tag "
           xx.extend(self.tag)
        elif xaxis == 'w' :
           x_label = " w "
           xx.extend(self.w)
    
        if yaxis == 'x' :
           y_label = " x (mm) "
           yy = [a * 1000 for a in self.x]
        elif yaxis == 'y' :
           y_label = " y (mm) "
           yy = [a * 1000 for a in self.y]
        elif yaxis == 'z' :
           y_label = " z (mm) "
           yy = [a * 1000 for a in self.z]
        elif yaxis == 'px' :
           y_label = " px/mc "
           yy.extend(self.px)
        elif yaxis == 'py' :
           y_label = " py/mc "
           yy.extend(self.py)
        elif yaxis == 'pz' :
           y_label = " pz/mc "
           yy.extend(self.pz)
        elif yaxis == 'ke' :
           y_label = " ke (GeV) "
           yy.extend(self.ke)
        elif yaxis == 'tag' :
           y_label = " tag "
           yy.extend(self.tag)
        elif yaxis == 'w' :
           y_label = " w "
           yy.extend(self.w)
        plt.figure()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.plot(xx,yy,".",markersize=1)
        if plot_type == 'png' :
           plt.savefig(outfile)
        elif plot_type == 'x11' :
           plt.show() 
        plt.close()      
  
    def make_Hist(self,plot_type,outfile,xaxis,binwidth) :

        ''' This method of class Ptcls plots a histogram of a physical variable on the screen or as png file.
            This method should be called after get_Ptcls_Data_From_h5_File() or after get_Ptcls_Data_From_txt_File().
            Arguments to the method are :
            plot_type = string png or x11.
            outfile = name of png file will be used if plot_type is png .
            xaxis = string physical varible whose  hisogram is needed, possible are x,y,z,px,py,pz,tag,w.
            binwidth = float width of the bin for histogram . 
        ''' 
        hd = []

        if xaxis == 'x' :
         x_label  = ' x (mm) '
         y_label  = ' charge(pC)/mm ' 
         hd = [a * 1000 for a in self.x]

        if xaxis == 'y' :
         x_label  = ' y (mm) '
         y_label  = ' charge(pC)/mm ' 
         hd = [a * 1000 for a in self.y]
     
        if xaxis == 'z' :
         x_label  = ' z (mm) '
         y_label  = ' charge(pC)/mm ' 
         hd = [a * 1000 for a in self.z]

        if xaxis == 'px' :
         x_label  = ' px/mc '
         y_label  = ' charge(pC) ' 
         hd = [a  for a in self.px]

        if xaxis == 'py' :
         x_label  = ' py/mc '
         y_label  = ' charge(pC) ' 
         hd = [a  for a in self.py]

        if xaxis == 'pz' :
         x_label  = ' pz/mc '
         y_label  = ' charge(pC) ' 
         hd = [a  for a in self.pz]

        if xaxis == 'ke' :
         x_label  = ' ke (GeV) '
         y_label  = ' charge(pC)/GeV ' 
         hd = [a  for a in self.ke]

        if xaxis == 'w' :
         x_label  = ' w '
         y_label  = ' charge(pC) ' 
         hd = [a  for a in self.w]


        imin = int(numpy.min(hd)/binwidth)
        imax = int(numpy.max(hd)/binwidth)

        ll = imax-imin
        bin = numpy.zeros(ll+1)


         
        for j in range(len(hd)) :
          i = int(hd[j]/binwidth)
          i = i - imin
          if i < 0 :
           i = i +abs(imin)

          bin[i] = bin[i] + 1.0*self.w[j]

        xx = numpy.arange(imin,imax+1,1)
        fac = (self.np2c*abs(self.ec)*1e12)

        plt.figure()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.plot(xx*binwidth,fac*bin,"-",markersize=1)
        if plot_type == 'png' :
           plt.savefig(outfile)
        elif plot_type == 'x11' :
           plt.show() 
        plt.close()     



class Fields :



    
    def get_Field_Data_From_h5_File(self,filename,attr) :

        '''
          This method of class Fields reads fields data from h5 file. Works with data generated from EMfiled vorpal input file.
          May not work with data generated from multifield vorpal input file.   
          Arguments to the method are as follows :
          filename = string Name of the particle h5 file.
          attr = string attribute in the file e.g YeeElecField,SumRhoJ
        '''

        self.filename = filename
        myFile = tables.openFile(filename)
        myData = myFile.root.__getattr__(attr)
        self.lGrid =  myFile.root.__getattr__("globalGridGlobalLimits")._v_attrs.vsLowerBounds
        self.rGrid =  myFile.root.__getattr__("globalGridGlobalLimits")._v_attrs.vsUpperBounds
        self.myData = myData 
        self.NY = 1
        self.NZ = 1  
        self.dim = len(self.lGrid)

        self.NX = len(myData)
        self.dx = (self.rGrid[0]-self.lGrid[0])/(self.NX-1)
     

        if self.dim == 1 :        
           self.E1 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E2 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E3 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E1[:,0,0] = myData[:,0] 
           self.E2[:,0,0] = myData[:,1] 
           self.E3[:,0,0] = myData[:,2] 

        if self.dim == 2 :
           self.NY = len(myData[0])

           self.dy = (self.rGrid[1]-self.lGrid[1])/(self.NY-1)
           self.E1 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E2 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E3 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E1[:,:,0] = myData[:,:,0] 
           self.E2[:,:,0] = myData[:,:,1] 
           self.E3[:,:,0] = myData[:,:,2] 
        if self.dim == 3 :
           self.NY = len(myData[0])
           self.NZ = len(myData[0][0]) 
           self.E1 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E2 = numpy.zeros((self.NX,self.NY,self.NZ))
           self.E3 = numpy.zeros((self.NX,self.NY,self.NZ))  
           self.dy = (self.rGrid[1]-self.lGrid[1])/(self.NY-1)
           self.dz = (self.rGrid[2]-self.lGrid[2])/(self.NZ-1)          
           self.E1 = myData[:,:,:,0]  
           self.E2 = myData[:,:,:,1]  
           self.E3 = myData[:,:,:,2] 
        myFile.close()

    def make_Field_lineout(self,plot_type,outfile,xaxis,yaxis,y_label,xp,yp,zp) :

        '''
          This method of class Fields plots the field lineout on the screen or png file as per the arguments.
          This method should be called after get_Field_Data_From_h5_File().
          Arguments to the method are as follows :
          plot_type = string png or x11
          outfile = string name of png file, will be used if plot_type is png .
          xaxis = string x or y or z only
          yaxis = string E1,E2,E3, Note for YeeElecfield this means Ex,Ey,Ez for YeeMagField Bx,By,Bz and for SumRhoJ Rho,Jx,Jy,Jz 
                  note currently Jz is not available.   
          y_label = string Y axis label e.g Ey (V/m) or Rho (C/m^3).
          xp = integer grid point in x. 
          yp = integer grid point in y. 
          zp = integer grid point in z.
          Note if you dont know what should be xp,yp,zp then simply use -1 for all. This will make a plot at y=0,z=0 or x=0 
          depending on what is the xaxis.

        '''
        if xp == -1 :
           xp = self.NX/2
        if yp == -1 :
           yp = self.NY/2
        if zp == -1 :
           zp = self.NZ/2

        if xaxis == 'x' :
           xx = numpy.arange(0,self.NX,1)*self.dx*1000 + self.lGrid[0]*1000   
           x_label = " x (mm) " 
           if yaxis == 'E1':
              yy = numpy.array(self.E1[:,yp,zp])              
           elif yaxis == 'E2' :
              yy = numpy.array(self.E2[:,yp,zp]) 
           elif yaxis == 'E3' :
              yy = numpy.array(self.E3[:,yp,zp])



        if xaxis == 'y' :
           xx = numpy.arange(0,self.NY,1)*self.dy*1000 + self.lGrid[1]*1000   
           x_label = " y (mm) " 
           if yaxis == 'E1':
              yy = numpy.array(self.E1[xp,:,zp])              
           elif yaxis == 'E2' :
              yy = numpy.array(self.E2[xp,:,zp]) 
           elif yaxis == 'E3' :
              yy = numpy.array(self.E3[xp,:,zp])


        if xaxis == 'z' :
           x_label = " z (mm) " 
           xx = numpy.arange(0,self.NZ,1)*self.dz*1000 + self.lGrid[2]*1000 
           if yaxis == 'E1':
              yy = numpy.array(self.E1[xp,yp,:])              
           elif yaxis == 'E2' :
              yy = numpy.array(self.E2[xp,yp,:]) 
           elif yaxis == 'E3' :
              yy = numpy.array(self.E3[xp,yp,:])


        plt.figure()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.plot(xx,yy,"b-",markersize=1)
        plt.xlim([numpy.min(xx),numpy.max(xx)])
        if plot_type == 'png' :
           plt.savefig(outfile)
        elif plot_type == 'x11' :
           plt.show()     
        plt.close()
  

    def make_Field_Contour(self,plot_type,outfile,field,contour_type,xp,yp,zp) :

        '''
          This method of class Fields plots the field contour as per the arguments.
          This method should be called after get_Field_Data_From_h5_File().
          Arguments to the method are as follows :
          plot_type = string png or x11
          outfile = string name of png file, will be used if plot_type is png .
          field = string E1,E2,E3, Note for YeeElecfield this means Ex,Ey,Ez for YeeMagField Bx,By,Bz and for SumRhoJ Rho,Jx,Jy,Jz 
                  note currently Jz is not available.   
          contour_type = string xy or xz  or yz only.
          xp = integer grid point in x. 
          yp = integer grid point in y. 
          zp = integer grid point in z.
          Note if you dont know what should be xp,yp,zp then simply use -1 for all. This will make a plot at y=0 or z=0 or x=0 
          depending on what is contour type.

        '''
        if xp == -1 :
           xp = self.NX/2
        if yp == -1 :
           yp = self.NY/2
        if zp == -1 :
           zp = self.NZ/2

        if contour_type == 'xy' :
           xgrid = numpy.zeros((self.NX,self.NY))
           ygrid = numpy.zeros((self.NX,self.NY))
           x_label = " x(mm) "
           y_label = " y(mm) "
           for i in range(self.NX) :
             for j in range(self.NY) :
               xgrid[i][j] = self.lGrid[0]+self.dx*i
               ygrid[i][j] = self.lGrid[1]+self.dy*j
           if field == 'E1':
              yy = numpy.array(self.E1[:,:,zp])              
           elif field == 'E2' :
              yy = numpy.array(self.E2[:,:,zp]) 
           elif field == 'E3' :
              yy = numpy.array(self.E3[:,:,zp])

        if contour_type == 'xz' :
           xgrid = numpy.zeros((self.NX,self.NY))
           ygrid = numpy.zeros((self.NX,self.NZ))
           x_label = " x(mm) "
           y_label = " z(mm) "
           for i in range(self.NX) :
             for j in range(self.NZ) :
               xgrid[i][j] = self.lGrid[0]+self.dx*i
               ygrid[i][j] = self.lGrid[2]+self.dz*j
           if field == 'E1':
              yy = numpy.array(self.E1[:,yp,:])              
           elif field == 'E2' :
              yy = numpy.array(self.E2[:,yp,:]) 
           elif field == 'E3' :
              yy = numpy.array(self.E3[:,yp,:])

        if contour_type == 'yz' :
           xgrid = numpy.zeros((self.NY,self.NZ))
           ygrid = numpy.zeros((self.NY,self.NZ))
           x_label = " y(mm) "
           y_label = " z(mm) "
           for i in range(self.NY) :
             for j in range(self.NZ) :
               xgrid[i][j] = self.lGrid[1]+self.dy*i
               ygrid[i][j] = self.lGrid[2]+self.dz*j
           if field == 'E1':
              yy = numpy.array(self.E1[xp,:,:])              
           elif field == 'E2' :
              yy = numpy.array(self.E2[xp,:,:]) 
           elif field == 'E3' :
              yy = numpy.array(self.E3[:,yp,:])


        plt.figure()
        plt.contourf(xgrid*1000,ygrid*1000,yy,50)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.colorbar()
        plt.xlim(1000*numpy.min(xgrid),1000*numpy.max(xgrid))
        plt.ylim(1000*numpy.min(ygrid),1000*numpy.max(ygrid))
        if plot_type == 'png' :
           plt.savefig(outfile)
        elif plot_type == 'x11' :
           plt.show() 
        plt.close()

    def make_amplitude_lineout(self,plot_type,outfile,xaxis,yaxis,y_label,xp,yp,zp) :

        '''
          This method of class Fields plots the field lineout on the screen or png file as per the arguments.
          This method should be called after get_Field_Data_From_h5_File().
          Arguments to the method are as follows :
          plot_type = string png or x11
          outfile = string name of png file, will be used if plot_type is png .
          xaxis = string x or y or z only
          yaxis = string E1,E2,E3, Note for amplitude of YeeElecfield this means Ax,Ay,Az for YeeMagField Bx,By,Bz and for SumRhoJ Rho,Jx,Jy,Jz 
                  note currently Jz is not available.   
          y_label = string Y axis label e.g Ey (V/m) or Rho (C/m^3) or Ay .
          xp = integer grid point in x. 
          yp = integer grid point in y. 
          zp = integer grid point in z.
          Note if you dont know what should be xp,yp,zp then simply use -1 for all. This will make a plot at y=0,z=0 or x=0 
          depending on what is the xaxis.

        '''
        if xp == -1 :
           xp = self.NX/2
        if yp == -1 :
           yp = self.NY/2
        if zp == -1 :
           zp = self.NZ/2

        if xaxis == 'x' :
           xx = numpy.arange(0,self.NX,1)*self.dx*1000 + self.lGrid[0]*1000   
           x_label = " x (mm) " 
           if yaxis == 'E1':
              yy = numpy.array(((self.ec*self.E1)/(self.m*c*omegaP))[:,yp,zp])              
           elif yaxis == 'E2' :
              yy = numpy.array(((self.ec*self.E2)/(self.m*c*omegaP))[:,yp,zp]) 
           elif yaxis == 'E3' :
              yy = numpy.array(((self.ec*self.E3)/(self.m*c*c))[:,yp,zp])



        if xaxis == 'y' :
           xx = numpy.arange(0,self.NY,1)*self.dy*1000 + self.lGrid[1]*1000   
           x_label = " y (mm) " 
           if yaxis == 'E1':
              yy = numpy.array(((self.ec*self.E1)/(self.m*c*omegaP))[xp,:,zp])              
           elif yaxis == 'E2' :
              yy = numpy.array(((self.ec*self.E2)/(self.m*c*omegaP))[xp,:,zp]) 
           elif yaxis == 'E3' :
              yy = numpy.array(((self.ec*self.E3)/(self.m*c*c))[xp,:,zp])


        if xaxis == 'z' :
           x_label = " z (mm) " 
           xx = numpy.arange(0,self.NZ,1)*self.dz*1000 + self.lGrid[2]*1000 
           if yaxis == 'E1':
              yy = numpy.array(((self.ec*self.E1)/(self.m*c*omegaP))[xp,yp,:])              
           elif yaxis == 'E2' :
              yy = numpy.array(((self.ec*self.E2)/(self.m*c*omegaP))[xp,yp,:]) 
           elif yaxis == 'E3' :
              yy = numpy.array(((self.ec*self.E3)/(self.m*c*c))[xp,yp,:])


        plt.figure()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.plot(xx,yy,"b-",markersize=1)
        plt.xlim([numpy.min(xx),numpy.max(xx)])
        if plot_type == 'png' :
           plt.savefig(outfile)
        elif plot_type == 'x11' :
           plt.show()     
        plt.close()
  

    def field_Energy(self,field) :
        '''
          This method of class Fields computes and returns  the Field energy over entire simulation domain.
          This method should be called after get_Field_Data_From_h5_File().
          Arguments to the method are as follows :
          field = string E or B 
          Note for electric field it returns [sum(0.5*epsilon0*Ex**2),sum(0.5*epsilon0*Ey**2),sum(0.5*epsilon0*Ez**2)] and 
          for magnetic field it returns [sum((0.5/mue0)*Bx**2),sum((0.5/mue0)*By**2),sum((0.5/mue0)*Bz**2)]
        '''
        if field == 'E' :
           factor = 0.5*8.85e-12
        if field == 'B' :
           factor = 0.5/1.2566370614e-6
        if self.dim == 1 :
          Exenergy = factor*self.dx*numpy.sum(self.E1*self.E1)
          Eyenergy = factor*self.dx*numpy.sum(self.E2*self.E2)
          Ezenergy = factor*self.dx*numpy.sum(self.E2*self.E3)
        if self.dim == 2 :
          Exenergy = factor*self.dx*self.dy*numpy.sum(self.E1*self.E1)
          Eyenergy = factor*self.dx*self.dy*numpy.sum(self.E2*self.E2)
          Ezenergy = factor*self.dx*self.dy*numpy.sum(self.E3*self.E3)
        if self.dim == 3 :
          Exenergy = factor*self.dx*self.dy*self.dz*numpy.sum(self.E1*self.E1)
          Eyenergy = factor*self.dx*self.dy*self.dz*numpy.sum(self.E2*self.E2)
          Ezenergy = factor*self.dx*self.dy*self.dz*numpy.sum(self.E3*self.E3)
        L = [Exenergy,Eyenergy,Ezenergy]
        return L

    def  line_spot(self,pp,field) :
        '''
          This method of class Fields computes and returns the laser spot size on a lineout .
          This method should be called after get_Field_Data_From_h5_File().
          Arguments to the method are as follows :
          pp = string x,y,z If you want spot size in y the use 'y'.
          field = string E1,E2,E3   If polarization is in y then use E2 . 
          Note spot size in x is determined at y=0 and z=0.
               spot size in y is determined at z=0 and x= point at which abs(field) is maximum.
               spot size in z is determined at y=0 and x= point at which abs(field) is maximum.
          Note that in transeverse spot size  laser peak is asumed at the centre i.e at y=0 for y spot size and z=0 for z spot size.  
          Alog longitudinal direction peak point is at the centre.
        '''
 
        if field == 'E1' :
           ff = self.E1
        if field == 'E2' :
           ff = self.E2
        if field == 'E3' :
           ff = self.E3

        xp = numpy.argmax(ff[:,self.NY/2,self.NZ/2])
        yp = self.NY/2
        zp = self.NZ/2

        if pp == 'x' :
           ff = ff[:,yp,zp]
           maxIndex = numpy.argmax(abs(ff))
           xx = numpy.arange(0,self.NX,1)*self.dx - maxIndex*self.dx

        if pp == 'y' :
           ff = ff[xp,:,zp]
           xx = numpy.arange(0,self.NY,1)*self.dy - self.NY/2*self.dy

        if pp == 'z' :
           ff = ff[xp,yp,:]
           xx = numpy.arange(0,self.NY,1)*self.dz - self.NZ/2*self.dz

        line_spotsize = numpy.sqrt(numpy.sum(ff**2*xx**2)/numpy.sum(ff**2))
        return line_spotsize

    def  integrated_spot(self,pp,field,itype) :
        '''
          This method of class Fields computes and returns the integrated laser spot size.
          This method should be called after get_Field_Data_From_h5_File().
          Arguments to the method are as follows :
          pp = string x,y,z If you want spot size in y the use 'y'
          field = string E1,E2,E3   If polarization is in y then use E2  
          itype = string along x,along x and y,along y and z.
          e.g pp = 'y' with itype = 'along x' means integrated y spot size along x.
          or pp = 'y'  with itype = 'along x and z' means integrated spot size along a nd z.
          Note that in transeverse spot size  laser peak is asumed at the centre i.e at y=0 for y spot size and z=0 for z spot size.  
          Alog longitudinal direction peak point is at the centre.
        '''
 
        if field == 'E1' :
           fff = self.E1
        if field == 'E2' :
           fff = self.E2
        if field == 'E3' :
           fff = self.E3

        spotsize = 0.0
        sumff2 = 0.0

        if itype == 'along x' :
           NX = self.NX
           YP = self.NY/2 
           NY = YP+1  
           ZP = self.NZ/2 
           NZ = ZP+1       
        if itype == 'along x and y' :
           NX = self.NX
           YP = 0 
           NY = self.NY 
           ZP = self.NZ/2 
           NZ = ZP+1 
        if itype == 'along x and z' :
           NX = self.NX
           YP = self.NY/2 
           NY = YP+1  
           ZP = 0 
           NZ = self.NZ
        if itype == 'along y and z' :
           NX = self.NX
           YP = 0
           NY = self.NY 
           ZP = 0 
           NZ = self.NZ 


        if pp == 'x' :
           for i in range(YP,NY) :
             for j in range(ZP,NZ) :
                 ff = fff[:,i,j]
                 maxIndex = numpy.argmax(abs(ff))       
                 xx = numpy.arange(0,self.NX,1)*self.dx - maxIndex*self.dx
                 sumff2 = sumff2 + numpy.sum(ff**2)
                 spotsize = spotsize+numpy.sum(ff**2*xx**2)

        if pp == 'y' :

           for i in range(NX) :
             for j in range(ZP,NZ) :
                 ff = fff[i,:,j]
                 xx = numpy.arange(0,self.NY,1)*self.dy - self.NY/2*self.dy
                 sumff2 = sumff2 + numpy.sum(ff**2)
                 spotsize = spotsize+numpy.sum(ff**2*xx**2)

        if pp == 'z' :

          for i in range(NX) :
             for j in range(YP,NY) :
                 ff = fff[i,self.NY/2,:]
                 maxIndex = numpy.argmax(ff)
                 xx = numpy.arange(0,self.NY,1)*self.dz - self.NZ/2*self.dz
                 sumff2 = sumff2 + numpy.sum(ff**2)
                 spotsize = spotsize+numpy.sum(ff**2*xx**2)

        spotsize = spotsize/sumff2 
        integrated_spotsize = numpy.sqrt(spotsize)

        return integrated_spotsize

    def  field_MAX(self,field,yp,zp) :
        '''
          This method of class Fields returns absolute maximum field along x for given y and z grid.
          This method should be called after get_Field_Data_From_h5_File().
          Arguments to the method are as follows :
          field = string E1,E2,E3   
          yp = integer grid point in y
          zp = integer grid point in z
      
        '''
        if field == 'E1' :
           fff = self.E1
        if field == 'E2' :
           fff = self.E2
        if field == 'E3' :
           fff = self.E3

        if yp == -1 :
           yp = self.NY/2
        if zp == -1 :
           zp = self.NZ/2

        return numpy.max(abs(fff[:,yp,zp]))


