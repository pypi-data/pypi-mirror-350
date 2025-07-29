subroutine wdatm(kanal,datei)

!!!$     Unterprogramm zum Schreiben der Strom- und Spannungs- bzw.
!!!$     scheinbaren Widerstandswerte sowie der Elektrodenkennungen
!!!$     in 'datei'.

!!!$     Andreas Kemna                                            22-Oct-1993
!!!$     Letzte Aenderung   10-Mar-2007

!!!$.....................................................................

  USE datmod
  USE errmod

  IMPLICIT none


!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Kanalnummer
  INTEGER (KIND=4) ::   kanal

!!!$     Datei
  CHARACTER (80)   ::  datei

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Indexvariable
  INTEGER (KIND=4) ::    i

!!!$     Pi
  REAL(KIND(0D0))  ::    pi

!!!$     Hilfsvariablen
  REAL(KIND(0D0))  ::   bet,pha,npi
  INTEGER (KIND=4) ::    ie1,ie2
!!!$     Standartabweichung.-..
  REAL(KIND(0D0))  ::    stab
!!!$.....................................................................

!100 FORMAT(2(4X,I8),2(1x,G14.7))
  pi = dacos(-1d0)

!!!$     'datei' oeffnen
  fetxt = datei
  errnr = 1
  open(kanal,file=TRIM(fetxt),status='replace',err=999)
  errnr = 4

!!!$     Anzahl der Messwerte schreiben
  write(kanal,*,err=1000) nanz

!!!$     Stromelektrodennummern, Spannungselektrodennummern und scheinbare
!!!$     Widerstandswerte (Betrag und Phase (in mrad)) schreiben
  stab=5.0
  do i=1,nanz
     bet = cdabs(sigmaa(i))
     pha = datan2(dimag(sigmaa(i)),dble(sigmaa(i)))

!!!$     ak
!!!$     Ggf. Polaritaet vertauschen
     npi = dnint(pha/pi)*pi
     if (dabs(npi).gt.1d-12) then
        pha    = pha-npi
        ie1    = mod(vnr(i),10000)
        ie2    = (vnr(i)-ie1)/10000
        vnr(i) = ie1*10000+ie2
     end if

!!!$  write(kanal,*,err=1000)
!!!$  1                  strnr(i),vnr(i),real(bet),real(1d3*pha)
     write(kanal,*,err=1000)strnr(i),vnr(i),real(bet),real(1d3*pha)
!!!$     1                  strnr(i),vnr(i),real(bet),real(1d3*pha),
!!!$     1                  real(kfak(i))
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

end subroutine wdatm
