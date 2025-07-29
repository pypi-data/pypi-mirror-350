!> \file rtrafo.f90
!> \brief inverse Fourier transform of the modeled potentials
!> \details Kemna (2000): For the purpose of this thesis (this program) all electrodes are assumed to lie in a plane perpendicular to the strike direction \f$ y \f$. Therefore, the complex potential needs to be calculated at \f$ y=0\f$ only, and the inverse Fourier transform \f[ \phi(x,y,z) = \frac{1}{\pi} \int_0^\infty \tilde \phi (x,k,z) \cos (ky) dk \f] simplifies to a pure integration of the transformed potential values: \f[ \phi_i = \frac{1}{\pi} \int_0^\infty \tilde \phi_i(k)dk. \f]
!> The numerical evaluation of the integral in the above equation is based on a combination of Gaussian quadrature and Laguerre integration as suggested by LaBrecque et al. (1996a). The result is an expression
!> \f[ \phi_i = \sum_n w_n \tilde \phi_i (k_n) \f]
!> with different abscissa \f$ k_n \f$, for which the Helmholtz equation has to be solved, and some real weights \f$w_n\f$. Details on the procedure can be found in Kemma (2000) in Appendix C.

!> Finally, the complex voltage \f$ V_i \f$ of any arbitrary electrode configuration is obtained by appropriate superposition of calculated potential values, i.e., \f$ V_i = \sum \phi_{i_m} \f$, or with the above equation,
!> \f[ V_i = \sum_m \sum_n w_n \tilde \phi_{i_m} (k_n) \f]
!> It is obvious that the order of inverse Fourier transform and superposition can be interchanged because of the linearity of both operations.
!> @author Andreas Kemna
!> @date 10/11/1993

subroutine rtrafo()

!     Unterprogramm zur Ruecktransformation.

!     Andreas Kemna                                            20-Dec-1993
!     Letzte Aenderung   13-Nov-1997

!.....................................................................

  USE alloci
  USE femmod
  USE electrmod
  USE elemmod
  USE wavenmod

  IMPLICIT none

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Pi
  REAL (KIND(0D0))  ::   pi

!     Hilfsvariablen
  COMPLEX (KIND(0D0))  ::    summe
  REAL (KIND(0D0))    ::     summdc

!     Indexvariablen
  INTEGER (KIND=4)    ::j,k,l

!.....................................................................

  pi = dacos(-1d0)

  if (ldc) then

     !$OMP PARALLEL DEFAULT (none) &
     !$OMP PRIVATE (summdc,l,j,k) &
     !$OMP SHARED (eanz,sanz,kwnanz,kwnwi,kpotdc,hpotdc,pi)
     !$OMP DO COLLAPSE (2) PRIVATE (l,j,k,summdc)
     do l=1,eanz
        do j=1,sanz
           summdc = 0d0

           do k=1,kwnanz
              summdc = summdc + kpotdc(j,l,k)*kwnwi(k)
           end do

           hpotdc(j,l) = summdc / pi
!!$           IF (summdc < EPSILON(0D0)) THEN
!!$              print*,'rtrafo::',l,j
!!$              STOP
!!$           END IF
        end do
     end do
     !$OMP END PARALLEL

  else

     !$OMP PARALLEL DEFAULT (none) &
     !$OMP PRIVATE(summe,l,j,k) &
     !$OMP SHARED (eanz,sanz,kwnanz,kwnwi,kpot,hpot,pi)
     !$OMP DO COLLAPSE (2) PRIVATE (l,j,k,summe)
     do l=1,eanz
        do j=1,sanz
           summe = dcmplx(0d0)

           do k=1,kwnanz
              summe = summe + kpot(j,l,k)*dcmplx(kwnwi(k))
           end do

           hpot(j,l) = summe / dcmplx(pi)
        end do
     end do
     !$OMP END PARALLEL

  end if

end subroutine rtrafo
