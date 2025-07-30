module welemmod
    contains
      subroutine welem(kanal,datei)

!     Unterprogramm zum Schreiben der FEM-Parameter in 'datei'.

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   21-Jan-2003

! ....................................................................

      USE elemmod
      USE errmod

      IMPLICIT none
! ....................................................................

!     EIN-/AUSGABEPARAMETER:

!     Kanalnummer
      integer :: kanal

!     Datei
      character(80) :: datei

! ....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariablen
      integer        ::     i,j,k

!     Hilfsvariable
      integer         ::    idum

! ....................................................................

!     'datei' oeffnen
      fetxt = datei

      errnr = 1
      open(kanal,file=fetxt,status='replace',err=999)

      errnr = 4

!     Anzahl der Knoten (bzw. Knotenvariablen), Anzahl der Elementtypen
!     sowie Bandbreite der Gesamtsteifigkeitsmatrix schreiben
      write(kanal,*,err=1000) sanz,typanz,mb

!     Elementtypen, Anzahl der Elemente eines bestimmten Typs sowie
!     Anzahl der Knoten in einem Elementtyp schreiben
      do i=1,typanz
         write(kanal,*,err=1000) typ(i),nelanz(i),selanz(i)
      end do

!     Zeiger auf Koordinaten, x-Koordinaten sowie y-Koordinaten der Knoten
!     schreiben
      do i=1,sanz
         write(kanal,'(I8,2F12.3)',err=1000) snr(i),real(sx(i)),real(sy(i))
      end do

!     Knotennummern der Elemente schreiben
      idum = 0
      do i=1,typanz
         do j=1,nelanz(i)
            write(kanal,*,err=1000) (nrel(idum+j,k),k=1,selanz(i))
         end do
         idum = idum + nelanz(i)
      end do

!     Zeiger auf Werte der Randelemente schreiben
      do i=1,relanz
         write(kanal,*,err=1000) rnr(i)
      end do

!     'datei' schliessen
      close(kanal)

      fetxt='ctm_triangles.txt'
      OPEN (kanal,FILE=fetxt,STATUS='replace',ACCESS='sequential')
      do j=1,nelanz(1)
         write(kanal,*,err=1000) (nrel(j,k),k=1,selanz(1))
      end do
      CLOSE (kanal)

      errnr = 0
      return

! ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

 999  return

 1000 close(kanal)
      return

      end subroutine welem
end module welemmod
