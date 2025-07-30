function filpat(disfile,ln,sw,slash)

!!!$     Die Funktion separiert aus einem kompletten Pfad 'disfile' den
!!!$     File-Namen (sw = 0) bzw. den Ordner (sw = 1) der Laenge 'ln'.

!!!$     Andreas Kemna                                            19-Jan-1993
!!!$     Letzte Aenderung   24-Oct-1996

!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

  IMPLICIT none
  CHARACTER (*)       ::  disfile
  CHARACTER (*)       ::  filpat
  INTEGER (KIND = 4)  ::     ln
  INTEGER (KIND = 4)  ::     sw
  CHARACTER (1)       ::    slash

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

  INTEGER (KIND = 4)  ::     id1,id2

!!!$.....................................................................

  id2 = 0
  id1 = 1
  DO WHILE (id1 /= 0) 
     id1 = index(disfile(id2+1:len(disfile)),slash(1:1))
     if (id1.ne.0) then
        id2 = id1+id2
     end if
  END DO
  if (sw.eq.0) then
     filpat = disfile(id2+1:len(disfile))
  else
     if (id2.ge.2) then
        filpat = disfile(1:id2-1)
     else
        filpat = ' '
     end if
  end if

  ln = index(filpat,' ')-1
  ln = max(ln,1)

  return
end function filpat
