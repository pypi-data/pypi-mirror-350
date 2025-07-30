REAL (KIND(0D0)) FUNCTION chareal(txt,ltxt)

!!$c Die Funktion wandelt einen String in einen Real-Wert;
!!$c bei Real-Werten muss die Laenge incl. '.' angegeben werden.
!!$
!!$c Andreas Kemna                                            03-Feb-1993
!!!$                                       Letzte Aenderung   24-Oct-1996

!!!$.....................................................................

  CHARACTER (*) ::  txt
  INTEGER (KIND = 4)  ::     ltxt
  INTEGER (KIND = 4)  ::     i,ih1,pos,j
  REAL (KIND(0D0)) ::    h2
  LOGICAL ::     neg

!!!$.....................................................................

  h2  = 0.
  pos = index(txt(1:ltxt),'.')-1

!!$c Vorzeichen bestimmen
  if (index(txt(1:ltxt),'-').gt.0) then
     neg = .true.
  else
     neg = .false.
  end if

!!$c Umrechnung von Integer-Werten ermoeglichen
  if (pos.eq.-1) pos=ltxt

  j = 0

!!$c Vorkommastellen
  do i=pos,1,-1
     ih1 = ichar(txt(i:i))

     if (ih1.ge.48.and.ih1.le.57) then
        h2 = real(ih1-48)*10.**j + h2
        j  = j+1
     end if
  END DO

!!$c Dezimalstellen
  if (pos.ne.ltxt) then
     j = -1

     do i=pos+2,ltxt
        ih1 = ichar(txt(i:i))

        if (ih1.ge.48.and.ih1.le.57) then
           h2 = real(ih1-48)*10.**j + h2
           j  = j-1
        end if

     END DO
  end if

  if (neg) then
     chareal = -h2
  else
     chareal = h2
  end if

  return
end FUNCTION chareal
