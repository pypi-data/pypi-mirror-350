subroutine kompbdc(nelec,b_komp,fak_komp)

!!!$     Unterprogramm zur Kompilation des Konstanten- bzw. Stromvektors 'bdc'
!!!$     fuer Einheitsstrom.

!!!$     Andreas Kemna                                            11-Oct-1993
!!!$     Letzte Aenderung   16-Jul-2007

!!!$.....................................................................

  USE femmod
  USE electrmod
  USE elemmod

  IMPLICIT none

!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:
  REAL (KIND(0D0)),DIMENSION (sanz) :: b_komp
  REAL (KIND(0D0)),DIMENSION (sanz) :: fak_komp
!!!$     Aktuelle Elektrodennummer
  INTEGER (KIND = 4) ::     nelec

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Indexvariable
  INTEGER (KIND = 4) ::     i

!!!$.....................................................................

!!!$     Konstantenvektor auf Null setzen
!!$  b_komp = 0D0
  do i=1,sanz
     b_komp(i) = 0d0
  end do

!!!$     Aufbau des Konstanten- bzw. Stromvektors mit Skalierung
!!!$     ( A * x + b = 0 )
  b_komp(enr(nelec)) = -fak_komp(enr(nelec))

!!!$     akc BAW-Tank
!!!$     ak        bdc(211) = fak(211)
!!!$     akc Model EGS2003
!!!$     ak        bdc(1683) = fak(1683)
!!!$     akc Lysimeter hor_elem\normal
!!!$     ak        bdc(129) = fak(129)
!!!$     akc Lysimeter hor_elem\fine
!!!$     ak        bdc(497) = fak(497)
!!!$     akc Simple Tucson Model
!!!$     ak        bdc(431) = fak(431)
!!!$     akc TU Berlin Mesokosmos
!!!$     ak        bdc(201) = fak(201)
!!!$     akc Andy
!!!$     ak        bdc(2508) = fak(2508)
!!!$     akc Sandra (ele?_anom)
!!!$     ak        bdc(497) = fak(497)

  if (lsink) b_komp(nsink) = fak_komp(nsink)

end subroutine kompbdc
