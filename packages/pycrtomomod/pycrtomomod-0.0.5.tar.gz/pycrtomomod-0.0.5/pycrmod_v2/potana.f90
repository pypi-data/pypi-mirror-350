!> \file potana.f90
!> \brief compute analytical solution
!> \details Compute the analytical solution of the Helmholtz equation of a homogeneous half-space for unity current \f$ 1A \f$. 
!> @author Andreas Kemna 
!> @date 01/04/1996

subroutine potana(l,k,my_pota)

!     Unterprogramm zur Berechnung der analytischen Loesung der
!     Helmholtzgleichung fuer einen homogenen Halbraum (fuer Einheitsstrom !).

!     Andreas Kemna                                            04-Jan-1996
!     Letzte Aenderung   11-Nov-1997

!.....................................................................

  USE sigmamod
  USE electrmod
  USE elemmod, ONLY : sanz, snr, sx, sy
  USE wavenmod

  IMPLICIT none

!.....................................................................

!     EIN-/AUSGABEPARAMETER:

!     Elektrodenindex
  INTEGER (KIND=4)  :: l

!     Wellenzahlindex
  INTEGER (KIND=4)  :: k

!!$ Analytische berechnete Potentialwerte 
  COMPLEX (KIND(0D0)), DIMENSION(sanz) :: my_pota

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Hilfsfunction
  REAL (KIND(0D0))  :: bessk0

!     Hilfsvariablen
  REAL (KIND(0D0))  :: xk1,yk1,xk2,yk2,x21,y21m,y21p,rm,rp,potmax,dum
  COMPLEX (KIND(0D0))  ::    dum2
  INTEGER (KIND=4)  ::  idum,j

!     Pi
  REAL (KIND(0D0))  ::  pi

!.....................................................................

  pi = dacos(-1d0)

  xk1    = sx(snr(enr(l)))
  yk1    = sy(snr(enr(l)))
  idum   = enr(l)
  potmax = 0d0

  do j=1,idum-1
     xk2  = sx(snr(j))
     yk2  = sy(snr(j))
     x21  = xk2-xk1
     y21m = yk2-yk1
     y21p = yk2+yk1
     rm   = dsqrt(x21*x21+y21m*y21m)
     rp   = dsqrt(x21*x21+y21p*y21p)

     dum     = bessk0(rm*kwn(k)) + bessk0(rp*kwn(k))
     potmax  = dmax1(potmax,dum)
     my_pota(j) = dcmplx(dum)
  end do

  do j=idum+1,sanz
     xk2  = sx(snr(j))
     yk2  = sy(snr(j))
     x21  = xk2-xk1
     y21m = yk2-yk1
     y21p = yk2+yk1
     rm   = dsqrt(x21*x21+y21m*y21m)
     rp   = dsqrt(x21*x21+y21p*y21p)

     dum     = bessk0(rm*kwn(k)) + bessk0(rp*kwn(k))
     potmax  = dmax1(potmax,dum)
     my_pota(j) = dcmplx(dum)
  end do

!     Endlichen Wert fuer Singularitaet vorgeben (beeinflusst nur
!     berechnete Potentialwerte in direkter Umgebung des Stromknotens !)
!     ak
  my_pota(idum) = dcmplx(5d0*potmax)

!     Potentialwerte skalieren (fuer Einheitsstrom !)
  dum2 = dcmplx(5d-1/pi) / sigma0

  my_pota = my_pota * dum2

end subroutine potana
