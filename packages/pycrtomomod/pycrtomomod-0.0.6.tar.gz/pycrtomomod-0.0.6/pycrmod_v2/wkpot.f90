subroutine wkpot(kanal,datei)

!!!$     Unterprogramm zur Ausgabe der transformierten Potentialwerte.

!!!$     Andreas Kemna                                            11-Oct-1993
!!!$     Letzte Aenderung   24-Jun-1997

!!!$.....................................................................

  USE alloci
  USE electrmod
  USE elemmod
  USE wavenmod
  USE errmod

  IMPLICIT none


!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Kanalnummer
  INTEGER (KIND=4) ::      kanal

!!!$     Datei
  CHARACTER (80)   ::      datei

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Elektrodennummer
  INTEGER (KIND=4) ::     nelec

!!!$     Anzahl der Knotenpunkte, an denen transformierte Potentialwerte
!!!$     ausgegeben werden sollen
  INTEGER (KIND=4) ::     kanz

!!!$     Nummern der Knotenpunkte, an denen transformierte Potentialwerte
!!!$     ausgegeben werden sollen
  INTEGER(KIND = 4),DIMENSION(:),ALLOCATABLE :: knr

!!!$     Indexvariablen
  INTEGER (KIND=4) ::     i,k

!!!$     Hilfsvariable
  COMPLEX(KIND(0D0)) ::    dum

!!!$.....................................................................

!!!$     'datei' oeffnen
  fetxt = datei
  errnr = 1
  open(kanal,file=TRIM(fetxt),status='old',err=999)
  errnr = 3

!!!$     Elektrodennummer einlesen
  read(kanal,*,end=1001,err=1000) nelec

!!!$     Ggf. Fehlermeldung
  if (nelec.gt.eanz) then
     fetxt = ' '
     errnr = 54
     goto 1000
  end if

!!!$     Anzahl der Knotenpunkte einlesen
  read(kanal,*,end=1001,err=1000) kanz

!!!$     Ggf. Fehlermeldung
  if (kanz.gt.sanz) then
     fetxt = ' '
     errnr = 52
     goto 1000
  end if
  ALLOCATE (knr(kanz),stat=errnr)
  IF (errnr /= 0) THEN
     fetxt = 'Error memory allocation hsens'
     errnr = 94
     GOTO 1000
  END IF

!!!$     Knotennummern einlesen
  do i=1,kanz
     read(kanal,*,end=1001,err=1000) knr(i)

!!!$     Ggf. Fehlermeldung
     if (knr(i).gt.sanz) then
        fetxt = ' '
        errnr = 53
        goto 1000
     end if
  end do

  errnr = 4

!!!$     Entsprechenden transformierten Potentialwerte schreiben
!!!$     (Real- und Imaginaerteil)
  do i=1,kanz
     write(kanal,*,err=1000)
     write(kanal,*,err=1000) knr(i)

     do k=1,kwnanz
        dum = kpot(knr(i),nelec,k)
        write(kanal,*,err=1000) real(dble(dum)),real(dimag(dum))
     end do
  end do

!!!$     'datei' schliessen
  close(kanal)

  errnr = 0
  return

!!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!!!$     Fehlermeldungen

999 return

1000 close(kanal)
  return

1001 close(kanal)
  errnr = 2
  return

end subroutine wkpot
