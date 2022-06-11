import {Injectable} from '@angular/core';
import {Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot} from '@angular/router';
import {GlobalService} from '../global.service';
// import {MakeToastrService} from '../toastr.service';


@Injectable()
export class AuthGuard implements CanActivate {

    constructor(private router: Router, private _global: GlobalService) {
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        const radiologist = localStorage.getItem('username');
        // not logged in so redirect to login page with the return url
        this.router.navigateByUrl('/login');
        return true;
    }
}
