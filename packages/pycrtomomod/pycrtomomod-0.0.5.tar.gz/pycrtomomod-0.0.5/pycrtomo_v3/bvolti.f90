!> \file bvolti.f90
!> \brief compute measured voltages for unity current \f$ 1A \f$.
!> \details Used for the inversion algorithm

!> @author Andreas Kemna
!> @date 09/03/1994, last change 11/13/1997

SUBROUTINE bvolti()

!     Unterprogramm zur Berechnung der modellierten Spannungswerte
!     (beachte: Potentialwerte wurden fuer Einheitsstrom berechnet).

!     Andreas Kemna                                            03-Sep-1994
!     Letzte Aenderung   13-Nov-1997

!.....................................................................

  USE alloci
  USE femmod
  USE datmod
  USE electrmod
  USE errmod

  IMPLICIT NONE


!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariable
  INTEGER (KIND = 4)  ::     i

!     Elektrodennummern
  INTEGER (KIND = 4)  ::     elec1,elec2,elec3,elec4

!     Hilfsvariablen
  COMPLEX (KIND(0D0)) ::    dum1,dum2,dum3,dum4
  REAL (KIND(0D0))    ::     dum1dc,dum2dc,dum3dc,dum4dc

!.....................................................................

  DO i=1,nanz

!     Stromelektroden bestimmen
     elec1 = MOD(strnr(i),10000)
     elec2 = (strnr(i)-elec1)/10000

!     Messelektroden bestimmen
     elec3 = MOD(vnr(i),10000)
     elec4 = (vnr(i)-elec3)/10000

!     Spannungswert berechnen (Superposition)
!     (beachte: Faktoren '.../2d0' (-> Potentialwerte fuer Einheitsstrom)
!     und '...*2d0' (-> Ruecktransformation) kuerzen sich weg !)
     IF (ldc) THEN
        dum1dc = DBLE(min0(elec4,1)*min0(elec2,1)) &
             *hpotdc(enr(max0(elec4,1)),max0(elec2,1))
        dum2dc = DBLE(min0(elec4,1)*min0(elec1,1)) &
             *hpotdc(enr(max0(elec4,1)),max0(elec1,1))
        dum3dc = DBLE(min0(elec3,1)*min0(elec2,1)) &
             *hpotdc(enr(max0(elec3,1)),max0(elec2,1))
        dum4dc = DBLE(min0(elec3,1)*min0(elec1,1)) &
             *hpotdc(enr(max0(elec3,1)),max0(elec1,1))

        volt(i) = dcmplx((dum1dc-dum2dc) - (dum3dc-dum4dc))
     ELSE
        dum1 = dcmplx(min0(elec4,1)*min0(elec2,1)) &
             *hpot(enr(max0(elec4,1)),max0(elec2,1))
        dum2 = dcmplx(min0(elec4,1)*min0(elec1,1)) &
             *hpot(enr(max0(elec4,1)),max0(elec1,1))
        dum3 = dcmplx(min0(elec3,1)*min0(elec2,1)) &
             *hpot(enr(max0(elec3,1)),max0(elec2,1))
        dum4 = dcmplx(min0(elec3,1)*min0(elec1,1)) &
             *hpot(enr(max0(elec3,1)),max0(elec1,1))

        volt(i) = (dum1-dum2) - (dum3-dum4)
     END IF

     IF (cdabs(volt(i)).EQ.0d0) THEN
        WRITE(fetxt,*)'index',i
        PRINT*,'bvolti exception::',i
        errnr = 82
        GOTO 1000
     END IF

!     Werte logarithmieren
     sigmaa(i) = -cdlog(volt(i))
  END DO

  errnr = 0
  RETURN

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 RETURN

END SUBROUTINE bvolti
