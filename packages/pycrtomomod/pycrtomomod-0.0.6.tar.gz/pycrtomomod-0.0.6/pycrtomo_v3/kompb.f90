subroutine kompb(nelec,b_komp,fak_komp)

!!!$     Unterprogramm zur Kompilation des Konstanten- bzw. Stromvektors 'b'
!!!$     fuer Einheitsstrom.

!!!$     Andreas Kemna                                            11-Oct-1993
!!!$     Letzte Aenderung   15-Jul-2007

!!!$.....................................................................

  USE femmod
  USE electrmod
  USE elemmod

  IMPLICIT none

!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:
!!$ Berechnete Potentialwerte (bzw. Loesungsverktor)
  COMPLEX (KIND(0D0)),DIMENSION(*):: b_komp
!!$ Skalirerungsfaktor
  REAL (KIND(0D0)),DIMENSION(*)  :: fak_komp

!!!$     Aktuelle Elektrodennummer
  INTEGER (KIND = 4) ::     nelec

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Indexvariable
  INTEGER (KIND = 4) ::     i

!!!$.....................................................................

!!!$     Konstantenvektor auf Null setzen
!!$  b_komp = 0.
  do i=1,sanz
     b_komp(i) = dcmplx(0d0)
  end do

!!!$     Aufbau des Konstanten- bzw. Stromvektors mit Skalierung
!!!$     ( A * x + b = 0 )
  b_komp(enr(nelec)) = dcmplx(-fak_komp(enr(nelec)))

!!!$     akc BAW-Tank
!!!$     ak        b_komp(211) = dcmplx(fak(211))
!!!$     akc Model EGS2003
!!!$     ak        b_komp(1683) = dcmplx(fak(1683))
!!!$     akc Lysimeter hor_elem\normal
!!!$     ak        b_komp(129) = dcmplx(fak(129))
!!!$     akc Lysimeter hor_elem\fine
!!!$     ak        b_komp(497) = dcmplx(fak(497))
!!!$     akc Simple Tucson Model
!!!$     ak        b_komp(431) = dcmplx(fak(431))
!!!$     akc TU Berlin Mesokosmos
!!!$     ak        b_komp(201) = dcmplx(fak(201))
!!!$     akc Andy
!!!$     ak        b_komp(2508) = dcmplx(fak(2508))
!!!$     akc Sandra (ele?_anom)
!!!$     ak        b_komp(497) = dcmplx(fak(497))
!!!$     akc Adrian (Tank)
!!!$     ak        b_komp(1660) = dcmplx(fak(1660))

  if (lsink) b_komp(nsink) = dcmplx(fak_komp(nsink))

  return
end subroutine kompb
