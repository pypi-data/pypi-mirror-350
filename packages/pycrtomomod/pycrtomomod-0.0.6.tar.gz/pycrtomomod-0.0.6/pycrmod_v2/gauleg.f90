!> \file gauleg.f90
!> \brief Gauss-Legendre integration
!> \details Gauss-Legendre integration: Returns the abcissas (x) and weights(w) of length n for a Gauss quadrature integration. Provides \f$x_i\f$ and \f$w_i \f$ inside
!> \f[ \sum_{x_1}^{x_2} f(x) dx = \sum_{i=1}^N w_i f(x_i) \f] 
!> Details can be found in Press et al. <I> Numerical Resipes in Fortran 77 and 90 (second edition) </I> (2001), pp. 145
!> @author William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
!> @date 2001

SUBROUTINE gauleg(x1,x2,x,w,n)
  IMPLICIT none
  INTEGER (KIND = 4)  :: n
  REAL (KIND(0D0))    :: x1,x2,x(n),w(n)
  REAL (KIND(0D0))    :: EPS
  PARAMETER (EPS=3.d-14)
  INTEGER (KIND = 4)  :: i,j,m
  REAL (KIND(0D0))    :: p1,p2,p3,pp,xl,xm,z,z1
  m=(n+1)/2
  xm=0.5d0*(x2+x1)
  xl=0.5d0*(x2-x1)
  do i=1,m
     z=cos(3.141592653589793d0*(dble(i)-.25d0)/(dble(n)+.5d0))
1    continue
     p1=1.d0
     p2=0.d0
     do j=1,n
        p3=p2
        p2=p1
        p1=((2.d0*dble(j)-1.d0)*z*p2-(dble(j)-1.d0)*p3)/dble(j)
     END DO
     pp=dble(n)*(z*p1-p2)/(z*z-1.d0)
     z1=z
     z=z1-p1/pp
     if(dabs(z-z1).gt.EPS)goto 1
     x(i)=xm-xl*z
     x(n+1-i)=xm+xl*z
     w(i)=2.d0*xl/((1.d0-z*z)*pp*pp)
     w(n+1-i)=w(i)
  END DO
  return
END SUBROUTINE gauleg
