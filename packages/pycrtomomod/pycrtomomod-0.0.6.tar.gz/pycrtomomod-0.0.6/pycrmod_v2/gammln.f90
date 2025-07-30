!> \file gammln.f90
!> \brief compute Gamma function \f$ \Gamma(x) \f$
!> \details Details can be found in Press et al. <I> Numerical Resipes in Fortran 77 and 90 (second edition) </I> (2001), pp. 207
!> @author William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
!> @date 2001
REAL (KIND(0D0))  FUNCTION gammln(xx)
  REAL (KIND(0D0))  :: xx
  INTEGER (KIND=4)  :: j
  REAL (KIND (0D0)) :: ser,stp,tmp,x,y,cof(6)
  SAVE cof,stp
  DATA cof,stp/76.18009172947146d0,-86.50532032941677d0, &
       24.01409824083091d0,-1.231739572450155d0,.1208650973866179d-2, &
       -.5395239384953d-5,2.5066282746310005d0/
  x=xx
  y=x
  tmp=x+5.5d0
  tmp=(x+0.5d0)*dlog(tmp)-tmp
  ser=1.000000000190015d0
  do j=1,6
     y=y+1.d0
     ser=ser+cof(j)/y
  END DO
  gammln=tmp+dlog(stp*ser/x)
  return
END FUNCTION gammln
