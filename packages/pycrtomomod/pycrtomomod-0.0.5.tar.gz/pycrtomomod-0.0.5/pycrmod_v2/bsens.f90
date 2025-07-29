!> \file bsens.f90
!> \brief forward modelling sensitivity calculation
!> \details Kemna (2000): An elegant way of deriving an appropriate sensitivity expression via reciprocity starts directly from the linear FE equations (e.g., Rodi, 1976; Oristaglio and Worthington, 1980). Substituting 
!> \f[ S = \sum_{j=1}^{N_e}{\sigma_j \left( S_{1j}+ k^2 S{2j} \right)} + \sum_{j=1}^{N_b}{\beta_j S_{3j}} \f]
!> and 
!> \f[ b = - \left[ \sum_{j=1}^{N_e}{\Delta \sigma_j \left( S_{1j} + k^2 S_{2j} \right)} + \sum_{j=1}^{N_e}{\Delta \beta_j S_{3j}} \right] \tilde \phi_p \f]
!> into the matrix equation
!> \f[ S\tilde \phi_s = b \f]
!>  and subsequently taking the derivative with respect to the complex conductivity of the j-th domain element, it is easily shown that
!> \f[ S \frac{\partial \tilde \phi}{\partial \sigma_j} = -\left( S_{1j} + k^2 S_{2j} \right) \tilde\phi \f]
!> Note that although the boundary-element parameters \f$ \beta_j \f$ in the first expression may be determined with the help of the conductivity values of the respective adjacent cells, virtually, they must not be considered as domain-element parameters. Therefore, the derivative within the right-hand side of the above equation includes no contribution on this account.
!> 
!> A further remark on the general complex differentiability of the discrete complex potential values in \f$ \tilde \phi \f$ may be added. Obviously, from the first equation it is  \f$ \partial S / \partial \sigma_j = \i \partial S / \partial \Re (\sigma_j) \f$. Hence, from the above equation, it is readily seen that each function \f$\tilde\phi_i (\sigma_j) \f$ fulfills the Cauchy-Riemann conditions
!> \f[ \frac{\partial \Re \tilde\phi_i}{\partial\Re \sigma_j} = \frac{\partial \Im \tilde\phi_i}{\partial\Im \sigma_j}, \ \frac{\partial \Im \tilde\phi_i}{\partial\Re \sigma_j} = -\frac{\partial \Re \tilde\phi_i}{\partial\Im \sigma_j} \f]
!> and, thus, is actually analytic (i.e., complex differentiable).
!> From the analogy with the original FE matrix equation for the (total) potential, the sensitivity \f$ \partial \tilde \phi_{i,l} / \partial \sigma_j \f$, corresponding to a potential \f$ \tilde \phi_{i,l} \f$ at node \f$ i \f$ due to a source at node \f$ l \f$, can be represented as a superposition of potentials \f$ \tilde \phi_{i,m} \f$ originated from ‘fictitious’ sources at the nodes  of the j-th domain element (e.g., Sasaki, 1989). By the principle of reciprocity, the values \f$ \tilde \phi_{i,m} \f$ can be expressed via potentials \f$ \tilde \phi_{m,i} \f$ at the nodes  due to a current \f$ I_i \f$ at node \f$ i \f$. Analogous to the DC resistivity problem (e.g., Kemna  1995), for the complex sensitivity the expression ultimately results in:
!> \f[ S \frac{\partial \tilde \phi}{\partial \sigma_j} = -\frac{1}{I_i} \sum_m{\sum_n{a_{j_{mn}} \tilde \phi_{{m,i}}} \tilde \phi_{n,l} }\f]
!> where the double sum is made over all nodes \f$ m,n \f$ of the respective element, and \f$ a_{j_{mn}}\f$ is the \f$ m,n\f$-th element of the matrix \f$ S_{1j} + k^2 S_{2j} \f$. From the last equation, the sensitivities are simply obtained by a weighted sum of complex potential products.

!> @author Andreas Kemna
!> @date 10/11/1993, last change 1/26/1998

subroutine bsens()

!     Unterprogramm zur Berechnung der Sensitivitaeten.

!     Andreas Kemna                                            09-Apr-1995
!     Letzte Aenderung   04-Dez-1998

!.....................................................................

  USE alloci
  USE femmod
  USE datmod
  USE electrmod
  USE modelmod
  USE elemmod
  USE wavenmod
  USE errmod
  USE konvmod , ONLY : lverb
  USE ompmod
  IMPLICIT none

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Aktuelle Elementnummer
  INTEGER (KIND = 4)  ::     iel

!     Aktueller Elementtyp
  INTEGER (KIND = 4)  ::     ntyp

!     Anzahl der Knoten im aktuellen Elementtyp
  INTEGER (KIND = 4)  ::     nkel

!     Elektrodennummern
  INTEGER (KIND = 4)  ::     elec1,elec2,elec3,elec4

!     Beitraege zur Superposition
  COMPLEX (KIND(0D0)) ::     sup(4)

