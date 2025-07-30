!> \file bessi0.f90
!> \brief compute modified Bessel function \f$ I_0 \f$
!> \details Details can be found in Press et al. <I> Numerical Resipes in Fortran 77 and 90 (second edition) </I> (2001), pp. 230
!> @author William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
!> @date 2001
REAL (KIND(0D0)) FUNCTION BESSI0(X)
!> input value x
  REAL (KIND (0D0)) :: x,ax
  REAL (KIND (0D0)) :: Y,P1,P2,P3,P4,P5,P6,P7,&
       Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9
  DATA P1,P2,P3,P4,P5,P6,P7/1.0D0,3.5156229D0,3.0899424D0,&
       1.2067492D0,0.2659732D0,0.360768D-1,0.45813D-2/
  DATA Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9/0.39894228D0,0.1328592D-1,&
       0.225319D-2,-0.157565D-2,0.916281D-2,-0.2057706D-1,&
       0.2635537D-1,-0.1647633D-1,0.392377D-2/
  IF (dabs(X).lt.3.75d0) THEN
     Y=(X/3.75d0)*(X/3.75d0)
     BESSI0=P1+Y*(P2+Y*(P3+Y*(P4+Y*(P5+Y*(P6+Y*P7)))))
  ELSE
     AX=dabs(X)
     Y=3.75d0/AX
     BESSI0=(dexp(AX)/dsqrt(AX))*(Q1+Y*(Q2+Y*(Q3+Y*(Q4+&
          Y*(Q5+Y*(Q6+Y*(Q7+Y*(Q8+Y*Q9))))))))
  ENDIF

END FUNCTION BESSI0
