!> \file bessk0.f90
!> \brief compute modified Bessel function \f$ K_0 \f$
!> \details Details can be found in Press et al. <I> Numerical Resipes in Fortran 77 and 90 (second edition) </I> (2001), pp. 231
!> @author William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
!> @date 2001
REAL (KIND(0D0))  FUNCTION BESSK0(X)
!> input value x
  REAL (KIND(0D0)) :: x,bessi0
  REAL (KIND(0D0)) :: Y,P1,P2,P3,P4,P5,P6,P7,&
       Q1,Q2,Q3,Q4,Q5,Q6,Q7
  DATA P1,P2,P3,P4,P5,P6,P7/-0.57721566D0,0.42278420D0,0.23069756D0,&
       0.3488590D-1,0.262698D-2,0.10750D-3,0.74D-5/
  DATA Q1,Q2,Q3,Q4,Q5,Q6,Q7/1.25331414D0,-0.7832358D-1,0.2189568D-1,&
       -0.1062446D-1,0.587872D-2,-0.251540D-2,0.53208D-3/
  IF (X.le.2d0) THEN
     Y=X*X/4d0
     BESSK0=(-dlog(X/2d0)*BESSI0(X))+(P1+Y*(P2+Y*(P3+&
          Y*(P4+Y*(P5+Y*(P6+Y*P7))))))
  else if (x.gt.5d2) then
     bessk0=0d0
  ELSE
     Y=(2d0/X)
     BESSK0=(dexp(-X)/dsqrt(X))*(Q1+Y*(Q2+Y*(Q3+&
          Y*(Q4+Y*(Q5+Y*(Q6+Y*Q7))))))
  ENDIF

END FUNCTION BESSK0
