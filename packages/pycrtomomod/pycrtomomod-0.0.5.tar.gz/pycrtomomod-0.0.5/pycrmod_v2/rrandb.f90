subroutine rrandb(kanal,datei)

!!!$     Unterprogramm zum Einlesen der Randwerte aus 'datei'.

!!!$     Andreas Kemna                                            12-Feb-1993
!!!$     Letzte Aenderung   15-Jul-2007

!!!$.....................................................................

  USE femmod
  USE elemmod
  USE randbmod
  USE errmod

  IMPLICIT none


!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Kanalnummer
  INTEGER (KIND =4) ::     kanal

!!!$     Datei
  CHARACTER (80)    ::    datei

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Indexvariable
  INTEGER (KIND=4)  ::  i

!!!$.....................................................................

!!!$     'datei' oeffnen
  fetxt = datei

  errnr = 1
  open(kanal,file=TRIM(fetxt),status='old',err=999)
  errnr = 3

!!!$     DC CASE
  if (ldc) then

!!!$     Anzahl der Randwerte einlesen (Dirichlet)
     read(kanal,*,end=1001,err=1000) rwdanz

     ALLOCATE (rwdnr(rwdanz),rwddc(rwdanz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation rwdnr '
        errnr = 94
        goto 1000
     END IF

!!!$     Knotennummern der Randwerte sowie Randwerte einlesen (Dirichlet)
     do i=1,rwdanz
        read(kanal,*,end=1001,err=1000) rwdnr(i),rwddc(i)

!!!$     Ggf. Fehlermeldung
        if (rwdnr(i).gt.sanz) then
           fetxt = ' '
           errnr = 30
           goto 1000
        end if
     end do

!!!$     Anzahl der Randwerte einlesen (Neumann)
     read(kanal,*,end=1001,err=1000) rwnanz

     ALLOCATE (rwndc(rwnanz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation rwdnr '
        errnr = 94
        goto 1000
     END IF

!!!$     Randwerte einlesen (Neumann)
     if (rwnanz.gt.0) read(kanal,*,end=1001,err=1000) &
          (rwndc(i),i=1,rwnanz)
  else

!!!$     COMPLEX CASE

!!!$     Anzahl der Randwerte einlesen (Dirichlet)
     read(kanal,*,end=1001,err=1000) rwdanz

     ALLOCATE (rwdnr(rwdanz),rwd(rwdanz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation rwdnr '
        errnr = 94
        goto 1000
     END IF

!!!$     Knotennummern der Randwerte sowie Randwerte einlesen (Dirichlet)
     do i=1,rwdanz
        read(kanal,*,end=1001,err=1000) rwdnr(i),rwd(i)

!!!$     Ggf. Fehlermeldung
        if (rwdnr(i).gt.sanz) then
           fetxt = ' '
           errnr = 30
           goto 1000
        end if
     end do

!!!$     Anzahl der Randwerte einlesen (Neumann)
     read(kanal,*,end=1001,err=1000) rwnanz

     ALLOCATE (rwn(rwnanz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation rwdnr '
        errnr = 94
        goto 1000
     END IF

!!!$     Randwerte einlesen (Neumann)
     if (rwnanz.gt.0) read(kanal,*,end=1001,err=1000) &
          (rwn(i),i=1,rwnanz)

!!!$     'datei' schliessen
  end if

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

end subroutine rrandb
