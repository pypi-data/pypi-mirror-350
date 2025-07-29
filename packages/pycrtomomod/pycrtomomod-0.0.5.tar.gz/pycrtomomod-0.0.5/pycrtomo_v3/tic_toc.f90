!!$ $Id: tic_toc.f90 1.4 2008/07/29 14:05:36 Roland Martin Exp $
MODULE tic_toc

    IMPLICIT none
    PUBLIC :: tic
    PUBLIC :: toc

    INTEGER(KIND = 4),public         :: fix_f2py
    INTEGER(KIND = 4),PRIVATE         :: c2,i,l
    INTEGER(KIND = 4),PRIVATE         :: se,mi,st,ta,ms

CONTAINS

    SUBROUTINE tic(c1)
        INTEGER(KIND = 4), INTENT(OUT) :: c1 ! first call -> tic
        CALL SYSTEM_CLOCK (c1,i)
    END SUBROUTINE tic


    SUBROUTINE toc(c1, csz)
        INTEGER(KIND = 4), INTENT(IN) :: c1 ! first call -> tic
        CHARACTER (*),INTENT(INOUT)   :: csz
        !f2py intent(in, out) csz

110 FORMAT(a,I3,'d/',1X,I2,'h/',1X,I2,'m/',1X,I2,'s/',1X,I3,'ms')

        CALL SYSTEM_CLOCK (c2,i)

        ms = c2-c1    ! Gesamt Millisekunden
        ms = MODULO(ms,1000)

        l = (c2-c1)/i ! Gesamt Sekunden

        ta = INT(l/24/3600) ! Tage
        l = l - ta*3600*24
        st = INT(l/3600) ! Stunden
        l = l - st*3600
        mi = INT(l/60) ! Minuten
        se = l - mi*60
        PRINT*,TRIM(csz)

        WRITE (csz,110)TRIM(csz),ta,st,mi,se,ms

        PRINT*,TRIM(csz)

    END SUBROUTINE toc
END MODULE tic_toc
