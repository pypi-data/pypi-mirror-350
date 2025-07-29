module cmk

    contains
        subroutine run_cutmck(return_value)

        !     Programm zur optimalen Numerierung der Knotenpukte nach dem
        !     Algorithmus von Cuthill-McKee. Ist die Anzahl der Startpunkte 'spanz'
        !     kleiner Null, werden die Startpunkte mit minimalem Grad automatisch
        !     bestimmt. Andernfalls werden die vorgegebenen Nummern der Startpunkte
        !     aus 'dstart' gelesen.

        !     Andreas Kemna                                            11-Oct-1993
        !     Letzte Aenderung, RM   11-Sep-2009

        !     ( Vgl. entspr. Hauptprogramm in Schwarz (1991) )

        !.....................................................................

        USE errmod, only: fetxt
        USE elemmod, only: sanz, snr, nelanz, selanz, nrel, elanz, typanz, mb
        USE electrmod
        USE relem_mod
        USE relectrmod
        USE welectrmod
        USE welemmod
        USE get_error_modx

        IMPLICIT none
        ! INCLUDE 'err.fin'
        ! COMMON
        INTEGER(KIND = 4), INTENT(OUT) :: return_value

        ! Fehlernummer
        integer :: errnr

        ! Fehlerart
        ! 0 : GKS - nicht aktiv, Programm nicht verlassen
        ! 1 : GKS - nicht aktiv, Programm verlassen
        ! 2 : GKS - aktiv      , Programm nicht verlassen
        ! 3 : GKS - aktiv      , Programm verlassen und GKS schlieáen
        integer :: errflag

        ! Fehlertext
        ! character(80) :: fetxt

!.....................................................................

!     Schalter ob Kontrolldateien ('*.ctr') ausgegeben werden sollen
      logical :: kont

!     Dateinamen
      character(80) :: delem,delectr
      CHARACTER(256) :: ftext
!     Maximaler Grad der Knotenpunkte
      INTEGER,PARAMETER :: grmax=500
!     Maximale Anzahl vorgegebener Startpunkte im Cuthill-McKee-Algorithmus
      INTEGER,PARAMETER :: spmax=100
!     Maximale Anzahl der Stufen im Cuthill-McKee-Algorithmus
      INTEGER,PARAMETER :: stmax=100

!     Permutationsvektor der Umnumerierung
      INTEGER,DIMENSION(:),ALLOCATABLE   :: perm

!     Knotennummern der Startpunkte
      INTEGER,DIMENSION(:),ALLOCATABLE   :: start

!     Hilfsvariablen
      INTEGER,DIMENSION(:,:),ALLOCATABLE :: graph
      INTEGER,DIMENSION(:),ALLOCATABLE   :: grad,neu,neuin,level

      integer ::  gradzp,fcm,kbdm,nstart,spanz,i,j,k,l,m,idum,is,nzp,nnp,maxgd,mingd, minbd,mmin,mingr,levs,leve,nlev

      LOGICAL,DIMENSION(:),ALLOCATABLE   :: num
      logical :: exi1,exi2,exi3
      integer :: c1,c2,se,mi,st,ta,fp,fp2
