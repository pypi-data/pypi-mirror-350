!> \file scaldc.f90
!> \brief scale the FE equations for better numerical accuracy for DC case
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

SUBROUTINE scaldc(a_scal,b_scal,fak_scal)

!     Unterprogramm skaliert 'adc' und 'bdc' und liefert die Skalierungs-
!     faktoren im Vektor 'fak'.

!     ( Vgl. Subroutine 'SCALBNDN' in Schwarz (1991) )

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   07-Mar-2003

!.....................................................................

  USE alloci
  USE femmod
  USE elemmod
  USE errmod

  IMPLICIT NONE


!.....................................................................
  REAL(KIND(0D0)),DIMENSION((mb+1)*sanz)  ::  a_scal
  REAL(KIND(0D0)),DIMENSION(sanz)  ::  b_scal
  REAL(KIND(0D0)),DIMENSION(sanz)  ::  fak_scal

!     Hilfsvariablen
  INTEGER (KIND=4) ::     idi,i0
  INTEGER (KIND=4) ::     ja
  REAL(KIND(0D0))  ::     dum

!     Indexvariablen
  INTEGER (KIND=4) ::     i,j

!.....................................................................

  DO i=1,sanz

     idi = i*(mb+1)
     dum = a_scal(idi)

     IF (dum.LE.0d0) THEN
        WRITE (fetxt,'(a,I6,A,I6)')'scaldc',i,'idi',idi
        errnr = 27
        RETURN
     END IF

     a_scal(idi) = 1d0
     fak_scal(i)   = 1d0 / dsqrt(dum)
     b_scal(i)   = b_scal(i) * fak_scal(i)

     IF (i == 1) CYCLE

     i0 = i*mb
     ja = max0(1,i-mb)

     DO j=ja,i-1
        a_scal(i0+j) = a_scal(i0+j)*fak_scal(i)*fak_scal(j)
     END DO

  END DO

  errnr = 0

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen
END SUBROUTINE scaldc
