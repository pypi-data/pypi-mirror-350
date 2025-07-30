!> \file refsig.f90
!> \brief compute reference conductivity for mixed boundaries
!> \details Compute the area-weighted conductivity average of the whole model. It is used in <I>beta</I> to determine the mixed boundary conditions. <I>Taking the overall model average is one possible option for the mixed boundary. However, it is also possible to use the adjacent model cell conductivity.</I> The area is computed with Gauss' area equation.
!> @author Andreas Kemna 
!> @date 02/29/1996

subroutine refsig()

!     Unterprogramm zum Bestimmen der Referenzleitfaehigkeit.

!     Andreas Kemna                                            29-Feb-1996
!     Letzte Aenderung   08-Nov-1997

!.....................................................................

  USE sigmamod
  USE elemmod,only:sx,sy,snr,typanz,nelanz,typ,nrel

  IMPLICIT none

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Indexvariablen
  INTEGER (KIND = 4 ) ::     i,j

!     Hilfsvariablen
  INTEGER (KIND = 4) ::      iel
  REAL (KIND(0D0))   ::     xk,yk,ax,ay,bx,by,cx,cy,dum,area

!.....................................................................
  dum    = 0D0
  iel    = 0
  area   = 0d0
  sigma0 = dcmplx(0d0)
  do i=1,typanz
     do j=1,nelanz(i)
        iel = iel + 1

        if (typ(i).gt.10) CYCLE

        xk = sx(snr(nrel(iel,1)))
        yk = sy(snr(nrel(iel,1)))
        ax = sx(snr(nrel(iel,2)))
        ay = sy(snr(nrel(iel,2)))
        bx = sx(snr(nrel(iel,3)))
        by = sy(snr(nrel(iel,3)))
        ax = ax - xk
        ay = ay - yk
        bx = bx - xk
        by = by - yk

        if (typ(i).eq.3) then
           dum = dabs(ax*by-ay*bx) / 2d0
        else if (typ(i).eq.5.or.typ(i).eq.8) then
           cx  = sx(snr(nrel(iel,4)))
           cy  = sy(snr(nrel(iel,4)))
           cx  = cx - xk
           cy  = cy - yk
           dum = (dabs(ax*by-ay*bx) + dabs(bx*cy-by*cx)) / 2d0
        end if

        sigma0 = sigma0 + dcmplx(dum)*cdlog(sigma(iel))
        area   = area   + dum

     end do
  end do

  sigma0 = cdexp(sigma0/dcmplx(area))

  return
end subroutine refsig
