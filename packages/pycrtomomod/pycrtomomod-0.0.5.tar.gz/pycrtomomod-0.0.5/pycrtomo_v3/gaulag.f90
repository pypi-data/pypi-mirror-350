!> \file gaulag.f90
!> \brief Gauss-Laguerre integration
!> \details Gauss-Laguerre integration: Computation of abcissas and weights for the numerical integration of the k integral for the backward transformation to the y space. Details can be found in Press et al. <I> Numerical Resipes in Fortran 77 and 90 (second edition) </I> (2001), pp. 146
!> @author William H. Press, Saul A. Teukolsky, William T. Vetterling, Brian P. Flannery
!> @date 2001
SUBROUTINE gaulag(x,w,n,alf)
  IMPLICIT none
  INTEGER (KIND = 4) ::n,MAXIT
  REAL (KIND(0D0)) :: alf,w(n),x(n)
  REAL (KIND(0D0)) :: EPS
  PARAMETER (EPS=3.D-14,MAXIT=10)
!!$CU    USES gammln
  INTEGER (KIND = 4) :: i,its,j
  REAL (KIND(0D0)) :: ai,gammln
  REAL (KIND(0D0)) :: p1,p2,p3,pp,z,z1
  do i=1,n
     if(i.eq.1)then
        z=(1.d0+alf)*(3.d0+.92d0*alf)/(1.d0+2.4d0*n+1.8d0*alf)
     else if(i.eq.2)then
        z=z+(15.d0+6.25d0*alf)/(1.d0+.9d0*alf+2.5d0*n)
     else
        ai=dble(i-2)
        z=z+((1.d0+2.55d0*ai)/(1.9d0*ai)+1.26d0*ai*alf/ &
             (1.d0+3.5d0*ai))*(z-x(i-2))/(1.d0+.3d0*alf)
     endif
     do its=1,MAXIT
        p1=1.d0
        p2=0.d0
        do j=1,n
           p3=p2
           p2=p1
           p1=((dble(2*j-1)+alf-z)*p2-(dble(j-1)+alf)*p3)/dble(j)
        END do
        pp=(dble(n)*p1-(dble(n)+alf)*p2)/z
        z1=z
        z=z1-p1/pp
        if(dabs(z-z1).le.EPS)goto 1
     END do
     print*,'too many iterations in gaulag'
1    x(i)=z
     w(i)=-dexp(gammln(alf+dble(n))-gammln(dble(n)))/(pp*dble(n)*p2)
  END do
  return
END SUBROUTINE gaulag
