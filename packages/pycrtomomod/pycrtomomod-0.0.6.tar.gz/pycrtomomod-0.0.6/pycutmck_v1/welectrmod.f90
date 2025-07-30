module welectrmod
    contains
      subroutine welectr(kanal,datei)

!     Unterprogramm zum Schreiben der Elektrodenverteilung in 'datei'.

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   21-Jan-2003

! ....................................................................

      USE electrmod
      USE errmod

      IMPLICIT none

! ....................................................................

!     EIN-/AUSGABEPARAMETER:

!     Kanalnummer
      integer :: kanal

!     Datei
      character(80) :: datei

! ....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariable
      integer    ::  i

! ....................................................................

!     'datei' oeffnen
      fetxt = datei

      errnr = 1
      open(kanal,file=fetxt,status='replace',err=1000)

      errnr = 4

!     Anzahl der Elektroden schreiben
      write(kanal,*,err=1000) eanz

!     Knotennummern der Elektroden schreiben
      do i=1,eanz
         write(kanal,*,err=1000) enr(i)
      end do

!     'datei' schliessen
      close(kanal)

      errnr = 0
      return

! ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

 1000 return

      end subroutine welectr
end module welectrmod
