!> \file bvolt.f90
!> \brief compute measured voltages and apparent resistivities.

!> @author Andreas Kemna
!> @date 11/06/1997

subroutine bvolt()

!     Unterprogramm zur Berechnung der Spannungs- und scheinbaren
!     Widerstandswerte (beachte: Potentialwerte wurden fuer Einheitsstrom
!     berechnet).

!     Andreas Kemna                                            03-Sep-1994
!     Letzte Aenderung   06-Nov-1997

!.....................................................................

  USE alloci
  USE datmod
  USE electrmod
  USE errmod

  IMPLICIT none


!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariable
  INTEGER (KIND = 4)  ::     i,j

!     Elektrodennummern
  INTEGER (KIND = 4)  ::     elec1,elec2,elec3,elec4

!     Hilfsvariablen
  COMPLEX (KIND(0D0)) ::    dum1,dum2,dum3,dum4

!.....................................................................
  j=0
  do i=1,nanz

!     Stromelektroden bestimmen
     elec1 = mod(strnr(i),10000)
     elec2 = (strnr(i)-elec1)/10000

!     Messelektroden bestimmen
     elec3 = mod(vnr(i),10000)
     elec4 = (vnr(i)-elec3)/10000

!     Spannungswert berechnen (Superposition)
!     (beachte: Faktoren '.../2d0' (-> Potentialwerte fuer Einheitsstrom)
!     und '...*2d0' (-> Ruecktransformation) kuerzen sich weg !)
     dum1 = dcmplx(min0(elec4,1)*min0(elec2,1)) &
          *hpot(enr(max0(elec4,1)),max0(elec2,1))
     dum2 = dcmplx(min0(elec4,1)*min0(elec1,1)) &
          *hpot(enr(max0(elec4,1)),max0(elec1,1))
     dum3 = dcmplx(min0(elec3,1)*min0(elec2,1)) &
          *hpot(enr(max0(elec3,1)),max0(elec2,1))
     dum4 = dcmplx(min0(elec3,1)*min0(elec1,1)) &
          *hpot(enr(max0(elec3,1)),max0(elec1,1))

     volt(i) = (dum1-dum2) - (dum3-dum4)

     if (cdabs(volt(i)).eq.0d0) then
        j=j+1
!     ak
        write(*,'(A,I8,A,I8)',ADVANCE='no')ACHAR(13)// &
             ' --- Messpannung',i,' ist null ',j
!     RM               fetxt = ' '
!     RM               errnr = 82
!     RM               goto 1000
     end if

!     Scheinbaren Widerstandswert berechnen
!     ak            sigmaa(i) = dcmplx(kfak(i)) * volt(i)
     sigmaa(i) = volt(i)
     sigmaa(i) = dcmplx(kfak(i)) * volt(i)
  end do
  IF (j/=0) WRITE (*,'(/A,I8,A)')' Vorsicht es wurde',j,&
       'mal keine Messpannung gemessen'
  errnr = 0
  return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

end subroutine bvolt
