SUBROUTINE bbsens(kanal,datei)
    !!!$     Unterprogramm zur Berechnung der Summe der Sensitivitaeten
    !!!$     aller Messungen (normiert)
    !!!$     Berechnet nun coverage als Summe der Absolutbetraege..
    !!!$     ('kpot' als Hilfsfeld benutzt).
    !!!$     Andreas Kemna 02-Mar-1995
    !!!$     Letzte Aenderung 31-Mar-2010
    !!!$....................................................................
    USE alloci , ONLY : sens,sensdc
    USE datmod , ONLY : nanz,wmatd_cri,wmatdr
    USE invmod , ONLY : lfpi,wmatd,wdfak
    USE modelmod , ONLY : manz
    USE elemmod , ONLY: espx,espy
    USE errmod , ONLY : errnr,fetxt
    USE femmod , ONLY : ldc
    USE konvmod, ONLY : lelerr
    USE ompmod
    IMPLICIT NONE

    ! input/output

    ! io-channel (Kanalnummer)
    INTEGER (KIND = 4)  ::     kanal

    !!!$     Datei
    CHARACTER (80)      ::  datei

    !!!$.....................................................................
    !!!$     PROGRAMMINTERNE PARAMETER:

    !!!$     Hilfsvariablen
    REAL (KIND(0D0)),ALLOCATABLE,DIMENSION(:) :: csens,csens_fpi
    REAL (KIND(0D0))                          :: csensmax
    REAL (KIND(0D0))                          :: dum,dum_fpi
    !!!$     Indexvariablen
    INTEGER (KIND = 4)  ::     i,j
    !!!$.....................................................................
    !!!$     'datei' oeffnen
    ALLOCATE (csens(manz),STAT=errnr)
    IF (errnr /= 0) RETURN
    !!!$     Werte berechnen
    csens = 0D0
    ALLOCATE (csens_fpi(manz),STAT=errnr)
    csens_fpi = 0D0

    DO j=1,manz
        DO i=1,nanz
            dum = SQRT(wmatd(i)) * DBLE(wdfak(i))
            !!!$ CR case:
            !!!$  wmatd = wmatdr without error ellipses
            !!!$  wmatd = wmatd_cri with error ellipses
            !!!$ DC case:
            !!!$  wmatd = wmatdr
            !!!$ FPI case:
            !!!$  wmatd = wmatdp

            ! RM: we modify this to make sure, that even for FPI (case lfpi=.T.)
            ! we can calculate a complex coverage as well as treating the error
            ! right
            IF (lfpi) THEN
                dum_fpi = SQRT(wmatd(i)) * DBLE(wdfak(i))
                IF (lelerr) THEN
                    dum = SQRT(wmatd_cri(i)) * DBLE(wdfak(i))
                ELSE
                    dum = SQRT(wmatdr(i)) * DBLE(wdfak(i))
                END IF
                !!!$ this sensitivity is the one which is used through the FPI
                csens_fpi(j) = csens_fpi(j) + ABS(DBLE(sens(i,j))) * dum_fpi

                !!!$ this one is the COMPLEX sensitivity of the final estimate
                csens(j) = csens(j) + ABS(sens(i,j)) * dum
            ELSE IF (ldc) THEN
                csens(j) = csens(j) + ABS(sensdc(i,j)) * dum
            ELSE
                ! complex inversion
                csens(j) = csens(j) + ABS(sens(i,j)) * dum
            ENDIF
         END DO
    END DO

    !!!$ for normalization
    csensmax = MAXVAL(csens)

    !!!$     'datei' oeffnen
    fetxt = datei
    errnr = 1
    OPEN(kanal,file=TRIM(fetxt),status='replace',err=999)
    errnr = 4
    ! write number of values and maximum sensitivity
    WRITE(kanal,*,err=1000) manz, csensmax

    !!!$     Koordinaten und Sensitivitaetsbetraege schreiben
    !!!$     (logarithmierter (Basis 10) normierter Betrag)
    DO i=1,manz
        WRITE (kanal,*,err=1000)espx(i),espy(i),LOG10(csens(i)/csensmax)
    END DO

    CLOSE (kanal)

    DEALLOCATE (csens)

    IF (lfpi) THEN
        !!!$ for normalization
        csensmax = MAXVAL(csens_fpi)

        !!!$     'datei' oeffnen
        fetxt = datei
        errnr = 1
        OPEN(kanal,file=TRIM(datei)//'_fpi',status='replace',err=999)
        errnr = 4
        WRITE(kanal,*,err=1000) manz

        !!!$     Koordinaten und Sensitivitaetsbetraege schreiben
        !!!$     (logarithmierter (Basis 10) normierter Betrag)
        DO i=1,manz
            WRITE (kanal,*,err=1000)espx(i),espy(i),LOG10(csens_fpi(i)/csensmax)
        END DO

        !!!$     Maximale Sensitivitaet schreiben
        WRITE(kanal,*,err=1000)'Max:',csensmax
        !!!$     'datei' schliessen
        CLOSE(kanal)
    END IF
    DEALLOCATE (csens_fpi)

    errnr = 0
    RETURN

!!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!!!$     Fehlermeldungen

999 RETURN

1000 CLOSE(kanal)
  RETURN

END SUBROUTINE bbsens
