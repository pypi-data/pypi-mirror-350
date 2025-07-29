subroutine randdc(my_a,my_b)

!!!$     Unterprogramm modifiziert die Matrix 'adc' (Bandbreite 'mb') und den
!!!$     Konstantenvektor 'bdc' gemaess homogener Dirichletscher Randbedingungen.

!!!$     ( Vgl. Subroutine 'RBSTBNDN' in Schwarz (1991) )

!!!$     Andreas Kemna                                            12-Feb-1993
!!!$     Letzte Aenderung   13-Nov-1997

!!!$.....................................................................

!!!$.....................................................................

  USE elemmod , ONLY : sanz, mb, typanz, typ, selanz, nrel, nelanz

  IMPLICIT none

!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

  REAL (KIND (0D0)),DIMENSION ((mb+1)*sanz) :: my_a
  REAL (KIND (0D0)),DIMENSION (sanz)        :: my_b
!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Aktuelle Elementnummer
  INTEGER (KIND = 4) ::     iel

!!!$     Aktueller Elementtyp
  INTEGER (KIND = 4) ::     ntyp

!!!$     Anzahl der Knoten im aktuellen Elementtyp
  INTEGER (KIND = 4) ::     nkel

!!!$     Index-/Hilfsvariablen
  INTEGER (KIND = 4) ::     m1,ir,i,j,k,ia,ki,i2,j2,idk,ji

!!!$.....................................................................

  m1  = mb+1
  iel = 0

  do i2=1,typanz
     ntyp = typ(i2)
     nkel = selanz(i2)

     do j2=1,nelanz(i2)
        iel = iel+1

        if (ntyp.ne.13) CYCLE

        do ir=1,nkel
           k      = nrel(iel,ir)
           my_b(k) = 0d0

           idk      = k*m1
           my_a(idk) = 1d0

           if (k /= 1) THEN

              ia = max0(1,mb+2-k)

              do i=ia,mb
                 ki      = idk+i-m1
                 my_a(ki) = 0d0
              end do
           END if
           if (k.eq.sanz) CYCLE

           ia = max0(1,k-sanz+m1)

           do i=ia,mb
              j       = k-i+m1
              ji      = (j-1)*m1+i
              my_a(ji) = 0d0
           end do

        end do ! ir
     END do ! j2
  end do !i2

end subroutine randdc
