!> \file scalab.f90
!> \brief scale the FE equations for better numerical accuracy
!> \details Schwarz 1991 and Kemna (private communication):
!> The diagonal elements of \f$ S \f$ in the linear system \f$ Sx = b \f$ are scaled to \f$ 1 \f$. Accordingly, the other elements of \f$ S\f$, \f$ x \f$ and \f$ b\f$ need to be scaled as well to maintain corrent results. In matrix notation, this is
!> \f[ S x = b \rightarrow (D S D) \  (D^{-1}x) = (D b) \f]
!> with the diagonal matrix \f$ D\f$ containing the scaling factors, namely
!> \f[ D_{ii} = 1/\sqrt{S_{ii}}, \ i = (1,...,n) \f]
!> Finally, the modified linear system 
!> \f[ \hat S \hat x = \hat b, \f]
!> with \f$ \hat S = D\ S\ D, \hat x = D^{-1}x, \hat b = D\ b \f$ is solved with super accuracy
!> @author Andreas Kemna 
!> @date 10/11/1993

subroutine scalab(a_scal,b_scal,fak_scal)

!     Unterprogramm skaliert 'a' und 'b' und liefert die Skalierungs-
!     faktoren im Vektor 'fak'.

!     ( Vgl. Subroutine 'SCALBNDN' in Schwarz (1991) )

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   07-Mar-2003

!.....................................................................

  USE alloci
  USE femmod
  USE elemmod
  USE errmod

  IMPLICIT none


!.....................................................................
!!$Gesamtsteifigkeitsmatrix
  COMPLEX (KIND(0D0)),DIMENSION(*):: a_scal
!!$ Berechnete Potentialwerte (bzw. Loesungsverktor)
  COMPLEX (KIND(0D0)),DIMENSION(*):: b_scal
!!$ Skalirerungsfaktor
  REAL (KIND(0D0)),DIMENSION(*)  :: fak_scal

!     Hilfsvariablen
  INTEGER (KIND=4) ::    idi,i0
  INTEGER (KIND=4) ::     ja
  REAL(KIND(0D0))  ::     dum

!     Indexvariablen
  INTEGER (KIND=4) ::     i,j

!.....................................................................

  do  i=1,sanz

     idi = i*(mb+1)
     dum = cdabs(a_scal(idi))

     if (dum.le.0d0) then
        WRITE (fetxt,*)'scalab idi',idi,'i',i
        errnr = 27
        goto 1000
     end if

     a_scal(idi) = a_scal(idi) / dcmplx(dum)
     fak_scal(i) = 1d0 / dsqrt(dum)
     b_scal(i)   = b_scal(i) * dcmplx(fak_scal(i))

     if (i.eq.1) CYCLE

     i0 = i*mb
     ja = max0(1,i-mb)

     do j=ja,i-1
        a_scal(i0+j) = a_scal(i0+j) * dcmplx(fak_scal(i)*fak_scal(j))
     END do

  END do

  errnr = 0
  return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 return

end subroutine scalab
