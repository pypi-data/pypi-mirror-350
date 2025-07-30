subroutine wpot(datei,np,mypot)

!!!$     Unterprogramm zum Schreiben der Potentialwerte.

!!!$     Andreas Kemna                                            17-Dec-1993
!!!$     Letzte Aenderung   10-Mar-2007

!!!$.....................................................................

  USE femmod
  USE datmod
  USE elemmod
  USE errmod

  IMPLICIT none


!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Kanalnummer
  INTEGER (KIND=4) ::   kanal

!!!$     Datei
  CHARACTER (80)   ::    datei

!!!$     Nummer der Projektion
  INTEGER (KIND=4) ::     np

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Indexvariable
  INTEGER (KIND=4) ::      i

!!!$     Hilfsvariablen
  INTEGER (KIND=4) ::     idum,idum2,lnanz
  CHARACTER (80)   ::    htxt
  CHARACTER (12)   ::     htxt2

!!!$     Hilfsfunctions
  CHARACTER (12)   ::    intcha
  CHARACTER (80)   ::    filpat

!!!$     (Back-) Slash
  CHARACTER (1)   ::     slash
  COMPLEX (KIND(0D0)), DIMENSION(sanz)  :: mypot

!!!$     tst        real            * 8     dum_re,dum_im,dum_mag,dum_pha

!!!$.....................................................................

  CALL get_unit(kanal)

!!!$     Slash
  slash = '/'

!!!$     'datei' modifizieren
  lnanz = int(log10(real(nanz)))+1
  htxt  = filpat(datei,idum2,1,slash(1:1))
  idum  = idum2+index(datei(idum2+1:80),'.')-1

  if ((idum-idum2-1).gt.(8-lnanz)) then
     fetxt = datei
     errnr = 15
     goto 999
  end if

  htxt2 = intcha(np,lnanz)
  htxt  = datei(1:idum)//htxt2(1:lnanz)//datei(idum+1:idum+4)

!!!$     'datei' oeffnen
  fetxt = htxt
  errnr = 1
  open(kanal,file=TRIM(fetxt),status='replace',err=999)
  errnr = 4

!!!$     Koordinaten und Potentialwerte (Real- und Imaginaerteil) der
!!!$     Knotenpunkte schreiben (in Reihenfolge der urspruenglichen
!!!$     Numerierung)
  do i=1,sanz
     write(kanal,*,err=1000)real(sx(snr(i))),real(sy(snr(i))),&
          real(dble(mypot(i))),real(dimag(mypot(i)))
!!!$     ak     1                real(cdabs(mypot(i))),
!!!$     ak     1                real(1d3*datan2(dimag(mypot(i)),dble(mypot(i))))
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

end subroutine wpot
