!> \file bessi1.f90
!> \brief compute modified Bessel function \f$ I_1 \f$
!> \details Details can be found in Press et al. <I> Numerical Resipes in Fortran 77 and 90 (second edition) </I> (2001), pp. 231
!> @author William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
!> @date 2001
REAL (KIND(0D0)) FUNCTION BESSI1(X)
!> input value x
  REAL (KIND(0D0))  :: x,ax
  REAL (KIND(0D0))  :: Y,P1,P2,P3,P4,P5,P6,P7,&
       Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9
  DATA P1,P2,P3,P4,P5,P6,P7/0.5D0,0.87890594D0,0.51498869D0,&
       0.15084934D0,0.2658733D-1,0.301532D-2,0.32411D-3/
  DATA Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9/0.39894228D0,-0.3988024D-1,&
       -0.362018D-2,0.163801D-2,-0.1031555D-1,0.2282967D-1,&
       -0.2895312D-1,0.1787654D-1,-0.420059D-2/
  IF (dabs(X).lt.3.75d0) THEN
     Y=(X/3.75d0)*(X/3.75d0)
     BESSI1=X*(P1+Y*(P2+Y*(P3+Y*(P4+Y*(P5+Y*(P6+Y*P7))))))
  ELSE
     AX=dabs(X)
     Y=3.75d0/AX
     BESSI1=(dexp(AX)/dsqrt(AX))*(Q1+Y*(Q2+Y*(Q3+Y*(Q4+&
          Y*(Q5+Y*(Q6+Y*(Q7+Y*(Q8+Y*Q9))))))))
  ENDIF
END FUNCTION BESSI1