!     Indexvariablen
  INTEGER (KIND = 4)  ::     ityp,jnel,mi,mj,imn,imax,imin
  INTEGER (KIND = 4)  ::     i,k

!     Hilfsfeld
  COMPLEX(KIND(0D0)),DIMENSION(:),ALLOCATABLE :: hsens

!     Hilfsvariablen
  INTEGER (KIND = 4)  ::     nzp,nnp
  COMPLEX (KIND(0D0)) ::     dum

!     Pi
  REAL (KIND(0D0))    ::  pi

! OMP zaehler
  INTEGER (KIND = 4) ::  icount

!.....................................................................

  pi = dacos(-1d0)
  !     get memory for hsens
  ALLOCATE (hsens(kwnanz),stat=errnr)
  IF (errnr /= 0) THEN
     fetxt = 'Error memory allocation hsens'
     errnr = 94
     RETURN
  END IF
!     Sensitivitaetenfeld auf Null setzen
  sens = 0d0
  icount = 0

  !$OMP PARALLEL DEFAULT(none) &
  !$OMP FIRSTPRIVATE(hsens) &
  !$OMP SHARED (icount,strnr,vnr,typanz,typ,selanz,kwnanz,lverb,&
  !$OMP nrel,kpot,elbg,strom,kwnwi,pi,mnr,nanz,swrtr,nelanz,sens) &
  !$OMP PRIVATE(iel,elec1,elec2,elec3,elec4,sup,imin,imn,&
  !$OMP ntyp,jnel,nkel,nzp,nnp,imax,dum)
  !$OMP DO SCHEDULE (GUIDED,CHUNK_0)

!     Messwert hochzaehlen
  do i=1,nanz
     iel = 0
     
     !OMP CRITICAL
     icount = icount + 1

!     Kontrollausgabe
     IF (lverb) write(*,'(a,t70,F10.2,A)',advance='no')ACHAR(13)//&
          'Sensitivity/ ',REAL(icount)/REAL(nanz) * 100. ,' %'

!     Stromelektroden bestimmen
     elec1 = mod(strnr(i),10000)
     elec2 = (strnr(i)-elec1)/10000

!     Messelektroden bestimmen
     elec3 = mod(vnr(i),10000)
     elec4 = (vnr(i)-elec3)/10000

!     Beitraege zur Superposition auf Null setzen
     sup = DCMPLX(0d0)

     do ityp=1,typanz
        ntyp = typ(ityp)
        nkel = selanz(ityp)

!     Ggf. zu neuem Messwert springen
        if (ntyp.gt.10) CYCLE

        do jnel=1,nelanz(ityp)

!     Elementnummer hochzaehlen
           iel = iel + 1

!     SENSITIVITAETEN BERECHNEN
           do k=1,kwnanz
              hsens(k) = dcmplx(0d0)

!     Knoten des aktuellen Elements hochzaehlen
              do mi=1,nkel
                 nzp = nrel(iel,mi)

                 do mj=1,nkel
                    nnp  = nrel(iel,mj)
                    imax = max0(mi,mj)
                    imin = min0(mi,mj)
                    imn  = imax*(imax-1)/2+imin

!     Beitraege nach "Reziprozitaetsmethode" gewichtet aufaddieren und
!     superponieren
!     (beachte: 'volt = pot(elec4) - pot(elec3)' ,
!     '+I' bei 'elec2', '-I' bei 'elec1' )
                    if (elec1.gt.0) sup(1) = kpot(nnp,elec1,k)
                    if (elec2.gt.0) sup(2) = kpot(nnp,elec2,k)
                    if (elec3.gt.0) sup(3) = kpot(nzp,elec3,k)
                    if (elec4.gt.0) sup(4) = kpot(nzp,elec4,k)

!     ACHTUNG: Bei grossen Quellabstaenden UNDERFLOW moeglich, da einzelnen
!     Potentiale sehr klein (vor allem bei grossen Wellenzahlen)!
!     -> mittels Compiler-Einstellung auf Null setzen!
!     MsDev5.0: "/fpe:3 /check:underflow" -> "/fpe:0"
                    dum      = (sup(2)-sup(1)) * (sup(4)-sup(3))
                    hsens(k) = hsens(k) + dcmplx(elbg(iel,imn,k)) * dum
                 end do
              end do
           end do

!     GGF. RUECKTRANSFORMATION
           if (swrtr.eq.0) then

              dum = hsens(1) * dcmplx(strom(i))

           else

              dum = dcmplx(0d0)

              do k=1,kwnanz
                 dum = dum + hsens(k)*dcmplx(kwnwi(k))
              end do

              dum = dum * dcmplx(strom(i)/pi)

           end if

!     Sensitivitaeten aufaddieren
           sens(i,mnr(iel)) = sens(i,mnr(iel)) - dum

        end do ! jnel=1,nelanz(i)
     end do ! ityp=1,typanz
  end do ! i=1,nanz
  !$OMP END DO
  !$OMP END PARALLEL
  
  DEALLOCATE (hsens)

end subroutine bsens
