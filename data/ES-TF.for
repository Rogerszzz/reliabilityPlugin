      SUBROUTINE UVARM(UVAR,DIRECT,T,TIME,DTIME,CMNAME,ORNAME,
     1 NUVARM,NOEL,NPT,LAYER,KSPT,KSTEP,KINC,NDI,NSHR,COORD,
     2 JMAC,JMATYP,MATLAYO,LACCFLA)
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME,ORNAME
      CHARACTER*3 FLGRAY(15)
      DIMENSION UVAR(NUVARM),DIRECT(3,3),T(3,3),TIME(2)
      DIMENSION ARRAY(15),JARRAY(15),JMAC(*),JMATYP(*),COORD(*)
      INTEGER i,j,k
      real*8 one
      
      REAL*8 mat1,mat2,mat3,mat4,mat5,mat6,mat7,mat8,mat9,mat10,
     1 mat11,mat12,mat13,mat14,mat15,mat16,mat17,mat18,mat19,mat20 
      REAL*8 theta,phi,alpha,A,B,p_crit,Xsigma,Xepsilon,b0,c0,th1,th2
     1 ,NN,dt,t_th,ddc,VVHP2,VVHP3,VVHP4,D,beta,VS,SR
      REAL*8 VHP3,VHP4,V3,V4,temp_n1,temp1,temp2,temp3,temp4,temp5,
     1 temp_aa,temp_bb,sig_mean,ein,ef,wmin,wfcrit,E,E_eff,XR,XD,AA,BB
      Parameter (PI=3.1415926)
      double precision TFK
      DIMENSION mat1(3,3),mat2(3,3),mat3(3,3),mat4(3,3),mat5(3,3),
     1 mat6(3,3),mat7(3,3),mat8(3,3),mat9(3,3),mat10(3,3),mat11(3,3),
     2 mat12(3,3),mat13(3,3),mat14(3,3),mat15(3,3),mat16(3,3),
     3 mat17(3,3),mat18(3,3),mat19(3,3),mat20(3,3),mat21(3,3)
      DIMENSION valt1(3,3),valt2(3,3),valt3(3,3),valt4(3,3),valt5(3,3),
     1 valt6(3,3),valt7(3,3),valt8(3,3),valt9(3,3),valt10(3,3),
     2 valt11(3,3),valt12(3,3),valt13(3,3),valt14(3,3),valt15(3,3),
     3 valt16(3,3),valt17(3,3),valt18(3,3),valt19(3,3),valt20(3,3),
     4 valt21(3,3)
c
c*************************************************************************
c     mat1(3,3)峰值应力分量矩阵
c     mat2(3,3)峰值应变分量矩阵
c     mat3(3,3)参考坐标系n方向矩阵(峰值)
c     mat4(3,3)参考坐标系q方向矩阵(峰值)
c     mat5(3,3)参考坐标系q方向转置矩阵(峰值)
c     mat6(3,3)q方向剪应变的1/2(峰值)
c     mat7(3,3)得到n方向转置矩阵(峰值)
c     mat8(3,3)得到n方向正应力
c     mat9(3,3)得到q方向剪应力
c     mat10(3,3)得到n方向正应力
c     mat11(3,3)得到q方向剪应力(1/2)
c error counter:
      jerror = 0
