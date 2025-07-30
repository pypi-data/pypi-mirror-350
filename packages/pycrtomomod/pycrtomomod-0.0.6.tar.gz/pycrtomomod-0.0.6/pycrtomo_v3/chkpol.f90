subroutine chkpol(lsetup)

!!!$     Unterprogramm zum automatischen Korrigieren der Polaritaeten.

!!!$     Andreas Kemna                                            07-Dec-1996
!!!$     Letzte Aenderung   07-Nov-1997

!!!$.....................................................................

  USE invmod
  USE datmod
  USE errmod
  USE pathmod

  IMPLICIT none


!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Hilfsschalter
  LOGICAL ::     lsetup

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Messelektrodennummern
  INTEGER (KIND = 4)  ::  elec3,elec4

!!!$     Hilfsvariablen
  INTEGER (KIND = 4)  ::  i,idat,isig

!!!$     Real-, Imaginaerteile
  REAL (KIND(0D0))    ::  redat,imdat,resig,imsig

!!!$     Pi
  REAL (KIND(0D0))    :: pi

!!!$.....................................................................

  pi = dacos(-1d0)



  do i=1,nanz
     wdfak(i) = 1

!!!$     Messelektroden bestimmen
     elec3 = mod(vnr(i),10000)
     elec4 = (vnr(i)-elec3)/10000

!!!$     Logarithmierte Betraege in den Realteilen,
!!!$     Phasen (in rad) in den Imaginaerteilen
     redat = dble(dat(i))
     imdat = dimag(dat(i))
     resig = dble(sigmaa(i))
     imsig = dimag(sigmaa(i))

!!!$     Phasenbereich checken
     if (imdat.gt.pi/2d0) then
        idat = -1
     else if (imdat.le.-pi/2d0) then
        idat = 1
     else
        idat = 0
     end if

     if (imsig.gt.pi/2d0) then
        isig = -1
     else if (imsig.le.-pi/2d0) then
        isig = 1
     else
        isig = 0
     end if

     if (idat.eq.0.and.isig.ne.0) then

!!!$     Falls lpol=.true., angenommene Polaritaet des Messdatums falsch,
!!!$     ggf. Korrektur; auf jeden Fall Polaritaetswechsel
        vnr(i)    = elec3*10000 + elec4
        imsig     = imsig + dble(isig)*pi
        sigmaa(i) = dcmplx(resig,imsig)
        volt(i)   = cdexp(-sigmaa(i))

        if (lpol) then
           write(fprun,'(i4,a30)')i,' : correct and change polarity'
           if (.not.lsetup) wdfak(i)=0
        else
           imdat  = imdat - dsign(pi,imdat)
           dat(i) = dcmplx(redat,imdat)

           write(fprun,'(i4,a18)')i,' : change polarity'
           wdfak(i) = 0
        end if

     else if (idat.ne.0.and.isig.eq.0) then

!!!$     Falls lpol=.true., angenommene Polaritaet des Messdatums falsch,
!!!$     ggf. Korrektur
        if (lpol) then
           imdat  = imdat + dble(idat)*pi
           dat(i) = dcmplx(redat,imdat)

           write(fprun,'(i4,a19)')i,' : correct polarity'
           if (.not.lsetup) wdfak(i)=0
        else
           wdfak(i) = 0
        end if

     else if (idat.ne.0.and.isig.ne.0) then

!!!$     Polaritaetswechsel
        vnr(i)    = elec3*10000 + elec4
        imsig     = imsig + dble(isig)*pi
        sigmaa(i) = dcmplx(resig,imsig)
        volt(i)   = cdexp(-sigmaa(i))
        imdat     = imdat + dble(idat)*pi
        dat(i)    = dcmplx(redat,imdat)

        write(fprun,'(i4,a18)')i,' : change polarity'

     end if
  end do

!!!$     Ggf. Ausgabe
  do i=1,nanz
     if (wdfak(i).eq.0) write(fprun,'(i4,a11)') i,' : excluded'
  end do


  return
end subroutine chkpol
