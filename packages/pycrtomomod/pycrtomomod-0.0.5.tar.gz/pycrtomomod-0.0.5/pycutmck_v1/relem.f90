module relem_mod
      contains
      subroutine relem(kanal,io,datei)

!     Unterprogramm zum Einlesen der FEM-Parameter aus 'datei'.

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   24-Oct-1996

! ....................................................................

      USE elemmod
      USE errmod

      IMPLICIT none

      ! INCLUDE 'err.fin'
! ....................................................................

!     EIN-/AUSGABEPARAMETER:

!     Kanalnummer
      integer :: kanal,io

!     Datei
      character(80) :: datei

! ....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariablen
      integer :: i,j,k

!     Hilfsvariable
      integer :: idum

! ....................................................................

!     'datei' oeffnen
      fetxt = datei

      errnr = 1
      open(kanal,file=fetxt,status='old',err=999)
      OPEN(io,file='ctmck.info',STATUS='replace')
      errnr = 3

!     Anzahl der Knoten (bzw. Knotenvariablen), Anzahl der Elementtypen
!     sowie Bandbreite der Gesamtsteifigkeitsmatrix einlesen
      read(kanal,*,end=1001,err=1000) sanz,typanz,mb
!     !$ now get some memory for the fields..
!     !$ first the sanz fields
      ALLOCATE (sx(sanz),sy(sanz),snr(sanz),stat=errnr)
      IF (errnr /= 0) THEN
         fetxt = 'Error memory allocation sx failed'
         errnr = 94
         GOTO 999
      END IF

      ALLOCATE (typ(typanz),nelanz(typanz),selanz(typanz),stat=errnr)
      IF (errnr /= 0) THEN
         fetxt = 'Error memory allocation selanz failed'
         errnr = 94
         GOTO 999
      END IF

!     Elementtypen, Anzahl der Elemente eines bestimmten Typs sowie
!     Anzahl der Knoten in einem Elementtyp einlesen
      read(kanal,*,end=1001,err=1000) (typ(i),nelanz(i),selanz(i),i=1,typanz)

!     !$ set number of node points for regular elements
      smaxs = MAXVAL(selanz)

!     Anzahl der Elemente (ohne Randelemente) und Anzahl der Randelemente
!     bestimmen
      relanz = 0
      elanz  = 0
      do i=1,typanz
         if (typ(i).gt.10) then
            relanz = relanz + nelanz(i)
         else
            elanz  = elanz  + nelanz(i)
         end if
      end do
!     !$ get memory for the element integer field
      ALLOCATE (nrel(elanz+relanz,smaxs),rnr(relanz),stat=errnr)
      IF (errnr /= 0) THEN
         fetxt = 'Error memory allocation nrel failed'
         errnr = 94
         GOTO 999
      END IF

      PRINT*,'check dis out ',4+sanz+elanz+relanz*2

!     Zeiger auf Koordinaten, x-Koordinaten sowie y-Koordinaten der Knoten
!     einlesen
      print*,'knoten::',sanz
      read(kanal,*,end=1001,err=1000) (snr(i),sx(i),sy(i),i=1,sanz)
      i = 0;j = 0
      DO k=1,sanz
         IF (sx(snr(k))==sx(snr(1))) j = j+1 !counts vertical grid nodes
         IF (sy(snr(k))==sy(snr(1))) i = i+1 !counts horizontal grid nodes
      END DO
      IF ((i-1) == 0 .OR. (j-1) == 0) THEN
         PRINT*,ACHAR(9)//'## GRID not regular ##'
         WRITE (io,'(a)')'## Grid not regular'
      ELSE
         WRITE (*,*)'Regular grid info NX=',i-1, '  NY=',j-1,'  NXY=',(i-1)*(j-1)
         WRITE (*,*)'x0=',MINVAL(sx(1:sanz)),'y0=', MINVAL(ABS(sy(1:sanz)))
         WRITE (*,'(2(a,2x,F10.4))')'Linear dx',sx((2))-sx((1)), 'dy',sy((i+1))-sy((1))
         WRITE (io,'(a)')'## Regular grid'
         WRITE (io,'(A,2X,I4)')'NX',i-1
         WRITE (io,'(a,2x,F10.3)')'X0',MINVAL(sx(1:sanz))
         WRITE (io,'(a,2x,F10.3)')'DX',sx((2))-sx((1))
         WRITE (io,'(A,2X,I4)')'NY',j-1
         WRITE (io,'(a,2x,F10.3)')'Y0',MINVAL(ABS(sy(1:sanz)))
         WRITE (io,'(a,2x,F10.3)')'DY',sy((i+1))-sy((1))
         WRITE (io,'(A,2X,I4)')'NXY',(i-1)*(j-1)
      END IF
!     Knotennummern der Elemente einlesen
      print*,'post knoten position',4+sanz
      idum = 0
      print*,'elemente::',elanz,relanz
      do i=1,typanz
         do j=1,nelanz(i)
            read(kanal,*,end=1001,err=1000) (nrel(idum+j,k),k=1,selanz(i))
         end do
         idum = idum + nelanz(i)
      end do
      print*,'post elemente position',4+sanz+elanz+relanz
      print*,'randpunkte::',relanz
!     Zeiger auf Werte der Randelemente einlesen
      read(kanal,*,end=1001,err=1000) (rnr(i),i=1,relanz)
      print*,'post randpunkte position',4+sanz+elanz+relanz*2
!     'datei' schliessen
      close(kanal)
      CLOSE(io)
      errnr = 0
      return

! ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

 999  return

 1000 close(kanal)
      return

 1001 close(kanal)
      errnr = 2
      return

      end subroutine relem
end module relem_mod
