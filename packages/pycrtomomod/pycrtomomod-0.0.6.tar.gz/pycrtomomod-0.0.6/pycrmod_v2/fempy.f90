module fem_pyw

contains
    subroutine forward_calculation(return_value)

        USE alloci
        USE tic_toc
        USE femmod
        USE datmod
        USE sigmamod
        USE electrmod
        USE modelmod
        USE elemmod
        USE wavenmod
        USE randbmod
        USE errmod
        USE konvmod
        USE omp_lib
        USE ompmod
        USE get_ver

        IMPLICIT none
        !....................................................................
        INTEGER(KIND = 4), INTENT(OUT) :: return_value

        !   channel numbers
        integer ::  kanal

        !!!$   file names
        character       * 80    delem,delectr,dsigma,dstrom,&
            dkpot,dpot,dvolt,dsens,drandb
        ! character       * 80    delem,delectr,dsigma,dstrom,&
        !     dkpot,dpot,dvolt,dsens,drandb

        !!!$   Schalter ob transformierte Potentialwerte ausgegeben werden sollen
        ! switch that controls whether transformed potentials shall be returned
        logical         * 4     lkpot

        !!!$   Schalter ob Potentialwerte ausgegeben werden sollen
        logical         * 4     lpot

        !!!$   Schalter ob Spannungswerte ausgegeben werden sollen
        logical         * 4     lvolt

        !!!$   Schalter ob weiterer Datensatz modelliert werden soll
        logical         * 4     lagain

        !!!$   Schalter ob mit K-Faktor modelliert werden soll (default ohne)
        logical         * 4     wkfak

        !!!$   Schalter ob nur analytisch modelliert werden soll (default ohne)
        logical         * 4     lana

        !!!$   Indexvariablen
        integer         * 4     j,k,l,c1

        !!!$ counting wavenumbers
        INTEGER :: count

        character       *256    ftext
        INTEGER :: getpid,pid,maxthreads,mythreads

        !!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        PRINT*,'######### CMod ############'
        WRITE(*,"(a)") 'Licence:', &
        'Copyright © 1990-2020 Andreas Kemna <kemna@geo.uni-bonn.de>', &
        'Copyright © 2008-2020 CRTomo development team (see AUTHORS file)',&
        'Permission is hereby granted, free of charge, to any person obtaining a copy of',&
        'this software and associated documentation files (the “Software”), to deal in',&
        'the Software without restriction, including without limitation the rights to',&
        'use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies',&
        'of the Software, and to permit persons to whom the Software is furnished to do',&
        'so, subject to the following conditions:',&
        '',&
        'The above copyright notice and this permission notice shall be included in all',&
        'copies or substantial portions of the Software.',&
        '',&
        'THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR',&
        'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,',&
        'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE',&
        'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER',&
        'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,',&
        'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE',&
        'SOFTWARE.'

        PRINT*, ''
        PRINT*, ''

        ! TODO: export via input_fempy module
        kanal = 11
        pid = getpid()
        fetxt = 'crmod.pid'
        PRINT*,'CRMod Process_ID ::',pid
        OPEN (kanal,FILE=TRIM(fetxt),STATUS='replace',err=999)
        WRITE (kanal,*)pid
        CLOSE (kanal)

        maxthreads = OMP_GET_MAX_THREADS()
        WRITE(6,"(a, i3)") " OpenMP max threads: ", maxthreads

        CALL get_git_ver

        CALL tic(c1)

        ! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ! read in crmod.cfg start
        !!!$   'crmod.cfg' oeffnen
        fetxt = 'crmod.cfg'
        errnr = 1
        open(12,file=TRIM(fetxt),status='old',err=999)

        !!!$   Allgemeine Parameter setzen
        !!!$   "singularity removal" ?
        lsr = .false.

        !!!$   Art der Ruecktransformation
        !!!$   ak        swrtr = 1
        !!!$   ak        swrtr = 0

        !!!$   Sonstiges
        lkpot = .false.
        wkfak = .false.
        lana = .FALSE.
        lprior = .false. ! kann prior modell verrauschen
        ldc = .FALSE.
        lnsepri = .false.
        !!!$   ak        lkpot = .true.
        !!!$   ak        dkpot = '..\tmp\kpot.ctr'

        !!!$   Kontrollausgabe
