subroutine wout(kanal,dsigma,dvolt)

!!!$     Unterprogramm zum Schreiben der Widerstandsverteilung und der
!!!$     modellierten Daten inkl. Elektrodenkennungen.

!!!$     Andreas Kemna                                            28-Sep-1994
!!!$     Letzte Aenderung   10-Mar-2007

!!!$.....................................................................

  USE datmod
  USE femmod
  USE invmod
  USE sigmamod
  USE modelmod
  USE elemmod
  USE errmod
  USE konvmod
  USE pathmod

  IMPLICIT none

!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Kanalnummer
  INTEGER (KIND=4) ::  kanal

!!!$     Dateinamen
  CHARACTER (80)   ::  dsigma,dvolt

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:
!!!$     Indexvariablen
  INTEGER (KIND=4) ::  i

!!!$     Hilfsvariablen
  INTEGER (KIND=4) ::  idum,idum2
  CHARACTER (80)   ::  htxt
  COMPLEX(KIND(0D0))  ::  dum

!!!$     Hilfsfunctions
  CHARACTER (80)   ::   filpat

!!!$     diff+<
  REAL(KIND(0D0))  ::   dum2,dum3
!!!$     diff+>
  CHARACTER (2)   ::   ci
!!!$.....................................................................

!!!$     'dsigma' modifizieren

  WRITE (ci,'(I2.2)')it
!!$  IF (it>9) THEN
!!$     WRITE (ci,'(I2)')it
!!$  ELSE 
!!$     WRITE (ci,'(a,I1)')'0',it
!!$  END IF
  htxt = filpat(dsigma,idum2,1,slash(1:1))
  idum = idum2+index(dsigma(idum2+1:80),'.')-1
  htxt  = dsigma(1:idum)//ci//dsigma(idum+1:idum+4)

!!!$     Betraege ausgeben
  idum  = index(htxt,' ')
  fetxt = htxt(1:idum-4)//'mag'
  OPEN (kanal,FILE='inv.lastmod',STATUS='replace')
  WRITE (kanal,*)TRIM(fetxt)
  CLOSE (kanal)
  errnr = 1
  open(kanal,file=TRIM(fetxt),status='replace',err=999)
  errnr = 4
  write(kanal,*,err=1000) elanz,ACHAR(9),betrms

  do i=1,elanz
!!!$     diff+<
     if (.not.ldiff.AND..NOT.lprior) then
!!!$  if (.not.ldiff) then
!!!$     diff+>
        dum = dcmplx(1d0)/sigma(i)
!!!$ak   write(kanal,*,err=1000) real(espx(i)),real(espy(i)),&
!!!$ak         real(cdabs(dum))
        write(kanal,*,err=1000) real(espx(i)),&
             real(espy(i)),real(dlog10(cdabs(dum)))
!!!$ro   write(kanal,*,err=1000) real(espy(i)),real(espx(i)),&
!!!$ro      real(cdabs(dum))
!!!$     diff+<
     ELSE IF (lprior) THEN
        dum3 = CDABS(dcmplx(1d0)/sigma(i))
        dum2 = CDABS(dcmplx(1d0)/cdexp(m0(mnr(i))))
        !     dum3 = REAL(CDLOG(sigma(i))/m0(mnr(i)))
        write(kanal,*,err=1000)REAL(espx(i)),&
             REAL(espy(i)),real(dlog10(dum3))
!!$        write(kanal,'(7(f10.4,2x))',err=1000)REAL(espx(i)),&
!!$             REAL(espy(i)),real(dlog10(dum3)),&
!!$             (DLOG10(dum3) - DLOG10(dum2)),&
!!$             real(dlog10(dum2)),real(1d2*(1d0-dum2/dum3)),&
!!$             real(1d2*(1d0-dum3/dum2))
     else
        ! model resistivity, linear
        dum3 = cdabs(dcmplx(1d0)/sigma(i))
        ! start model, linear, resistivity
        dum2 = cdabs(dcmplx(1d0)/cdexp(m0(mnr(i))))
        write(kanal,'(7(f10.4,2x))',err=1000)&
             real(espx(i)),real(espy(i)),&
             ! log10(rho)
             real(dlog10(dum3)),&
             ! log10(rho0)
             real(dlog10(dum2)),&
             ! log10(rho) - log10(rho0)
             real(dlog10(dum3) - dlog10(dum2)),&
             ! (rho - rho0) / rho0 * 100
             real(1d2*(dum3/dum2-1d0)),&
             ! (sigma - sigma0) / sigma0 * 100
             real(1d2*(dum2/dum3-1d0))
     end if