c
c*************************************************************************
c     UVAR(1) 最小主应力
c     UVAR(2) 中间主应力
c     UVAR(3) 最大主应力
c     UVAR(4) 绝对值最大主应力
c     UVAR(5) 等效应力
c     UVAR(6) 带正负号的等效应力
c     UVAR(7) 应力三轴度
c     UVAR(8) 最小主应变
c     UVAR(9) 中间主应变
c     UVAR(10) 最大主应变
c     UVAR(11) 绝对值最大主应力
c     UVAR(12) 等效应变
c     UVAR(13) 带正负号的等效应变
c     UVAR(14) 第一段保载前的峰值等效应力
c     UVAR(15) 第一段保载前的WEN-TU的多轴延性因子
c     UVAR(16) 第一段保载前的峰值等效塑性应变
c     UVAR(17) 第一段临界面的峰值法向应力
c     UVAR(18) 第一段临界面的峰值剪切应力
c     UVAR(19) 第一段临界面的峰值法向应变
c     UVAR(20) 第一段临界面的峰值剪切应变
c     UVAR(21) 第一段MGSA参数
c     UVAR(22) 第一段最大的MGSA参数
c     UVAR(23) theta(角度)
c     UVAR(24) phi(角度)
c     UVAR(25) alpha(角度)
c     UVAR(26) 保载阶段前一个KNIC蠕变应变
c     UVAR(27) 保载阶段每个KINC增加的蠕变应变
c     UVAR(28) 保载阶段每个KNIC的时间增量步
c     UVAR(29) 保载阶段每个KNIC的能量密度耗散率
c     UVAR(30) 计算该能量耗散率条件下的失效应变能密度
c     UVAR(31) 保载阶段每个KINC真实的失效应变能密度
c     UVAR(32) 保载阶段每个KINC的蠕变损伤
c     UVAR(33) SEDE一个周次蠕变损伤
c     UVAR(34) 一个周次疲劳寿命
c     UVAR(35) 一个周次疲劳损伤
c     UVAR(37) 累积疲劳损伤
c     UVAR(40) 第一段临界面的谷值法向应力
c     UVAR(41) 第一段临界面的谷值剪切应力
c     UVAR(42) 第一段临界面的谷值法向应变
c     UVAR(43) 第一段临界面的谷值剪切应变
C     UVAR(61) MSEDE一个周次蠕变损伤
c     UVAR(62) MSEDE累积蠕变损伤
c     UVAR(63) MSEDE一个周次蠕变疲劳损伤
c     UVAR(64) MSEDE累积总损伤
c     UVAR(65) DE一个周次蠕变损伤
c     UVAR(66) DE累积蠕变损伤
c     UVAR(67) DE一个周次蠕变疲劳损伤
c     UVAR(68) DE累积总损伤
c     UVAR(71) TF一个周次蠕变损伤
c     UVAR(72) TF累积蠕变损伤
c     UVAR(73) TF一个周次蠕变疲劳损伤
c     UVAR(74) TF累积总损伤
c     UVAR(76) 每个KINC的应力变化
c     UVAR(77) DE每个KINC的蠕变损伤
c*************************************************************************
c *** 蠕变模型常数
      D = 55.84
      beta =0.093

      fai=161
      temp_n1=0.0835
      wfcrit=64.5

      TFK = 4.93D34
      TFA = 8.97
      Xsigma=1586
      Xepsilon=0.553
      b0=-1.0*0.07
      c0=-1.0*0.76
c *** 弹性模量
      E=190000.0
c *** 泊松比
      Poi=0.3
c *** 诺顿方程的N
      XN=5.8
c *** 用于三维的弹性模量
      E_eff=3.0*E/(2.0*(1.0+Poi))
c *** 估算一个所能用到疲劳最大寿命
      xnfmax=200000
	  one=1.0d0