5 write(*,*)
  write(*,'(a20)') ' Reading Input-Files'

        !!$   'crmod.cfg' einlesen
        fetxt = 'crmod.cfg'
        errnr = 3
        mswitch = 0
        read(12,*,end=1001,err=999)
        read(12,'(a80)',end=1001,err=999) delem
        read(12,'(a80)',end=1001,err=999) delectr
        read(12,'(a80)',end=1001,err=999) dsigma
        read(12,'(a80)',end=1001,err=999) dstrom
        read(12,*,end=1001,err=999) lpot
        read(12,'(a80)',end=1001,err=999) dpot
        read(12,*,end=1001,err=999) lvolt
        read(12,'(a80)',end=1001,err=999) dvolt
        read(12,*,end=1001,err=999) lsens
        read(12,'(a80)',end=1001,err=999) dsens
        read(12,*,end=1001,err=999) lagain
        read(12,*,end=1001,err=999) swrtr
        read(12,*,end=1001,err=999) lsink
        read(12,*,end=1001,err=999) nsink
        read(12,*,end=1001,err=999) lrandb2
        read(12,'(a80)',end=1001,err=999) drandb
        fetxt = 'reading mswitch'
        read(12,'(I4)',end=101,err=100) mswitch

        !GOTO 101

100 BACKSPACE (12)
    close(12)
    ! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ! read in crmod.cfg end

101 lana = BTEST(mswitch,0)
  wkfak = BTEST(mswitch,1)
  lsr = BTEST(mswitch,2)
  lverb = BTEST(mswitch,10)

  IF (lana) PRINT*,'ANALYTICAL SOLUTION'
  IF (wkfak) PRINT*,'WITH K-FAKTOR'
  IF (lsr) THEN
     PRINT*,'WITH SINGULARITY REMOVAL'
     lana = .FALSE. ! analytical for singularity
! is indeed controlled by lsr and not lana..
! lana is only true for analytical solution only
  END IF

  IF (lverb) PRINT*,'VERBOSE OUTPUT'

