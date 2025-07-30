!> \file vre.f90
!> \brief perform forward and backward substitution
!> \details Perform forward and backward substitution of the linear system \f$ S\ x = b\f$ after the Cholesky decomposition, namely with \f$ S = L^*\ L .\f$  

subroutine vre(a_vre,b_vre,pot_vre)

!     Fuehrt das Vorwaerts- und Rueckwaertseinsetzen mit der Cholesky-Links-
!     dreiecksmatrix aus;
!     'b' bleibt unveraendert, 'pot' ist Loesungsvektor.

!     ( Vgl. Subroutine 'VRBNDN' in Schwarz (1991) )

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   24-Feb-1997

!.....................................................................

  USE alloci
  USE femmod
  USE elemmod

  IMPLICIT none

!.....................................................................
!!$Gesamtsteifigkeitsmatrix
  COMPLEX (KIND(0D0)), DIMENSION(*) :: a_vre
!!$ Konstanten-(bzw. Strom-) Vektor
  COMPLEX (KIND(0D0)), DIMENSION(*) :: b_vre
!!$ Berechnete Potentialwerte (bzw. Loesungsverktor)
  COMPLEX (KIND(0D0)), DIMENSION(*) :: pot_vre
!     PROGRAMMINTERNE PARAMETER:

!     Hilfsvariablen
  INTEGER (KIND=4)   :: idi,i0
  INTEGER (KIND=4)   :: m1,jlow
  COMPLEX(KIND(0D0)) ::   s

!     Indexvariablen
  INTEGER (KIND=4)   ::     i,j

!.....................................................................

  m1 = mb+1

  do i=1,sanz
     idi  = i*m1
     s    = b_vre(i)
     i0   = idi-i
     jlow = max0(1,i-mb)

     do j=jlow,i-1
        s = s - a_vre(i0+j)*pot_vre(j)
     END do

     pot_vre(i) = s / a_vre(idi)
  END do

  do i=sanz,1,-1
     pot_vre(i) = - pot_vre(i) / a_vre(idi)

     jlow = max0(1,i-mb)
     i0   = idi-i

     do j=jlow,i-1
        pot_vre(j) = pot_vre(j) + a_vre(i0+j)*pot_vre(i)
     END do

     idi = idi-m1
  END do

end subroutine vre