c*************************************************************************      
c *** 求三个主应力
         call getvrm('SP',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        UVAR(1)= array (1)
        UVAR(2)= array (2)
        UVAR(3)= array (3)
        
c *** 求绝对值最大主应力
        if (abs (UVAR(3)) .GE. abs (UVAR(1))) then
           UVAR(4)=UVAR(3)
        else
           UVAR(4)=UVAR(1)
        endif
        
c *** 获得应力
        call getvrm('S',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        VHP4 = (array(1) + array(2) + array(3))/3.0
        V4=1.5*((array(1)-VHP4)**2.0+(array(2)-VHP4)**2.0+
     1       (array(3)-VHP4)**2.0+2.0*array(4)**2.0+
     2        2.0*array(5)**2.0+2.0*array(6)**2.0)
       UVAR(5) = SQRT(V4)
        
c *** 给Mises应力加上方向
      if (UVAR(4) .NE. 0) then
          UVAR(6) = UVAR(5)*UVAR(4)/(abs (UVAR(4)))
      else
          UVAR(6) = UVAR(5)
      endif

c *** 获得应力三轴度
      if (UVAR(5) .NE. 0) then
          UVAR(7) = VHP4/SQRT(V4)
      end if      
        
c************************************************************************* 
c *** 求三个主应变
         call getvrm('EP',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        UVAR(8)= array (1)
        UVAR(9)= array (2)
        UVAR(10)= array (3)
c *** 储存谷值应变
      IF ((mod(KSTEP-4,3) .eq. 0) .and. (KINC .eq. 1)) THEN
        UVAR(60)=UVAR(8)
        UVAR(61)=UVAR(9)
        UVAR(62)=UVAR(10)
      ENDIF
c *** 储存峰值应变与等效应变幅
      IF ((mod(KSTEP-2,3) .eq. 0) .and. (KINC .eq. 1)) THEN
        UVAR(63)=UVAR(8)
        UVAR(64)=UVAR(9)
        UVAR(65)=UVAR(10)
        UVAR(66)=(((2**(0.5))/3)*
     &  (((UVAR(63)-UVAR(60))-(UVAR(64)-UVAR(61)))**2+
     &  ((UVAR(63)-UVAR(60))-(UVAR(65)-UVAR(62)))**2+
     &  ((UVAR(64)-UVAR(61))-(UVAR(65)-UVAR(62)))**2)**(0.5))/2
      ENDIF
c *** 求绝对值最大主应变
        if (abs (UVAR(10)) .GE. abs (UVAR(8))) then
           UVAR(11)=UVAR(10)
        else
           UVAR(11)=UVAR(8)
        endif
        
c *** 求等效总应变
        call getvrm('E',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        VVHP4 = (array(1)+array(2)+array(3))/3.0
        temp4 = (array(1)-VVHP4)**2.0+(array(2)-VVHP4)**2.0
     &   +(array(3)-VVHP4)**2.0
        temp4 = temp4+0.5*(array(4)**2.0+array(5)**2.0+array(6)**2.0)
        temp4 = temp4 * 2.0/3.0
        UVAR(12)= SQRT(temp4)
c *** 给总应变加正负号
      if (UVAR(11) .NE. 0) then
          UVAR(13) = UVAR(12)*UVAR(11)/
     &                  (abs (UVAR(11)))
      else
          UVAR(13) = UVAR(12)
      endif
c*************************************************************************
c *** 把谷值的场变量装入矩阵?
      IF ((mod(KSTEP-4,3) .eq. 0) .and. (KINC .eq. 1)) THEN
c *** 谷值应力
        call getvrm('SINV',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        UVAR(99)= array(1)
c *** 估值等效塑性应变
        call getvrm('PE',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        VVHP3 = (array(1)+array(2)+array(3))/3.0
        temp3 = (array(1)-VVHP3)**2.0+(array(2)-VVHP3)**2.0
     &   +(array(3)-VVHP3)**2.0
        temp3 = temp3+0.5*(array(4)**2.0+array(5)**2.0+array(6)**2.0)
        temp3 = temp3 * 2.0/3.0
        UVAR(56)= SQRT(temp3) 
c *** 谷值应力
        call getvrm('SINV',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        UVAR(57)= array(1)
      
c *** 将第一段谷值应力分量装入矩阵mat1
        call getvrm('S',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd                
      do i=1,3
        do j=1,3
         if (i.EQ.j) then
         valt1(i,j)=array(i)
         UVAR(43+i)=array(i)
         else
         valt1(i,j)=array(i+j+1)
         UVAR(44+i+j)=array(i+j+1)
         end if
        end do
      end do
      
c *** 将第一段谷值应变分量装入矩阵mat2
        call getvrm('E',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd                     
        do i=1,3
         do j=1,3
          if (i.EQ.j) then
          valt2(i,j)=array(i)
          UVAR(49+i)=array(i)
          else
          valt2(i,j)=array(i+j+1)
          UVAR(50+i+j)=array(i+j+1)
          end if
         end do
        end do
      ENDIF
c************************************************************************* 
c *** 把第一段大保载前的场变量装入矩阵
      IF ((mod(KSTEP-2,3) .eq. 0) .and. (KINC .eq. 1)) THEN
          
c *** 峰值应力
        call getvrm('SINV',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        UVAR(14)= array(1)
        
c *** WEN-TU的多轴延性因子
        UVAR(15)=(exp(2.0/3.0*(XN-0.5)/(XN+0.5)))/
     &     (exp(2.0*(XN-0.5)/(XN+0.5))*UVAR(7))

c *** 峰值的等效塑性应变
        call getvrm('PE',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
        VVHP2 = (array(1)+array(2)+array(3))/3.0
        temp2 = (array(1)-VVHP2)**2.0+(array(2)-VVHP2)**2.0
     &   +(array(3)-VVHP2)**2.0
        temp2 = temp2+0.5*(array(4)**2.0+array(5)**2.0+array(6)**2.0)
        temp2 = temp2 * 2.0/3.0
        UVAR(16)= SQRT(temp2)

c *** 将第一段峰值应力分量装入矩阵mat1
        call getvrm('S',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd
      do i=1,3
        do j=1,3
         if (i.EQ.j) then
         mat1(i,j)=array(i)
         else
         mat1(i,j)=array(i+j+1)
         end if
        end do
      end do

c *** 将第一段峰值应变分量装入矩阵mat2
        call getvrm('E',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &            ,laccfla)
        jerror = jerror + jrcd                     
        do i=1,3
         do j=1,3
          if (i.EQ.j) then
          mat2(i,j)=array(i)
          else
          mat2(i,j)=array(i+j+1)
          end if
         end do
        end do
        valt1(1,1)=UVAR(44)
        valt1(2,2)=UVAR(45)
        valt1(3,3)=UVAR(46)
        valt1(1,2)=UVAR(47)
	    valt1(2,1)=UVAR(47)
        valt1(1,3)=UVAR(48)
	    valt1(3,1)=UVAR(48)
        valt1(2,3)=UVAR(49)
	    valt1(3,2)=UVAR(49)
        valt2(1,1)=UVAR(50)
        valt2(2,2)=UVAR(51)
        valt2(3,3)=UVAR(52)
        valt2(1,2)=UVAR(53)
	    valt2(2,1)=UVAR(53)
        valt2(1,3)=UVAR(54)
	    valt2(3,1)=UVAR(54)
        valt2(2,3)=UVAR(55)
	    valt2(3,2)=UVAR(55)
c *** 获得部分应变范围的临界平面
c ******** 临界平面法坐标转换
      dpasso=5.0/180.0*PI
      do theta=0,PI,dpasso
       do phi=0,PI,dpasso
         do alpha=0,PI,dpasso
c *** 参考坐标系的峰值n方向矩阵(mat3),峰值q方向矩阵(mat4)
            mat3(1,1)=sin (theta)* cos (phi)
            mat3(2,1)=sin (theta)* sin (phi)
            mat3(3,1)=cos (theta)
            mat3(1,2)=0
            mat3(2,2)=0
            mat3(3,2)=0
            mat3(1,3)=0
            mat3(2,3)=0
            mat3(3,3)=0
            mat4(1,1)=-1.0*cos (alpha)* sin (phi)-sin (alpha)*
     &                 cos (theta)* cos (phi)
            mat4(2,1)=cos (alpha)* cos (phi)-sin (alpha)*
     &                 cos (theta)* sin (phi)
            mat4(3,1)=sin (alpha)* sin (theta)
            mat4(1,2)=0
            mat4(2,2)=0
            mat4(3,2)=0
            mat4(1,3)=0
            mat4(2,3)=0
            mat4(3,3)=0
c 另一个矩阵系
            valt3(1,1)=sin (theta)* cos (phi)
            valt3(2,1)=sin (theta)* sin (phi)
            valt3(3,1)=cos (theta)
            valt3(1,2)=0
            valt3(2,2)=0
            valt3(3,2)=0
            valt3(1,3)=0
            valt3(2,3)=0
            valt3(3,3)=0
            valt4(1,1)=-1.0*cos (alpha)* sin (phi)-sin (alpha)*
     &                 cos (theta)* cos (phi)
            valt4(2,1)=cos (alpha)* cos (phi)-sin (alpha)*
     &                 cos (theta)* sin (phi)
            valt4(3,1)=sin (alpha)* sin (theta)
            valt4(1,2)=0
            valt4(2,2)=0
            valt4(3,2)=0
            valt4(1,3)=0
            valt4(2,3)=0
            valt4(3,3)=0
c *** 参考坐标系峰值/谷值q矩阵的转置
            mat5=transpose (mat4)
            valt5=transpose (valt4)
c *** 考虑q方向峰值/谷值剪应变(mat6)
            mat6=matmul (matmul(mat5,mat2), mat3)
            valt6=matmul (matmul(valt5,valt2), valt3)
c *** 参考坐标系峰值/谷值矩阵的转置(mat7)
            mat7=transpose (mat3)
            valt7=transpose (valt3)
c *** 考虑n方向的峰值/guzhi正应力(mat8),以及q方向峰值/guzhi剪应力(mat9)
            mat8=matmul (matmul(mat7,mat1), mat3)
            mat9=matmul (matmul(mat5,mat1), mat3)
            valt8=matmul (matmul(valt7,valt1), valt3)
            valt9=matmul (matmul(valt5,valt1), valt3)
            UVAR(17)=mat8(1,1)
            UVAR(18)=mat9(1,1)
            UVAR(40)=valt8(1,1)
            UVAR(41)=valt9(1,1)
c *** 考虑n方向的峰值/guzhi正应变(mat10),以及q方向峰值/guzhi剪应变(mat11)
            mat10=matmul (matmul(mat7,mat2), mat3)
            mat11=matmul (matmul(mat5,mat2), mat3)
            valt10=matmul (matmul(valt7,valt2), valt3)
            valt11=matmul (matmul(valt5,valt2), valt3)
            UVAR(19)=mat10(1,1) 
            UVAR(20)=2.0*mat11(1,1)
            UVAR(42)=valt10(1,1) 
            UVAR(43)=2.0*valt11(1,1)  
c *** 计算MGSA参数
        UVAR(21)=(UVAR(18))/(Xsigma/SQRT(3.0))
     &      *(UVAR(20)-UVAR(43))/2
     &      +(UVAR(17))/(Xsigma)
     &      *(UVAR(19)-UVAR(42))/2
c *** 找出最大的MGSA参数(UVAR22)
            IF (UVAR(22).LE.UVAR(21)) THEN
                UVAR(22)=UVAR(21)
                UVAR(23)=180.0*theta/PI
                UVAR(24)=180.0*phi/PI
                UVAR(25)=180.0*alpha/PI                
            ELSE
                GO TO 4100
            ENDIF              
4100        CONTINUE    
         end do
        end do       
       end do       
      ENDIF   
c************************************************************************* 
c *** 获得第一段保载后的场变量
      IF (mod(KSTEP-2,3) .eq. 0) THEN
c *** 每个KINC的所需的时间增量
        UVAR(70)=DTIME
c *** 每个KINC增加的蠕变应变
        call getvrm('CE',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &              ,laccfla)
        jerror = jerror + jrcd
        VVHP5 = (array(1)+array(2)+array(3))/3.0
        temp5 = (array(1)-VVHP5)**2.0+(array(2)-VVHP5)**2.0
     &   +(array(3)-VVHP5)**2.0
        temp5 = temp5+0.5*(array(4)**2.0+array(5)**2.0+array(6)**2.0)
        temp5 = temp5 * 2.0/3.0
        VCE1= UVAR(71)
        UVAR(71)= SQRT(temp5)
        UVAR(72)= UVAR(71)-VCE1
c *** 每个KINC的应力
        call getvrm('SINV',array,jarray,flgray,jrcd,jmac,jmatyp,matlayo
     &              ,laccfla)
        jerror = jerror + jrcd
        UVAR(73)=array(1)


        IF (UVAR(70) .NE. 0) THEN
C *** MSEDE
         UVAR(77) = (UVAR(5)+(UVAR(99)+UVAR(14))/2)*UVAR(72)/UVAR(70)
         UVAR(78)=abs(UVAR(15)*fai*UVAR(77)**temp_n1)
         UVAR(79)=abs(min(UVAR(78),wfcrit))
         UVAR(80)=abs((UVAR(77)/UVAR(79)-UVAR(77)/wfcrit)*(UVAR(70)))
         UVAR(82)=UVAR(82) + UVAR(80)
C *** DE
         ein= UVAR(72)/UVAR(70)
         ef=UVAR(15)*D*(ein)**beta
         UVAR(74) = ein
         UVAR(75) = ef
         UVAR(81) = UVAR(81) + (ein/ef)*DTIME
C *** TF
         UVAR(76)=TFK*(UVAR(73)**(-TFA))
         UVAR(83) =UVAR(83)+UVAR(70)/UVAR(76)
        ENDIF
      ENDIF
c*************************************************************************          
c 结算第一个保载后的疲劳和蠕变损伤
      IF ((mod(KSTEP-3,3) .eq. 0) .and. (KINC .eq. 1)) THEN  
c *** 计算第一段的MGSA纯疲劳寿命
      DO xnf=1,xnfmax,0.5
         XR=(Xsigma/SQRT(3.0))/(E_eff/3.0)*(2.0*xnf)**(2*b0)+
     &    (Xepsilon*SQRT(3.0))*(2.0*xnf)**(c0)
         XD=abs(XR-UVAR(22))
c*** 由matlab算得大概十万分之一合适
         IF (XD.LE.1E-5) THEN
         UVAR(34)=xnf 
         GO TO 100
         END IF
      END DO
  100 CONTINUE
c *** 计算第一段的等效应变疲劳寿命
      DO xnf=1,xnfmax,0.5
         XR=(Xsigma/E)*(2.0*xnf)**(b0)+Xepsilon*(2.0*xnf)**(c0)
         XD=abs(XR-UVAR(66))
c*** 由matlab算得大概十万分之一合适
         IF (XD.LE.1E-4) THEN
         UVAR(67)=xnf
         GO TO 500
         END IF
      END DO
  500 CONTINUE
      IF (UVAR(34).EQ.0) THEN
          UVAR(34)=xnfmax
      END IF
      IF (UVAR(67).EQ.0) THEN
          UVAR(67)=xnfmax
      END IF
      
c *** 一周次疲劳损伤
         UVAR(35)=one/UVAR(67)
         UVAR(68)=one/UVAR(34)
c *** 累计蠕变损伤
         UVAR(84)=UVAR(84)+UVAR(81)
         UVAR(85)=UVAR(85)+UVAR(82)
         UVAR(86)=UVAR(86)+UVAR(83)
c *** 累计疲劳损伤
         UVAR(37)=UVAR(35)+UVAR(37)
         UVAR(93)=UVAR(93)+UVAR(68)
c *** 一周次蠕变疲劳损伤
         UVAR(87)=UVAR(81)+UVAR(35)
         UVAR(88)=UVAR(82)+UVAR(35)
         UVAR(89)=UVAR(83)+UVAR(35)
c *** 累计总损伤
         UVAR(90)=UVAR(84)+UVAR(37)
         UVAR(91)=UVAR(85)+UVAR(37)
         UVAR(92)=UVAR(86)+UVAR(37)
         UVAR(94)=UVAR(84)+UVAR(93)
         UVAR(95)=UVAR(85)+UVAR(93)
         UVAR(96)=UVAR(86)+UVAR(93)
      ENDIF
c *** 结算第一个保载后的疲劳和蠕变损伤
      IF ((mod(KSTEP-3,3) .eq. 0) .and. (KINC .eq. 5)) THEN  
c *** 置零
         UVAR(22)=0
         UVAR(35)=0
         UVAR(70)=0
         UVAR(72)=0
         UVAR(73)=0
         UVAR(74)=0
         UVAR(75)=0
         UVAR(76)=0
         UVAR(77)=0
         UVAR(78)=0
         UVAR(79)=0
         UVAR(80)=0
         UVAR(81)=0
         UVAR(82)=0
         UVAR(83)=0
      ENDIF

      
c**********************************************************************     
      
C If error, write comment to .DAT file:
      IF(JRCD.NE.0)THEN
       WRITE(6,*) 'REQUEST ERROR IN UVARM FOR ELEMENT NUMBER ',
     1     NOEL,'INTEGRATION POINT NUMBER ',NPT
      ENDIF


       
      RETURN
      END

