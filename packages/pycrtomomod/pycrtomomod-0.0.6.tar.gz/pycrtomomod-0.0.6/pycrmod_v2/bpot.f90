!> \file bpot.f90
!> \brief compute the potential values in real space by applying the current strength \f$ I_i \f$
!> @author Andreas Kemna
!> @date 08/17/1994, last change 06/24/1997

subroutine bpot(kanal,datei)

!     Unterprogramm zur Berechnung der Potentialwerte
!     (beachte: Potentialwerte wurden fuer Einheitsstrom berechnet).

!     Andreas Kemna                                            17-Aug-1994
!     Letzte Aenderung   24-Jun-1997

!.....................................................................

  USE alloci
  USE femmod
  USE datmod
  USE elemmod
  USE errmod
  USE ompmod

  IMPLICIT none


!.....................................................................

!     EIN-/AUSGABEPARAMETER:

!     Kanalnummer
  INTEGER (KIND = 4)  ::     kanal

!     Datei
  CHARACTER (80)      ::    datei

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariablen
  INTEGER (KIND = 4)  ::     i,j

!     Elektrodennummern
  INTEGER (KIND = 4)  ::     elec1,elec2

  INTEGER (KIND = 4) ::  icount
!.....................................................................

  icount = 0

  !$OMP PARALLEL DEFAULT(none) &
  !$OMP SHARED (nanz,sanz,hpot,strom,strnr,datei,errnr,icount) &
  !$OMP PRIVATE(elec1,elec2,pot)
  !$OMP DO SCHEDULE (GUIDED,CHUNK_0)
  do i=1,nanz

     !$OMP ATOMIC
     icount = icount + 1

     WRITE (*,'(a,F10.2,A)',ADVANCE='no')ACHAR(13)//'Potential :',REAL(icount)/REAL(nanz)*100.,' %'
!     Stromelektroden bestimmen
     elec1 = mod(strnr(i),10000)
     elec2 = (strnr(i)-elec1)/10000

     do j=1,sanz

!     (beachte: Faktoren '.../2d0' (-> Potentialwerte fuer Einheitsstrom)
!     und '...*2d0' (-> Ruecktransformation) kuerzen sich weg !)
        if (elec1.eq.0) then
           pot(j) = hpot(j,elec2) * dcmplx(strom(i))
        else if (elec2.eq.0) then
           pot(j) = -hpot(j,elec1) * dcmplx(strom(i))
        else
           pot(j) = (hpot(j,elec2)-hpot(j,elec1)) * dcmplx(strom(i))
        end if
     end do

!     Potentialwerte ausgeben
     call wpot(datei,i,pot)
  end do
  !$OMP END DO
  !$OMP END PARALLEL

  IF (errnr /= 0) THEN
     PRINT*,'something went wrong during potential output'
     RETURN
  END IF

  errnr = 0
  return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 return

end subroutine bpot