!!!$     diff+>
  end do
  close(kanal)
  fetxt = htxt(1:idum-4)//'modl'
  OPEN (kanal,file=TRIM(fetxt),status='replace')

  WRITE (kanal,'(I7)',err=1000) elanz
  IF (.NOT.lprior) then
     DO i=1,elanz
        dum = dcmplx(1d0)/sigma(i)
        dum2 = real(1d3*datan2(dimag(dum),dble(dum)))
        WRITE (kanal,'(2(1x,G12.4))')1./REAL(sigma(i)),dum2
     END DO
  ELSE
     DO i=1,elanz
        dum = dcmplx(1d0)/sigma(i) ! - DCMPLX(1d0)/CDEXP(m0(mnr(i)))
        dum2 = real(1d3*datan2(dimag(dum),dble(dum)))
        WRITE (kanal,'(2(1x,G12.4))')1./REAL(sigma(i)),dum2
     END DO
  END IF
  CLOSE (kanal)
!!!$     Ggf. Phasen ausgeben
  if (.not.ldc) then
     fetxt = htxt(1:idum-4)//'pha'
     errnr = 1
     open(kanal,file=TRIM(fetxt),status='replace',err=999)
     errnr = 4
     write(kanal,*,err=1000) elanz,ACHAR(9),pharms

     do i=1,elanz
        dum = dcmplx(1d0)/sigma(i)
        write(kanal,*,err=1000)&
!!!$     ak Default
             real(espx(i)),real(espy(i)),&
             real(1d3*datan2(dimag(dum),dble(dum)))
!!!$     ak MMAJ
!!!$     ak     1                      real(espx(i)),real(espy(i)),
!!!$     ak     1                      -real(1d3*datan2(dimag(dum),dble(dum)))
     end do
     close(kanal)

     fetxt = htxt(1:idum-4)//'sig'
     errnr = 1
     open(kanal,file=TRIM(fetxt),status='replace',err=999)
     errnr = 4
     write(kanal,*,err=1000) elanz,betrms,pharms
     do i=1,elanz
        write(kanal,*,err=1000)REAL(sigma(i)),IMAG(sigma(i))
     end do
     close(kanal)
  end if

!!!$     'dvolt' modifizieren
  htxt = filpat(dvolt,idum2,1,slash(1:1))
  idum = idum2+index(dvolt(idum2+1:80),'.')-1

  htxt  = dvolt(1:idum)//ci//dvolt(idum+1:idum+4)

  fetxt = htxt
  errnr = 1
  open(kanal,file=TRIM(fetxt),status='replace',err=999)

  errnr = 4
  write(kanal,*,err=1000) nanz

!!!$     Stromelektrodennummern, Spannungselektrodennummern und scheinbare
!!!$     Widerstandswerte (Betrag und Phase (in mrad)) schreiben
  if (ldc) then
     do i=1,nanz
        write(kanal,*,err=1000)strnr(i),vnr(i),&
!!!$     diff-     1                      real(1d0/dexp(dble(sigmaa(i))))
!!!$     diff+<
             real(1d0/dexp(dble(sigmaa(i)))),wdfak(i)
!!!$     diff+>
     end do
  else
     do i=1,nanz
        write(kanal,*,err=1000)strnr(i),vnr(i),&
             real(1d0/dexp(dble(sigmaa(i)))),&
!!!$     diff-     1                      real(-1d3*dimag(sigmaa(i)))
!!!$     diff+<
             real(-1d3*dimag(sigmaa(i))),wdfak(i)
!!!$     diff+>
     end do
  end if

  close(kanal)

  errnr = 0
  return

!!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!!!$     Fehlermeldungen

999 return

1000 close(kanal)
  return

end subroutine wout
