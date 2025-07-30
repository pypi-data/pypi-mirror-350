module relectrmod
    contains
      subroutine relectr(kanal,datei)

!     Unterprogramm zum Einlesen der Elektrodenverteilung aus 'datei'.

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   24-Oct-1996

! ....................................................................
      USE electrmod
      USE elemmod
      USE errmod

      IMPLICIT none

! ....................................................................

!     EIN-/AUSGABEPARAMETER:

!     Kanalnummer
      integer     ::   kanal

!     Datei
      character(80) :: datei

! ....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariable
      integer      ::   i

! ....................................................................

!     'datei' oeffnen
      fetxt = datei

      errnr = 1
      open(kanal,file=fetxt,status='old',err=999)

      errnr = 3

!     Anzahl der Elektroden einlesen
      read(kanal,*,end=1001,err=1000) eanz

!!!   $ memory allocation
      ALLOCATE (enr(eanz),stat=errnr)
      IF (errnr /= 0) THEN
         fetxt = 'Error memory allocation enr'
         errnr = 94
         goto 1000
      END IF

!     Knotennummern der Elektroden einlesen
      do i=1,eanz
         read(kanal,*,end=1001,err=1000) enr(i)

!     Ggf. Fehlermeldung
         if (enr(i).gt.sanz) then
            fetxt = ' '
            errnr = 29
            goto 1000
         end if
      end do

!     'datei' schliessen
      close(kanal)

      errnr = 0
      return

! ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

 999  return

 1000 close(kanal)
      return

 1001 close(kanal)
      errnr = 2
      return

      end subroutine relectr
end module relectrmod
