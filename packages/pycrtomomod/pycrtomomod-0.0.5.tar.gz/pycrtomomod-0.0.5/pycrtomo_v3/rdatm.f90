!> \file rdatm.f90
!> \brief read data and electrode configurations for the forward modelling
!> @author Andreas Kemna 
!> @date 10/11/1993

subroutine rdatm(kanal,datei)

!     Unterprogramm zum Einlesen der Stromwerte sowie der Elektroden-
!     kennungen aus 'datei'.

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   22-Feb-2006

!.....................................................................

  USE datmod
  USE electrmod
  USE errmod

  IMPLICIT none


!.....................................................................

!     EIN-/AUSGABEPARAMETER:

!> unit number
  INTEGER(KIND = 4) ::    kanal

!> filename
  CHARACTER (80)    ::   datei

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariable
  INTEGER(KIND = 4) ::     i

!     Elektrodennummern
  INTEGER(KIND = 4) ::     elec1,elec2,elec3,elec4
!c check whether the file format is crtomo konform or not..
  LOGICAL           ::    crtf
!c
!.....................................................................

!     'datei' oeffnen
  fetxt = datei
  errnr = 1
  open(kanal,file=TRIM(fetxt),status='old',err=999)
  errnr = 3

!     Anzahl der Messwerte lesen
  read(kanal,*,end=1001,err=1000) nanz
!c check if data file format is CRTOmo konform..
  read(kanal,*,end=1001,err=1000) elec1
  BACKSPACE(kanal)

  elec3=elec1-10000 ! are we still positive?

  crtf=(elec3 .ge. 0) ! crtomo konform?

  ALLOCATE (strnr(nanz),strom(nanz),volt(nanz),sigmaa(nanz),&
       kfak(nanz),vnr(nanz),stat=errnr)
  IF (errnr /= 0) THEN
     fetxt = 'Error memory allocation volt '
     errnr = 94
     goto 1000
  END IF


!     Stromelektrodennummern, Stromwerte und Spannungselektrodennummern lesen
  do i=1,nanz
     WRITE (*,'(A,I6)',ADVANCE='no')ACHAR(13)//'Getting voltage ',i
     IF (crtf) THEN
        read(kanal,*,end=1001,err=1000)strnr(i),vnr(i)
     ELSE
        read(kanal,*,end=1001,err=1000)elec1,elec2,elec3,elec4
        strnr(i) = elec1*10000 + elec2
        vnr(i)   = elec3*10000 + elec4
     END IF
!     Einheitsstrom annehmen
     strom(i) = 1d0

!     Stromelektroden bestimmen
     elec1 = mod(strnr(i),10000)
     elec2 = (strnr(i)-elec1)/10000

!     Messelektroden bestimmen
     elec3 = mod(vnr(i),10000)
     elec4 = (vnr(i)-elec3)/10000

!     Ggf. Fehlermeldung
     if (elec1.lt.0.or.elec1.gt.eanz.or. &
          elec2.lt.0.or.elec2.gt.eanz.or. &
          elec3.lt.0.or.elec3.gt.eanz.or. &
          elec4.lt.0.or.elec4.gt.eanz) then
        WRITE (fetxt,'(a,I5,a)')'Electrode pair ',i,'not correct '
        errnr = 46
        goto 1000
     end if
! >> RM
! plausibility check of possible electrode intersection
! devide the strnr and vnr into elec{1,2,3,4}
! 
     IF ((elec1.eq.elec2).OR.(elec3.eq.elec4).OR.&
          &((((elec1.eq.elec3).or.(elec1.eq.elec4)).and.(elec1.ne.0)).or.&
          (((elec2.eq.elec3).or.(elec2.eq.elec4)).and.(elec2.ne.0)))) THEN
        WRITE (fetxt,'(a,I7)')' duplicate electrodes for reading ',i
        errnr = 73
        GOTO 1000
     END IF
! << RM

  end do

!     'datei' schliessen
  close(kanal)

  errnr = 0
  return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

999 return

1000 close(kanal)
  return

1001 close(kanal)
  errnr = 2
  return

end subroutine rdatm