!!!$   Alles einlesen
  call relem(kanal,delem)
  if (errnr.ne.0) goto 999

  call relectr(kanal,delectr)
  if (errnr.ne.0) goto 999

  call rdatm(kanal,dstrom)
  if (errnr.ne.0) goto 999

  if (swrtr.eq.0) then
     lana = .FALSE.
     lsr = .FALSE.
     kwnanz = 1
     ALLOCATE (kwn(kwnanz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation kwn'
        errnr = 94
        GOTO 999
     END IF
     kwn(1) = 0d0
  else
     call rwaven()
     if (errnr.ne.0) goto 999
  end if
  print*,''
  NTHREADS = maxthreads
!!!$ now that we know nf and kwnanz, we can adjust the OMP environment..
  IF (maxthreads > 2) THEN ! single or double processor machines don't need scheduling..
     mythreads = MAX(kwnanz,2)
     mythreads = kwnanz
     PRINT*,'Rescheduling..'
     IF ( mythreads <= maxthreads ) THEN ! best case,
!!!$ the number of processors is greater or equal the assumed
!!!$ workload
        PRINT*,'perfect match'
     ELSE
!!!$ is smaller than the minimum workload.. now we have to devide a bit..
        PRINT*,'less nodes than wavenumbers'
        DO k = 1, INT(kwnanz/2)
           mythreads = INT(kwnanz / k) + 1
           IF (mythreads < maxthreads) EXIT
        END DO
     END IF
     NTHREADS = mythreads
  END IF
  CALL OMP_SET_NUM_THREADS ( NTHREADS )
  ! recheck ..
  k = OMP_GET_MAX_THREADS()
  WRITE(6,'(2(a, i3),a)') " OpenMP threads: ",k,'(',maxthreads,')'
  print*
!!!$   Startmodell belegen
  ALLOCATE (sigma(elanz),stat=errnr)
  IF (errnr /= 0) THEN
     fetxt = 'Error memory allocation fem sigma'
     errnr = 94
     goto 999
  END IF

!!$ manz = elanz
  manz =elanz

  call rsigma(kanal,dsigma)
  if (errnr.ne.0) goto 999

  if (lrandb2) then
     call rrandb(kanal,drandb)
     if (errnr.ne.0) goto 999
  end if

!!!$   Ggf. Referenzleitfaehigkeit bestimmen
  call refsig()

  IF (lsink) WRITE(6,'(/A,I5,2F12.3/)')&
       'Fictious sink @ node ',nsink,sx(snr(nsink)),sy(snr(nsink))
!!!$   Element- und Randelementbeitraege sowie Konfigurationsfaktoren zur
!!!$   Berechnung der gemischten Randbedingung bestimmen
  call precal()
  if (errnr.ne.0) goto 999

  if (.not.lbeta) lsr=.false.

    !!!$   'a', 'hpot' und 'kpot' zuweisen
    ALLOCATE(a((mb+1)*sanz),hpot(sanz,eanz),&
        kpot(sanz,eanz,kwnanz),b(sanz),stat=errnr)
  if (errnr.ne.0) then
     fetxt = 'allocation problem a and hpot'
     errnr = 97
     goto 999
  end if
  ALLOCATE(pot(sanz),pota(sanz),fak(sanz),stat=errnr)
  if (errnr.ne.0) then
     fetxt = 'allocation problem pot to fak'
     errnr = 97
     goto 999
  end if
  count = 0
  !$OMP PARALLEL DEFAULT (none) &
  !$OMP FIRSTPRIVATE (pota,fak,pot,a,b,fetxt) &
  !$OMP PRIVATE (j,l,k) &
  !$OMP SHARED (kwnanz,lverb,eanz,lsr,lbeta,lrandb,lrandb2,&
  !$OMP  sanz,kpot,swrtr,hpot,count,lana,kg,elbg,relanz,sigma)
  !$OMP DO
!!!$   POTENTIALWERTE BERECHNEN
  do k=1,kwnanz
!!!$   Kontrollausgabe
     !$OMP ATOMIC
     count = count + 1

     if (swrtr.eq.0) then
        write(*,'(a)')' Calculating Potentials'
     else
        WRITE (*,'(a,t45,I4,t100,a)',ADVANCE='no')&
             ACHAR(13)//' Calculating Potentials : Wavenumber ',count
     end if

     do l=1,eanz

!!!$   Ggf. Potentialwerte fuer homogenen Fall analytisch berechnen
        if (lsr.OR.lana) call potana(l,k,pota)
!!!$ is also needed by kompab for reference therfore it is placed here
!!!$

!!!$ for analytical only, the linear system is never solved
        if ((lbeta.or.l.eq.1.OR.lsr).AND..NOT.lana) then

!!!$   Kompilation des Gleichungssystems (fuer Einheitsstrom !)
           call kompab(l,k,a,b)
           !           if (errnr.ne.0) goto 999

!!!$   Ggf. Randbedingung beruecksichtigen
           if (lrandb) call randb(a,b)
           if (lrandb2) call randb2(a,b)

!!!$   Gleichungssystem skalieren
           call scalab(a,b,fak)
           !           if (errnr.ne.0) goto 999

!!!$   Cholesky-Zerlegung der Matrix
           call chol(a)
           !           if (errnr.ne.0) goto 999
        else if (.NOT. lana) THEN

!!!$   Stromvektor modifizieren
           call kompb(l,b,fak)
        end if

!!!$   Gleichungssystem loesen only for
!!!$ non analytical
        IF (.NOT. lana) call vre(a,b,pot)
!!!$   Potentialwerte zurueckskalieren und umspeichern sowie ggf.
!!!$   analytische Loesung addieren
        do j=1,sanz
           IF (lana) THEN

              kpot(j,l,k) = pota(j)
           ELSE
              kpot(j,l,k) = pot(j) * dcmplx(fak(j))
              if (lsr) kpot(j,l,k) = kpot(j,l,k) + pota(j)
           END IF
!!!$   ak (fuer Testzwecke)
!!!$   ak                    kpot(j,l,k) = pota(j)
           if (swrtr.eq.0) hpot(j,l) = kpot(j,l,k)
        end do
     end do
  end do
  !$OMP END PARALLEL
  print*,'done, now processing'
!!!$   Ggf. Ruecktransformation der Potentialwerte
  if (swrtr.eq.1) call rtrafo()

!!!$   Ggf. transformierte Potentialwerte ausgeben
  if (lkpot) then
     call wkpot(kanal,dkpot)
     if (errnr.ne.0) goto 999
  end if

!!!$   Ggf. Potentialwerte berechnen und ausgeben
  if (lpot) then
     call bpot(kanal,dpot)
     if (errnr.ne.0) goto 999
  end if

!!!$   Ggf. Spannungswerte berechnen und ausgeben
!!!$   (bzw. scheinbaren Widerstandswerte)
  if (lvolt) then
     IF (wkfak.AND.lbeta) then
        call bkfak()
        if (errnr.ne.0) goto 999
     else
!!!$   nur echte Spannungen ausgeben...
        kfak=1.0
     end if

     call bvolt()
     if (errnr.ne.0) goto 999

     call wdatm(kanal,dvolt)
     if (errnr.ne.0) goto 999
  end if

!!!$   'a' und 'hpot' freigeben
  DEALLOCATE(a,hpot,b)

!!!$   Ggf. Sensitivitaeten aller Messungen berechnen und ausgeben
  if (lsens) then

     if (manz.ne.elanz) then
        fetxt = 'manz /= elanz .. is not implemented yet'
        errnr = 50
        goto 999
     end if
     !     !$ get memory for mnr..
     ALLOCATE (mnr(elanz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation mnr failed'
        errnr = 94
        goto 999
     END IF
!!!$   Modelleinteilung gemaess Elementeinteilung belegen

     do j=1,elanz
        mnr(j) = j
     end do

!!!$   'sens' zuweisen
     ALLOCATE(sens(nanz,manz),stat=errnr)
     if (errnr.ne.0) then
        errnr = 97
        goto 999
     end if

     call bsens()

     call wsens(kanal,dsens)
     if (errnr.ne.0) goto 999

!!!$   'sens' freigeben
     DEALLOCATE(sens)
  end if

!!!$   'kpot' freigeben
  DEALLOCATE(kpot,pot,pota,fak)

    !!!$   Ggf. weiteren Datensatz modellieren
    if (lagain) goto 5

    !!!$   Kontrollausgabe
    fetxt = 'solution time'
    CALL TOC(c1,fetxt)

    write(*,*)
    write(*,'(a)',ADVANCE='no')' Modelling completed'
    write(*,*)


  IF (ALLOCATED (snr)) DEALLOCATE (snr,sx,sy)
  IF (ALLOCATED (typ)) DEALLOCATE (typ,nelanz,selanz)
  IF (ALLOCATED (nrel)) DEALLOCATE (nrel,rnr)

  IF (ALLOCATED (strnr)) DEALLOCATE (strnr,strom,volt,sigmaa,&
       kfak,vnr)
    IF (ALLOCATED (sigma)) DEALLOCATE (sigma)
    IF (ALLOCATED (enr)) DEALLOCATE (enr)
    IF (ALLOCATED (mnr)) DEALLOCATE (mnr)
    IF (ALLOCATED (kwn)) DEALLOCATE (kwn)
    IF (ALLOCATED (kwnwi)) DEALLOCATE (kwnwi)

    IF (ALLOCATED (rwddc)) DEALLOCATE (rwddc)
    IF (ALLOCATED (rwndc)) DEALLOCATE (rwndc)
    IF (ALLOCATED (rwd)) DEALLOCATE (rwd)
    IF (ALLOCATED (rwn)) DEALLOCATE (rwn)
    IF (ALLOCATED (rwdnr)) DEALLOCATE (rwdnr)

    ! not sure when we actually want to deallocate this
    ! if (allocated(out_ab)) deallocate(out_ab)

    return_value = 25
    return

    ! various error states
!!!$   (Fehler-) Meldung schreiben
999 open(9,file='error.dat',status='replace')
    errflag = 2
    CALL get_error(ftext,errnr,errflag,fetxt)
    write(9,'(a80,i3,i1)') fetxt,errnr,errflag
    write(9,*) ftext
    close(9)
    return_value = -1
    return

1001 open(9,file='error.dat',status='replace')
        errnr   = 2
        errflag = 2
        CALL get_error(ftext,errnr,errflag,fetxt)
        write(9,'(a80,i3,i1)') fetxt,errnr,errflag
        write(9,*)ftext
        close(9)
        return_value = -2
        return

    end subroutine forward_calculation

end module fem_pyw