!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
4    FORMAT(/'  minimum grade =',I6/'  maximum grade =',I6, '  minimum bandwidth =',I6)
! 6    FORMAT(/'Ergebnisse der Nuenummerierungen '/,'Startpunkt',3x, 'Bandbreite',3x,'Profil (normal)',3x,'Profil (reverse)')
8    FORMAT(3(I8,4X),I8)
9    FORMAT(//'  minimum bandwidth =',i5,'  for init.node', i5//'  vector of permutation ='/)
11   FORMAT((3x,10i5))
!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
      CALL SYSTEM_CLOCK (c1,i)
      kont   = .FALSE.

      fp = 11
      fp2 = 12
!     Fehlerdatei oeffnen
      open(10,file='error.dat',status='unknown')

!     Fehlerflag setzen
      errflag = 2

!     'CutMck.cfg' einlesen
      fetxt = 'cutmck.cfg'
      INQUIRE (FILE=fetxt,EXIST=exi1)
      IF (exi1) THEN
         errnr = 1
         open(fp,file=fetxt,status='old',err=1000)

         errnr = 3
         read(fp,'(a,/,a)',end=1001,err=1000) delem,delectr
         close(fp)
      ELSE                      !check for defaults
         delem='elem.dat'
         delectr='elec.dat'
         INQUIRE (FILE=delem,EXIST=exi2)
         INQUIRE (FILE=delectr,EXIST=exi3)
         IF (exi2.AND.exi3) THEN
            PRINT*,'trying default::',TRIM(delem),'  ',TRIM(delectr)
         ELSE
            IF (.NOT.exi2) THEN
               fetxt=TRIM(delem)
               PRINT*,'no default grid file::',TRIM(delem)
            END IF
            IF (.NOT.exi3)THEN
               fetxt=TRIM(fetxt)//' '//TRIM(delectr)
               PRINT*,'no default electrode file::',TRIM(delectr)
            END IF
            errnr = 3
            GOTO 1000
         END IF
      END IF
      print*,'read in elements...'
!     'delem' einlesen
      call relem(fp,fp2,delem)
      if (errnr.ne.0) goto 1000
      print*,'read in electrodes'
!     'delectr' einlesen
      call relectr(fp,delectr)
      if (errnr.ne.0) goto 1000
      print*,'ok'

      ALLOCATE (graph(grmax,sanz),perm(sanz),grad(sanz),neu(sanz), neuin(sanz),level(sanz),start(sanz),num(sanz),stat=errnr)

      IF (errnr /= 0) THEN
         PRINT*,'error allocating fields',errnr
         RETURN
      END IF

!     Aufbau des Graphen aufgrund der Knotennummern der Elemente
      grad=0;graph=0

      idum = 0
      grad=0.;graph=0.
      DO l = 1 , typanz

         DO m = 1 , nelanz(l)

            DO i = 1 , selanz(l)-1

               nzp = nrel(idum+m,i)

               DO j=i+1,selanz(l)

                  nnp = nrel(idum+m,j)

                  DO k=1,grmax

                     IF (graph(k,nzp) == nnp) GOTO 10
                     IF (graph(k,nzp) > 0) CYCLE

                     graph(k,nzp)=nnp
                     grad(nzp)=grad(nzp)+1

                     EXIT
                  END DO

                  grad(nnp) = grad(nnp)+1
                  IF (grad(nnp) <= grmax) graph(grad(nnp),nnp)=nzp

10               CONTINUE

               END DO

            END DO

         END DO

         idum = idum + nelanz(l)

      END DO

      PRINT*,'graph erstellt'

      mingd = MINVAL(grad(1:sanz))
      maxgd = MAXVAL(grad(1:sanz))

      IF (mingd==0) THEN
         PRINT*,'existance of zero nodes.. aborting'
         return_value = -1
         return
      ENDIF

      minbd = (maxgd+1)/2
!     Ggf. Kontrolldatei oeffnen

      IF (kont) THEN
         fetxt = 'cutmck.ctr'
         OPEN(fp,file=TRIM(fetxt),status='unknown')
         WRITE(fp,4) mingd,maxgd,minbd
      END IF

!     rm
      spanz = INT(elanz / 10)
      spanz = MAX(spanz,1000)
      k = 0
      spanz = MIN(spanz,spmax)
      WRITE(*,'(a,I8)',ADVANCE='no')'mingd::',mingd
110  do 120 i=1,sanz
         if (grad(i).eq.mingd) then
            k = k+1
            start(k) = i
            if (k.ge.spanz) goto 130
         end if
120  continue
      IF (mingd>elanz/10) GOTO 130
      mingd = mingd+1
      WRITE(*,'(a,I8)',ADVANCE='no')ACHAR(13)//'mingd::',mingd
      goto 110

130  continue

      spanz=k-1
      print*,'errechnete startpunkte ',spanz
      if (kont) then

         errnr = 4
         write(11,7,err=1000)
7       format(//'  init.node   bandwidth'/)
      end if

!     Neunumerierung der Knotenpunkte fuer alle Startpunkte
      mmin = sanz
      kbdm = 0

      do is=1,spanz
         nstart        = start(is)

         WRITE (*,'(2(a,1X,I6,2X))',ADVANCE='no') ACHAR(13)//'startknoten',nstart,'bandbreite',mmin

         neu(1)        = nstart
         neuin(nstart) = 1

         do i=1,sanz
            num(i) = .false.
         end do

         num(nstart) = .true.
         level(1)    = 1
         levs        = 1
         leve        = 1
         nlev        = 1
         l           = 1

150     do 180 j=levs,leve
            nzp    = neu(j)
            gradzp = grad(nzp)
160        mingr  = grmax
            k      = 0

            do 170 i=1,gradzp
               nnp = graph(i,nzp)

               if (num(nnp).or.grad(nnp).gt.mingr) goto 170

               mingr = grad(nnp)
               k     = nnp
170        continue

            if (k.eq.0) goto 180

            l        = l+1
            neu(l)   = k
            neuin(k) = l
            num(k)   = .true.

            goto 160
180     continue
         levs        = levs+level(nlev)
         nlev        = nlev+1
         level(nlev) = l-levs+1
         leve        = leve+level(nlev)


         if (leve.lt.sanz) goto 150

!     Bandbreite 'mb'
         mb = 0

         do i=1,sanz
            nzp    = neuin(i)
            fcm    = nzp
            gradzp = grad(i)

            do j=1,gradzp
               k   = neuin(graph(j,i))
               mb  = max0(mb,iabs(k-nzp))
               fcm = min0(fcm,k)
            end do
         end do

         if (kont) then
            write(fp,8,err=1000) nstart,mb
         end if

         if (mb.lt.mmin) then

            mmin = mb
            kbdm = is
            do i=1,sanz
               perm(i) = neuin(i)
            end do
         end if

      end do                    ! is

      if (kont) then
         write(fp,9,err=1000) mmin,start(kbdm)
         write(fp,11,err=1000) (perm(i),i=1,sanz)
         close(fp)
      end if

!     Minimale Bandbreite setzen
      mb = mmin

!     UMNUMERIERUNG

!     Knotennummern der Elemente umspeichern
      idum = 0

      do i=1,typanz
         do j=1,nelanz(i)
            do k=1,selanz(i)
               nrel(idum+j,k) = perm(nrel(idum+j,k))
            end do
         end do
         idum = idum+nelanz(i)
      end do

!     Zeiger auf Koordinaten der Knoten umspeichern ('grad' als Hilfsfeld)
      do i=1,sanz
         grad(i) = snr(i)
      end do

      do i=1,sanz
         snr(perm(i)) = grad(i)
      end do

!     Knotennummern der Elektroden umspeichern
      do i=1,eanz
         enr(i) = perm(enr(i))
      end do

!     Startwerte umspeichern (zur Kontrolle)
      do i=1,spanz
         start(i) = perm(start(i))
      end do
      PRINT*,' writing out new values '
!     Elementeinteilung und Elektrodenverteilung schreiben
!     delem=TRIM(ADJUSTL(delem))//'_ctm'
      fetxt='cp -f '//TRIM(delem)//' '//TRIM(delem)//'.orig'
      CALL SYSTEM (fetxt)
      call welem(11,delem)
      if (errnr.ne.0) goto 1000

      fetxt='cp -f '//TRIM(delectr)//' '//TRIM(delectr)//'.orig'
      CALL SYSTEM (fetxt)
!     delectr=TRIM(ADJUSTL(delectr))//'_ctm'
      call welectr(11,delectr)
      if (errnr.ne.0) goto 1000

!     Fehlerdatei loeschen
      close(10,status='delete')

      CALL SYSTEM_CLOCK (c2,i)
      k=(c2-c1)/i               ! Sekunden
      mi=INT(k/60)              ! Minuten
      st=INT(k/60/60)           ! Stunden
      ta=INT(k/60/60/24)        ! Tage
      se=k-mi*60-st*60*60-ta*60*60*24 ! Sekunden
3    FORMAT(I2,'d/',1X,I2,'h/',1X,I2,'m/',1X,I2,'s')
      WRITE (*,3)ta,st,mi,se

      return_value = 0
      return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 CALL get_error(ftext,errnr,errflag,fetxt)
      write(10,'(a80,i2,i1)') fetxt,errnr,errflag
      write(10,*)ftext
      close(10)
      return_value = -1
      return

1001 errnr = 2
      CALL get_error(ftext,errnr,errflag,fetxt)
      write(10,'(a80,i2,i1)') fetxt,errnr,errflag
      write(10,*)ftext
      close(10)
      return_value = -1
      return

      end subroutine run_cutmck
 end module cmk
