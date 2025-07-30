character (12) function intcha(idum,lidum)

!!!$ Die Function wandelt einen Integer 'idum' in einen String der
!!!$ Laenge 'lidum'.

!!!$ Andreas Kemna                                            22-Jan-1993
!!!$                                       Letzte Aenderung   24-Oct-1996

!!!$.....................................................................

  INTEGER (KIND = 4)  :: idum
  INTEGER (KIND = 4)  :: lidum
  INTEGER (KIND = 4)  :: i,ih1
  character (5)       :: form

!!!$.....................................................................

!!!$ Integer in String schreiben
  if (lidum.lt.10) then
     write(form,'(a2,i1,a1)') '(i',lidum,')'
  else
     write(form,'(a2,i2,a1)') '(i',lidum,')'
  end if

  write(intcha,form) idum

!!!$ Moegliche Blanks mit Nullen ueberschreiben
  do i=1,lidum
     ih1 = ichar(intcha(i:i))

     if (ih1.eq.32) then
        intcha(i:i) = '0'
     end if
  END DO

  return
end function intcha
