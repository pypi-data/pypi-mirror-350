!> \file bessk1.f90
!> \brief compute modified Bessel function \f$ K_1 \f$
!> \details Details can be found in Press et al. <I> Numerical Resipes in Fortran 77 and 90 (second edition) </I> (2001), pp. 232
!> @author William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
!> @date 2001
REAL (KIND(0D0))  FUNCTION BESSK1(X)
  REAL (KIND(0D0)) :: x,bessi1
  REAL (KIND(0D0)) :: Y,P1,P2,P3,P4,P5,P6,P7,&
       Q1,Q2,Q3,Q4,Q5,Q6,Q7
  DATA P1,P2,P3,P4,P5,P6,P7/1.0D0,0.15443144D0,-0.67278579D0,&
       -0.18156897D0,-0.1919402D-1,-0.110404D-2,-0.4686D-4/
  DATA Q1,Q2,Q3,Q4,Q5,Q6,Q7/1.25331414D0,0.23498619D0,-0.3655620D-1,&
       0.1504268D-1,-0.780353D-2,0.325614D-2,-0.68245D-3/
  IF (X.LE.2d0) THEN
     Y=X*X/4d0
     BESSK1=(dlog(X/2d0)*BESSI1(X))+(1d0/X)*(P1+Y*(P2+&
          Y*(P3+Y*(P4+Y*(P5+Y*(P6+Y*P7))))))
  else if (x.gt.5d2) then
     bessk1=0d0
  ELSE
     Y=2d0/X
     BESSK1=(dexp(-X)/dsqrt(X))*(Q1+Y*(Q2+Y*(Q3+Y*(Q4+Y*&
          (Q5+Y*(Q6+Y*Q7))))))
  ENDIF

END FUNCTION BESSK1
